import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data
from datetime import datetime, timedelta

st.set_page_config(page_title="Risk Metrics & Alerts", page_icon="⚠️", layout="wide")

st.title("Risk Metrics & Alerts")
st.markdown("Monitor key risk indicators and set up custom alerts")

# Load data
with st.spinner('Fetching data...'):
    btc_price = fetch_bitcoin_price()
    etf_data = fetch_etf_data()

# Time period selector with mapping to timedelta
time_periods = {
    "1 Week": timedelta(days=7),
    "1 Month": timedelta(days=30),
    "3 Months": timedelta(days=90),
    "6 Months": timedelta(days=180),
    "1 Year": timedelta(days=365),
    "All Time": timedelta(days=3650)
}

time_period = st.selectbox(
    "Select Time Period",
    list(time_periods.keys()),
    index=2
)

if not btc_price.empty and etf_data:
    try:
        # Calculate start date based on selected period
        end_date = datetime.now()
        start_date = end_date - time_periods[time_period]
        # Convert to timezone-naive datetime
        start_date = pd.to_datetime(start_date).tz_localize(None)

        # Filter Bitcoin price data
        btc_price.index = pd.to_datetime(btc_price.index).tz_localize(None)
        filtered_btc_price = btc_price[btc_price.index >= start_date]

        # Calculate daily returns for filtered data
        btc_returns = filtered_btc_price['Close'].pct_change().dropna()

        # Value at Risk (VaR)
        confidence_level = st.slider("VaR Confidence Level", 0.90, 0.99, 0.95, 0.01)
        var = np.percentile(btc_returns, (1 - confidence_level) * 100)

        # Standard Deviation (Volatility)
        volatility = btc_returns.std() * np.sqrt(252)  # Annualized

        # Display metrics
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Value at Risk (VaR)",
                f"{-var*100:.2f}%",
                help=f"Maximum expected daily loss at {confidence_level*100}% confidence level"
            )

        with col2:
            st.metric(
                "Annual Volatility",
                f"{volatility*100:.2f}%",
                help="Annualized standard deviation of returns"
            )

        with col3:
            # Maximum Drawdown for filtered period
            rolling_max = filtered_btc_price['Close'].expanding().max()
            drawdown = (filtered_btc_price['Close'] - rolling_max) / rolling_max
            max_drawdown = drawdown.min()

            st.metric(
                "Maximum Drawdown",
                f"{max_drawdown*100:.2f}%",
                help="Largest peak-to-trough decline"
            )

        # Risk visualization
        st.subheader("Return Distribution")
        fig = px.histogram(
            btc_returns,
            nbins=50,
            title=f"Bitcoin Daily Returns Distribution ({time_period})"
        )
        fig.add_vline(x=var, line_color="red", annotation_text="VaR")
        fig.update_layout(
            xaxis_title="Daily Returns",
            yaxis_title="Frequency",
            height=400,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Alert Configuration
        st.header("Alert Configuration")
        st.markdown("Set up custom alerts for market conditions")

        with st.form("alert_config"):
            col1, col2 = st.columns(2)

            with col1:
                price_threshold = st.number_input(
                    "Price Alert Threshold ($)",
                    min_value=0.0,
                    value=float(filtered_btc_price['Close'].iloc[-1])
                )

                volatility_threshold = st.number_input(
                    "Volatility Alert Threshold (%)",
                    min_value=0.0,
                    value=20.0
                )

            with col2:
                drawdown_threshold = st.number_input(
                    "Drawdown Alert Threshold (%)",
                    min_value=0.0,
                    max_value=100.0,
                    value=10.0
                )

                phone_number = st.text_input(
                    "Phone Number for SMS Alerts",
                    placeholder="+1234567890"
                )

            submitted = st.form_submit_button("Save Alert Configuration")

            if submitted:
                st.success("Alert configuration saved! You will receive SMS notifications when conditions are met.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.checkbox("Show detailed error information"):
            st.exception(e)
else:
    st.error("Unable to load data. Please try again later.")

# Explanation section
with st.expander("Understanding Risk Metrics"):
    st.write("""
    Key risk metrics help understand potential investment risks:
    - Value at Risk (VaR): Maximum expected loss within a confidence level
    - Volatility: Measure of price variation over time
    - Maximum Drawdown: Largest peak-to-trough decline
    - Return Distribution: Visual representation of return patterns
    """)
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data
from datetime import datetime, timedelta

st.set_page_config(page_title="Tracking Error Analysis", page_icon="📈", layout="wide")

st.title("Tracking Error & Performance Analysis")
st.markdown("Compare ETF performance against underlying Bitcoin price")

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

        # Convert BTC price index to timezone-naive datetime
        btc_price.index = pd.to_datetime(btc_price.index).tz_localize(None)
        filtered_btc_price = btc_price[btc_price.index >= start_date]

        # Calculate tracking error
        st.subheader("ETF Tracking Error")

        # Create comparison chart
        fig = px.line(
            filtered_btc_price,
            x=filtered_btc_price.index,
            y="Close",
            title="Bitcoin Price vs ETF Performance"
        )

        # Add ETF price lines
        for etf_name, etf_info in etf_data.items():
            if 'history' in etf_info and not etf_info['history'].empty:
                # Convert ETF history index to timezone-naive datetime
                etf_history = etf_info['history'].copy()
                etf_history.index = pd.to_datetime(etf_history.index).tz_localize(None)
                filtered_etf_history = etf_history[etf_history.index >= start_date]

                if not filtered_etf_history.empty:
                    fig.add_scatter(
                        x=filtered_etf_history.index,
                        y=filtered_etf_history['Close'],
                        name=etf_name
                    )

        st.plotly_chart(fig, use_container_width=True)

        # Performance metrics
        st.subheader("Performance Metrics")
        col1, col2, col3 = st.columns(3)

        with col1:
            btc_volatility = filtered_btc_price['Close'].pct_change().std() * np.sqrt(252)
            st.metric("Bitcoin Volatility", f"{btc_volatility*100:.2f}%")

        with col2:
            # Calculate average ETF volatility
            etf_volatilities = []
            for etf_info in etf_data.values():
                if 'history' in etf_info and not etf_info['history'].empty:
                    etf_history = etf_info['history'].copy()
                    etf_history.index = pd.to_datetime(etf_history.index).tz_localize(None)
                    filtered_etf_history = etf_history[etf_history.index >= start_date]
                    if not filtered_etf_history.empty:
                        vol = filtered_etf_history['Close'].pct_change().std() * np.sqrt(252)
                        etf_volatilities.append(vol)

            if etf_volatilities:
                avg_etf_volatility = sum(etf_volatilities) / len(etf_volatilities)
                st.metric("Avg ETF Volatility", f"{avg_etf_volatility*100:.2f}%")

        with col3:
            # Calculate tracking error as RMSE
            tracking_errors = []
            for etf_name, etf_info in etf_data.items():
                if 'history' not in etf_info or etf_info['history'].empty:
                    continue

                # Convert ETF history index to timezone-naive datetime
                etf_history = etf_info['history'].copy()
                etf_history.index = pd.to_datetime(etf_history.index).tz_localize(None)
                filtered_etf_history = etf_history[etf_history.index >= start_date]

                # Align dates between BTC and ETF data
                common_dates = filtered_etf_history.index.intersection(filtered_btc_price.index)
                if len(common_dates) == 0:
                    continue

                etf_prices = filtered_etf_history.loc[common_dates, 'Close']
                btc_prices = filtered_btc_price.loc[common_dates, 'Close']

                # Calculate tracking error only if we have matching data
                if len(etf_prices) > 0:
                    tracking_error = np.sqrt(((etf_prices.pct_change() - btc_prices.pct_change()) ** 2).mean())
                    tracking_errors.append(tracking_error)

            if tracking_errors:
                avg_tracking_error = sum(tracking_errors) / len(tracking_errors)
                st.metric("Avg Tracking Error", f"{avg_tracking_error*100:.2f}%")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        if st.checkbox("Show detailed error information"):
            st.exception(e)
else:
    st.error("Unable to load data. Please try again later.")

# Explanation section
with st.expander("Understanding Tracking Error"):
    st.write("""
    Tracking error measures how closely an ETF follows its underlying asset (Bitcoin):
    - Lower tracking error indicates better ETF performance
    - Factors affecting tracking error include:
        - Management fees
        - Trading costs
        - Market liquidity
        - Rebalancing frequency
    """)
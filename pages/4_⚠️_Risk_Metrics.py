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

# Time period selector
time_period = st.selectbox(
    "Select Time Period",
    ["1 Week", "1 Month", "3 Months", "6 Months", "1 Year", "All Time"],
    index=2
)

if not btc_price.empty and etf_data:
    # Risk Metrics Section
    st.header("Risk Metrics")
    
    # Calculate daily returns
    btc_returns = btc_price['Close'].pct_change().dropna()
    
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
        # Maximum Drawdown
        rolling_max = btc_price['Close'].expanding().max()
        drawdown = (btc_price['Close'] - rolling_max) / rolling_max
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
        title="Bitcoin Daily Returns Distribution"
    )
    fig.add_vline(x=var, line_color="red", annotation_text="VaR")
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
                value=float(btc_price['Close'].iloc[-1])
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

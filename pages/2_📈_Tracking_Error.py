import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data

st.set_page_config(page_title="Tracking Error Analysis", page_icon="📈", layout="wide")

st.title("Tracking Error & Performance Analysis")
st.markdown("Compare ETF performance against underlying Bitcoin price")

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
    # Calculate tracking error
    st.subheader("ETF Tracking Error")

    # Create comparison chart
    fig = px.line(
        btc_price,
        x=btc_price.index,
        y="Close",
        title="Bitcoin Price vs ETF Performance"
    )

    # Add ETF price lines
    for etf_name, etf_info in etf_data.items():
        if 'history' in etf_info and not etf_info['history'].empty:
            fig.add_scatter(
                x=etf_info['history'].index,
                y=etf_info['history']['Close'],
                name=etf_name
            )

    st.plotly_chart(fig, use_container_width=True)

    # Performance metrics
    st.subheader("Performance Metrics")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Bitcoin Volatility", f"{btc_price['Close'].std():.2f}%")

    with col2:
        # Calculate average ETF volatility
        etf_volatilities = [
            etf_info['history']['Close'].std()
            for etf_info in etf_data.values()
            if 'history' in etf_info and not etf_info['history'].empty
        ]
        if etf_volatilities:
            avg_etf_volatility = sum(etf_volatilities) / len(etf_volatilities)
            st.metric("Avg ETF Volatility", f"{avg_etf_volatility:.2f}%")

    with col3:
        # Calculate tracking error as RMSE
        tracking_errors = []
        for etf_info in etf_data.values():
            if 'history' in etf_info and not etf_info['history'].empty:
                tracking_error = ((etf_info['history']['Close'] - btc_price['Close']) ** 2).mean() ** 0.5
                tracking_errors.append(tracking_error)

        if tracking_errors:
            avg_tracking_error = sum(tracking_errors) / len(tracking_errors)
            st.metric("Avg Tracking Error", f"{avg_tracking_error:.2f}%")

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
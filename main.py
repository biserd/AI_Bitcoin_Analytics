import streamlit as st
import pandas as pd
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics
from utils.visualizations import create_price_chart
from components.metrics import display_metrics_section

# Page configuration
st.set_page_config(
    page_title="Bitcoin Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

# Load custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header
st.title("Bitcoin Analytics Dashboard")
st.markdown("### Comprehensive Bitcoin ETF and On-Chain Analytics Platform")

# Load key metrics for homepage
with st.spinner('Fetching latest data...'):
    btc_price = fetch_bitcoin_price()
    onchain_data = fetch_onchain_metrics()
    if not btc_price.empty and not onchain_data.empty:
        display_metrics_section(btc_price, onchain_data)
    else:
        st.warning("Some data is currently unavailable. Please try again later.")

    # Main price chart
    if not btc_price.empty:
        st.subheader("Bitcoin Price Overview")
        st.plotly_chart(create_price_chart(btc_price), use_container_width=True)

# Feature Overview
st.header("Available Analytics Features")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📊 Market Analysis")
    st.write("""
    - Correlation Analysis
    - Tracking Error & Performance
    - Liquidity & Volume Insights
    """)

    st.subheader("📈 Risk Management")
    st.write("""
    - Risk Metrics and Alerts
    - Portfolio Diversification
    """)

with col2:
    st.subheader("💰 ETF Analysis")
    st.write("""
    - Fee and Expense Analysis
    - Comparative Analytics
    """)

    st.subheader("📰 Market Intelligence")
    st.write("""
    - Regulatory Updates
    - Market Sentiment Indicators
    """)

# Footer
st.markdown("---")
st.markdown(
    "Data updates daily. On-chain metrics and ETF data are sourced from various providers. "
    "This dashboard is for informational purposes only."
)
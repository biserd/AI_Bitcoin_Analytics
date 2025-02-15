import streamlit as st
import pandas as pd
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics
from utils.visualizations import create_price_chart, create_etf_comparison
from components.metrics import display_metrics_section
from components.education import display_education_section
from components.analytics import inject_ga

# Page configuration
st.set_page_config(
    page_title="Bitcoin Analytics Dashboard | Real-time Crypto Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for data caching
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = {
        'btc_price': None,
        'etf_data': None,
        'onchain_data': None,
        'last_update': None
    }

# Add Google Analytics
inject_ga()

# Header
st.title("Bitcoin Analytics Dashboard")
st.markdown("### Real-time Cryptocurrency Market Analysis")

try:
    with st.spinner('Fetching latest data...'):
        # Fetch Bitcoin price data
        btc_price = fetch_bitcoin_price()
        st.session_state.data_cache['btc_price'] = btc_price

        # Fetch ETF data
        etf_data = fetch_etf_data()
        st.session_state.data_cache['etf_data'] = etf_data

        # Fetch on-chain metrics
        onchain_data = fetch_onchain_metrics()
        st.session_state.data_cache['onchain_data'] = onchain_data

    # Display metrics section if data is available
    if not btc_price.empty and not onchain_data.empty:
        display_metrics_section(btc_price, onchain_data)
    else:
        st.warning("Some data is currently unavailable. Please try again later.")

    # Main price chart
    if not btc_price.empty:
        st.subheader("Bitcoin Price Overview")
        price_chart = create_price_chart(btc_price)
        st.plotly_chart(price_chart, use_container_width=True)

    # ETF Comparison
    if etf_data:
        st.subheader("ETF Performance Comparison")
        etf_chart = create_etf_comparison(etf_data)
        st.plotly_chart(etf_chart, use_container_width=True)

    # Education Section
    display_education_section()

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Data updates in real-time. Market analysis and predictions are for informational purposes only.")
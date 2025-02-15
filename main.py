
import streamlit as st
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics
from components.metrics import display_metrics_section
from components.analytics import inject_ga

st.set_page_config(
    page_title="Bitcoin ETF Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Add custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Inject Google Analytics
inject_ga()

st.title("Bitcoin ETF Analytics Dashboard")
st.markdown("Real-time analysis of Bitcoin ETF performance and market metrics")

# Load data
with st.spinner('Loading data...'):
    btc_price = fetch_bitcoin_price()
    etf_data = fetch_etf_data()
    onchain_data = fetch_onchain_metrics()

# Display metrics
display_metrics_section(btc_price, onchain_data)

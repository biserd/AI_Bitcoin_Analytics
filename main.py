
import streamlit as st
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics

st.set_page_config(
    page_title="Bitcoin ETF Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Bitcoin ETF Analytics Dashboard")
st.markdown("Real-time analysis of Bitcoin ETF performance and market metrics")

# Load data
with st.spinner('Loading data...'):
    btc_price = fetch_bitcoin_price()
    
    if not btc_price.empty:
        st.metric(
            label="Bitcoin Price",
            value=f"${btc_price['Close'].iloc[-1]:,.2f}"
        )
    else:
        st.error("Unable to load Bitcoin price data")

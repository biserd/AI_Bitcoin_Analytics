
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
    
    try:
        if not btc_price.empty and 'Close' in btc_price.columns:
            latest_price = btc_price['Close'].iloc[-1]
            if pd.notna(latest_price):
                st.metric(
                    label="Bitcoin Price",
                    value=f"${latest_price:,.2f}"
                )
            else:
                st.error("Invalid price data received")
        else:
            st.error("No price data available")
    except Exception as e:
        st.error(f"Error displaying price: {str(e)}")

import streamlit as st
import pandas as pd
from utils.data_fetcher import (
    get_bitcoin_data,
    fetch_bitcoin_price,
    fetch_etf_data,
    fetch_onchain_metrics
)
from utils.visualizations import (
    create_price_chart,
    create_metric_chart,
    create_etf_comparison
)

st.set_page_config(
    page_title="Bitcoin Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("Bitcoin Analytics Dashboard 📊")

# Fetch current Bitcoin price and metrics
btc_data = get_bitcoin_data()
if btc_data:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(
            "Bitcoin Price",
            f"${btc_data['price']:,.2f}",
            f"{btc_data['change_24h']:,.2f}"
        )
    with col2:
        st.metric(
            "24h Volume",
            f"${btc_data['volume']:,.0f}"
        )
    with col3:
        st.metric(
            "Last Updated",
            btc_data['timestamp'].split('T')[0]
        )

# Historical price chart
st.subheader("Price History")
historical_data = fetch_bitcoin_price()
if not historical_data.empty:
    price_chart = create_price_chart(historical_data)
    st.plotly_chart(price_chart, use_container_width=True)

# ETF Comparison
st.subheader("ETF Analysis")
etf_data = fetch_etf_data()
if etf_data:
    etf_chart = create_etf_comparison(etf_data)
    st.plotly_chart(etf_chart, use_container_width=True)

# On-chain Metrics
st.subheader("On-chain Metrics")
metrics_data = fetch_onchain_metrics()
if not metrics_data.empty:
    col1, col2 = st.columns(2)
    with col1:
        active_addresses_chart = create_metric_chart(
            metrics_data, 'active_addresses', '#1f77b4'
        )
        st.plotly_chart(active_addresses_chart, use_container_width=True)
    with col2:
        hash_rate_chart = create_metric_chart(
            metrics_data, 'hash_rate', '#2ca02c'
        )
        st.plotly_chart(hash_rate_chart, use_container_width=True)
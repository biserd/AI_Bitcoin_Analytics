import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics

st.set_page_config(page_title="Correlation Analysis", page_icon="📊", layout="wide")

st.title("Correlation Analysis")
st.markdown("Analyze relationships between on-chain metrics and ETF performance")

# Load data
with st.spinner('Fetching data...'):
    btc_price = fetch_bitcoin_price()
    etf_data = fetch_etf_data()
    onchain_data = fetch_onchain_metrics()

# Time period selector
time_period = st.selectbox(
    "Select Time Period",
    ["1 Week", "1 Month", "3 Months", "6 Months", "1 Year", "All Time"],
    index=2
)

# Metric selectors
col1, col2 = st.columns(2)
with col1:
    onchain_metric = st.selectbox(
        "Select On-Chain Metric",
        ["Active Addresses", "Transaction Volume", "Hash Rate", "Mining Revenue"]
    )

with col2:
    etf_metric = st.selectbox(
        "Select ETF Metric",
        ["Price", "Volume", "Net Flows", "Assets Under Management"]
    )

# Display correlation analysis
if not btc_price.empty and etf_data and not onchain_data.empty:
    st.subheader(f"Correlation: {onchain_metric} vs {etf_metric}")
    
    # Create correlation plot
    fig = px.scatter(
        onchain_data,
        x=onchain_metric.lower().replace(" ", "_"),
        y="price",
        trendline="ols",
        title=f"{onchain_metric} vs {etf_metric} Correlation"
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate and display correlation coefficient
    correlation = onchain_data[onchain_metric.lower().replace(" ", "_")].corr(onchain_data["price"])
    st.metric("Correlation Coefficient", f"{correlation:.2f}")
else:
    st.error("Unable to load data. Please try again later.")

# Explanation section
with st.expander("Understanding Correlation Analysis"):
    st.write("""
    Correlation analysis helps understand the relationship between different metrics:
    - A correlation of 1.0 indicates perfect positive correlation
    - A correlation of -1.0 indicates perfect negative correlation
    - A correlation of 0 indicates no linear relationship
    
    This analysis can help identify leading indicators and market patterns.
    """)

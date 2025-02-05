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
        ["Price", "Volume", "Net Flows"]
    )

# Column name mappings
onchain_column_mapping = {
    "Active Addresses": "active_addresses",
    "Transaction Volume": "transaction_volume",
    "Hash Rate": "hash_rate",
    "Mining Revenue": "mining_revenue"
}

etf_column_mapping = {
    "Price": "Close",
    "Volume": "Volume",
    "Net Flows": "net_flows"
}

# Display correlation analysis
if not btc_price.empty and etf_data and not onchain_data.empty:
    st.subheader(f"Correlation: {onchain_metric} vs {etf_metric}")

    try:
        # Get the selected ETF data
        first_etf_data = next(iter(etf_data.values()))['history']

        # Debug information
        st.write("### Data Validation")
        st.write(f"On-chain data shape: {onchain_data.shape}")
        st.write(f"ETF data shape: {first_etf_data.shape}")

        # Ensure both DataFrames have datetime index
        onchain_data.index = pd.to_datetime(onchain_data.index)
        first_etf_data.index = pd.to_datetime(first_etf_data.index)

        # Create a merged dataset for correlation
        merged_data = pd.merge(
            onchain_data,
            first_etf_data[etf_column_mapping[etf_metric]],
            left_index=True,
            right_index=True,
            how='inner'
        )

        # Debug merged data
        st.write(f"Merged data shape: {merged_data.shape}")

        # Check for missing values
        missing_values = merged_data[[onchain_column_mapping[onchain_metric], etf_column_mapping[etf_metric]]].isnull().sum()
        if missing_values.any():
            st.warning(f"Missing values detected:\n{missing_values}")
            # Drop missing values for correlation calculation
            merged_data = merged_data.dropna()
            st.write(f"Shape after dropping missing values: {merged_data.shape}")

        if not merged_data.empty:
            # Create correlation plot
            fig = px.scatter(
                merged_data,
                x=onchain_column_mapping[onchain_metric],
                y=etf_column_mapping[etf_metric],
                trendline="ols",
                title=f"{onchain_metric} vs {etf_metric} Correlation"
            )
            st.plotly_chart(fig, use_container_width=True)

            # Calculate and display correlation coefficient
            correlation = merged_data[onchain_column_mapping[onchain_metric]].corr(
                merged_data[etf_column_mapping[etf_metric]]
            )

            if pd.isna(correlation):
                st.error("Unable to calculate correlation. Please check if the selected metrics contain valid numerical data.")
            else:
                st.metric("Correlation Coefficient", f"{correlation:.2f}")
        else:
            st.error("No overlapping data points found between the selected metrics.")

    except (KeyError, StopIteration) as e:
        st.error("Error processing data. Please ensure all required metrics are available.")
        st.exception(e)
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
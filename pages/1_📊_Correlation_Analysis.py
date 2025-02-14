import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics
from datetime import datetime, timedelta

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

# Convert time period to timedelta
period_mapping = {
    "1 Week": timedelta(days=7),
    "1 Month": timedelta(days=30),
    "3 Months": timedelta(days=90),
    "6 Months": timedelta(days=180),
    "1 Year": timedelta(days=365),
    "All Time": timedelta(days=3650)  # Effectively no limit
}

# Calculate the start date based on selected period
end_date = datetime.now()
start_date = end_date - period_mapping[time_period]

# Metric selectors
col1, col2 = st.columns(2)
with col1:
    onchain_metric = st.selectbox(
        "Select On-Chain Metric",
        ["Active Addresses", "Transaction Volume", "Hash Rate"]
    )

with col2:
    etf_metric = st.selectbox(
        "Select ETF Metric",
        ["Price", "Volume"]
    )

# Column name mappings
onchain_column_mapping = {
    "Active Addresses": "active_addresses",
    "Transaction Volume": "transaction_volume",
    "Hash Rate": "hash_rate"
}

etf_column_mapping = {
    "Price": "Close",
    "Volume": "Volume"
}

# Display correlation analysis
if not btc_price.empty and etf_data and not onchain_data.empty:
    st.subheader(f"Correlation: {onchain_metric} vs {etf_metric}")

    try:
        # Get the selected ETF data
        first_etf_data = next(iter(etf_data.values()))['history']

        # Filter data based on selected time period
        onchain_data = onchain_data[onchain_data.index >= pd.to_datetime(start_date)]
        first_etf_data = first_etf_data[first_etf_data.index >= pd.to_datetime(start_date)]

        # Convert timezone-aware timestamps to naive timestamps for both DataFrames
        onchain_data.index = pd.to_datetime(onchain_data.index).tz_localize(None)
        first_etf_data.index = pd.to_datetime(first_etf_data.index).tz_localize(None)

        # Create a merged dataset for correlation
        merged_data = pd.merge(
            onchain_data[onchain_column_mapping[onchain_metric]],
            first_etf_data[etf_column_mapping[etf_metric]],
            left_index=True,
            right_index=True,
            how='inner',
            suffixes=('_onchain', '_etf')
        )

        if not merged_data.empty:
            # Create scatter plot
            fig = px.scatter(
                merged_data,
                x=onchain_column_mapping[onchain_metric],
                y=etf_column_mapping[etf_metric],
                title=f"{onchain_metric} vs {etf_metric} Correlation"
            )

            # Add trendline
            fig.add_traces(px.scatter(
                merged_data,
                x=onchain_column_mapping[onchain_metric],
                y=etf_column_mapping[etf_metric],
                trendline="ols"
            ).data)

            st.plotly_chart(fig, use_container_width=True)

            # Calculate and display correlation coefficient
            correlation = merged_data[onchain_column_mapping[onchain_metric]].corr(
                merged_data[etf_column_mapping[etf_metric]]
            )

            if not pd.isna(correlation):
                st.metric("Correlation Coefficient", f"{correlation:.2f}")

                # Add correlation interpretation
                if abs(correlation) > 0.7:
                    strength = "Strong"
                elif abs(correlation) > 0.3:
                    strength = "Moderate"
                else:
                    strength = "Weak"

                direction = "positive" if correlation > 0 else "negative"
                st.info(f"There is a {strength} {direction} correlation between {onchain_metric} and {etf_metric}.")
            else:
                st.warning("Unable to calculate correlation. This might be due to insufficient data points or non-numeric values.")
        else:
            st.warning("No overlapping data points found for the selected time period.")

    except Exception as e:
        st.error("An error occurred while processing the data. Please try different metrics or time period.")
        st.exception(e)
else:
    st.error("Unable to load data. Please try again later.")

# Explanation section
with st.expander("Understanding Correlation Analysis"):
    st.write("""
    Correlation analysis helps understand the relationship between different metrics:
    - A correlation of 1.0 indicates perfect positive correlation (metrics move together)
    - A correlation of -1.0 indicates perfect negative correlation (metrics move in opposite directions)
    - A correlation of 0 indicates no linear relationship

    The scatter plot shows individual data points and a trend line to visualize the relationship.
    The correlation coefficient quantifies the strength and direction of this relationship.
    """)
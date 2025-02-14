import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics
from datetime import datetime, timedelta

st.set_page_config(page_title="Correlation Analysis", page_icon="📊", layout="wide")

st.title("Correlation Analysis")
st.markdown("Analyze relationships between on-chain metrics and ETF performance")

# Clear cache if time period changes
if 'last_time_period' not in st.session_state:
    st.session_state.last_time_period = None

# Time period selector
time_period = st.selectbox(
    "Select Time Period",
    ["1 Week", "1 Month", "3 Months", "6 Months", "1 Year", "All Time"],
    index=2
)

# Clear cache if time period changes
if st.session_state.last_time_period != time_period:
    st.session_state.last_time_period = time_period
    st.cache_data.clear()

# Load data with proper caching
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_all_data():
    with st.spinner('Fetching data...'):
        btc_price = fetch_bitcoin_price()
        etf_data = fetch_etf_data()
        onchain_data = fetch_onchain_metrics()
        return btc_price, etf_data, onchain_data

btc_price, etf_data, onchain_data = load_all_data()

# Debug information toggle
show_debug = st.checkbox("Show Debug Information", value=False)

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

# Convert time period to timedelta
period_mapping = {
    "1 Week": timedelta(days=7),
    "1 Month": timedelta(days=30),
    "3 Months": timedelta(days=90),
    "6 Months": timedelta(days=180),
    "1 Year": timedelta(days=365),
    "All Time": timedelta(days=3650)
}

# Display correlation analysis
if not btc_price.empty and etf_data and not onchain_data.empty:
    try:
        # Calculate the start date based on selected period
        end_date = datetime.now()
        start_date = end_date - period_mapping[time_period]
        start_date_naive = pd.to_datetime(start_date).tz_localize(None)

        # Get ETF data
        first_etf_data = next(iter(etf_data.values()))['history'].copy()

        # Debug data shapes and date ranges
        if show_debug:
            st.write("Debug Information:")
            st.write(f"Time Period: {time_period}")
            st.write(f"Start Date: {start_date_naive}")
            st.write(f"End Date: {end_date}")
            st.write("\nData Shapes:")
            st.write(f"On-chain Data: {onchain_data.shape}")
            st.write(f"ETF Data: {first_etf_data.shape}")
            st.write("\nDate Ranges:")
            st.write(f"On-chain Data: {onchain_data.index.min()} to {onchain_data.index.max()}")
            st.write(f"ETF Data: {first_etf_data.index.min()} to {first_etf_data.index.max()}")

        # Ensure all datetime indices are timezone-naive
        onchain_data.index = pd.to_datetime(onchain_data.index).tz_localize(None)
        first_etf_data.index = pd.to_datetime(first_etf_data.index).tz_localize(None)

        # Filter data based on selected time period
        filtered_onchain = onchain_data[onchain_data.index >= start_date_naive].copy()
        filtered_etf = first_etf_data[first_etf_data.index >= start_date_naive].copy()

        if show_debug:
            st.write("\nFiltered Data:")
            st.write(f"Filtered On-chain Data: {filtered_onchain.shape}")
            st.write(f"Filtered ETF Data: {filtered_etf.shape}")
            if not filtered_onchain.empty:
                st.write(f"Filtered On-chain Range: {filtered_onchain.index.min()} to {filtered_onchain.index.max()}")
            if not filtered_etf.empty:
                st.write(f"Filtered ETF Range: {filtered_etf.index.min()} to {filtered_etf.index.max()}")

        # Create a merged dataset for correlation
        merged_data = pd.merge(
            filtered_onchain[onchain_column_mapping[onchain_metric]],
            filtered_etf[etf_column_mapping[etf_metric]],
            left_index=True,
            right_index=True,
            how='inner'
        )

        if show_debug:
            st.write("\nMerged Data:")
            st.write(f"Merged Data Shape: {merged_data.shape}")
            if not merged_data.empty:
                st.write("First few rows of merged data:")
                st.write(merged_data.head())

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

            # Calculate correlation
            correlation = merged_data[onchain_column_mapping[onchain_metric]].corr(
                merged_data[etf_column_mapping[etf_metric]]
            )

            if pd.isna(correlation):
                st.warning("Unable to calculate correlation coefficient")
            else:
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
            st.warning("No overlapping data points found in the selected time period. Try selecting a different time period or metrics.")

    except Exception as e:
        st.error(f"An error occurred during analysis: {str(e)}")
        if show_debug:
            st.exception(e)
else:
    st.error("Unable to load required data. Please try again later.")

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
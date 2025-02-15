import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from components.metrics import display_metrics_section
from components.education import display_education_section
from components.analytics import inject_ga

# API Configuration
API_BASE_URL = "http://0.0.0.0:8000/api"

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
        'last_update': None,
        'predictions': None,
        'metrics': None
    }

# Add Google Analytics
inject_ga()

# Header
st.title("Bitcoin Analytics Dashboard")
st.markdown("### Real-time Cryptocurrency Market Analysis")

def fetch_api_data(endpoint):
    """Fetch data from FastAPI endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}{endpoint}")
        response.raise_for_status()
        data = response.json()
        if data.get('success'):
            return data.get('data')
        return None
    except Exception as e:
        st.error(f"Error fetching data from {endpoint}: {str(e)}")
        return None

try:
    with st.spinner('Fetching latest data...'):
        # Fetch Bitcoin price data
        price_data = fetch_api_data('/bitcoin/price')
        if price_data:
            # Convert the data into a pandas DataFrame for visualization
            price_df = pd.DataFrame([{
                'timestamp': datetime.fromisoformat(price_data['timestamp']),
                'Close': price_data['price'],
                'Volume': price_data['volume'],
                'Change_24h': price_data['change_24h']
            }])
            price_df.set_index('timestamp', inplace=True)
            st.session_state.data_cache['btc_price'] = price_df

        # Fetch market predictions
        predictions = fetch_api_data('/bitcoin/predictions')
        if predictions:
            st.session_state.data_cache['predictions'] = predictions

        # Fetch metrics
        metrics = fetch_api_data('/bitcoin/metrics')
        if metrics:
            st.session_state.data_cache['metrics'] = metrics

    # Display metrics section if data is available
    if price_data:
        st.subheader("Current Bitcoin Metrics")
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                label="Bitcoin Price",
                value=f"${price_data['price']:,.2f}",
                delta=f"{price_data['change_24h']:+.2f}%"
            )

        with col2:
            st.metric(
                label="24h Volume",
                value=f"${price_data['volume']:,.0f}"
            )

        with col3:
            current_time = datetime.fromisoformat(price_data['timestamp'])
            st.metric(
                label="Last Updated",
                value=current_time.strftime("%Y-%m-%d %H:%M:%S")
            )

    # Display predictions if available
    if predictions:
        st.subheader("Market Predictions")
        for scenario, data in predictions.items():
            with st.expander(f"{scenario.title()} Scenario (Probability: {data['probability']*100:.1f}%)"):
                st.write("Supporting Factors:")
                for factor in data['factors']:
                    st.write(f"- {factor}")

    # Main price chart
    if st.session_state.data_cache['btc_price'] is not None:
        st.subheader("Bitcoin Price Overview")
        price_chart = create_price_chart(st.session_state.data_cache['btc_price'])
        st.plotly_chart(price_chart, use_container_width=True)


    # ETF Comparison -  This section needs adjustment as the ETF data fetching is removed from the edited code.
    # Leaving this section commented out because no ETF data is fetched from the new API.
    #if etf_data:
    #    st.subheader("ETF Performance Comparison")
    #    etf_chart = create_etf_comparison(etf_data)
    #    st.plotly_chart(etf_chart, use_container_width=True)

    # Education Section
    display_education_section()

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")

# Footer
st.markdown("---")
st.markdown("Data updates in real-time. Market analysis and predictions are for informational purposes only.")
import streamlit as st
import requests
import pandas as pd
import json
from datetime import datetime

# Configure page settings
st.set_page_config(
    page_title="Bitcoin Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# Load custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# API Configuration
API_BASE_URL = "http://localhost:8000/api"

def fetch_api_data(endpoint):
    """Fetch data from API endpoint"""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}")
        response.raise_for_status()
        return response.json()['data']
    except Exception as e:
        st.error(f"Error fetching data from {endpoint}: {str(e)}")
        return None

def main():
    st.title("Bitcoin Analytics Dashboard")

    # Fetch current Bitcoin data
    bitcoin_data = fetch_api_data("bitcoin/price")

    if bitcoin_data:
        col1, col2, col3 = st.columns(3)

        # Display current price
        with col1:
            st.metric(
                "Bitcoin Price",
                bitcoin_data['current_price']['formatted'],
                f"{bitcoin_data['current_price']['change_24h']:+.2f} USD"
            )

        # Display volume
        with col2:
            st.metric(
                "24h Volume",
                bitcoin_data['volume']['formatted']
            )

        # Display market cap
        with col3:
            market_cap = bitcoin_data['market_metrics']['market_cap']
            st.metric(
                "Market Cap",
                f"${market_cap:,.0f}"
            )

    # Fetch and display market analysis
    st.subheader("Market Analysis")
    analysis_data = fetch_api_data("bitcoin/analysis")

    if analysis_data:
        analysis = json.loads(analysis_data['analysis'])

        # Display sentiment and predictions
        col1, col2 = st.columns(2)

        with col1:
            st.markdown(f"### Market Sentiment")
            st.markdown(f"**Current Sentiment**: {analysis['market_sentiment'].title()}")
            st.markdown(f"**Confidence Score**: {analysis['confidence_score']*100:.1f}%")

            st.markdown("### Key Factors")
            for factor in analysis['key_factors']:
                st.markdown(f"- {factor}")

        with col2:
            st.markdown("### Market Outlook")
            st.markdown(f"**Short Term**: {analysis['short_term_outlook']}")
            st.markdown(f"**Medium Term**: {analysis['medium_term_outlook']}")

    # Fetch and display ETF data
    st.subheader("Bitcoin ETF Data")
    etf_data = fetch_api_data("etf/data")

    if etf_data:
        col1, col2, col3 = st.columns(3)

        for i, (etf, data) in enumerate(etf_data.items()):
            with [col1, col2, col3][i % 3]:
                st.markdown(f"### {etf}")
                st.metric(
                    "Price",
                    f"${data['latest_price']:.2f}",
                    delta=None
                )
                st.metric(
                    "Volume",
                    f"${data['volume']:,.0f}"
                )

    # Fetch and display educational content
    st.subheader("Educational Resources")
    edu_content = fetch_api_data("education/content")

    if edu_content:
        for section, content in edu_content.items():
            with st.expander(content['title']):
                st.markdown(content['content'])

                if 'key_benefits' in content:
                    st.markdown("#### Key Benefits")
                    for benefit in content['key_benefits']:
                        st.markdown(f"- {benefit}")

                if 'key_metrics' in content:
                    st.markdown("#### Key Metrics")
                    for metric in content['key_metrics']:
                        st.markdown(f"- **{metric['name']}**: {metric['description']}")

if __name__ == "__main__":
    main()
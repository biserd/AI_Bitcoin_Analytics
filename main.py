import streamlit as st
import pandas as pd
import numpy as np
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics
from utils.visualizations import create_price_chart, create_metric_chart, create_etf_comparison
from components.metrics import display_metrics_section
from components.education import display_education_section

# Page configuration
st.set_page_config(
    page_title="Bitcoin Analytics Dashboard",
    page_icon="📈",
    layout="wide"
)

# Load custom CSS
with open('styles/custom.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Header
st.title("Bitcoin Analytics Dashboard")
st.markdown("Comprehensive analysis combining on-chain metrics and ETF data")

# Load data with loading states
with st.spinner('Fetching latest data...'):
    price_data = fetch_bitcoin_price()
    etf_data = fetch_etf_data()
    onchain_data = fetch_onchain_metrics()

# Display metrics
if price_data is not None and onchain_data is not None:
    display_metrics_section(price_data, onchain_data)
else:
    st.error("Unable to load metrics data. Please try again later.")

# Main dashboard tabs
tab1, tab2, tab3 = st.tabs(["Price Analysis", "On-Chain Metrics", "ETF Analysis"])

with tab1:
    st.plotly_chart(create_price_chart(price_data), use_container_width=True)
    
with tab2:
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            create_metric_chart(onchain_data, 'active_addresses'),
            use_container_width=True
        )
    with col2:
        st.plotly_chart(
            create_metric_chart(onchain_data, 'transaction_volume'),
            use_container_width=True
        )
    
    st.plotly_chart(
        create_metric_chart(onchain_data, 'hash_rate'),
        use_container_width=True
    )

with tab3:
    if etf_data:
        st.plotly_chart(create_etf_comparison(etf_data), use_container_width=True)
        
        # ETF Metrics Table
        etf_metrics = []
        for etf, data in etf_data.items():
            if 'info' in data:
                etf_metrics.append({
                    'ETF': etf,
                    'Price': data['history']['Close'].iloc[-1],
                    'Volume': data['info'].get('volume', 'N/A'),
                    'Assets': data['info'].get('totalAssets', 'N/A')
                })
        
        st.dataframe(pd.DataFrame(etf_metrics))
    else:
        st.error("Unable to load ETF data. Please try again later.")

# Educational Section
display_education_section()

# Footer
st.markdown("---")
st.markdown(
    "Data updates daily. On-chain metrics and ETF data are sourced from various providers. "
    "This dashboard is for informational purposes only."
)

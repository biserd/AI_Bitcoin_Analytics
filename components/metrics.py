import streamlit as st
import pandas as pd

def display_metrics_section(price_data, onchain_data):
    """Display key metrics in a structured format"""
    try:
        col1, col2, col3 = st.columns(3)

        # Current Bitcoin Price
        with col1:
            current_price = price_data['Close'].iloc[-1]
            price_change = ((current_price - price_data['Close'].iloc[-2]) / 
                           price_data['Close'].iloc[-2] * 100)

            st.metric(
                label="Bitcoin Price",
                value=f"${current_price:,.2f}",
                delta=f"{price_change:.2f}%"
            )

        # Active Addresses
        with col2:
            current_addresses = onchain_data['active_addresses'].iloc[-1]
            address_change = ((current_addresses - onchain_data['active_addresses'].iloc[-2]) /
                             onchain_data['active_addresses'].iloc[-2] * 100)

            st.metric(
                label="Active Addresses",
                value=f"{current_addresses:,}",
                delta=f"{address_change:.2f}%"
            )

        # Hash Rate
        with col3:
            current_hashrate = onchain_data['hash_rate'].iloc[-1]
            hashrate_change = ((current_hashrate - onchain_data['hash_rate'].iloc[-2]) /
                              onchain_data['hash_rate'].iloc[-2] * 100)

            st.metric(
                label="Hash Rate (EH/s)",
                value=f"{current_hashrate:,}",
                delta=f"{hashrate_change:.2f}%"
            )
    except Exception as e:
        st.error(f"Error displaying metrics: {str(e)}")
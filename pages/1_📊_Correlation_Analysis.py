import streamlit as st
import pandas as pd
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data
from utils.visualizations import create_etf_comparison

st.set_page_config(page_title="Correlation Analysis", page_icon="📊")

st.title("Bitcoin & ETF Correlation Analysis")

# Fetch data
btc_data = fetch_bitcoin_price()
etf_data = fetch_etf_data()

if not btc_data.empty and etf_data:
    # Display correlation metrics
    st.subheader("Price Correlation")
    
    # Calculate correlation between BTC and ETF prices
    for etf, data in etf_data.items():
        if not data['history'].empty:
            # Resample both series to daily and align dates
            btc_daily = btc_data['Close'].resample('D').last()
            etf_daily = data['history']['Close'].resample('D').last()
            
            # Calculate correlation on aligned data
            corr = btc_daily.corr(etf_daily)
            
            st.metric(
                f"BTC-{etf} Correlation",
                f"{corr:.2%}",
                help=f"Price correlation between Bitcoin and {etf}"
            )

    # Show comparison chart
    st.subheader("Price Comparison")
    comparison_chart = create_etf_comparison(etf_data)
    st.plotly_chart(comparison_chart, use_container_width=True)

else:
    st.warning("Unable to fetch required data for correlation analysis.")

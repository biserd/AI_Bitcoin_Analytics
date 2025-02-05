import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_fetcher import fetch_etf_data, fetch_onchain_metrics

st.set_page_config(page_title="Liquidity Analysis", page_icon="💧", layout="wide")

st.title("Liquidity & Volume Analysis")
st.markdown("Analyze trading volumes and liquidity metrics across Bitcoin ETFs")

# Load data
with st.spinner('Fetching data...'):
    etf_data = fetch_etf_data()
    onchain_data = fetch_onchain_metrics()

# Time period selector
time_period = st.selectbox(
    "Select Time Period",
    ["1 Week", "1 Month", "3 Months", "6 Months", "1 Year", "All Time"],
    index=2
)

if etf_data and not onchain_data.empty:
    # Volume comparison
    st.subheader("Trading Volume Comparison")
    
    # Create volume chart
    volume_data = []
    for etf_name, etf_info in etf_data.items():
        if 'history' in etf_info and not etf_info['history'].empty:
            volume_data.append({
                'ETF': etf_name,
                'Volume': etf_info['history']['Volume'].mean(),
                'Total Volume': etf_info['history']['Volume'].sum()
            })
    
    if volume_data:
        volume_df = pd.DataFrame(volume_data)
        fig = px.bar(
            volume_df,
            x='ETF',
            y='Volume',
            title="Average Daily Trading Volume"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Liquidity metrics
        st.subheader("Liquidity Metrics")
        col1, col2 = st.columns(2)
        
        with col1:
            # Market depth chart
            depth_fig = go.Figure()
            for etf_name, etf_info in etf_data.items():
                if 'orderbook' in etf_info:
                    depth_fig.add_trace(go.Scatter(
                        name=f"{etf_name} Bids",
                        x=etf_info['orderbook']['bid_prices'],
                        y=etf_info['orderbook']['bid_volumes'],
                        fill='tozeroy'
                    ))
                    depth_fig.add_trace(go.Scatter(
                        name=f"{etf_name} Asks",
                        x=etf_info['orderbook']['ask_prices'],
                        y=etf_info['orderbook']['ask_volumes'],
                        fill='tozeroy'
                    ))
            
            depth_fig.update_layout(title="Market Depth")
            st.plotly_chart(depth_fig, use_container_width=True)
        
        with col2:
            # Bid-ask spread chart
            spreads = []
            for etf_name, etf_info in etf_data.items():
                if 'orderbook' in etf_info:
                    spread = (etf_info['orderbook']['ask_prices'][0] - 
                            etf_info['orderbook']['bid_prices'][0])
                    spreads.append({
                        'ETF': etf_name,
                        'Spread': spread
                    })
            
            if spreads:
                spread_df = pd.DataFrame(spreads)
                spread_fig = px.bar(
                    spread_df,
                    x='ETF',
                    y='Spread',
                    title="Current Bid-Ask Spreads"
                )
                st.plotly_chart(spread_fig, use_container_width=True)

else:
    st.error("Unable to load data. Please try again later.")

# Explanation section
with st.expander("Understanding Liquidity Metrics"):
    st.write("""
    Key liquidity metrics help understand ETF trading efficiency:
    - Trading Volume: Higher volumes generally indicate better liquidity
    - Bid-Ask Spread: Tighter spreads suggest better liquidity
    - Market Depth: Shows available liquidity at different price levels
    - On-chain Volume: Provides context for overall market activity
    """)

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from utils.data_fetcher import fetch_etf_data, fetch_onchain_metrics
from datetime import datetime, timedelta

st.set_page_config(page_title="Liquidity Analysis", page_icon="💧", layout="wide")

st.title("Liquidity & Volume Analysis")
st.markdown("Analyze trading volumes and liquidity metrics across Bitcoin ETFs")

# Load data
with st.spinner('Fetching data...'):
    etf_data = fetch_etf_data()
    onchain_data = fetch_onchain_metrics()

# Time period selector with mapping to timedelta
time_periods = {
    "1 Week": timedelta(days=7),
    "1 Month": timedelta(days=30),
    "3 Months": timedelta(days=90),
    "6 Months": timedelta(days=180),
    "1 Year": timedelta(days=365),
    "All Time": timedelta(days=3650)
}

time_period = st.selectbox(
    "Select Time Period",
    list(time_periods.keys()),
    index=2
)

if etf_data and not onchain_data.empty:
    # Calculate start date based on selected period
    end_date = datetime.now()
    start_date = end_date - time_periods[time_period]

    # Filter data based on selected time period
    filtered_etf_data = {}
    volume_data = []

    for etf_name, etf_info in etf_data.items():
        if 'history' in etf_info and not etf_info['history'].empty:
            # Convert index to datetime if needed and filter
            history = etf_info['history'].copy()
            history.index = pd.to_datetime(history.index)
            filtered_history = history[history.index >= start_date]

            if not filtered_history.empty:
                volume_data.append({
                    'ETF': etf_name,
                    'Volume': filtered_history['Volume'].mean(),
                    'Total Volume': filtered_history['Volume'].sum()
                })

                filtered_etf_data[etf_name] = {
                    'history': filtered_history,
                    'orderbook': etf_info.get('orderbook', {})
                }

    if volume_data:
        # Volume comparison chart
        st.subheader("Trading Volume Comparison")
        volume_df = pd.DataFrame(volume_data)
        fig = px.bar(
            volume_df,
            x='ETF',
            y='Volume',
            title=f"Average Daily Trading Volume ({time_period})"
        )
        fig.update_layout(
            yaxis_title="Volume",
            xaxis_title="ETF",
            height=400,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Liquidity metrics
        st.subheader("Liquidity Metrics")
        col1, col2 = st.columns(2)

        with col1:
            # Market depth chart
            depth_fig = go.Figure()
            for etf_name, etf_info in filtered_etf_data.items():
                if 'orderbook' in etf_info:
                    depth_fig.add_trace(go.Scatter(
                        name=f"{etf_name} Bids",
                        x=etf_info['orderbook'].get('bid_prices', []),
                        y=etf_info['orderbook'].get('bid_volumes', []),
                        fill='tozeroy'
                    ))
                    depth_fig.add_trace(go.Scatter(
                        name=f"{etf_name} Asks",
                        x=etf_info['orderbook'].get('ask_prices', []),
                        y=etf_info['orderbook'].get('ask_volumes', []),
                        fill='tozeroy'
                    ))

            depth_fig.update_layout(
                title=f"Market Depth ({time_period})",
                xaxis_title="Price",
                yaxis_title="Volume",
                height=400,
                margin=dict(l=40, r=40, t=60, b=40)
            )
            st.plotly_chart(depth_fig, use_container_width=True)

        with col2:
            # Bid-ask spread chart
            spreads = []
            for etf_name, etf_info in filtered_etf_data.items():
                if 'orderbook' in etf_info:
                    spread = (etf_info['orderbook'].get('ask_prices', [0])[0] - 
                            etf_info['orderbook'].get('bid_prices', [0])[0])
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
                    title=f"Current Bid-Ask Spreads ({time_period})"
                )
                spread_fig.update_layout(
                    yaxis_title="Spread",
                    xaxis_title="ETF",
                    height=400,
                    margin=dict(l=40, r=40, t=60, b=40)
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
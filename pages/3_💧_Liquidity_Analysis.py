import streamlit as st
import plotly.graph_objects as go
from utils.data_fetcher import fetch_etf_data

st.set_page_config(page_title="Liquidity Analysis", page_icon="💧")

st.title("Market Liquidity Analysis")

# Add period selector
period = st.selectbox(
    "Select Time Period",
    ["1 Week", "1 Month", "3 Months", "6 Months", "1 Year"],
    key="liquidity_period_selector"
)

# Convert period to parameter for data fetching
period_param = period.lower().replace(" ", "_")
etf_data = fetch_etf_data(period=period_param)

# Add a divider
st.divider()

if etf_data:
    for etf, data in etf_data.items():
        st.subheader(f"{etf} Order Book Depth")
        
        # Create order book visualization
        fig = go.Figure()
        
        # Add bid side (buyers)
        fig.add_trace(go.Bar(
            x=data['orderbook']['bid_volumes'],
            y=data['orderbook']['bid_prices'],
            orientation='h',
            name='Bids',
            marker_color='rgba(33, 206, 153, 0.7)'
        ))
        
        # Add ask side (sellers)
        fig.add_trace(go.Bar(
            x=data['orderbook']['ask_volumes'],
            y=data['orderbook']['ask_prices'],
            orientation='h',
            name='Asks',
            marker_color='rgba(255, 80, 0, 0.7)'
        ))
        
        fig.update_layout(
            title=f"{etf} Order Book",
            yaxis_title="Price (USD)",
            xaxis_title="Volume",
            barmode='overlay',
            template='plotly_white'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Show key metrics
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Total Bid Volume",
                f"${sum(data['orderbook']['bid_volumes']):,.0f}"
            )
        with col2:
            st.metric(
                "Total Ask Volume",
                f"${sum(data['orderbook']['ask_volumes']):,.0f}"
            )
else:
    st.warning("Unable to fetch ETF data for liquidity analysis.")

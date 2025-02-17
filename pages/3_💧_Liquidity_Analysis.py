
import streamlit as st
import plotly.graph_objects as go
from utils.data_fetcher import fetch_etf_data

st.set_page_config(page_title="Liquidity Analysis", page_icon="💧")

st.title("Market Liquidity Analysis")

# Add period selector in a container
with st.container():
    period_options = {
        "1 Week": "1_week",
        "1 Month": "1_month",
        "3 Months": "3_months",
        "6 Months": "6_months",
        "1 Year": "1_year"
    }
    
    selected_period = st.selectbox(
        "Select Analysis Period",
        options=list(period_options.keys()),
        key="liquidity_period_selector"
    )
    
    # Convert selected period to the format expected by fetch_etf_data
    period_param = period_options[selected_period]
    
    # Fetch data based on selected period
    etf_data = fetch_etf_data(period=period_param)

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

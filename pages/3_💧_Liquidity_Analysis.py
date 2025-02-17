import streamlit as st
import plotly.graph_objects as go
from utils.data_fetcher import fetch_etf_data

st.set_page_config(page_title="Liquidity Analysis", page_icon="💧")

# Title and period selector
st.title("Market Liquidity Analysis")

periods = ["1_week", "1_month", "3_months", "6_months", "1_year"]
period_display = {"1_week": "1 Week", "1_month": "1 Month", 
                 "3_months": "3 Months", "6_months": "6 Months", 
                 "1_year": "1 Year"}

period_param = st.selectbox("Select Time Period", 
                          options=periods,
                          format_func=lambda x: period_display[x])

# Fetch data
etf_data = fetch_etf_data(period=period_param)

if etf_data:
    for etf, data in etf_data.items():
        st.subheader(f"{etf} Order Book Depth")

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=data['orderbook']['bid_volumes'],
            y=data['orderbook']['bid_prices'],
            orientation='h',
            name='Bids',
            marker_color='rgba(33, 206, 153, 0.7)'
        ))

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

        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Bid Volume", f"${sum(data['orderbook']['bid_volumes']):,.0f}")
        with col2:
            st.metric("Total Ask Volume", f"${sum(data['orderbook']['ask_volumes']):,.0f}")
else:
    st.warning("Unable to fetch ETF data for liquidity analysis.")
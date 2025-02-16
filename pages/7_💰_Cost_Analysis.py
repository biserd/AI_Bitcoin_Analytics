import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data

st.set_page_config(page_title="Cost Analysis", page_icon="💰")

st.title("Investment Cost Analysis: Bitcoin vs ETFs")

# Fetch required data
btc_data = fetch_bitcoin_price()
etf_data = fetch_etf_data()

# Define fee structures
fee_structure = {
    'Spot Bitcoin': {
        'Trading Fee': '0.1-0.5%',
        'Custody Fee': '0%',
        'Management Fee': '0%',
        'Withdrawal Fee': '$5-25',
        'Security': 'Self-custody',
        'Pros': ['Lower fees', 'Direct ownership', 'No management fees'],
        'Cons': ['Security responsibility', 'Complex setup', 'Multiple fees for trading']
    },
    'Bitcoin ETFs': {
        'Trading Fee': '0-0.1%',
        'Custody Fee': '0%',
        'Management Fee': '0.25-1%',
        'Withdrawal Fee': '0',
        'Security': 'Institutional',
        'Pros': ['Easy to buy/sell', 'Professional management', 'Traditional brokerage'],
        'Cons': ['Higher management fees', 'No direct BTC ownership', 'Premium/Discount to NAV']
    }
}

# Investment Calculator
st.header("Investment Calculator")

col1, col2 = st.columns(2)
with col1:
    investment_amount = st.number_input("Investment Amount ($)", min_value=100, value=10000)
    investment_period = st.slider("Investment Period (Years)", min_value=1, max_value=10, value=5)

with col2:
    trading_frequency = st.selectbox(
        "Trading Frequency",
        ["Buy and Hold", "Monthly", "Weekly", "Daily"]
    )

# Calculate costs for different scenarios
def calculate_costs(amount, period, frequency):
    trades_per_year = {
        "Buy and Hold": 1,
        "Monthly": 12,
        "Weekly": 52,
        "Daily": 252
    }
    
    spot_costs = {
        'trading_fees': amount * 0.003 * trades_per_year[frequency] * period,
        'custody_fees': 0,
        'withdrawal_fees': 15 * period  # Assuming one withdrawal per year
    }
    
    etf_costs = {
        'trading_fees': amount * 0.001 * trades_per_year[frequency] * period,
        'management_fees': amount * 0.005 * period,  # 0.5% annual management fee
        'other_fees': 0
    }
    
    return spot_costs, etf_costs

spot_costs, etf_costs = calculate_costs(investment_amount, investment_period, trading_frequency)

# Display cost comparison
st.header("Cost Comparison")

# Create comparison chart
fig = go.Figure()

# Spot Bitcoin costs
spot_total = sum(spot_costs.values())
fig.add_trace(go.Bar(
    name='Spot Bitcoin',
    x=list(spot_costs.keys()),
    y=list(spot_costs.values()),
    marker_color='#F7931A'
))

# ETF costs
etf_total = sum(etf_costs.values())
fig.add_trace(go.Bar(
    name='Bitcoin ETFs',
    x=list(etf_costs.keys()),
    y=list(etf_costs.values()),
    marker_color='#1E88E5'
))

fig.update_layout(
    title='Cost Breakdown Comparison',
    yaxis_title='Cost ($)',
    barmode='group',
    template='plotly_white'
)

st.plotly_chart(fig, use_container_width=True)

# Display total costs
col1, col2 = st.columns(2)
with col1:
    st.metric(
        "Total Spot Bitcoin Costs",
        f"${spot_total:,.2f}",
        f"{((spot_total/investment_amount)*100):,.2f}% of investment"
    )
with col2:
    st.metric(
        "Total ETF Costs",
        f"${etf_total:,.2f}",
        f"{((etf_total/investment_amount)*100):,.2f}% of investment"
    )

# Fee Structure Comparison
st.header("Fee Structure Details")

col1, col2 = st.columns(2)
with col1:
    st.subheader("Spot Bitcoin")
    for key, value in fee_structure['Spot Bitcoin'].items():
        if key not in ['Pros', 'Cons']:
            st.write(f"**{key}:** {value}")
    
    st.write("**Advantages:**")
    for pro in fee_structure['Spot Bitcoin']['Pros']:
        st.write(f"✅ {pro}")
    
    st.write("**Disadvantages:**")
    for con in fee_structure['Spot Bitcoin']['Cons']:
        st.write(f"⚠️ {con}")

with col2:
    st.subheader("Bitcoin ETFs")
    for key, value in fee_structure['Bitcoin ETFs'].items():
        if key not in ['Pros', 'Cons']:
            st.write(f"**{key}:** {value}")
    
    st.write("**Advantages:**")
    for pro in fee_structure['Bitcoin ETFs']['Pros']:
        st.write(f"✅ {pro}")
    
    st.write("**Disadvantages:**")
    for con in fee_structure['Bitcoin ETFs']['Cons']:
        st.write(f"⚠️ {con}")

# Investment Recommendations
st.header("Investment Recommendations")

st.info("""
Based on your investment profile:

1. **For long-term investors (Buy and Hold):**
   - Consider spot Bitcoin if you're comfortable with self-custody
   - ETFs might be better if you prefer traditional investment vehicles

2. **For active traders:**
   - ETFs generally offer lower trading fees and better liquidity
   - Consider the impact of management fees on long-term returns

3. **For new investors:**
   - ETFs provide an easier entry point and familiar structure
   - Lower technical barriers to entry
""")

# Disclaimer
st.warning("""
**Disclaimer:** This analysis is for informational purposes only and should not be considered financial advice. 
Actual costs may vary based on your chosen exchange, ETF provider, and market conditions. 
Always conduct your own research and consider consulting with a financial advisor before making investment decisions.
""")


import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data
from datetime import datetime, timedelta

st.set_page_config(page_title="Cost Analysis", page_icon="💰", layout="wide")

st.title("Bitcoin vs ETF Cost Analysis")
st.markdown("Compare the total cost of ownership between spot Bitcoin and Bitcoin ETFs")

# Load data
with st.spinner('Fetching data...'):
    btc_price = fetch_bitcoin_price()
    etf_data = fetch_etf_data()

# Input parameters
col1, col2 = st.columns(2)

with col1:
    investment_amount = st.number_input("Investment Amount (USD)", min_value=100, value=10000)
    holding_period = st.slider("Holding Period (Years)", min_value=1, max_value=10, value=1)

with col2:
    trading_frequency = st.selectbox(
        "Trading Frequency",
        ["Buy and Hold", "Monthly", "Weekly", "Daily"]
    )

# ETF costs
etf_costs = {
    'BITO': {'expense_ratio': 0.0095, 'avg_spread': 0.0010},
    'BTF': {'expense_ratio': 0.0065, 'avg_spread': 0.0012},
    'BITI': {'expense_ratio': 0.0095, 'avg_spread': 0.0015}
}

# Bitcoin costs
bitcoin_costs = {
    'exchange_fee': 0.001,  # 0.1% trading fee
    'withdrawal_fee': 0.0002,  # BTC network fee
    'custody_cost': 0.001  # Annual custody solution cost
}

# Calculate costs
def calculate_total_cost(investment_amount, holding_period, is_etf=True, expense_ratio=0.0095):
    trading_costs = investment_amount * (0.001 if is_etf else bitcoin_costs['exchange_fee'])
    annual_costs = investment_amount * (expense_ratio if is_etf else bitcoin_costs['custody_cost'])
    total_cost = trading_costs + (annual_costs * holding_period)
    return total_cost

# Display comparison
st.subheader("Cost Comparison")

costs_data = []
# Calculate Bitcoin costs
btc_total_cost = calculate_total_cost(investment_amount, holding_period, False)
costs_data.append({
    'Investment Type': 'Spot Bitcoin',
    'Total Cost (USD)': btc_total_cost,
    'Cost Percentage': (btc_total_cost / investment_amount) * 100
})

# Calculate ETF costs
for etf, cost_info in etf_costs.items():
    total_cost = calculate_total_cost(investment_amount, holding_period, True, cost_info['expense_ratio'])
    costs_data.append({
        'Investment Type': f'{etf} ETF',
        'Total Cost (USD)': total_cost,
        'Cost Percentage': (total_cost / investment_amount) * 100
    })

# Create comparison chart
df_costs = pd.DataFrame(costs_data)
fig = px.bar(
    df_costs,
    x='Investment Type',
    y='Cost Percentage',
    title='Total Cost Comparison (% of Investment)',
    labels={'Cost Percentage': 'Cost (%)'}
)
st.plotly_chart(fig, use_container_width=True)

# Display detailed breakdown
st.subheader("Detailed Cost Breakdown")
st.dataframe(df_costs)

# Recommendation
st.subheader("Investment Recommendation")
min_cost_option = df_costs.loc[df_costs['Cost Percentage'].idxmin()]
st.success(f"Based on your parameters, **{min_cost_option['Investment Type']}** is the most cost-effective option with a total cost of {min_cost_option['Cost Percentage']:.2f}% over {holding_period} years.")

# Considerations
st.markdown("""
### Additional Considerations
- **ETF Advantages**: Professional management, regulatory oversight, easier tax reporting
- **Bitcoin Advantages**: Direct ownership, no management fees, potential for yield generation
- **Risk Factors**: Consider tracking error, liquidity, and custody security
""")

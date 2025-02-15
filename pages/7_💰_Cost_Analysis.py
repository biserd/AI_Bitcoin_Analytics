
import streamlit as st
import pandas as pd
import plotly.express as px
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data
from datetime import datetime, timedelta

st.set_page_config(page_title="Bitcoin Price Analysis", page_icon="💰", layout="wide")

st.title("Bitcoin Price Analysis")
st.markdown("Compare investment options between spot Bitcoin and Bitcoin ETFs")

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

df_costs = pd.DataFrame(costs_data)

# Display recommendation first
# Calculate potential returns
returns_data = []
btc_historical_return = btc_price['Close'].pct_change().mean() * 252  # Annualized return

for investment_type in df_costs['Investment Type']:
    if investment_type == 'Spot Bitcoin':
        annual_return = btc_historical_return
    else:
        # ETF returns are slightly lower due to tracking error
        annual_return = btc_historical_return * 0.99
    
    # Calculate net return after costs
    cost_pct = df_costs.loc[df_costs['Investment Type'] == investment_type, 'Cost Percentage'].values[0]
    net_annual_return = annual_return - (cost_pct / holding_period)
    
    potential_profit = investment_amount * (pow(1 + net_annual_return, holding_period) - 1)
    returns_data.append({
        'Investment Type': investment_type,
        'Potential Profit': potential_profit,
        'Net Annual Return': net_annual_return * 100
    })

df_returns = pd.DataFrame(returns_data)

# Display combined recommendation
st.subheader("Investment Recommendation")
best_profit_option = df_returns.loc[df_returns['Potential Profit'].idxmax()]
min_cost_option = df_costs.loc[df_costs['Cost Percentage'].idxmin()]

col1, col2 = st.columns(2)
with col1:
    st.info(f"**Most Cost-Effective**: {min_cost_option['Investment Type']}\nTotal Cost: {min_cost_option['Cost Percentage']:.2f}%")
    
with col2:
    st.success(f"**Highest Profit Potential**: {best_profit_option['Investment Type']}\nEstimated Return: {best_profit_option['Net Annual Return']:.1f}% per year")

# Display profit comparison
st.subheader("Profit Potential Comparison")
profit_fig = px.bar(
    df_returns,
    x='Investment Type',
    y='Potential Profit',
    title=f'Estimated Profit Over {holding_period} Years (USD)',
    labels={'Potential Profit': 'Profit ($)'}
)
st.plotly_chart(profit_fig, use_container_width=True)

# Display comparison
st.subheader("Cost Comparison")
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

# Considerations
st.markdown("""
### Additional Considerations
- **ETF Advantages**: Professional management, regulatory oversight, easier tax reporting
- **Bitcoin Advantages**: Direct ownership, no management fees, potential for yield generation
- **Risk Factors**: Consider tracking error, liquidity, and custody security
""")

import streamlit as st

def display_education_section():
    """Display educational content about Bitcoin and cryptocurrency markets"""
    st.header("Educational Resources")

    with st.expander("What are Bitcoin ETFs?"):
        st.write("""
        Bitcoin ETFs (Exchange-Traded Funds) are investment vehicles that track the price of Bitcoin 
        and trade on traditional stock exchanges. They allow investors to gain exposure to Bitcoin 
        without directly owning the cryptocurrency.

        Key benefits include:
        - Regulated investment vehicle
        - Easy to buy and sell through traditional brokerage accounts
        - No need for crypto wallets or direct crypto custody
        - Potential tax advantages in certain accounts
        """)

    with st.expander("Understanding On-Chain Metrics"):
        st.write("""
        On-chain metrics are measurements of activity occurring on the Bitcoin blockchain. 
        They provide insights into network usage and health.

        Key metrics include:
        - Active Addresses: Number of unique addresses participating in transactions
        - Transaction Volume: Total value of Bitcoin being transferred
        - Hash Rate: Total computational power securing the network
        """)

    with st.expander("How to Use This Dashboard"):
        st.write("""
        This dashboard combines on-chain metrics with ETF data to provide a comprehensive view of the Bitcoin market.

        Tips for usage:
        - Compare on-chain metrics with price movements
        - Monitor ETF flows for institutional interest
        - Use interactive features to zoom and analyze specific time periods
        - Check daily for updated metrics and trends
        """)
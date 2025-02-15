import streamlit as st
import pandas as pd
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics
from utils.visualizations import create_price_chart, create_etf_comparison
from components.metrics import display_metrics_section
from components.education import display_education_section

# Page configuration
st.set_page_config(
    page_title="Bitcoin Analytics Dashboard | Real-time Crypto Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About':
        """
        # Bitcoin Analytics Dashboard
        Comprehensive Bitcoin ETF and On-Chain Analytics Platform providing real-time market insights, ETF analysis, and AI-powered predictions.

        Keywords: Bitcoin, ETF, Cryptocurrency, Market Analysis, Trading, Blockchain
        """
    })

# Add Google Analytics
from components.analytics import inject_ga
inject_ga()

# Add meta tags
st.markdown("""
    <head>
        <title>Bitcoin Analytics Dashboard | Real-time Crypto Analysis</title>
        <meta name="description" content="Comprehensive Bitcoin ETF and cryptocurrency analytics platform. Track real-time market data, ETF performance, and on-chain metrics.">
        <meta name="keywords" content="Bitcoin, ETF, Cryptocurrency, Market Analysis, Trading, Blockchain, Analytics">
        <meta property="og:title" content="Bitcoin Analytics Dashboard">
        <meta property="og:description" content="Real-time Bitcoin ETF and cryptocurrency analytics platform">
        <meta property="og:type" content="website">
    </head>
    <script type="application/ld+json">
    {
      "@context": "https://schema.org",
      "@type": "WebApplication",
      "name": "Bitcoin ETF Analytics Dashboard",
      "description": "Real-time Bitcoin ETF and cryptocurrency analytics platform providing market insights and trading analysis",
      "applicationCategory": "FinanceApplication",
      "operatingSystem": "Any",
      "offers": {
        "@type": "Offer",
        "price": "0"
      }
    }
    </script>
    """, unsafe_allow_html=True)

# CSS is now loaded via config.toml

# Header
st.title("Bitcoin AI Analytics Dashboard")
st.markdown("### Comprehensive Bitcoin ETF and On-Chain Analytics Platform")

# Sidebar for navigation with custom styling
with st.sidebar:
    st.markdown("### 📊 Navigation")
    page = st.radio(
        "",  # Empty label for cleaner look
        ["Home", "ETF Analysis", "Market Metrics"],
        format_func=lambda x:
        f"{'🏠' if x == 'Home' else '📈' if x == 'ETF Analysis' else '📊'} {x}")

# Load key metrics for homepage
with st.spinner('Fetching latest data...'):
    btc_price = fetch_bitcoin_price()
    etf_data = fetch_etf_data()
    onchain_data = fetch_onchain_metrics()

if page == "Home":
    # Display metrics section if data is available
    if not btc_price.empty and not onchain_data.empty:
        display_metrics_section(btc_price, onchain_data)
    else:
        st.warning(
            "Some data is currently unavailable. Please try again later.")

    # Main price chart
    if not btc_price.empty:
        st.subheader("Bitcoin Price Overview")
        st.plotly_chart(create_price_chart(btc_price),
                        use_container_width=True)

    # ETF Comparison
    if etf_data:
        st.subheader("ETF Performance Comparison")
        st.plotly_chart(create_etf_comparison(etf_data),
                        use_container_width=True)

elif page == "ETF Analysis":
    st.header("ETF Analysis")
    if etf_data:
        # ETF Performance Metrics
        for etf_name, etf_info in etf_data.items():
            with st.expander(f"{etf_name} Details"):
                if 'history' in etf_info and not etf_info['history'].empty:
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Current Price",
                            f"${etf_info['history']['Close'].iloc[-1]:.2f}",
                            f"{((etf_info['history']['Close'].iloc[-1] / etf_info['history']['Close'].iloc[-2]) - 1) * 100:.2f}%"
                        )
                    with col2:
                        st.metric(
                            "Volume",
                            f"{etf_info['history']['Volume'].iloc[-1]:,.0f}")

                    # Historical performance chart
                    st.line_chart(etf_info['history']['Close'])

elif page == "Market Metrics":
    st.header("Market Metrics")
    if not onchain_data.empty:
        # Display on-chain metrics
        metrics_tab1, metrics_tab2 = st.tabs(
            ["Network Activity", "Mining Metrics"])

        with metrics_tab1:
            st.subheader("Network Activity")
            st.line_chart(onchain_data['active_addresses'])
            st.line_chart(onchain_data['transaction_volume'])

        with metrics_tab2:
            st.subheader("Mining Metrics")
            st.line_chart(onchain_data['hash_rate'])

# Footer
st.markdown("---")
st.markdown(
    "Data updates daily. On-chain metrics and ETF data are sourced from various providers. "
    "This dashboard is for informational purposes only.")
<replit_final_file>
import streamlit as st
import pandas as pd
import json
from utils.predictions import analyze_market_trends
from utils.data_fetcher import fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics
from utils.visualizations import create_price_chart, create_etf_comparison
from components.metrics import display_metrics_section
from components.education import display_education_section
from components.analytics import inject_ga


# Page configuration
st.set_page_config(
    page_title="Bitcoin Analytics Dashboard | Real-time Crypto Analysis",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for data caching
if 'data_cache' not in st.session_state:
    st.session_state.data_cache = {
        'btc_price': None,
        'etf_data': None,
        'onchain_data': None,
        'last_update': None
    }

# Add Google Analytics
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
st.title("Bitcoin Analytics Dashboard")
st.markdown("### Real-time Cryptocurrency Market Analysis")

try:
    with st.spinner('Fetching latest data...'):
        # Fetch data with error handling
        try:
            btc_price = fetch_bitcoin_price()
            st.session_state.data_cache['btc_price'] = btc_price
        except Exception as e:
            st.error(f"Error fetching Bitcoin price data: {str(e)}")
            btc_price = st.session_state.data_cache.get('btc_price', pd.DataFrame())

        try:
            etf_data = fetch_etf_data()
            st.session_state.data_cache['etf_data'] = etf_data
        except Exception as e:
            st.error(f"Error fetching ETF data: {str(e)}")
            etf_data = st.session_state.data_cache.get('etf_data', {})

        try:
            onchain_data = fetch_onchain_metrics()
            st.session_state.data_cache['onchain_data'] = onchain_data
        except Exception as e:
            st.error(f"Error fetching on-chain metrics: {str(e)}")
            onchain_data = st.session_state.data_cache.get('onchain_data', pd.DataFrame())

    # Display AI Predictions
    if not btc_price.empty and not onchain_data.empty:
        try:
            analysis_json = analyze_market_trends(btc_price, onchain_data)
            if analysis_json:
                analysis = json.loads(analysis_json)

                col1, col2, col3 = st.columns([2,1,1])
                with col1:
                    sentiment_color = {
                        "bullish": "🟢",
                        "bearish": "🔴",
                        "neutral": "⚪"
                    }.get(analysis["market_sentiment"], "⚪")
                    st.subheader(f"Market Sentiment: {sentiment_color} {analysis['market_sentiment'].title()}")
                    st.progress(analysis["confidence_score"])

                with col2:
                    st.metric(
                        "Direction", 
                        analysis["prediction"]["price_direction"].title(),
                        f"{analysis['prediction']['confidence']*100:.1f}% confidence"
                    )

                with col3:
                    if "key_factors" in analysis:
                        with st.expander("Key Factors"):
                            for factor in analysis["key_factors"][:2]:
                                st.markdown(f"• {factor}")
        except Exception as e:
            st.error(f"Error generating market analysis: {str(e)}")

    st.divider()

    # Sidebar for navigation with custom styling
    with st.sidebar:
        st.markdown("### 📊 Navigation")
        page = st.radio(
            "",  # Empty label for cleaner look
            ["Home", "ETF Analysis", "Market Metrics"],
            format_func=lambda x:
            f"{'🏠' if x == 'Home' else '📈' if x == 'ETF Analysis' else '📊'} {x}")

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
            try:
                price_chart = create_price_chart(btc_price)
                st.plotly_chart(price_chart, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating price chart: {str(e)}")

        # ETF Comparison
        if etf_data:
            st.subheader("ETF Performance Comparison")
            try:
                etf_chart = create_etf_comparison(etf_data)
                st.plotly_chart(etf_chart, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating ETF comparison chart: {str(e)}")

        #On-chain Metrics Section (Added from edited code)
        if not onchain_data.empty:
            st.subheader("Network Activity")
            try:
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Active Addresses",
                        f"{onchain_data['active_addresses'].iloc[-1]:,.0f}",
                        f"{((onchain_data['active_addresses'].iloc[-1] / onchain_data['active_addresses'].iloc[-2]) - 1) * 100:.1f}%"
                    )
                with col2:
                    st.metric(
                        "Transaction Volume",
                        f"${onchain_data['transaction_volume'].iloc[-1]:,.0f}",
                        f"{((onchain_data['transaction_volume'].iloc[-1] / onchain_data['transaction_volume'].iloc[-2]) - 1) * 100:.1f}%"
                    )
            except Exception as e:
                st.error(f"Error displaying network metrics: {str(e)}")



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
        "Data updates in real-time. Market analysis and predictions are for informational purposes only.")

except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
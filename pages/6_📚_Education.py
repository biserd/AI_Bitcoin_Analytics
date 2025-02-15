
import streamlit as st
from components.education import display_education_section

st.set_page_config(
    page_title="Bitcoin Education | Learn Crypto Analytics",
    page_icon="📚",
    layout="wide",
    menu_items={
        'About': """
        # Bitcoin Education Resources
        Learn about Bitcoin ETFs, On-Chain Metrics, and cryptocurrency market analysis.
        
        Keywords: Bitcoin Education, Crypto Learning, ETF Analysis, Trading Guide
        """
    }
)

st.markdown("""
    <head>
        <title>Bitcoin Education | Learn Crypto Analytics</title>
        <meta name="description" content="Learn about Bitcoin ETFs, cryptocurrency trading, and market analysis. Comprehensive educational resources for crypto investors.">
        <meta name="keywords" content="Bitcoin Education, Crypto Learning, ETF Analysis, Trading Guide">
        <meta property="og:title" content="Bitcoin Education Resources">
        <meta property="og:description" content="Learn about Bitcoin ETFs and cryptocurrency trading">
        <meta property="og:type" content="article">
    </head>
    """, unsafe_allow_html=True)

st.title("Educational Resources")
st.markdown("Learn about Bitcoin ETFs, On-Chain Metrics, and how to use this dashboard effectively")

# Display education content
display_education_section()

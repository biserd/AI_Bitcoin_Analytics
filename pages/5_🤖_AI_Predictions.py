import streamlit as st
import json
from utils.predictions import analyze_market_trends, generate_predictions
from utils.data_fetcher import fetch_bitcoin_price, fetch_onchain_metrics

st.set_page_config(page_title="AI Predictions", page_icon="🤖")

st.title("AI Market Predictions")

# Fetch required data
price_data = fetch_bitcoin_price()
onchain_data = fetch_onchain_metrics()

if not price_data.empty and not onchain_data.empty:
    # Generate analysis and predictions
    analysis = json.loads(analyze_market_trends(price_data, onchain_data))
    predictions = generate_predictions()
    
    # Display market sentiment
    st.header("Market Sentiment")
    sentiment_color = {
        'bullish': 'green',
        'bearish': 'red',
        'neutral': 'orange'
    }.get(analysis['market_sentiment'], 'blue')
    
    st.markdown(f"""
    <h2 style='color: {sentiment_color}'>
        {analysis['market_sentiment'].upper()}
    </h2>
    """, unsafe_allow_html=True)
    
    st.metric("Confidence Score", f"{analysis['confidence_score']*100:.1f}%")
    
    # Display key factors
    st.subheader("Key Market Factors")
    for factor in analysis['key_factors']:
        st.markdown(f"- {factor}")
    
    # Display predictions
    st.subheader("Market Scenarios")
    cols = st.columns(len(predictions))
    for col, (scenario, data) in zip(cols, predictions.items()):
        with col:
            st.metric(
                scenario.title(),
                f"{data['probability']*100:.1f}%",
                help="\n".join(data['factors'])
            )
    
    # Risk Analysis
    st.subheader("Risk Analysis")
    for risk in analysis['risk_factors']:
        st.warning(risk)
        
    # Market Outlook
    st.subheader("Market Outlook")
    st.info(analysis['short_term_outlook'])
    st.info(analysis['medium_term_outlook'])
else:
    st.warning("Unable to fetch required data for market predictions.")

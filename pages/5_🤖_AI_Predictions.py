import streamlit as st
import json
import pandas as pd
import plotly.graph_objects as go
from utils.data_fetcher import fetch_bitcoin_price, fetch_onchain_metrics
from utils.predictions import analyze_market_trends, generate_price_scenarios

st.set_page_config(page_title="AI Market Predictions", page_icon="🤖", layout="wide")

st.title("AI-Powered Market Analysis")
st.markdown("Advanced market predictions and trend analysis using artificial intelligence")

# Load data
with st.spinner('Analyzing market data...'):
    btc_price = fetch_bitcoin_price()
    onchain_data = fetch_onchain_metrics()

if not btc_price.empty and not onchain_data.empty:
    # Generate AI analysis
    analysis_json = analyze_market_trends(btc_price, onchain_data)
    
    if analysis_json:
        try:
            analysis = json.loads(analysis_json)
            
            # Display market sentiment
            sentiment_color = {
                "bullish": "🟢",
                "bearish": "🔴",
                "neutral": "⚪"
            }.get(analysis["market_sentiment"], "⚪")
            
            st.header(f"Market Sentiment: {sentiment_color} {analysis['market_sentiment'].title()}")
            st.progress(analysis["confidence_score"])
            
            # Display predictions in columns
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Short-term Outlook (7 days)")
                st.write(analysis["short_term_outlook"])
                
                st.subheader("Key Factors")
                for factor in analysis["key_factors"]:
                    st.markdown(f"• {factor}")
            
            with col2:
                st.subheader("Medium-term Outlook (30 days)")
                st.write(analysis["medium_term_outlook"])
                
                st.subheader("Risk Factors")
                for risk in analysis["risk_factors"]:
                    st.markdown(f"• {risk}")
            
            # Generate price scenarios
            scenarios = generate_price_scenarios(btc_price)
            
            st.subheader("Price Scenarios")
            
            # Create price scenarios visualization
            fig = go.Figure()

            current_price = btc_price['Close'].iloc[-1]

            # Add scenarios to plot with proper spacing
            for i, (scenario, data) in enumerate(scenarios.items()):
                fig.add_trace(go.Indicator(
                    mode="number+delta",
                    value=data["price"],
                    title={"text": f"<b>{scenario.title()}</b><br><span style='font-size:0.8em'>({data['probability']*100:.0f}% probability)</span>"},
                    delta={'reference': current_price, 'relative': True},
                    domain={'row': 0, 'column': i}
                ))

            # Update layout for better spacing
            fig.update_layout(
                grid={'rows': 1, 'columns': 3, 'pattern': "independent"},
                height=250,
                margin=dict(l=40, r=40, t=30, b=30),
            )

            st.plotly_chart(fig, use_container_width=True)

            # Display factors for each scenario
            col1, col2, col3 = st.columns(3)
            for col, (scenario, data) in zip([col1, col2, col3], scenarios.items()):
                with col:
                    st.markdown(f"**{scenario.title()} Scenario Factors:**")
                    for factor in data["factors"]:
                        st.markdown(f"• {factor}")

            # Trading volume analysis
            st.subheader("Trading Volume Analysis")
            st.write(analysis["trading_volume_analysis"])
            
            # Prediction confidence
            st.subheader("Price Direction Prediction")
            pred = analysis["prediction"]
            st.metric(
                label="Predicted Direction",
                value=pred["price_direction"].title(),
                delta=f"{pred['confidence']*100:.1f}% confidence"
            )
            
            st.subheader("Supporting Metrics")
            for metric in pred["supporting_metrics"]:
                st.markdown(f"• {metric}")
            
        except Exception as e:
            st.error(f"Error parsing AI analysis: {str(e)}")
    else:
        st.error("Unable to generate AI analysis. Please try again later.")
else:
    st.error("Unable to load market data. Please try again later.")

# Add explanation
with st.expander("About AI Market Predictions"):
    st.write("""
    This analysis uses advanced AI to process multiple data points:
    - Historical price and volume data
    - On-chain metrics and network activity
    - Market sentiment indicators
    - Technical analysis patterns
    
    The AI model considers these factors to generate insights and predictions.
    However, please note that these are estimates and should not be used as
    financial advice.
    """)
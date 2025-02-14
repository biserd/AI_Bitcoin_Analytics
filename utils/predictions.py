import os
from openai import OpenAI
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024
# do not change this unless explicitly requested by the user
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def analyze_market_trends(price_data, onchain_data):
    """
    Analyze market trends using GPT-4o to generate insights and predictions
    """
    # Prepare recent market data summary
    recent_price_change = ((price_data['Close'].iloc[-1] - price_data['Close'].iloc[-7]) / 
                          price_data['Close'].iloc[-7] * 100)
    
    avg_volume = price_data['Volume'].tail(7).mean()
    price_volatility = price_data['Close'].tail(30).std()
    
    # Prepare on-chain metrics summary
    recent_active_addresses = onchain_data['active_addresses'].tail(7).mean()
    recent_transaction_volume = onchain_data['transaction_volume'].tail(7).mean()
    
    # Create prompt for GPT-4o
    prompt = f"""Analyze the following Bitcoin market data and provide insights:
    - 7-day price change: {recent_price_change:.2f}%
    - 7-day average trading volume: ${avg_volume:,.0f}
    - 30-day price volatility: ${price_volatility:.2f}
    - 7-day average active addresses: {recent_active_addresses:,.0f}
    - 7-day average transaction volume: ${recent_transaction_volume:,.0f}

    Provide market analysis in JSON format with the following structure:
    {{
        "market_sentiment": "bullish/bearish/neutral",
        "confidence_score": 0.0-1.0,
        "key_factors": ["factor1", "factor2", "factor3"],
        "short_term_outlook": "detailed analysis for 7-day outlook",
        "medium_term_outlook": "detailed analysis for 30-day outlook",
        "risk_factors": ["risk1", "risk2"],
        "trading_volume_analysis": "analysis of trading volumes",
        "prediction": {{
            "price_direction": "up/down/sideways",
            "confidence": 0.0-1.0,
            "supporting_metrics": ["metric1", "metric2"]
        }}
    }}
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a cryptocurrency market analyst expert."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        analysis = response.choices[0].message.content
        return analysis
    except Exception as e:
        st.error(f"Error generating market analysis: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def generate_price_scenarios(price_data):
    """
    Generate potential price scenarios based on historical patterns
    """
    current_price = price_data['Close'].iloc[-1]
    
    # Calculate historical volatility
    volatility = price_data['Close'].pct_change().std()
    
    # Generate scenarios
    scenarios = {
        "bullish": {
            "price": current_price * (1 + volatility * 2),
            "probability": 0.0,  # Will be set by AI
            "factors": []
        },
        "neutral": {
            "price": current_price * (1 + volatility * 0.5),
            "probability": 0.0,
            "factors": []
        },
        "bearish": {
            "price": current_price * (1 - volatility * 1.5),
            "probability": 0.0,
            "factors": []
        }
    }
    
    return scenarios

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st

def analyze_market_trends(price_data, onchain_data):
    """
    Analyze market trends using technical indicators and historical patterns
    """
    try:
        # Calculate recent price changes
        recent_price_change = ((price_data['Close'].iloc[-1] - price_data['Close'].iloc[-7]) / 
                             price_data['Close'].iloc[-7] * 100)

        # Calculate volatility
        volatility = price_data['Close'].pct_change().std() * 100

        # Calculate volume trends
        avg_volume = price_data['Volume'].tail(7).mean()
        volume_change = ((price_data['Volume'].iloc[-1] - price_data['Volume'].iloc[-7]) /
                        price_data['Volume'].iloc[-7] * 100)

        # Analyze on-chain metrics
        active_addresses_change = ((onchain_data['active_addresses'].iloc[-1] - 
                                  onchain_data['active_addresses'].iloc[-7]) /
                                 onchain_data['active_addresses'].iloc[-7] * 100)

        # Determine market sentiment
        sentiment_factors = [
            recent_price_change > 0,  # Price trending up
            volume_change > 0,        # Volume trending up
            active_addresses_change > 0  # Network activity increasing
        ]

        bullish_factors = sum(sentiment_factors)

        if bullish_factors >= 2:
            sentiment = "bullish"
            confidence = min(0.5 + (bullish_factors - 2) * 0.25 + abs(recent_price_change) * 0.01, 0.95)
        elif bullish_factors <= 1:
            sentiment = "bearish"
            confidence = min(0.5 + (1 - bullish_factors) * 0.25 + abs(recent_price_change) * 0.01, 0.95)
        else:
            sentiment = "neutral"
            confidence = 0.5

        # Generate analysis
        analysis = {
            "market_sentiment": sentiment,
            "confidence_score": confidence,
            "key_factors": [
                f"Price {'increased' if recent_price_change > 0 else 'decreased'} by {abs(recent_price_change):.1f}%",
                f"Trading volume {'increased' if volume_change > 0 else 'decreased'} by {abs(volume_change):.1f}%",
                f"Network activity {'increased' if active_addresses_change > 0 else 'decreased'} by {abs(active_addresses_change):.1f}%"
            ],
            "short_term_outlook": (
                f"Market showing {'strength' if sentiment == 'bullish' else 'weakness' if sentiment == 'bearish' else 'stability'} "
                f"with {volatility:.1f}% volatility. "
                f"Volume trends suggest {'increasing' if volume_change > 0 else 'decreasing'} market participation."
            ),
            "medium_term_outlook": (
                f"Network fundamentals are {'improving' if active_addresses_change > 0 else 'declining'}, "
                f"suggesting potential for {'continued' if sentiment == 'bullish' else 'reversal in'} current trend."
            ),
            "risk_factors": [
                f"High market volatility ({volatility:.1f}%)" if volatility > 20 else "Stable market conditions",
                "Decreasing network activity" if active_addresses_change < 0 else "Healthy network growth",
                "Low trading volume" if volume_change < 0 else "Strong trading volume"
            ],
            "trading_volume_analysis": (
                f"Average 7-day trading volume: ${avg_volume:,.0f}. "
                f"Volume is {volume_change:+.1f}% compared to last week."
            ),
            "prediction": {
                "price_direction": "up" if sentiment == "bullish" else "down" if sentiment == "bearish" else "sideways",
                "confidence": confidence,
                "supporting_metrics": [
                    "Price momentum",
                    "Volume trend",
                    "Network activity"
                ]
            }
        }

        return analysis

    except Exception as e:
        st.error(f"Error generating market analysis: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def generate_price_scenarios(price_data):
    """
    Generate potential price scenarios based on historical patterns
    """
    try:
        current_price = price_data['Close'].iloc[-1]

        # Calculate historical volatility
        volatility = price_data['Close'].pct_change().std()

        # Generate scenarios
        scenarios = {
            "bullish": {
                "price": current_price * (1 + volatility * 2),
                "probability": 0.3,
                "factors": [
                    "Strong network growth",
                    "Increasing trading volume",
                    "Positive price momentum"
                ]
            },
            "neutral": {
                "price": current_price * (1 + volatility * 0.5),
                "probability": 0.4,
                "factors": [
                    "Stable network metrics",
                    "Average trading volume",
                    "Sideways price action"
                ]
            },
            "bearish": {
                "price": current_price * (1 - volatility * 1.5),
                "probability": 0.3,
                "factors": [
                    "Decreasing network activity",
                    "Lower trading volume",
                    "Negative price momentum"
                ]
            }
        }

        return scenarios
    except Exception as e:
        st.error(f"Error generating price scenarios: {str(e)}")
        return None
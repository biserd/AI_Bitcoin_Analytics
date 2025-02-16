import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json

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

        # Calculate sentiment and confidence scores
        if bullish_factors >= 2:
            sentiment = "bullish"
            confidence_scores = {
                "bullish": 0.6,
                "neutral": 0.3,
                "bearish": 0.1
            }
        elif bullish_factors <= 1:
            sentiment = "bearish"
            confidence_scores = {
                "bullish": 0.1,
                "neutral": 0.3,
                "bearish": 0.6
            }
        else:
            sentiment = "neutral"
            confidence_scores = {
                "bullish": 0.33,
                "neutral": 0.34,
                "bearish": 0.33
            }

        # Generate analysis with detailed insights
        analysis = {
            "market_sentiment": sentiment,
            "confidence_scores": confidence_scores,
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
                f"{'High market volatility' if volatility > 20 else 'Stable market conditions'} ({volatility:.1f}%)",
                f"{'Declining' if active_addresses_change < 0 else 'Healthy'} network growth",
                f"{'Low' if volume_change < 0 else 'Strong'} trading volume"
            ]
        }

        return json.dumps(analysis)

    except Exception as e:
        raise Exception(f"Error generating market analysis: {str(e)}")

def generate_predictions():
    """Generate potential price scenarios based on historical patterns"""
    try:
        scenarios = {
            "bullish": {
                "probability": 0.4,
                "factors": [
                    "Strong network growth",
                    "Increasing trading volume",
                    "Positive price momentum"
                ]
            },
            "neutral": {
                "probability": 0.3,
                "factors": [
                    "Stable network metrics",
                    "Average trading volume",
                    "Sideways price action"
                ]
            },
            "bearish": {
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
        raise Exception(f"Error generating price scenarios: {str(e)}")
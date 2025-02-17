import pandas as pd
import numpy as np
import json

def analyze_market_trends(price_data: pd.DataFrame, onchain_data: pd.DataFrame) -> str:
    """Analyze market trends using price and on-chain data"""
    try:
        # Calculate basic trends
        price_change = price_data['Close'].pct_change().mean()
        volume_trend = price_data['Volume'].pct_change().mean()
        avg_volume = price_data['Volume'].mean()
        volume_change = (price_data['Volume'].mean() - price_data['Volume'].shift(7).mean()) / price_data['Volume'].shift(7).mean() * 100

        # Determine market sentiment
        if price_change > 0.02 and volume_trend > 0:
            sentiment = "bullish"
            confidence_score = min(0.5 + abs(price_change), 0.95)
        elif price_change < -0.02:
            sentiment = "bearish"
            confidence_score = min(0.5 + abs(price_change), 0.95)
        else:
            sentiment = "neutral"
            confidence_score = 0.5

        # Generate prediction
        prediction = {
            "price_direction": "up" if price_change > 0 else "down",
            "confidence": confidence_score
        }

        # Key factors affecting the market
        factors = []
        if not onchain_data.empty:
            active_addr_trend = onchain_data['active_addresses'].pct_change().mean()
            hash_rate_trend = onchain_data['hash_rate'].pct_change().mean()

            if active_addr_trend > 0:
                factors.append("Increasing network activity")
            if hash_rate_trend > 0:
                factors.append("Growing network security")
            if volume_trend > 0:
                factors.append("Rising trading volume")

        analysis = {
            "market_sentiment": sentiment,
            "confidence_score": confidence_score,
            "prediction": prediction,
            "key_factors": factors,
            "scenario_factors": {
                "bullish": [
                    "Strong network growth",
                    "Increasing trading volume",
                    "Positive price momentum"
                ],
                "neutral": [
                    "Stable network metrics",
                    "Average trading volume",
                    "Sideways price action"
                ],
                "bearish": [
                    "Decreasing network activity",
                    "Lower trading volume",
                    "Negative price momentum"
                ]
            },
            "volume_analysis": {
                "avg_7day": avg_volume,
                "volume_change": volume_change
            },
            "supporting_metrics": [
                "Price momentum",
                "Volume trend",
                "Network activity"
            ],
            "outlook": {
                "short_term": "7-day consolidation with increased volatility expected",
                "medium_term": "30-day outlook shows potential upward trend based on institutional adoption",
                "long_term": "Bullish outlook supported by halving cycle dynamics"
            }
        }

        return json.dumps(analysis)
    except Exception as e:
        return json.dumps({
            "market_sentiment": "neutral",
            "confidence_score": 0.5,
            "prediction": {"price_direction": "neutral", "confidence": 0.5},
            "key_factors": ["Insufficient data for analysis"]
        })

def generate_predictions():
    """Generate future price predictions and market scenarios"""
    return {
        "short_term": "Consolidation expected with increased volatility",
        "medium_term": "Potential upward trend based on institutional adoption",
        "long_term": "Bullish outlook supported by halving cycle"
    }
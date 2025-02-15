"""Metrics service module for Bitcoin analytics platform"""

from datetime import datetime
from typing import Dict, Any, Optional

def format_metrics(price_data: Dict[str, Any]) -> Dict[str, Any]:
    """Format metrics data for API response"""
    try:
        return {
            "current_price": {
                "value": float(price_data['price']),
                "change_24h": float(price_data['change_24h']),
                "formatted": f"${float(price_data['price']):,.2f}"
            },
            "volume": {
                "value": float(price_data['volume']),
                "formatted": f"${float(price_data['volume']):,.0f}"
            },
            "last_update": {
                "timestamp": price_data['timestamp'],
                "formatted": datetime.fromisoformat(price_data['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            }
        }
    except Exception as e:
        raise ValueError(f"Error formatting metrics: {str(e)}")

def calculate_market_metrics(price_data: Dict[str, Any]) -> Dict[str, Any]:
    """Calculate additional market metrics"""
    try:
        return {
            "market_cap": float(price_data['price']) * 21_000_000,  # Approximate total supply
            "daily_change": float(price_data['change_24h']),
            "volume_to_market_cap": float(price_data['volume']) / (float(price_data['price']) * 21_000_000)
        }
    except Exception as e:
        raise ValueError(f"Error calculating market metrics: {str(e)}")

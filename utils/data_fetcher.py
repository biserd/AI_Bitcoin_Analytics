import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy import func
from utils.database import (
    store_bitcoin_price, store_etf_data, store_onchain_metrics,
    BitcoinPrice, ETFData, OnchainMetric, get_db
)
import logging

logger = logging.getLogger(__name__)

def get_bitcoin_data():
    """Fetch current Bitcoin price data"""
    try:
        btc = yf.Ticker("BTC-USD")
        history = btc.history(period="1d")

        if isinstance(history, pd.DataFrame) and not history.empty:
            latest_data = {
                'price': float(history['Close'].iloc[-1]),
                'volume': float(history['Volume'].iloc[-1]),
                'change_24h': float(history['Close'].iloc[-1] - history['Open'].iloc[0]),
                'timestamp': history.index[-1].isoformat()
            }
            # Store in database
            store_bitcoin_price(history)
            return latest_data
        return None
    except Exception as e:
        raise Exception(f"Error fetching Bitcoin data: {str(e)}")

def fetch_bitcoin_price():
    """Fetch Bitcoin historical price data"""
    try:
        btc = yf.Ticker("BTC-USD")
        history = btc.history(period="1y")

        if isinstance(history, pd.DataFrame) and not history.empty:
            # Store in database
            store_bitcoin_price(history)
            return history
        return pd.DataFrame()
    except Exception as e:
        raise Exception(f"Error fetching Bitcoin price data: {str(e)}")

def fetch_etf_data(period='1_week'):
    """Fetch Bitcoin ETF data and store in database"""
    period_map = {
        '1_week': '7d',
        '1_month': '30d',
        '3_months': '90d',
        '6_months': '180d',
        '1_year': '365d'
    }
    interval = period_map.get(period, '7d')
    etfs = ['BITO', 'BITI', 'BTF']  # Example Bitcoin ETF tickers
    data = {}

    for etf in etfs:
        try:
            ticker = yf.Ticker(etf)
            history = ticker.history(period="1y")

            if not isinstance(history, pd.DataFrame) or history.empty:
                logger.warning(f"No data available for ETF {etf}")
                continue

            required_columns = ['Close', 'Open', 'High', 'Low', 'Volume']
            if not all(col in history.columns for col in required_columns):
                logger.warning(f"Missing required columns for ETF {etf}")
                continue

            # Convert any numeric columns to float
            for col in required_columns:
                if col in history.columns:
                    history[col] = history[col].astype(float)

            # Generate simulated orderbook data
            current_price = float(history['Close'].iloc[-1])
            spread_percentage = 0.005  # 0.5% spread for better visibility
            depth_levels = 10

            # Generate bid and ask prices with wider spread
            bid_prices = [current_price * (1 - spread_percentage * (i + 1)) for i in range(depth_levels)]
            ask_prices = [current_price * (1 + spread_percentage * (i + 1)) for i in range(depth_levels)]

            # Generate more realistic volumes that decrease exponentially
            base_volume = float(history['Volume'].mean()) / 50  # Adjusted divisor for better scale
            volumes = [base_volume * np.exp(-0.3 * i) for i in range(depth_levels)]

            # Create orderbook with sorted prices and volumes
            orderbook = {
                'bid_prices': sorted(bid_prices, reverse=True),  # Higher to lower
                'bid_volumes': volumes,
                'ask_prices': sorted(ask_prices),  # Lower to higher
                'ask_volumes': volumes[::-1]  # Reverse volumes for asks
            }

            data[etf] = {
                'history': history,
                'orderbook': orderbook
            }

            # Store valid data in database
            store_etf_data(etf, data[etf])
            logger.info(f"Successfully fetched and stored data for ETF {etf}")

        except Exception as e:
            logger.error(f"Error fetching data for {etf}: {str(e)}")
            continue

    if len(data) == 0:
        logger.warning("No ETF data available")
        return None

    return data

def fetch_onchain_metrics():
    """Fetch on-chain metrics and store in database"""
    try:
        # Generate sample data for the last year to match ETF data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')

        data = {
            'timestamp': dates,
            'active_addresses': np.random.randint(800000, 1200000, size=len(dates)),
            'transaction_volume': np.random.randint(200000, 500000, size=len(dates)),
            'hash_rate': np.random.randint(200, 300, size=len(dates))
        }

        df = pd.DataFrame(data)
        df.set_index('timestamp', inplace=True)

        # Store in database
        store_onchain_metrics(df)
        return df
    except Exception as e:
        raise Exception(f"Error generating on-chain metrics: {str(e)}")


def get_historical_metrics():
    """Retrieve historical metrics from database"""
    try:
        db = next(get_db())

        # Get latest metrics
        latest_metrics = db.query(OnchainMetric).order_by(
            OnchainMetric.timestamp.desc()
        ).limit(30).all()

        if not latest_metrics:
            return pd.DataFrame()

        return pd.DataFrame([{
            'date': metric.timestamp,
            'active_addresses': metric.active_addresses,
            'transaction_volume': metric.transaction_volume,
            'hash_rate': metric.hash_rate
        } for metric in latest_metrics])
    except Exception as e:
        raise Exception(f"Error retrieving historical metrics: {str(e)}")
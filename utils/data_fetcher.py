import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import streamlit as st
from utils.database import (
    store_bitcoin_price, store_etf_data, store_onchain_metrics,
    BitcoinPrice, ETFData, OnchainMetric, get_db
)
from sqlalchemy import func

@st.cache_data(ttl=3600)
def fetch_bitcoin_price():
    """Fetch Bitcoin price data and store in database"""
    try:
        btc = yf.Ticker("BTC-USD")
        history = btc.history(period="1y")

        if isinstance(history, pd.DataFrame) and history.empty:
            st.error("No Bitcoin price data available")
            return pd.DataFrame()

        # Store in database
        store_bitcoin_price(history)
        return history
    except Exception as e:
        st.error(f"Error fetching Bitcoin price data: {str(e)}")
        return pd.DataFrame()

@st.cache_data(ttl=3600)
def fetch_etf_data():
    """Fetch Bitcoin ETF data and store in database"""
    etfs = ['BITO', 'BITI', 'BTF']  # Example Bitcoin ETF tickers
    data = {}

    for etf in etfs:
        try:
            ticker = yf.Ticker(etf)
            history = ticker.history(period="1y")

            if not isinstance(history, pd.DataFrame) or history.empty or len(history.index) == 0:
                continue

            required_columns = ['Close', 'Open', 'High', 'Low', 'Volume']
            if not all(col in history.columns for col in required_columns):
                continue

            # Convert any numeric columns to float
            for col in required_columns:
                if col in history.columns:
                    history[col] = history[col].astype(float)

            # Generate simulated orderbook data
            current_price = history['Close'].iloc[-1]
            spread_percentage = 0.005  # 0.5% spread for better visibility
            depth_levels = 10

            # Generate bid and ask prices with wider spread
            bid_prices = [current_price * (1 - spread_percentage * (i + 1)) for i in range(depth_levels)]
            ask_prices = [current_price * (1 + spread_percentage * (i + 1)) for i in range(depth_levels)]

            # Generate more realistic volumes that decrease exponentially
            base_volume = history['Volume'].mean() / 50  # Adjusted divisor for better scale
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

        except Exception as e:
            if "ambiguous" not in str(e).lower():  # Only show non-ambiguous errors
                st.warning(f"Error fetching data for {etf}: {str(e)}")
            continue

    if len(data) == 0:
        st.warning("No ETF data available")

    return data

@st.cache_data(ttl=3600)
def fetch_onchain_metrics():
    """Fetch on-chain metrics and store in database"""
    try:
        # Generate sample data for the last year to match ETF data
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        dates = pd.date_range(start=start_date, end=end_date, freq='D')

        data = {
            'date': dates,
            'active_addresses': np.random.randint(800000, 1200000, size=len(dates)),
            'transaction_volume': np.random.randint(200000, 500000, size=len(dates)),
            'hash_rate': np.random.randint(200, 300, size=len(dates))
        }

        df = pd.DataFrame(data)
        df.set_index('date', inplace=True)

        # Store in database
        store_onchain_metrics(df)
        return df
    except Exception as e:
        st.error(f"Error generating on-chain metrics: {str(e)}")
        return pd.DataFrame()

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
        st.error(f"Error retrieving historical metrics: {str(e)}")
        return pd.DataFrame()
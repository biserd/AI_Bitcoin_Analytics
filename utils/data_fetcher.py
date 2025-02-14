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
            # Changed from 1mo to 1y to match onchain data timeframe
            history = ticker.history(period="1y")
            
            if not isinstance(history, pd.DataFrame):
                st.warning(f"Invalid data type for {etf}")
                continue
                
            if history.empty:
                st.warning(f"No data available for {etf}")
                continue

            required_columns = ['Close', 'Open', 'High', 'Low', 'Volume']
            has_required = all(col in history.columns for col in required_columns)
            if not has_required:
                st.warning(f"Missing required price columns for {etf}")
                continue

            # Convert any numeric columns to float
            for col in required_columns:
                if col in history.columns:
                    history[col] = history[col].astype(float)

            # Safely get ticker info
            info = {}
            try:
                if hasattr(ticker, 'info'):
                    info_dict = ticker.info
                    if isinstance(info_dict, dict):
                        info = info_dict
            except Exception:
                info = {}

            data[etf] = {
                'info': info,
                'history': history
            }

            # Store valid data in database
            store_etf_data(etf, data[etf])

        except Exception as e:
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
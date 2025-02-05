import yfinance as yf
import pandas as pd
import requests
from datetime import datetime, timedelta
import streamlit as st

@st.cache_data(ttl=3600)
def fetch_bitcoin_price():
    try:
        btc = yf.Ticker("BTC-USD")
        history = btc.history(period="1y")
        return history
    except Exception as e:
        st.error(f"Error fetching Bitcoin price data: {str(e)}")
        return None

@st.cache_data(ttl=3600)
def fetch_etf_data():
    """Fetch Bitcoin ETF data"""
    etfs = ['BITO', 'BITI', 'BTF']  # Example Bitcoin ETF tickers
    data = {}
    
    for etf in etfs:
        try:
            ticker = yf.Ticker(etf)
            data[etf] = {
                'info': ticker.info,
                'history': ticker.history(period="1mo")
            }
        except Exception as e:
            st.warning(f"Error fetching data for {etf}: {str(e)}")
    
    return data

@st.cache_data(ttl=3600)
def fetch_onchain_metrics():
    """Simulate fetching on-chain metrics"""
    # In a real implementation, this would call blockchain API
    # Using mock data for demonstration
    dates = pd.date_range(start='2023-01-01', end=datetime.now(), freq='D')
    
    data = {
        'date': dates,
        'active_addresses': np.random.randint(800000, 1200000, size=len(dates)),
        'transaction_volume': np.random.randint(200000, 500000, size=len(dates)),
        'hash_rate': np.random.randint(200, 300, size=len(dates))
    }
    
    return pd.DataFrame(data)

import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import streamlit as st

# Initialize SQLAlchemy with PostgreSQL
try:
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")

    engine = create_engine(DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
except Exception as e:
    st.error(f"Database initialization error: {str(e)}")
    raise

class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False, default=0.0)

class ETFData(Base):
    __tablename__ = "etf_data"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    symbol = Column(String, nullable=False, index=True)
    price = Column(Float, nullable=False)
    volume = Column(Float, nullable=False, default=0.0)
    assets = Column(Float, nullable=True)

class OnchainMetric(Base):
    __tablename__ = "onchain_metrics"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, nullable=False, index=True)
    active_addresses = Column(Integer, nullable=False)
    transaction_volume = Column(Float, nullable=False)
    hash_rate = Column(Float, nullable=False)

def init_db():
    """Initialize database tables"""
    try:
        inspector = inspect(engine)
        tables_exist = all(
            table in inspector.get_table_names()
            for table in ['bitcoin_prices', 'etf_data', 'onchain_metrics']
        )

        if not tables_exist:
            Base.metadata.create_all(bind=engine)
            st.success("Database tables created successfully")
        return True
    except Exception as e:
        st.error(f"Failed to initialize database: {str(e)}")
        return False

def get_db():
    """Database session context manager"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def store_bitcoin_price(df):
    """Store Bitcoin price data in the database"""
    if df.empty:
        return

    try:
        db = next(get_db())
        for index, row in df.iterrows():
            try:
                price = BitcoinPrice(
                    timestamp=index,
                    open_price=float(row['Open']),
                    high_price=float(row['High']),
                    low_price=float(row['Low']),
                    close_price=float(row['Close']),
                    volume=float(row['Volume']) if 'Volume' in row else 0.0
                )
                db.merge(price)
            except (ValueError, TypeError) as e:
                st.warning(f"Skipping invalid price data: {str(e)}")
                continue
        db.commit()
    except Exception as e:
        st.error(f"Failed to store Bitcoin price data: {str(e)}")
        if 'db' in locals():
            db.rollback()

def store_etf_data(symbol, data):
    """Store ETF data in the database"""
    if not data or not data.get('history') or data['history'].empty:
        return

    try:
        db = next(get_db())
        timestamp = datetime.now()
        try:
            price = float(data['history']['Close'].iloc[-1])
            volume = float(data['info'].get('volume', 0))
            assets = float(data['info'].get('totalAssets', 0))
        except (ValueError, TypeError):
            price = 0.0
            volume = 0.0
            assets = None

        etf = ETFData(
            timestamp=timestamp,
            symbol=symbol,
            price=price,
            volume=volume,
            assets=assets
        )
        db.merge(etf)
        db.commit()
    except Exception as e:
        st.error(f"Failed to store ETF data: {str(e)}")
        if 'db' in locals():
            db.rollback()

def store_onchain_metrics(metrics_df):
    """Store on-chain metrics in the database"""
    if metrics_df.empty:
        return

    try:
        db = next(get_db())
        for index, row in metrics_df.iterrows():
            try:
                metric = OnchainMetric(
                    timestamp=index,  # Use the index as timestamp since it contains the date
                    active_addresses=int(row['active_addresses']),
                    transaction_volume=float(row['transaction_volume']),
                    hash_rate=float(row['hash_rate'])
                )
                db.merge(metric)
            except (ValueError, TypeError) as e:
                st.warning(f"Skipping invalid metric data: {str(e)}")
                continue
        db.commit()
    except Exception as e:
        st.error(f"Failed to store on-chain metrics: {str(e)}")
        if 'db' in locals():
            db.rollback()

# Initialize database on module import
if not init_db():
    st.error("Failed to initialize database. Some features may not work properly.")
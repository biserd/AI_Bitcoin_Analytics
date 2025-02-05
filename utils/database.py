import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Initialize SQLAlchemy with PostgreSQL
DATABASE_URL = os.getenv('DATABASE_URL')
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    volume = Column(Float)

class ETFData(Base):
    __tablename__ = "etf_data"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    volume = Column(Float)
    assets = Column(Float)

class OnchainMetric(Base):
    __tablename__ = "onchain_metrics"
    
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, index=True)
    active_addresses = Column(Integer)
    transaction_volume = Column(Float)
    hash_rate = Column(Float)

# Create tables
def init_db():
    Base.metadata.create_all(bind=engine)

# Database session context manager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Helper functions for data operations
def store_bitcoin_price(df):
    """Store Bitcoin price data in the database"""
    db = next(get_db())
    for index, row in df.iterrows():
        price = BitcoinPrice(
            timestamp=index,
            open_price=row['Open'],
            high_price=row['High'],
            low_price=row['Low'],
            close_price=row['Close'],
            volume=row['Volume'] if 'Volume' in row else 0
        )
        db.merge(price)
    db.commit()

def store_etf_data(symbol, data):
    """Store ETF data in the database"""
    db = next(get_db())
    timestamp = datetime.now()
    etf = ETFData(
        timestamp=timestamp,
        symbol=symbol,
        price=data['history']['Close'].iloc[-1],
        volume=data['info'].get('volume', 0),
        assets=data['info'].get('totalAssets', 0)
    )
    db.merge(etf)
    db.commit()

def store_onchain_metrics(metrics_df):
    """Store on-chain metrics in the database"""
    db = next(get_db())
    for index, row in metrics_df.iterrows():
        metric = OnchainMetric(
            timestamp=row['date'],
            active_addresses=row['active_addresses'],
            transaction_volume=row['transaction_volume'],
            hash_rate=row['hash_rate']
        )
        db.merge(metric)
    db.commit()

# Initialize database
init_db()

import os
import pandas as pd
from sqlalchemy import create_engine, Column, Integer, Float, String, DateTime, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from datetime import datetime
import streamlit as st
from sqlalchemy.engine.url import make_url
from time import sleep
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize SQLAlchemy with PostgreSQL
try:
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL environment variable is not set")

    # Parse the URL to add SSL mode
    url = make_url(DATABASE_URL)
    url = url.set(query={'sslmode': 'require'})

    # Create engine with connection pooling and retry settings
    engine = create_engine(
        url,
        pool_size=5,
        max_overflow=10,
        pool_timeout=30,
        pool_recycle=1800,  # Recycle connections after 30 minutes
        pool_pre_ping=True,  # Enable connection health checks
        connect_args={
            "connect_timeout": 10,
            "keepalives": 1,
            "keepalives_idle": 30,
            "keepalives_interval": 10,
            "keepalives_count": 5
        }
    )

    # Create thread-safe session factory
    session_factory = sessionmaker(bind=engine, autocommit=False, autoflush=False)
    SessionLocal = scoped_session(session_factory)
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

def get_db():
    """Database session context manager with retry logic"""
    max_retries = 3
    retry_delay = 1  # seconds

    for attempt in range(max_retries):
        try:
            db = SessionLocal()
            # Test the connection
            db.execute("SELECT 1")
            yield db
            return
        except Exception as e:
            logger.warning(f"Database connection attempt {attempt + 1} failed: {str(e)}")
            if db:
                db.close()
            if attempt < max_retries - 1:
                sleep(retry_delay)
                retry_delay *= 2  # Exponential backoff
            else:
                logger.error("Failed to establish database connection after maximum retries")
                raise
        finally:
            if 'db' in locals():
                db.close()

def init_db():
    """Initialize database tables with retry logic"""
    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            inspector = inspect(engine)
            tables_exist = all(
                table in inspector.get_table_names()
                for table in ['bitcoin_prices', 'etf_data', 'onchain_metrics']
            )

            if not tables_exist:
                Base.metadata.create_all(bind=engine)
                logger.info("Database tables created successfully")
            return True
        except Exception as e:
            logger.error(f"Database initialization attempt {attempt + 1} failed: {str(e)}")
            if attempt < max_retries - 1:
                sleep(retry_delay)
                retry_delay *= 2
            else:
                st.error("Failed to initialize database after maximum retries")
                return False

def store_bitcoin_price(df):
    """Store Bitcoin price data with retry logic"""
    if df.empty:
        return

    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            db = next(get_db())
            for index, row in df.iterrows():
                price = BitcoinPrice(
                    timestamp=index,
                    open_price=float(row['Open']),
                    high_price=float(row['High']),
                    low_price=float(row['Low']),
                    close_price=float(row['Close']),
                    volume=float(row['Volume']) if 'Volume' in row else 0.0
                )
                db.merge(price)
            db.commit()
            return
        except Exception as e:
            logger.error(f"Failed to store Bitcoin price data (attempt {attempt + 1}): {str(e)}")
            if 'db' in locals():
                db.rollback()
            if attempt < max_retries - 1:
                sleep(retry_delay)
                retry_delay *= 2
            else:
                raise

def store_etf_data(symbol, data):
    """Store ETF data with retry logic"""
    if not data or not data.get('history') or data['history'].empty:
        return

    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            db = next(get_db())
            timestamp = datetime.now()
            try:
                price = float(data['history']['Close'].iloc[-1])
                volume = float(data['history']['Volume'].iloc[-1])
                assets = None  # We don't have this information from yfinance
            except (ValueError, TypeError, KeyError):
                logger.warning(f"Invalid data format for ETF {symbol}")
                return

            etf = ETFData(
                timestamp=timestamp,
                symbol=symbol,
                price=price,
                volume=volume,
                assets=assets
            )
            db.merge(etf)
            db.commit()
            return
        except Exception as e:
            logger.error(f"Failed to store ETF data (attempt {attempt + 1}): {str(e)}")
            if 'db' in locals():
                db.rollback()
            if attempt < max_retries - 1:
                sleep(retry_delay)
                retry_delay *= 2
            else:
                raise

def store_onchain_metrics(metrics_df):
    """Store on-chain metrics with retry logic"""
    if metrics_df.empty:
        return

    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            db = next(get_db())
            for index, row in metrics_df.iterrows():
                metric = OnchainMetric(
                    timestamp=index,
                    active_addresses=int(row['active_addresses']),
                    transaction_volume=float(row['transaction_volume']),
                    hash_rate=float(row['hash_rate'])
                )
                db.merge(metric)
            db.commit()
            return
        except Exception as e:
            logger.error(f"Failed to store on-chain metrics (attempt {attempt + 1}): {str(e)}")
            if 'db' in locals():
                db.rollback()
            if attempt < max_retries - 1:
                sleep(retry_delay)
                retry_delay *= 2
            else:
                raise

# Initialize database on module import
if not init_db():
    logger.error("Failed to initialize database. Some features may not work properly.")
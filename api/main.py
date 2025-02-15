import sys
import os
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel

# Configure detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Add the project root to Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_root)
logger.debug(f"Added to Python path: {project_root}")

try:
    # Import existing utilities
    logger.debug("Importing utilities...")
    from utils.data_fetcher import get_bitcoin_data, fetch_bitcoin_price
    from utils.database import get_db_connection, init_db
    from utils.predictions import generate_predictions
    from utils.alerts import check_price_alerts
    logger.debug("Successfully imported all utilities")
except Exception as e:
    logger.error(f"Error importing utilities: {str(e)}")
    raise

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Response models
class BitcoinPriceResponse(BaseModel):
    price: float
    volume: float
    change_24h: float
    timestamp: str

class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

# Initialize FastAPI app
app = FastAPI(
    title="Bitcoin Analytics Dashboard API",
    description="API endpoints for Bitcoin market analysis and predictions",
    version="1.0.0"
)

# Configure CORS
origins = [
    "http://localhost:5000",
    "http://0.0.0.0:5000",
    "*"  # For development only, restrict in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    logger.info("Initializing application components...")
    try:
        # Initialize database
        if not init_db():
            raise Exception("Failed to initialize database")
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

@app.get("/")
async def root():
    """Root endpoint for health check"""
    return APIResponse(success=True, data={"message": "Bitcoin Analytics Dashboard API"})

@app.get("/api/bitcoin/price", response_model=APIResponse)
async def get_bitcoin_price():
    """Get current Bitcoin price data"""
    try:
        logger.debug("Fetching Bitcoin price data...")
        data = get_bitcoin_data()

        if not data:
            logger.warning("No Bitcoin price data available")
            return APIResponse(
                success=False,
                error="Bitcoin price data not available"
            )

        return APIResponse(success=True, data=data)
    except Exception as e:
        logger.error(f"Error fetching Bitcoin price: {str(e)}")
        return APIResponse(success=False, error=str(e))

@app.get("/api/bitcoin/predictions", response_model=APIResponse)
async def get_predictions():
    """Get market predictions"""
    try:
        logger.debug("Generating predictions...")
        predictions = generate_predictions()

        if not predictions:
            logger.warning("No prediction data available")
            return APIResponse(
                success=False,
                error="Prediction data not available"
            )

        return APIResponse(success=True, data=predictions)
    except Exception as e:
        logger.error(f"Error generating predictions: {str(e)}")
        return APIResponse(success=False, error=str(e))

@app.get("/api/bitcoin/metrics", response_model=APIResponse)
async def get_metrics():
    """Get Bitcoin metrics"""
    db = None
    try:
        logger.debug("Fetching metrics...")
        db = next(get_db_connection())

        # Get the latest Bitcoin price data
        btc_data = get_bitcoin_data()
        if not btc_data:
            return APIResponse(
                success=False,
                error="Failed to fetch Bitcoin metrics"
            )

        return APIResponse(success=True, data=btc_data)
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        return APIResponse(success=False, error=str(e))
    finally:
        if db:
            db.close()

if __name__ == "__main__":
    try:
        import uvicorn
        logger.info("Starting FastAPI server...")
        uvicorn.run(
            "main:app", 
            host="0.0.0.0", 
            port=8000, 
            reload=True,
            log_level="debug"
        )
    except Exception as e:
        logger.error(f"Server startup error: {str(e)}")
        raise
import sys
import os
import logging
from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

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
    # Import existing utilities and services
    logger.debug("Importing utilities and services...")
    from utils.data_fetcher import get_bitcoin_data, fetch_bitcoin_price, fetch_etf_data, fetch_onchain_metrics
    from utils.database import get_db_connection, init_db
    from utils.predictions import analyze_market_trends, generate_predictions
    from utils.alerts import check_price_alerts
    from api.services.metrics import format_metrics, calculate_market_metrics
    from api.services.education import get_educational_content
    logger.debug("Successfully imported all utilities and services")
except Exception as e:
    logger.error(f"Error importing utilities: {str(e)}")
    raise

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles

# Response models
class APIResponse(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[str] = None

# Initialize FastAPI app
app = FastAPI(
    title="Bitcoin Analytics Dashboard API",
    description="Advanced Bitcoin market analysis and predictions API",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Initialize components on startup"""
    logger.info("Initializing application components...")
    try:
        if not init_db():
            raise Exception("Failed to initialize database")
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Startup error: {str(e)}")
        raise

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"success": True, "message": "Bitcoin Analytics Dashboard API"}

@app.get("/api/health")
async def health_check():
    """API health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/bitcoin/price")
async def get_bitcoin_price():
    """Get current Bitcoin price data"""
    try:
        logger.debug("Fetching Bitcoin price data...")
        data = get_bitcoin_data()

        if not data:
            return APIResponse(success=False, error="Bitcoin price data not available")

        # Format metrics
        formatted_data = format_metrics(data)
        market_metrics = calculate_market_metrics(data)

        response_data = {**formatted_data, "market_metrics": market_metrics}
        return APIResponse(success=True, data=response_data)
    except Exception as e:
        logger.error(f"Error fetching Bitcoin price: {str(e)}")
        return APIResponse(success=False, error=str(e))

@app.get("/api/bitcoin/historical")
async def get_historical_data():
    """Get historical Bitcoin price data"""
    try:
        logger.debug("Fetching historical Bitcoin data...")
        data = fetch_bitcoin_price()

        if data.empty:
            return APIResponse(success=False, error="Historical data not available")

        # Convert DataFrame to dict for JSON serialization
        historical_data = data.reset_index().to_dict('records')
        return APIResponse(success=True, data=historical_data)
    except Exception as e:
        logger.error(f"Error fetching historical data: {str(e)}")
        return APIResponse(success=False, error=str(e))

@app.get("/api/bitcoin/analysis")
async def get_market_analysis():
    """Get comprehensive market analysis"""
    try:
        logger.debug("Generating market analysis...")
        price_data = fetch_bitcoin_price()
        onchain_data = fetch_onchain_metrics()

        if price_data.empty or onchain_data.empty:
            return APIResponse(success=False, error="Required data not available")

        analysis = analyze_market_trends(price_data, onchain_data)
        predictions = generate_predictions()

        return APIResponse(success=True, data={
            "analysis": analysis,
            "predictions": predictions
        })
    except Exception as e:
        logger.error(f"Error generating analysis: {str(e)}")
        return APIResponse(success=False, error=str(e))

@app.get("/api/etf/data")
async def get_etf_data():
    """Get Bitcoin ETF data"""
    try:
        logger.debug("Fetching ETF data...")
        data = fetch_etf_data()

        if not data:
            return APIResponse(success=False, error="ETF data not available")

        # Process ETF data for response
        etf_summary = {}
        for etf, etf_data in data.items():
            etf_summary[etf] = {
                "latest_price": float(etf_data['history']['Close'].iloc[-1]),
                "volume": float(etf_data['history']['Volume'].iloc[-1]),
                "orderbook": etf_data['orderbook']
            }

        return APIResponse(success=True, data=etf_summary)
    except Exception as e:
        logger.error(f"Error fetching ETF data: {str(e)}")
        return APIResponse(success=False, error=str(e))

@app.get("/api/education/content")
async def get_education():
    """Get educational content"""
    try:
        logger.debug("Fetching educational content...")
        content = get_educational_content()
        return APIResponse(success=True, data=content)
    except Exception as e:
        logger.error(f"Error fetching educational content: {str(e)}")
        return APIResponse(success=False, error=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server...")
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000, 
        reload=True,
        log_level="debug"
    )
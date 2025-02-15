import sys
import os
import logging

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
    from utils.data_fetcher import get_bitcoin_data
    from utils.database import get_db_connection, init_db
    from utils.predictions import generate_predictions
    from utils.visualizations import create_price_chart
    from utils.alerts import check_price_alerts
    logger.debug("Successfully imported all utilities")
except Exception as e:
    logger.error(f"Error importing utilities: {str(e)}")
    raise

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Initialize FastAPI app
app = FastAPI(
    title="Bitcoin Analytics Dashboard API",
    description="API endpoints for Bitcoin market analysis and predictions",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
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
    return {"message": "Bitcoin Analytics Dashboard API"}

@app.get("/api/bitcoin/price")
async def get_bitcoin_price():
    try:
        logger.debug("Fetching Bitcoin price data...")
        data = get_bitcoin_data()
        if not data:
            raise HTTPException(status_code=404, detail="Bitcoin price data not available")
        return {"success": True, "data": data}
    except Exception as e:
        logger.error(f"Error fetching Bitcoin price: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/bitcoin/predictions")
async def get_predictions():
    try:
        logger.debug("Generating predictions...")
        predictions = generate_predictions()
        if not predictions:
            raise HTTPException(status_code=404, detail="Prediction data not available")
        return {"success": True, "data": predictions}
    except Exception as e:
        logger.error(f"Error generating predictions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/bitcoin/metrics")
async def get_metrics():
    db = None
    try:
        logger.debug("Fetching metrics...")
        db = next(get_db_connection())
        metrics = {"price": 0, "volume": 0}  # Placeholder
        return {"success": True, "data": metrics}
    except Exception as e:
        logger.error(f"Error fetching metrics: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
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
            port=5000, 
            reload=True,
            log_level="debug"
        )
    except Exception as e:
        logger.error(f"Server startup error: {str(e)}")
        raise
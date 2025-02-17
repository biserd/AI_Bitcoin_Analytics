from flask import Flask, render_template, jsonify, send_from_directory
import pandas as pd
from utils.data_fetcher import (
    get_bitcoin_data,
    fetch_bitcoin_price,
    fetch_etf_data,
    fetch_onchain_metrics
)
from utils.visualizations import (
    create_price_chart,
    create_metric_chart,
    create_etf_comparison
)
from utils.sitemap import generate_sitemap, write_sitemap
from utils.predictions import analyze_market_trends, generate_predictions # Fixed import path
import logging
import os
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Add sum function to Jinja context
app.jinja_env.globals.update(sum=sum)

# Flag to track if sitemap has been generated
_sitemap_generated = False

def get_routes():
    """Get all routes with metadata for sitemap"""
    return [
        {'path': '/', 'changefreq': 'always', 'priority': '1.0'},
        {'path': '/correlation', 'changefreq': 'daily', 'priority': '0.8'},
        {'path': '/liquidity', 'changefreq': 'daily', 'priority': '0.8'},
        {'path': '/predictions', 'changefreq': 'daily', 'priority': '0.8'},
        {'path': '/education', 'changefreq': 'weekly', 'priority': '0.7'},
        {'path': '/cost-analysis', 'changefreq': 'weekly', 'priority': '0.7'}, #Added cost analysis route
        {'path': '/risk-metrics', 'changefreq': 'weekly', 'priority': '0.7'} #Added risk metrics route
    ]

@app.before_request
def init_sitemap():
    """Generate sitemap.xml before first request"""
    global _sitemap_generated
    if not _sitemap_generated:
        try:
            base_url = 'https://bitcoin-etf-analytics.replit.app'
            routes = get_routes()
            sitemap_content = generate_sitemap(base_url, routes)
            write_sitemap(sitemap_content)
            logger.info("Sitemap generated successfully")
            _sitemap_generated = True
        except Exception as e:
            logger.error(f"Error generating sitemap: {str(e)}")

@app.route('/sitemap.xml')
def serve_sitemap():
    """Serve the sitemap.xml file"""
    return send_from_directory('.', 'sitemap.xml')

@app.route('/')
def index():
    """Main dashboard page"""
    try:
        btc_data = get_bitcoin_data()
        if not btc_data:
            logger.error("Failed to fetch Bitcoin data")
            return render_template('index.html', error="Unable to fetch Bitcoin data")

        historical_data = fetch_bitcoin_price()
        price_chart = create_price_chart(historical_data) if not historical_data.empty else None
        if not price_chart:
            logger.warning("No historical price data available")

        etf_data = fetch_etf_data()
        etf_chart = create_etf_comparison(etf_data) if etf_data else None
        if not etf_chart:
            logger.warning("No ETF data available")

        metrics_data = fetch_onchain_metrics()
        active_addresses_chart = None
        hash_rate_chart = None

        if not metrics_data.empty:
            active_addresses_chart = create_metric_chart(metrics_data, 'active_addresses', '#1f77b4')
            hash_rate_chart = create_metric_chart(metrics_data, 'hash_rate', '#2ca02c')
        else:
            logger.warning("No metrics data available")

        return render_template('index.html',
            btc_data=btc_data,
            price_chart=price_chart,
            etf_chart=etf_chart,
            active_addresses_chart=active_addresses_chart,
            hash_rate_chart=hash_rate_chart
        )
    except Exception as e:
        logger.error(f"Error rendering dashboard: {str(e)}", exc_info=True)
        return render_template('index.html', error=f"An error occurred: {str(e)}")

@app.route('/correlation')
def correlation():
    """Correlation analysis page"""
    try:
        historical_data = fetch_bitcoin_price()
        etf_data = fetch_etf_data()
        return render_template('correlation.html',
            price_chart=create_price_chart(historical_data) if not historical_data.empty else None,
            etf_chart=create_etf_comparison(etf_data) if etf_data else None
        )
    except Exception as e:
        logger.error(f"Error in correlation analysis: {str(e)}", exc_info=True)
        return render_template('correlation.html', error=str(e))

@app.route('/liquidity')
def liquidity():
    """Liquidity analysis page"""
    try:
        etf_data = fetch_etf_data()
        logger.info(f"Fetched ETF data: {etf_data}")  # Add logging
        if not etf_data:
            return render_template('liquidity.html', error="Unable to fetch ETF data")
        return render_template('liquidity.html', etf_data=etf_data)
    except Exception as e:
        logger.error(f"Error in liquidity analysis: {str(e)}", exc_info=True)
        return render_template('liquidity.html', error=str(e))

@app.route('/predictions')
def predictions():
    """AI predictions page"""
    try:
        historical_data = fetch_bitcoin_price()
        metrics_data = fetch_onchain_metrics()

        if not historical_data.empty and not metrics_data.empty:
            # Generate market analysis
            analysis = json.loads(analyze_market_trends(historical_data, metrics_data))
            predictions = generate_predictions()

            return render_template('predictions.html',
                historical_data=historical_data,
                metrics_data=metrics_data,
                analysis=analysis,
                predictions=predictions
            )
        else:
            logger.warning("Missing data for predictions")
            return render_template('predictions.html', error="Unable to fetch required data")
    except Exception as e:
        logger.error(f"Error in predictions: {str(e)}", exc_info=True)
        return render_template('predictions.html', error=str(e))

@app.route('/education')
def education():
    """Educational content page"""
    return render_template('education.html')

@app.route('/cost-analysis')
def cost_analysis():
    """Cost analysis page"""
    # Placeholder for charts -  needs actual chart generation logic
    cost_chart = "Cost Analysis Chart Placeholder"
    return render_template('cost_analysis.html', cost_chart=cost_chart)

@app.route('/risk-metrics')
def risk_metrics():
    """Risk metrics and alerts page"""
    return render_template('risk_metrics.html')

@app.route('/health')
def health_check():
    """Simple health check endpoint"""
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
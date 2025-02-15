from flask import Flask, render_template
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

app = Flask(__name__)

@app.route('/')
def index():
    # Fetch current Bitcoin price and metrics
    btc_data = get_bitcoin_data()

    # Get historical price data
    historical_data = fetch_bitcoin_price()
    price_chart = create_price_chart(historical_data) if not historical_data.empty else None

    # Get ETF data
    etf_data = fetch_etf_data()
    etf_chart = create_etf_comparison(etf_data) if etf_data else None

    # Get metrics data
    metrics_data = fetch_onchain_metrics()
    if not metrics_data.empty:
        active_addresses_chart = create_metric_chart(metrics_data, 'active_addresses', '#1f77b4')
        hash_rate_chart = create_metric_chart(metrics_data, 'hash_rate', '#2ca02c')
    else:
        active_addresses_chart = hash_rate_chart = None

    return render_template('index.html',
        btc_data=btc_data,
        price_chart=price_chart,
        etf_chart=etf_chart,
        active_addresses_chart=active_addresses_chart,
        hash_rate_chart=hash_rate_chart
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
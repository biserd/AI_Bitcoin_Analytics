import plotly.graph_objects as go
import plotly.express as px
import pandas as pd

def create_price_chart(df):
    fig = go.Figure()

    fig.add_trace(go.Candlestick(
        x=df.index,
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='BTC/USD'
    ))

    fig.update_layout(
        template='plotly_white',
        title='Bitcoin Price Chart',
        yaxis_title='Price (USD)',
        xaxis_title='Date',
        height=600,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

def create_metric_chart(df, metric_name, color='#F7931A'):
    # Reset index to make the timestamp a column
    df_plot = df.reset_index()

    fig = px.line(df_plot, x='timestamp', y=metric_name,
                  title=f'{metric_name.replace("_", " ").title()}')

    fig.update_traces(line_color=color)
    fig.update_layout(
        template='plotly_white',
        height=400,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig

def create_etf_comparison(etf_data):
    fig = go.Figure()

    for etf, data in etf_data.items():
        fig.add_trace(go.Scatter(
            x=data['history'].index,
            y=data['history']['Close'],
            name=etf,
            mode='lines'
        ))

    fig.update_layout(
        template='plotly_white',
        title='ETF Performance Comparison',
        yaxis_title='Price (USD)',
        xaxis_title='Date',
        height=500,
        margin=dict(l=20, r=20, t=40, b=20)
    )

    return fig
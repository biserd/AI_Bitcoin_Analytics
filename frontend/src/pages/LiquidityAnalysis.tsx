import React from 'react';
import Plot from 'react-plotly.js';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const LiquidityAnalysis = () => {
  const { data: etfData } = useQuery({
    queryKey: ['etf-data'],
    queryFn: async () => {
      const response = await axios.get('/api/etf/data');
      return response.data.data;
    }
  });

  if (!etfData) return <div>Loading...</div>;

  const createOrderbookChart = (symbol: string, data: any) => {
    const { orderbook } = data;

    return {
      data: [
        {
          type: 'bar' as const,
          x: orderbook.bid_volumes,
          y: orderbook.bid_prices,
          name: 'Bids',
          orientation: 'h' as const,
          marker: { color: '#21CE99' }
        },
        {
          type: 'bar' as const,
          x: orderbook.ask_volumes,
          y: orderbook.ask_prices,
          name: 'Asks',
          orientation: 'h' as const,
          marker: { color: '#FF5000' }
        }
      ],
      layout: {
        title: `${symbol} Orderbook Depth`,
        barmode: 'overlay' as const,
        xaxis: { title: 'Volume' },
        yaxis: { title: 'Price (USD)' },
        paper_bgcolor: 'white',
        plot_bgcolor: 'white'
      }
    };
  };

  return (
    <div>
      <h1>Liquidity Analysis</h1>
      {Object.entries(etfData).map(([symbol, data]: [string, any]) => {
        const chart = createOrderbookChart(symbol, data);
        return (
          <div key={symbol} style={{ marginBottom: '2rem' }}>
            <Plot
              data={chart.data}
              layout={chart.layout}
              style={{ width: '100%', height: '400px' }}
            />
          </div>
        );
      })}
    </div>
  );
};

export default LiquidityAnalysis;
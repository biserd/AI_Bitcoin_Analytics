import React from 'react';
import Plot from 'react-plotly.js';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const CorrelationAnalysis = () => {
  const { data: btcData } = useQuery({
    queryKey: ['bitcoin-historical'],
    queryFn: async () => {
      const response = await axios.get('/api/bitcoin/historical');
      return response.data.data;
    }
  });

  const { data: etfData } = useQuery({
    queryKey: ['etf-data'],
    queryFn: async () => {
      const response = await axios.get('/api/etf/data');
      return response.data.data;
    }
  });

  if (!btcData || !etfData) return <div>Loading...</div>;

  const createCorrelationChart = () => {
    const btcPrices = btcData.map((d: any) => d.Close);
    const etfPrices = Object.values(etfData).map((etf: any) => etf.latest_price);

    return {
      data: [{
        type: 'scatter' as const,
        mode: 'markers' as const,
        x: btcPrices,
        y: etfPrices,
        marker: {
          size: 8,
          color: '#F7931A',
          opacity: 0.7
        },
        name: 'BTC vs ETF Correlation'
      }],
      layout: {
        title: 'Bitcoin vs ETF Price Correlation',
        xaxis: { title: 'Bitcoin Price (USD)' },
        yaxis: { title: 'ETF Price (USD)' },
        paper_bgcolor: 'white',
        plot_bgcolor: 'white'
      }
    };
  };

  const chart = createCorrelationChart();

  return (
    <div>
      <h1>Correlation Analysis</h1>
      <Plot
        data={chart.data}
        layout={chart.layout}
        style={{ width: '100%', height: '600px' }}
      />
    </div>
  );
};

export default CorrelationAnalysis;
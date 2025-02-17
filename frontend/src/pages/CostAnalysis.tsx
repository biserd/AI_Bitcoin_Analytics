
import React from 'react';
import Plot from 'react-plotly.js';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const CostAnalysis = () => {
  const [investment, setInvestment] = React.useState(10000);
  const [period, setPeriod] = React.useState(5);
  const [frequency, setFrequency] = React.useState('buy-hold');

  const calculateCosts = (amount: number, years: number, freq: string) => {
    const tradesPerYear = {
      'buy-hold': 1,
      'monthly': 12,
      'weekly': 52,
      'daily': 252
    };

    const trades = tradesPerYear[freq as keyof typeof tradesPerYear];
    
    const spotCosts = {
      'Trading Fees': amount * 0.003 * trades * years,
      'Custody Fees': 0,
      'Withdrawal Fees': 15 * years
    };

    const etfCosts = {
      'Trading Fees': amount * 0.001 * trades * years,
      'Management Fees': amount * 0.005 * years,
      'Other Fees': 0
    };

    return { spotCosts, etfCosts };
  };

  const { spotCosts, etfCosts } = calculateCosts(investment, period, frequency);

  const chartData = [
    {
      name: 'Spot Bitcoin',
      type: 'bar' as const,
      x: Object.keys(spotCosts),
      y: Object.values(spotCosts),
      marker: { color: '#F7931A' }
    },
    {
      name: 'Bitcoin ETFs',
      type: 'bar' as const,
      x: Object.keys(etfCosts),
      y: Object.values(etfCosts),
      marker: { color: '#1E88E5' }
    }
  ];

  const layout = {
    title: 'Cost Breakdown Comparison',
    barmode: 'group' as const,
    yaxis: { title: 'Cost ($)' },
    paper_bgcolor: 'white',
    plot_bgcolor: 'white'
  };

  return (
    <div>
      <h1>Investment Cost Analysis</h1>
      <div style={{ marginBottom: '2rem' }}>
        <label>
          Investment Amount ($):
          <input 
            type="number" 
            value={investment}
            onChange={(e) => setInvestment(Number(e.target.value))}
            min={100}
          />
        </label>
        <br />
        <label>
          Investment Period (Years):
          <input 
            type="range"
            value={period}
            onChange={(e) => setPeriod(Number(e.target.value))}
            min={1}
            max={10}
          />
          {period} years
        </label>
        <br />
        <label>
          Trading Frequency:
          <select 
            value={frequency}
            onChange={(e) => setFrequency(e.target.value)}
          >
            <option value="buy-hold">Buy and Hold</option>
            <option value="monthly">Monthly</option>
            <option value="weekly">Weekly</option>
            <option value="daily">Daily</option>
          </select>
        </label>
      </div>
      <Plot
        data={chartData}
        layout={layout}
        style={{ width: '100%', height: '600px' }}
      />
    </div>
  );
};

export default CostAnalysis;

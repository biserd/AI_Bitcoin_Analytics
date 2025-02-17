
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
    <div style={{ marginTop: '2rem', padding: '1rem', background: '#f8f9fa', borderRadius: '8px' }}>
        <h2>Detailed Cost Breakdown</h2>
        <div style={{ marginTop: '1rem' }}>
          <h3>Additional Considerations</h3>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
            <div style={{ padding: '1rem', background: 'white', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
              <h4>ETF Advantages</h4>
              <ul>
                <li>Professional management</li>
                <li>Regulatory oversight</li>
                <li>Easier tax reporting</li>
              </ul>
            </div>
            <div style={{ padding: '1rem', background: 'white', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
              <h4>Bitcoin Advantages</h4>
              <ul>
                <li>Direct ownership</li>
                <li>No management fees</li>
                <li>Potential for yield generation</li>
              </ul>
            </div>
          </div>
          <div style={{ marginTop: '1rem', padding: '1rem', background: 'white', borderRadius: '8px', boxShadow: '0 2px 4px rgba(0,0,0,0.1)' }}>
            <h4>Risk Factors</h4>
            <ul>
              <li>Tracking error</li>
              <li>Liquidity considerations</li>
              <li>Custody security</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CostAnalysis;

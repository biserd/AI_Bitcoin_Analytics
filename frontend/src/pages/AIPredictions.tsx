import React from 'react';
import Plot from 'react-plotly.js';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const AIPredictions = () => {
  const { data: analysisData } = useQuery({
    queryKey: ['market-analysis'],
    queryFn: async () => {
      const response = await axios.get('/api/bitcoin/analysis');
      return response.data.data;
    }
  });

  if (!analysisData) return <div>Loading...</div>;

  const createPredictionChart = () => {
    const { predictions } = analysisData;
    const scenarios = Object.keys(predictions);
    const probabilities = scenarios.map(s => predictions[s].probability * 100);

    return {
      data: [{
        type: 'bar' as const,
        x: scenarios,
        y: probabilities,
        marker: {
          color: ['#21CE99', '#FFD700', '#FF5000']
        }
      }],
      layout: {
        title: 'Market Scenario Probabilities',
        xaxis: { title: 'Scenario' },
        yaxis: { 
          title: 'Probability (%)',
          range: [0, 100]
        },
        paper_bgcolor: 'white',
        plot_bgcolor: 'white'
      }
    };
  };

  const analysis = JSON.parse(analysisData.analysis);

  return (
    <div>
      <h1>AI Predictions</h1>
      <div style={{ marginBottom: '2rem' }}>
        <h2>Market Sentiment: {analysis.market_sentiment}</h2>
        <p>Confidence Score: {(analysis.confidence_score * 100).toFixed(1)}%</p>
        <Plot
          data={createPredictionChart().data}
          layout={createPredictionChart().layout}
          style={{ width: '100%', height: '400px' }}
        />
      </div>
      <div>
        <h2>Key Factors</h2>
        <ul>
          {analysis.key_factors.map((factor: string, index: number) => (
            <li key={index}>{factor}</li>
          ))}
        </ul>
        <h2>Risk Factors</h2>
        <ul>
          {analysis.risk_factors.map((factor: string, index: number) => (
            <li key={index}>{factor}</li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default AIPredictions;
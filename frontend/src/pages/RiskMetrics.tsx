
import React from 'react';
import { useQuery } from '@tanstack/react-query';
import axios from 'axios';

const RiskMetrics = () => {
  const { data: riskData } = useQuery({
    queryKey: ['risk-metrics'],
    queryFn: async () => {
      const response = await axios.get('/api/risk/metrics');
      return response.data;
    }
  });

  if (!riskData) return <div>Loading...</div>;

  return (
    <div>
      <h1>Risk Metrics & Alerts</h1>
      <div style={{ display: 'grid', gap: '1rem', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))' }}>
        {Object.entries(riskData.metrics).map(([key, value]: [string, any]) => (
          <div key={key} style={{ 
            padding: '1rem', 
            background: 'white', 
            borderRadius: '8px',
            boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
          }}>
            <h3>{key}</h3>
            <p>{value}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RiskMetrics;

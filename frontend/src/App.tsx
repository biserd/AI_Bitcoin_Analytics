import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CorrelationAnalysis from './pages/CorrelationAnalysis';
import LiquidityAnalysis from './pages/LiquidityAnalysis';
import AIPredictions from './pages/AIPredictions';
import CostAnalysis from './pages/CostAnalysis';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

const App = () => {
  const [currentPage, setCurrentPage] = React.useState('correlation');

  const renderPage = () => {
    switch (currentPage) {
      case 'correlation':
        return <CorrelationAnalysis />;
      case 'liquidity':
        return <LiquidityAnalysis />;
      case 'predictions':
        return <AIPredictions />;
      case 'costs':
        return <CostAnalysis />;
      default:
        return <CorrelationAnalysis />;
    }
  };

  return (
    <QueryClientProvider client={queryClient}>
      <div style={{ padding: '2rem' }}>
        <nav style={{ marginBottom: '2rem' }}>
          <button onClick={() => setCurrentPage('correlation')}>
            📊 Correlation Analysis
          </button>
          <button onClick={() => setCurrentPage('liquidity')}>
            💧 Liquidity Analysis
          </button>
          <button onClick={() => setCurrentPage('predictions')}>
            🤖 AI Predictions
          </button>
        </nav>
        {renderPage()}
      </div>
    </QueryClientProvider>
  );
};

export default App;

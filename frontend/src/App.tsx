import React from 'react';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import CorrelationAnalysis from './pages/CorrelationAnalysis';
import LiquidityAnalysis from './pages/LiquidityAnalysis';
import AIPredictions from './pages/AIPredictions';
import CostAnalysis from './pages/CostAnalysis';
import RiskMetrics from './pages/RiskMetrics';

const Navigation = ({ currentPage, setCurrentPage }: { currentPage: string, setCurrentPage: (page: string) => void }) => (
  <nav className="main-nav">
    <button 
      className={currentPage === 'correlation' ? 'active' : ''} 
      onClick={() => setCurrentPage('correlation')}
    >
      📊 Correlation Analysis
    </button>
    <button 
      className={currentPage === 'liquidity' ? 'active' : ''} 
      onClick={() => setCurrentPage('liquidity')}
    >
      💧 Liquidity Analysis
    </button>
    <button 
      className={currentPage === 'predictions' ? 'active' : ''} 
      onClick={() => setCurrentPage('predictions')}
    >
      🤖 AI Predictions
    </button>
    <button 
      className={currentPage === 'costs' ? 'active' : ''} 
      onClick={() => setCurrentPage('costs')}
    >
      💰 Cost Analysis
    </button>
    <button 
      className={currentPage === 'risk' ? 'active' : ''} 
      onClick={() => setCurrentPage('risk')}
    >
      ⚠️ Risk Metrics & Alerts
    </button>
  </nav>
);

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
      case 'risk':
        return <RiskMetrics />;
      default:
        return <CorrelationAnalysis />;
    }
  };

  return (
    <QueryClientProvider client={queryClient}>
      <div style={{ padding: '2rem' }}>
        <Navigation currentPage={currentPage} setCurrentPage={setCurrentPage} />
        {renderPage()}
      </div>
    </QueryClientProvider>
  );
};

export default App;

import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// Get the Replit URL from environment
const replitUrl = process.env.REPL_SLUG && process.env.REPL_OWNER
  ? `${process.env.REPL_SLUG}.${process.env.REPL_OWNER}.repl.co`
  : null;

export default defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://0.0.0.0:5001',
        changeOrigin: true,
        secure: false
      }
    },
    hmr: {
      clientPort: 443,
      protocol: 'wss'
    }
  }
});
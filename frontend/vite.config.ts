import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import path from 'path'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
  ],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8001', 
        changeOrigin: true,
        // Removed rewrite: (path) => path.replace(/^\/api/, '') 
        // to ensure backend receives the full /api/... path
        configure: (proxy, _options) => {
          proxy.on('error', (err, _req, _res) => {
            console.log('proxy error', err);
          });
          proxy.on('proxyRes', (_proxyRes, _req, res) => {
            res.setHeader('cache-control', 'no-cache');
            res.setHeader('connection', 'keep-alive');
            res.setHeader('x-accel-buffering', 'no');
          });
        },
      }
    }
  }
})

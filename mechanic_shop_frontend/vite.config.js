import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      // Everything starting with /api goes to your Render backend
      '/api': {
        target: 'https://mechanic-shop-db.onrender.com',
        changeOrigin: true,
        // follow redirects if your platform sends any
        followRedirects: true,
      },
      // (optional) if you also fetch /diag or other top-level paths:
      '/diag': {
        target: 'https://mechanic-shop-db.onrender.com',
        changeOrigin: true,
        followRedirects: true,
      },
    },
  },
})

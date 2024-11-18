import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url))
    }
  },
  server: {
    host: '0.0.0.0', // Make the dev server accessible externally
    port: 8080,      // Optionally change the port to 8080, if needed
  },
  define: {
    'process.env': {} // Đảm bảo không có lỗi liên quan đến process
  }
})

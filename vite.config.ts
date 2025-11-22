import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { resolve } from 'path'
import { copyFileSync, existsSync, mkdirSync } from 'fs'

export default defineConfig({
  plugins: [
    react(),
    {
      name: 'copy-files',
      writeBundle() {
        if (!existsSync('dist')) {
          mkdirSync('dist')
        }
        copyFileSync('public/manifest.json', 'dist/manifest.json')
        copyFileSync('src/popup/index.html', 'dist/popup.html')
      }
    }
  ],
  build: {
    outDir: 'dist',
    rollupOptions: {
      input: {
        popup: resolve(__dirname, 'src/popup/main.tsx'),
        content: resolve(__dirname, 'src/content/content.ts'),
        background: resolve(__dirname, 'src/background/background.ts')
      },
      output: {
        entryFileNames: '[name].js',
        chunkFileNames: '[name].js',
        assetFileNames: '[name].[ext]'
      }
    }
  },
  define: {
    global: 'globalThis'
  }
})
import path from "node:path";
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  base: "/academy/",
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 5173,
    proxy: {
      // Frontend hits `/api/academy/...`; in prod a reverse proxy (Cloudflare
      // Worker) strips `/api/academy` before the request reaches FastAPI.
      // In dev we strip it here so the backend served at root `/` matches.
      "/api/academy": {
        target: process.env.VITE_API_BASE_URL || "http://localhost:8000",
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api\/academy/, ""),
      },
    },
  },
});

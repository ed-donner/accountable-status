import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

const webPort = Number(process.env.STATUS_WEB_PORT ?? 5190);
const apiPort = Number(process.env.STATUS_API_PORT ?? 8790);

export default defineConfig({
  plugins: [react()],
  server: {
    host: "127.0.0.1",
    port: webPort,
    strictPort: true,
    proxy: { "/api": `http://127.0.0.1:${apiPort}` },
  },
});

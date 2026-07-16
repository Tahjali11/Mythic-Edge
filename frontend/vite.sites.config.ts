import { fileURLToPath } from "node:url";

import { cloudflare } from "@cloudflare/vite-plugin";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

import { sitesHostingMetadataPlugin } from "./build/sites-vite-plugin";

const frontendRoot = fileURLToPath(new URL(".", import.meta.url));

export default defineConfig({
  plugins: [
    cloudflare({
      config: {
        name: "server",
        main: "./worker/index.ts",
        compatibility_date: "2026-07-15",
        assets: {
          binding: "ASSETS",
          not_found_handling: "single-page-application",
          run_worker_first: ["/api", "/api/*"]
        },
        observability: {
          enabled: false
        }
      },
      persistState: false,
      remoteBindings: false,
      viteEnvironment: {
        name: "server"
      }
    }),
    react(),
    sitesHostingMetadataPlugin(frontendRoot)
  ]
});

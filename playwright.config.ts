import os from "node:os";
import path from "node:path";

import { defineConfig } from "@playwright/test";

// The tests run the app on their own ports and database, and a stand-in for Accountable.
const WEB_PORT = 5191;
const API_PORT = 8791;
const STAND_IN_PAGE_PORT = 8792;
const STAND_IN_API_PORT = 8793;
const STAND_IN_CONTROL_PORT = 8794;
const dbPath = path.join(os.tmpdir(), "accountable-status-e2e", "status.db");

export default defineConfig({
  testDir: "e2e",
  testMatch: "*.spec.ts",
  workers: 1,
  fullyParallel: false,
  forbidOnly: true,
  retries: 0,
  timeout: 60_000,
  reporter: [["list"]],
  outputDir: path.join(os.tmpdir(), "accountable-status-e2e", "results"),
  use: {
    baseURL: `http://127.0.0.1:${WEB_PORT}`,
    // The installed Google Chrome.
    channel: "chrome",
    launchOptions: { args: ["--disable-gpu"] },
    viewport: { width: 1280, height: 900 },
    screenshot: "only-on-failure",
    trace: "off",
  },
  metadata: { standInControl: `http://127.0.0.1:${STAND_IN_CONTROL_PORT}` },
  webServer: [
    {
      command: "node e2e/stand-in.mjs",
      env: {
        STAND_IN_PAGE_PORT: String(STAND_IN_PAGE_PORT),
        STAND_IN_API_PORT: String(STAND_IN_API_PORT),
        STAND_IN_CONTROL_PORT: String(STAND_IN_CONTROL_PORT),
      },
      url: `http://127.0.0.1:${STAND_IN_CONTROL_PORT}/state`,
      reuseExistingServer: false,
      timeout: 15_000,
    },
    {
      command: "node e2e/start-app.mjs",
      env: {
        STATUS_DB: dbPath,
        STATUS_WEB_PORT: String(WEB_PORT),
        STATUS_API_PORT: String(API_PORT),
        STATUS_CHECK_INTERVAL: "1",
        STATUS_CHECK_TIMEOUT: "2",
        STATUS_TARGETS: JSON.stringify({
          accountable: {
            page: `http://127.0.0.1:${STAND_IN_PAGE_PORT}/`,
            api: `http://127.0.0.1:${STAND_IN_API_PORT}/api/meta`,
          },
        }),
      },
      url: `http://127.0.0.1:${WEB_PORT}/api/status`,
      reuseExistingServer: false,
      timeout: 120_000,
    },
  ],
});

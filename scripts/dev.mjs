// npm run dev: fetch what is missing, start the backend and the frontend, print the address.

import path from "node:path";

import { ROOT, setup, start, waitUntilReady } from "./common.mjs";

const webPort = Number(process.env.STATUS_WEB_PORT ?? 5190);
const apiPort = Number(process.env.STATUS_API_PORT ?? 8790);
const READY_TIMEOUT_MS = 90_000;

setup();

const env = { ...process.env, STATUS_WEB_PORT: String(webPort), STATUS_API_PORT: String(apiPort) };
const vite = path.join(ROOT, "node_modules", "vite", "bin", "vite.js");

const children = [
  start("uv", ["run", "--no-sync", "uvicorn", "status.main:app", "--host", "127.0.0.1", "--port", String(apiPort), "--log-level", "warning"], { env }),
  start(process.execPath, [vite, path.join(ROOT, "frontend"), "--logLevel", "warn"], { env }),
];

let running = true;
let exitCode = 0;
function stopAll(signal = "SIGTERM") {
  for (const child of children) {
    if (child.exitCode === null && !child.killed) child.kill(signal);
  }
}
for (const child of children) {
  child.on("error", (error) => {
    console.error(`Could not start a server: ${error.message}`);
    exitCode = 1;
    stopAll();
  });
  child.on("exit", (code) => {
    if (running && code) exitCode = code;
    running = false;
    stopAll();
    if (children.every((c) => c.exitCode !== null || c.signalCode !== null)) process.exit(exitCode);
  });
}
for (const signal of ["SIGINT", "SIGTERM"]) {
  process.on(signal, () => stopAll(signal));
}

const ready = await waitUntilReady(
  [`http://127.0.0.1:${apiPort}/api/status`, `http://127.0.0.1:${webPort}/`],
  () => running,
  READY_TIMEOUT_MS,
);
if (ready) {
  console.log(`\nAccountable Status is running at http://localhost:${webPort}`);
  console.log("Keep this window open while you use it. Press Ctrl+C to stop.\n");
} else if (running) {
  console.error("Accountable Status did not start in time.");
  stopAll();
  exitCode = 1;
}

// Shared helpers for the npm scripts.

import { spawn, spawnSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
export const isWindows = process.platform === "win32";

/** Run a command to the end, showing its output. Returns its exit code. */
export function run(command, args, options = {}) {
  const result = spawnSync(command, args, { cwd: ROOT, stdio: "inherit", shell: isWindows, ...options });
  if (result.error) {
    console.error(`Could not run ${command}: ${result.error.message}`);
    return 1;
  }
  return result.status ?? 1;
}

/** Start a long-running command. */
export function start(command, args, options = {}) {
  return spawn(command, args, { cwd: ROOT, stdio: "inherit", shell: false, ...options });
}

/** Fetch what is missing: node packages and the Python environment. */
export function setup() {
  if (!fs.existsSync(path.join(ROOT, "node_modules", "vite")) || !fs.existsSync(path.join(ROOT, "node_modules", ".bin"))) {
    console.log("Installing node packages (first run)");
    if (run("npm", ["install"]) !== 0) fail("npm install failed");
  }
  if (!fs.existsSync(path.join(ROOT, ".venv"))) {
    console.log("Setting up the Python environment (first run)");
    if (run("uv", ["sync"]) !== 0) fail("uv sync failed. Is uv installed?");
  }
}

export function fail(message) {
  console.error(message);
  process.exit(1);
}

/** Wait until every address answers, or time runs out. */
export async function waitUntilReady(urls, stillRunning, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline && stillRunning()) {
    const answers = await Promise.all(
      urls.map((url) =>
        fetch(url, { signal: AbortSignal.timeout(2000) }).then(
          (r) => r.ok,
          () => false,
        ),
      ),
    );
    if (answers.every(Boolean)) return true;
    await new Promise((resolve) => setTimeout(resolve, 500));
  }
  return false;
}

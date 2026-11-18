// npm test: backend, frontend, then end-to-end tests. Fails if any of them fails.

import { run, setup } from "./common.mjs";

setup();
const steps = [
  ["Backend (pytest)", "uv", ["run", "--no-sync", "pytest", "backend/tests"]],
  ["Frontend (Vitest)", "npm", ["run", "test", "--workspace", "frontend"]],
  ["End to end (Playwright)", "npx", ["playwright", "test", "--config", "playwright.config.ts"]],
];

const failed = [];
for (const [name, command, args] of steps) {
  console.log(`\n== ${name}`);
  if (run(command, args) !== 0) failed.push(name);
}
if (failed.length) {
  console.error(`\nFailed: ${failed.join(", ")}`);
  process.exit(1);
}
console.log("\nAll tests passed");

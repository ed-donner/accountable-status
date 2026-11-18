# Build Instructions: Accountable Status

Based on the code generation plan (`construction/code-generation/code-generation-plan.md`), the unit test instructions (`unit-test-instructions.md`) and the code summary (`code-summary.md`) in the same record.

## Prerequisites

- Node.js 24 or later (26 is the current LTS), with npm
- Python 3.12 and `uv`
- Google Chrome, for the end-to-end tests
- Free ports: 5190 and 8790 for the app, and 5191 and 8791 to 8794 for the end-to-end tests

## Install

- `npm run dev` fetches whatever is missing on the first run (npm packages, Python packages with `uv`), then starts the backend and page.
- To install without starting: `npm install` and `uv sync`.

## Environment

No secrets are needed. Optional settings, all with defaults:

- `STATUS_TARGETS`: JSON that replaces the watched addresses
- `STATUS_DB`: database path (default `data/status.db`)
- `STATUS_WEB_PORT` (5190), `STATUS_API_PORT` (8790)
- `STATUS_CHECK_INTERVAL` (60 seconds), `STATUS_CHECK_TIMEOUT` (5 seconds)

To watch the real Accountable, run `npm run dev` in `../accountable` as a background task. It is ready when it prints "Accountable is running at http://localhost:5173". Its API answers 401 at http://localhost:8765/api/meta, which still counts as up.

## Build

- Frontend type check and bundle: `npm run build --workspace frontend`
- The backend needs no build step. `uv run` runs it from source.

## Verify the build

- `npm run build --workspace frontend` exits 0 and writes `frontend/dist/`
- `npm run dev`, then http://localhost:8790/api/status returns JSON with 90 days of data, and http://localhost:5190 shows the page

## Troubleshooting

- A port is in use: another copy of the app is probably running. Stop that task, or set `STATUS_WEB_PORT` and `STATUS_API_PORT`.
- The page shows Accountable as down: start Accountable as above. The checker needs both its page and its API to answer.
- The sample history looks stale: `npm run seed` resets the database after asking (`--yes` skips the question).
- Chunk size warning from Vite during the build: the bundle is about 636 kB because of the chart library. It is a warning, not a failure.

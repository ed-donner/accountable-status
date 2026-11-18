# Code Summary: Accountable Status

## How to run it

- `npm run dev` installs what is missing on the first run, starts the backend (port 8790) and the page (port 5190), and prints the app's address, http://localhost:5190. A new database is filled with 90 days of sample history on first start.
- `npm test` runs the backend, frontend and end-to-end tests.
- `npm run seed` asks "Replace all data with sample data? (y/N)" and resets the database. `--yes` skips the question.
- Accountable runs separately from `../accountable` with `npm run dev` there. It is only read, never changed.
- Settings: `STATUS_TARGETS` (JSON, replaces the watched addresses), `STATUS_DB`, `STATUS_WEB_PORT`, `STATUS_API_PORT`, `STATUS_CHECK_INTERVAL`, `STATUS_CHECK_TIMEOUT`. The database defaults to `data/status.db`.

## Files created

- Root: `package.json`, `package-lock.json`, `pyproject.toml`, `uv.lock`, `playwright.config.ts`
- `scripts/`: `common.mjs`, `dev.mjs`, `seed.mjs`, `test.mjs`
- `backend/status/`: `__init__.py`, `config.py`, `db.py`, `repository.py`, `checker.py`, `incidents.py`, `stats.py`, `scheduler.py`, `api.py`, `main.py`, `seed.py`
- `backend/tests/`: `conftest.py` and tests for the database, repository, checker, incidents, stats, scheduler, API and sample history
- `frontend/`: `package.json`, `index.html`, `tsconfig.json`, `vite.config.ts`, `vitest.config.ts`
- `frontend/src/`: `main.tsx`, `App.tsx`, `api.ts`, `types.ts`, `format.ts`, `styles.css`, test files, and `components/` with `ServiceCard`, `UptimeBars`, `ResponseChart`, `IncidentList`
- `e2e/`: `stand-in.mjs`, `start-app.mjs`, `status.spec.ts`

## Files modified

- `.gitignore`: lines added after the AI-DLC block for `node_modules/`, `.venv/`, caches, `data/`, database files, test output and `frontend/dist/`

`README.md`, `docs/` and `../accountable` are unchanged.

## Key decisions

- A day with no checks shows a grey "No data" bar and is left out of uptime figures.
- Uptime is compared unrounded against 99.9% and 99%, and shown cut to two decimals so 99.996% never shows as 100%.
- The 24-hour chart leaves down checks out and joins the line across them.
- The API adds a 90-day uptime figure, and each incident's open state and duration (time elapsed so far while open).
- Sample history is generated relative to the current time from local midnight 89 days ago: 5 closed outages of 2, 7, 15, 42 and 185 minutes, and 3 slow stretches of 25, 35 and 70 minutes. The first start fills the database only when it has no checks at all.
- The three brand fonts come from `@fontsource` packages, so nothing loads from the network.
- A bug found by a test: summing the true/false `up` column returned 1 instead of a count, which would have made every day look green. It is fixed and a test guards it.

## Test summary

| Suite | Command | Result |
|---|---|---|
| Backend (pytest) | `uv run pytest backend/tests` | 29 passed |
| Frontend (Vitest) | `npm run test --workspace frontend` | 8 passed |
| End to end (Playwright, installed Chrome) | `npx playwright test --config playwright.config.ts` | 2 passed |

No coverage floor applies in the poc scope.

## Tests written but not run

None. `npm test` as a single command was not run in this stage; the three commands it chains were.

## Deviations from the plan

- 39 tests instead of about 20 (29 pytest, 8 Vitest, 2 Playwright), all small cases on the same behaviors.
- Extra dev dependencies: pytest-asyncio, Testing Library jest-dom, and the `@fontsource` font packages.
- The backend is an installable `status` package so `uv run` and `python -m status.seed` work.
- The end-to-end tests run the real `npm run dev` on ports 5191 and 8791 to 8794 with a database in the OS temp folder, and reload the page instead of waiting for the 30-second refresh.

## Not yet done

- A check against the real Accountable: it was not running during the build, so the checker showed it as down. This is left for Build and Test.

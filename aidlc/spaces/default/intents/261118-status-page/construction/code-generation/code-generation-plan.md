# Code Generation Plan: Accountable Status

## Summary

- Builds: a status page for Accountable: a once-a-minute checker, incident tracking, a JSON API, 90 days of sample data and a React page
- Touches: new `backend/`, `frontend/`, `e2e/`, `scripts/`, `package.json`, `pyproject.toml`, `playwright.config.ts` at the repo root; nothing in `../accountable`, `README.md` or `docs/`
- Tests: about 20 tests: 11 pytest, 6 Vitest, 2 Playwright (Minimal strategy, test-after)

## Inputs

- Requirements: `inception/requirements-analysis/requirements.md` (FR1 to FR5, NFR1 to NFR5)
- Stack: `docs/TECH_STACK.md` (React and Vite in `frontend/`, FastAPI and SQLAlchemy Core with SQLite in `backend/`, ports 5190 and 8790)
- Look: the brand skill (Instrument Sans, JetBrains Mono, Sea Green / Marigold / Coral / Raspberry, light and dark surfaces, rounded panels with no outline)
- Accountable is read only. Its page is http://localhost:5173 and its API is http://localhost:8765/api/meta.

## Decisions this plan makes

These cover points the requirements leave open. The code summary lists them again after the build.

- A day with no checks shows a grey "No data" bar and is left out of uptime figures (FR3.2).
- A "slow stretch" in the sample data is 20 or more minutes in a row with a response time of 1,200 ms or more, against a normal 80 to 250 ms (FR4.2).
- `npm run seed` asks "Replace all data with sample data? (y/N)". Declining leaves the database as it was. `--yes` skips the question for tests and scripts (FR4.3).
- Service addresses can be overridden by an environment variable (`STATUS_TARGETS`, JSON) so tests can point the checker at test servers (FR5.2).
- An incident left open when the backend stops stays open until the first successful check after it restarts. While open, its duration is the time elapsed so far (FR2.4).

## Steps

- [x] Step 1: Project structure and configuration skeleton (FR5.2, NFR4)
  - Root `package.json` with `frontend/` as a workspace and scripts `dev`, `test`, `seed`
  - Root `pyproject.toml` (Python 3.12, FastAPI, uvicorn, SQLAlchemy, httpx, pytest) and `uv.lock`
  - `scripts/dev.mjs` (fetch what is missing, start backend on 8790 and frontend on 5190, print the app's address), `scripts/test.mjs`, `scripts/seed.mjs`
  - `backend/status/config.py`: services list (Accountable with its page and API addresses), check interval, 5 second timeout, database path, `STATUS_TARGETS` override
- [x] Step 2: Bootstrap the minimal test runners and record the unit-scoped commands (NFR5)
  - pytest config in `pyproject.toml`; `frontend/vitest.config.ts`; `playwright.config.ts` and `e2e/`
  - Commands are recorded in `unit-test-instructions.md`
- [x] Step 3: Data model implementation (FR1.3, FR2.4)
  - Table `checks`: `id`, `service_id`, `checked_at`, `up`, `response_ms` (blank for a down check, FR1.3)
  - Table `incidents`: `id`, `service_id`, `opened_at`, `closed_at` (blank while open, FR2.4)
  - Index on `checks (service_id, checked_at)`, which the daily bars (FR3.1) and the 24 hour chart (FR3.3) read by
  - `backend/status/db.py` with SQLAlchemy Core table definitions and engine setup
- [x] Step 4: Data model tests, written and run after Step 3 (FR1.3, FR2.4)
- [x] Step 5: Data access implementation (FR1.3, FR2.1, FR2.2, FR3.1, FR3.3, FR3.4)
  - `backend/status/repository.py`: insert a check, find the open incident, open and close an incident, read checks by day and by last 24 hours, list incidents newest first
- [x] Step 6: Data access tests, written and run after Step 5
- [x] Step 7: Business logic implementation (FR1.1, FR1.2, FR1.4, FR2.1 to FR2.3, FR3.2)
  - `backend/status/checker.py`: probe both addresses; up only when both answer with any HTTP status; slower of the two times; timeout counts as no answer; down check has no response time
  - `backend/status/incidents.py`: open on the first failed check, close on the first successful check, one open incident per service
  - `backend/status/stats.py`: daily uptime in local time (today counts so far), bar color by 99.9 and 99 thresholds compared unrounded, grey for no data
  - `backend/status/scheduler.py`: a loop inside the backend that runs every 60 seconds
- [x] Step 8: Business logic tests, written and run after Step 7
- [x] Step 9: API implementation (FR3.5, NFR1)
  - `backend/status/api.py` and `main.py`: FastAPI app, `GET /api/status` returning each service with 90 days of daily uptime and color, last 24 hours of response times, and incidents; checker started when the app starts
- [x] Step 10: API tests, written and run after Step 9
- [x] Step 11: Sample history (FR4.1 to FR4.3)
  - `backend/status/seed.py`: 90 days of once-a-minute checks and incidents, mostly up, at least 3 closed incidents of different lengths and at least 2 slow stretches, the same data each run
  - Runs on first start when the database is empty, and from `npm run seed` after the question
- [x] Step 12: Sample history tests, written and run after Step 11 (FR4.1, FR4.2, FR4.3)
- [x] Step 13: Frontend implementation (FR3.1 to FR3.6, NFR3)
  - Vite, React and TypeScript in `frontend/`; Recharts for the response time chart
  - Components: `App`, `ServiceCard` (name, current state, daily bars), `UptimeBars` (90 bars, tooltip with date and uptime), `ResponseChart`, `IncidentList` (open ones marked, empty message when none)
  - Data fetched from `/api/status` and refreshed every 30 seconds (FR3.5)
  - Brand: Instrument Sans for text, JetBrains Mono for numbers, light and dark surfaces by system setting, rounded panels, no gradients, no single-edge borders; `data-testid` on interactive and key elements
- [x] Step 14: Frontend tests, written and run after Step 13 (FR3.2, FR3.4)
- [x] Step 15: End-to-end tests (FR2.1, FR2.2, FR3.1, NFR2)
  - Playwright with the installed Google Chrome; tests start the app themselves with their own database and a small test server standing in for Accountable
- [x] Step 16: Environment and build configuration
  - `.gitignore` additions for `node_modules`, `.venv`, the database file and Playwright output (the one existing file this plan changes; the person's other files stay as they are)
- [x] Step 17: Documentation and traceability
  - Notes on how to run it go in `code-summary.md`; `README.md` is left as it is
  - Run `aidlc engine sensor-traceability` for `traceability.json`

## Requirement coverage

| Requirement | Plan steps |
|---|---|
| FR1.1 to FR1.4 | 7, 8 |
| FR2.1 to FR2.4 | 3, 5, 7, 8, 15 |
| FR3.1 to FR3.6 | 5, 9, 13, 14, 15 |
| FR4.1 to FR4.3 | 11, 12 |
| FR5.1, FR5.2 | 1, 7 |
| NFR1 | 9, 13 |
| NFR2 | 11, 15 |
| NFR3 | 13 |
| NFR4 | 1, 2 |
| NFR5 | 2, 4, 6, 8, 10, 12, 14, 15 |

## Testing Contract

```json
{
  "version": 1,
  "methodology": "test-after",
  "source": "org",
  "ordering": "implement each applicable testable layer, then write and run that layer's tests.",
  "scope": "poc",
  "test_strategy": "minimal",
  "project_type": "greenfield",
  "applicable_notes": [
    {
      "layer": "org",
      "text": "We treat tests as a first-class deliverable in every Bolt. The specific\nmethodology (TDD, BDD, ATDD, or classic test-after) is affirmed at\npractices-discovery and recorded in `team.md` under this heading with explicit\n`Methodology` and `Ordering` fields; Code Generation resolves those fields\nindependently from coverage, tooling, and scope notes.\n\nWhen no posture has been affirmed, our default per scope is:\n- **Methodology**: test-after\n- **Ordering**: implement each applicable testable layer, then write and run\n  that layer's tests.\n- `mvp`, `enterprise`, `feature`, `infra` add an 80% line-coverage\n  floor and CI execution before merge.\n- `bugfix`, `security-patch` add a targeted regression for the specific\n  bug/vulnerability and require the existing suite to remain green.\n- `express` uses the Minimal strategy: requirement-driven unit tests (one per\n  requirement, with a happy-path floor per component); existing tests remain\n  green.\n- `poc`, `refactor`, `workshop`, `classic` add no extra new-test floor and require the\n  existing suite to remain green.\n\nThe active `Test Strategy` still applies in every scope and determines test\nvolume/types. Scope floors are additive; they never reduce or replace the\nselected strategy.\n\nBuild and Test verifies defined coverage floors and affirmed quality targets;\nthey may not be weakened to make a step pass.\n\nAffirm a stricter posture in `team.md` if the team commits to one."
    }
  ],
  "obligations": {
    "strategy": "minimal",
    "strategy_volume": [
      "One verifiable test per requirement at the narrowest effective level.",
      "At least one happy-path unit test per component.",
      "Unit tests are the default; a bugfix/security scope floor may require an integration or E2E regression when that is the narrowest level that reproduces the defect."
    ],
    "scope_floor": [
      "Keep the existing test suite green.",
      "This scope adds no extra new-test floor beyond the selected test strategy."
    ],
    "combination_rule": "Apply every selected-strategy obligation and every scope-floor obligation; neither replaces the other, and a targeted scope regression may add the narrowest necessary test type beyond the strategy default."
  },
  "plan_profile": {
    "methodology": "test-after",
    "runner_step": "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
    "runner_ready_before_first_test": true,
    "testable_layers": [
      "Data model / database behavior",
      "Repository / data access",
      "Business logic",
      "API / endpoint",
      "Frontend behavior"
    ],
    "steps": [
      "Project structure and production configuration skeleton.",
      "Bootstrap the minimal test runner/configuration and record the exact unit-scoped command.",
      "Data model / database behavior - implement.",
      "Data model / database behavior - write and run its tests after implementation.",
      "Repository / data access - implement.",
      "Repository / data access - write and run its tests after implementation.",
      "Business logic - implement.",
      "Business logic - write and run its tests after implementation.",
      "API / endpoint - implement.",
      "API / endpoint - write and run its tests after implementation.",
      "Frontend behavior - implement.",
      "Frontend behavior - write and run its tests after implementation.",
      "Environment/build configuration.",
      "Documentation and traceability."
    ]
  },
  "input_sha256": "sha256:8ea1ef920e68ca73437a39f413355d71d0d909a57d5d857da31deb5d9355e261",
  "contract_sha256": "sha256:615d0f211ddcd07aebccb0dd6a68c9e4b811c5fab93b04a37004687ace5379de"
}
```

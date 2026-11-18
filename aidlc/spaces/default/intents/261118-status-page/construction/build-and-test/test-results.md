# Test Results: Accountable Status

Run on 2026-11-18 against the code described in `construction/code-generation/code-summary.md`, using the commands in `unit-test-instructions.md` and the plan in `code-generation-plan.md`.

## Build

| Command | Exit | Result |
|---|---|---|
| `npm run build --workspace frontend` | 0 | Type check passed and the bundle was written. One chunk-size warning (636 kB), not a failure. |

## Tests

`npm test` was run as one command: it runs the three suites in order and exited 0 ("All tests passed").

| Suite | Where it ran | Total | Passed | Failed | Skipped |
|---|---|---|---|---|---|
| Backend (pytest), `uv run pytest backend/tests` | Python 3.12 | 29 | 29 | 0 | 0 |
| Frontend (Vitest), `npm run test --workspace frontend` | Node with jsdom (a DOM emulator, not a browser) | 8 | 8 | 0 | 0 |
| End to end (Playwright), `npx playwright test --config playwright.config.ts` | Installed Google Chrome (a real browser engine), with a stand-in for Accountable | 2 | 2 | 0 | 0 |

## Check against the real Accountable

Done by hand, with Accountable started from `../accountable` with `npm run dev` as a background task and `npm run dev` here as another. Both tasks were stopped afterwards, and ports 5173, 8765, 5190 and 8790 no longer answered.

| Step | Result |
|---|---|
| Accountable running | Page answered 200 and API answered 401; the checker showed it as up |
| Stop Accountable | Page stopped answering; an incident opened 56 seconds later |
| Start Accountable again | API answered 401; the incident closed 56 seconds later, after 60 seconds open |
| Page in Chrome | 90 bars, last-24-hour chart, incident list, all rendering with the brand fonts and colors |

An earlier incident of 1 minute, from 16:56 to 16:57 local time, is from the first start-up of the status page before Accountable was running. It is real data, not sample data.

## Coverage

No coverage floor applies. The scope is poc and the Testing Contract adds none, so no coverage report was produced.

## Target Verification Matrix

| Target ID | Source | Expected | Actual | Evidence | Owning Stage | Verdict |
|---|---|---|---|---|---|---|
| NFR1 | requirements.md, NFR1 | Incident visible within 2 minutes of stopping Accountable, and shown closed within 2 minutes of starting it | Opened after 56 seconds and closed after 56 seconds | Real Accountable check above; e2e incident test in Chrome | build-and-test | Met |
| NFR2 | requirements.md, NFR2 | A fresh install shows 90 bars and the sample incidents with no step beyond `npm run dev` | Fresh database filled on first start; page showed 90 bars and sample incidents | e2e first-run test in Chrome; screenshot | build-and-test | Met |
| NFR3 | requirements.md, NFR3 | Page follows the brand skill with no departure | Brand fonts, colors, rounded panels, no outlines, no gradients, plain labels | Screenshot of the page in Chrome, compared with the brand skill | build-and-test | Met |
| NFR4 | requirements.md, NFR4 | The stack in `docs/TECH_STACK.md`, ports 5190 and 8790 | React, Vite, FastAPI, SQLAlchemy Core and SQLite; ports as stated | `npm run dev` output; status API at 8790; page at 5190 | build-and-test | Met |
| NFR5 | requirements.md, NFR5 | `npm test` runs unit and end-to-end tests and fails if any fails | Exit 0 with 39 of 39 passing | `npm test` output | build-and-test | Met |
| TC-1 | Testing Contract (poc) | Existing suite stays green | There was no existing suite; the new one is green | `npm test` output | build-and-test | Met |
| TC-2 | Testing Contract, CI obligation | CI before merge | The plan runs no CI Pipeline | Plan stages | ci-pipeline | N/A |

Browser behavior was checked in a real browser engine (Chrome, driven by Playwright). The component tests in Vitest ran in jsdom and are integration evidence only.

## Failures

None.

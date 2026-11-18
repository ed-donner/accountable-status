# Unit Test Instructions: Accountable Status

Strategy: Minimal, test-after. About 20 tests: one per requirement group at the narrowest effective level, and at least one happy-path test per component. The scope (poc) adds no coverage floor, so none is set.

## Frameworks

- Backend: pytest, run with `uv run`
- Frontend: Vitest with Testing Library
- End to end: Playwright Test with the installed Google Chrome, in `e2e/`

## Commands

Each command runs this work's tests only and is runnable once the matching plan step has bootstrapped its runner (Step 2).

- Backend: `uv run pytest backend/tests`
- Frontend: `npm run test --workspace frontend`
- End to end: `npx playwright test --config playwright.config.ts`
- All of them: `npm test`, which fails if any test fails

## Backend tests (pytest, 11)

- Data model: a check row and an incident row round-trip; a down check stores no response time
- Data access: the open incident is found; daily rows and last-24-hour rows come back in order
- Checker: both addresses answer, including a 401, so the check is up with the slower time; one address stopped, so the check is down with no time; no answer within the timeout counts as down
- Incidents: first failed check opens one; more failed checks add none; first successful check closes it
- Stats: 99.95%, 99.5% and 98% give green, amber and red; 99.9% is green and 99% is amber (unrounded); a day with no checks is grey
- API: `GET /api/status` returns 90 days, the 24 hour series and incidents
- Sample history: 90 days, at least 3 closed incidents with different lengths, at least 2 slow stretches; seeding twice gives the same data

## Frontend tests (Vitest, 6)

- Bar color function matches the thresholds, and grey for no data
- A service card renders 90 bars
- The incident list marks an open incident and shows a message when there are none
- The page asks for data again after 30 seconds
- The response chart leaves down checks out
- Durations and response times are formatted for reading

## End-to-end tests (Playwright, 2)

- First run: with a fresh database the page shows 90 bars and the sample incidents
- Incident cycle: stop the stand-in service and an incident opens; start it again and the incident closes

## Test data and stand-ins

- Backend tests use a SQLite database in a temporary folder, one per test
- The checker's HTTP calls go to small local test servers, not to Accountable
- End-to-end tests start the backend and frontend themselves on their own ports and database, and set `STATUS_TARGETS` to a test server they can stop and start
- Nothing in `../accountable` is started, stopped or changed by the automated tests. The real Accountable check is done by hand in Build and Test.

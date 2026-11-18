# Requirements: Accountable Status

Sources: the intent statement (`ideation/intent-capture/intent-statement.md`), the original request, the answers in `requirements-analysis-questions.md` (Q1 to Q4), and `docs/TECH_STACK.md`.

## Intent Analysis

The suite team wants one page that shows, at a glance, whether each Accountable service is responding and how fast, with 90 days of history and a list of incidents (intent statement; Q1 in the intent questions). The first version watches one service, Accountable, and must look complete on the first run.

## Functional Requirements

### FR1. Checking a service

- FR1.1 Every minute, the system checks each service's addresses. Pass: with Accountable running, a new check record exists for each minute that passes.
- FR1.2 A check counts as up only when both Accountable addresses answer: the page (http://localhost:5173) and the API (http://localhost:8765/api/meta). Any HTTP status counts as an answer, including the API's 401 (Q1). Pass: with both running, the check is up; with either stopped, the check is down.
- FR1.3 Each check records when it ran, whether the service responded, and how fast (response time in milliseconds). The response time of a check is the slower of the two addresses' response times. A down check stores no response time. Pass: all three values are stored for every up check, and a down check has no response time.
- FR1.4 A check that gets no answer within the timeout counts as not responded. The timeout is 5 seconds (see Assumptions).

### FR2. Incidents

- FR2.1 An incident opens on the first failed check for a service (Q2). Pass: stopping Accountable opens an incident after the next check runs.
- FR2.2 An incident closes on the first successful check after it opened (Q2). Pass: starting Accountable again closes the open incident after the next check runs.
- FR2.3 Only one incident is open per service at a time. Pass: repeated failed checks do not create more incidents.
- FR2.4 Each incident records when it opened, when it closed (blank while open), and its duration.

### FR3. The status page

- FR3.1 The page shows each service with a row of 90 daily bars, one per day, oldest to newest.
- FR3.2 Each bar is colored by that day's uptime: green at 99.9% or higher, amber from 99% up to 99.9%, red below 99% (Q4). Pass: days with uptime of 99.95%, 99.5% and 98% show green, amber and red. A day follows this computer's local time, and today's bar counts only today's checks so far.
- FR3.3 The page shows a chart of response times for each service over the last 24 hours. Down checks have no response time and are left off the chart.
- FR3.4 The page shows a list of incidents, newest first, with open incidents marked as open (FR2).
- FR3.5 The page gets its data from the backend's JSON API (tech stack). The page refreshes its data by itself every 30 seconds, so a new incident shows without reloading. Pass: an incident opened while the page is open appears within 30 seconds of the check that opened it.
- FR3.6 The page is written for the team that runs the Accountable suite (Q1 in the intent questions).

### FR4. Sample history

- FR4.1 A new database is filled with 90 days of sample history so the page looks complete on the first run (request).
- FR4.2 The sample history is mostly up, with a few past incidents of different lengths, a couple of slow stretches, and varied response times (Q3). Pass: the 90 days include at least 3 closed incidents with different durations, and at least 2 slow stretches.
- FR4.3 `npm run seed` resets the database to the sample data, after asking (tech stack).

### FR5. Services

- FR5.1 The first version watches one service, Accountable, which runs locally from `../accountable`. Its code is read there and is never copied or changed.
- FR5.2 The list of services is kept in code or a config file, so more services can be added later without a new screen.

## Non-Functional Requirements

- NFR1 Timeliness: after Accountable is stopped, an incident is visible on the page within 2 minutes; after it is started again, the incident shows as closed within 2 minutes (once-a-minute checks, plus the 30-second page refresh in FR3.5).
- NFR2 First run: on a fresh install, `npm run dev` brings up the backend and page, and the page shows 90 bars and the sample incidents with no manual step beyond that command.
- NFR3 Look: the page follows the brand skill (fonts, colors, tone) and looks polished. Pass: a reviewer compares it against the brand skill and finds no departure.
- NFR4 Stack: Node.js with TypeScript, React and Vite in `frontend/`, and Python 3.12 with FastAPI, SQLAlchemy Core and SQLite in `backend/`. The page runs on port 5190 and the backend on port 8790.
- NFR5 Tests: `npm test` runs unit tests (Vitest, pytest) and end-to-end tests (Playwright) and fails if any test fails. For this proof of concept, no extra coverage floor applies beyond the Minimal test strategy.

## Constraints

- Accountable's code is read only. No file in `../accountable` is changed.
- The tech stack in `docs/TECH_STACK.md` is used as written, including the npm scripts.
- Servers are started as background tasks, never with `&` in a shell command, and only processes started here are stopped.

## Assumptions

- The check timeout is 5 seconds. [assumption] It was not asked, so the team can change it.
- Daily uptime is the share of that day's checks that were up. [assumption]
- The checker runs inside the backend process while the backend is running, so checks stop when the backend stops. [assumption]

## Out of Scope

- Alerts and notifications (email, chat messages) when a service goes down (Q3 in the intent questions).
- Screens for adding or editing services (Q3 in the intent questions).

## Open Questions

- What response time counts as a slow stretch for the chart and the sample data? To be settled in code generation, since it was not asked.

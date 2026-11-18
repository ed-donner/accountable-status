# Cross-Unit Traceability: Accountable Status

Verdict: pass. Every requirement from `inception/requirements-analysis/requirements.md` is built, and no ID is uncovered. This work has no Units (poc scope), so each ID has one owner, code generation. The table comes from `aidlc engine sensor-traceability --stage build-and-test`, and refers to the plan, test instructions and code summary under `construction/code-generation/`.

| ID | Owning stage | Target file | Tested in |
|---|---|---|---|
| FR1.1 | code-generation | backend/status/scheduler.py | backend/tests/test_scheduler.py |
| FR1.2 | code-generation | backend/status/checker.py | backend/tests/test_checker.py |
| FR1.3 | code-generation | backend/status/db.py | backend/tests/test_db.py |
| FR1.4 | code-generation | backend/tests/test_checker.py | backend/tests/test_checker.py |
| FR2.1 | code-generation | backend/status/incidents.py | backend/tests/test_incidents.py; e2e (Chrome) |
| FR2.2 | code-generation | backend/status/incidents.py | backend/tests/test_incidents.py; e2e (Chrome) |
| FR2.3 | code-generation | backend/tests/test_incidents.py | backend/tests/test_incidents.py |
| FR2.4 | code-generation | backend/status/api.py | backend/tests/test_api.py |
| FR3.1 | code-generation | frontend/src/components/UptimeBars.tsx | components.test.tsx (jsdom); e2e (Chrome) |
| FR3.2 | code-generation | backend/status/stats.py | backend/tests/test_stats.py |
| FR3.3 | code-generation | frontend/src/components/ResponseChart.tsx | components.test.tsx (jsdom) |
| FR3.4 | code-generation | frontend/src/components/IncidentList.tsx | components.test.tsx (jsdom) |
| FR3.5 | code-generation | backend/status/api.py | backend/tests/test_api.py; components.test.tsx (30-second refresh) |
| FR3.6 | code-generation | frontend/src/App.tsx | Screenshot review |
| FR4.1 | code-generation | backend/status/seed.py | backend/tests/test_seed.py |
| FR4.2 | code-generation | backend/tests/test_seed.py | backend/tests/test_seed.py |
| FR4.3 | code-generation | scripts/seed.mjs | backend/tests/test_seed.py |
| FR5.1 | code-generation | backend/status/config.py | Real Accountable check |
| FR5.2 | code-generation | backend/status/config.py | e2e (Chrome, via `STATUS_TARGETS`) |
| NFR1 | code-generation | e2e/status.spec.ts | e2e (Chrome); real Accountable check |
| NFR2 | code-generation | e2e/status.spec.ts | e2e (Chrome) |
| NFR3 | code-generation | frontend/src/styles.css | Screenshot review in Chrome |
| NFR4 | code-generation | package.json | `npm run dev` |
| NFR5 | code-generation | scripts/test.mjs | `npm test` |

Uncovered IDs: none.

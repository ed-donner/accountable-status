This project uses the same technical stack as Accountable:

1. Node.js 26, the current LTS (24 or later works) / TypeScript for the frontend, using React and Vite, in `frontend/`
2. Python 3.12 for the backend using uv, with FastAPI, in `backend/`, with `pyproject.toml` and `uv.lock` at the repo root

The frontend gets its data from the backend's JSON API. The backend uses SQLAlchemy Core with a SQLite file and fills a new database with the sample data. Prefer popular, well-supported libraries to custom code, such as for the charts.

Commands are npm scripts in a `package.json` at the repo root, with `frontend/` as an npm workspace, so they work the same on Mac, Linux and Windows:

- `npm run dev` fetches whatever is missing on the first run, then starts the backend and frontend together and prints the app's address
- `npm test` runs all the tests and fails if any test fails
- `npm run seed` resets the database to the sample data, after asking

Testing will cover unit tests for the frontend with Vitest, unit tests for the backend with pytest, and end-to-end tests in `e2e/` with Playwright Test and the installed Google Chrome. The tests start the app themselves and use databases of their own.

Status runs its page on port 5190 and its backend on port 8790, so it doesn't clash with Accountable.

## Accountable

Accountable is the CRM this status page watches. Its code is in ~/projects/accountable. Read it there; never copy it into this repo or change any file in it.

- **Start it** by running `npm run dev` in ~/projects/accountable as a background task. The first run can take a minute while it sets itself up. It's ready when it prints "Accountable is running at http://localhost:5173". If it says a port is in use, Accountable is probably running already, so check it instead of starting another.
- **It's up** when both its page, http://localhost:5173, and its API, http://localhost:8765/api/meta, answer. The API answers 401 because nobody is signed in, and that still means it's up.
- **Stop it** by stopping the background task you started it with. Only ever stop processes you started yourself, and never stop a process by its name or port.

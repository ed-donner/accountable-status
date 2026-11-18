// Starts the app for the tests with a fresh database, so the first-run sample data is what they see.

import fs from "node:fs";

const db = process.env.STATUS_DB;
if (!db) throw new Error("STATUS_DB is not set");
for (const suffix of ["", "-wal", "-shm"]) fs.rmSync(`${db}${suffix}`, { force: true });

await import("../scripts/dev.mjs");

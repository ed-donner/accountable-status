// npm run seed: reset the database to the sample data, after asking. Pass --yes to skip the question.

import { ROOT, run, setup } from "./common.mjs";

setup();
const extra = process.argv.slice(2);
process.exit(run("uv", ["run", "--no-sync", "python", "-m", "status.seed", ...extra], { cwd: ROOT }));

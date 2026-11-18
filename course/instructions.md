# Week 2 Day 2: the optional AWS AI-DLC lesson

My steps and prompts for building Accountable Status with AWS AI-DLC and Claude Code. Accountable Status is a status page that checks your local Accountable every minute.

This repo starts with two files:

- `docs/TECH_STACK.md`: the stack, the ports, and how to start and stop Accountable
- `.claude/skills/brand/SKILL.md`: Accountable's brand skill, so Status matches the rest of the suite

## Before you start

- Your `accountable` folder from the course, where `npm run dev` starts Accountable
- Claude Code, Node.js 24 or later, uv and Google Chrome, as for Accountable
- About 45 minutes. Most of it is the agents working.

## 1. Get this repo beside Accountable

In a terminal in your `accountable` folder:

```
cd ..
git clone https://github.com/ed-donner/accountable-status.git
cd accountable-status
```

## 2. Install AI-DLC

Run the installer in your own terminal, not through your coding agent.

Mac and Linux:

```
curl -fsSL https://github.com/awslabs/aidlc-workflows/releases/latest/download/install.sh | sh
```

Windows (PowerShell):

```
irm https://github.com/awslabs/aidlc-workflows/releases/latest/download/install.ps1 | iex
```

It ends with `PASS installed AI-DLC`. If it says its folder isn't on your PATH, run the line it prints and open a new terminal. Then check:

```
aidlc --version
```

This prints `aidlc 2.11.4 (runtime 2.11.4)` or a later version.

## 3. Add AI-DLC to this repo

```
aidlc config --harness claude
aidlc doctor
```

`aidlc config` adds about 400 files: AI-DLC's skills, agents and hooks in `.claude/`, and its records in `aidlc/`. `aidlc doctor` should report 0 problems. Its warnings are advice, and you can ignore them. Commit what it added:

```
git add -A
git commit -m "Add AI-DLC"
```

## 4. Add the guard rules

AI-DLC's agents start and stop Accountable to test Status. These rules stop them from killing processes or changing Accountable's files. Create `.claude/settings.local.json` with:

```json
{
  "permissions": {
    "allow": ["Read(~/projects/accountable/**)"],
    "deny": [
      "Bash(kill)", "Bash(kill *)", "Bash(pkill)", "Bash(pkill *)",
      "Bash(killall)", "Bash(killall *)", "Bash(xargs kill *)",
      "Bash(taskkill)", "Bash(taskkill *)",
      "PowerShell(Stop-Process)", "PowerShell(Stop-Process *)",
      "Edit(~/projects/accountable/**)"
    ],
    "blockWritesOutsideWorkingDirectories": true
  }
}
```

If your `accountable` folder isn't `~/projects/accountable`, change both paths to its full path. Git ignores this file.

## 5. Start Claude Code

```
claude --model sonnet --effort medium
```

When it asks whether you trust the folder, it lists the tool permissions AI-DLC pre-approves. Choose "Yes, I trust this folder". I used Sonnet at medium effort in auto mode.

## 6. Send the intent

```
/aidlc Build Accountable Status, a status page for the Accountable suite of apps. Every minute it checks each service's address and records whether it responded and how fast. The page shows each service with a row of 90 daily bars colored by uptime, a chart of response times and a list of incidents, which open when a service stops responding and close when it comes back. Start with one service, Accountable, running locally from ../accountable, beside this repo. Read its code there; don't copy it or change it. Fill a new database with 90 days of sample history so the page looks complete on the first run. Make the page look polished, following the brand skill. Use the tech stack in docs/TECH_STACK.md, which includes how to start and stop Accountable.
```

## 7. Answer as the product owner

AI-DLC first proposes the "mvp" plan, with 19 stages. Choose "Use a different plan", then "poc (4 stages)".

At each stage it writes its questions to a file and asks how you'd like to answer them. Choose "Guide me" to answer in forms. For an answer that needs more than a choice, pick "Chat about this" and type it.

Its questions change from run to run. These are the ones it asked me, with my answers:

| Stage | Question | My answer |
|---|---|---|
| Intent Capture | Who will look at this status page? | Only the team that builds and runs the apps |
| | What would make this first version a success? | The page looks complete, and the checker really runs every minute against Accountable |
| | What should this first version leave out? | Alerts, and sign-in or admin screens |
| | Who decides what is in scope and when it is done? | You alone |
| Requirements Analysis | What counts as Accountable being "up"? | Both the page and the API answer below 500, with 401 counting as up |
| | How long before a check counts as "no response"? | 10 seconds |
| | How many failed checks open an incident, and how many good ones close it? | One and one |
| | How should each daily bar be colored? | Green at 99.9% or more, yellow from 99%, red below 99% |

After each stage, a reviewer lists its findings and you approve the stage or ask for changes. At Requirements Analysis I chose "Request Changes", then "Chat about this", and typed:

```
Please fix these and accept the rest as they are. A check's response time is the slower of the two addresses; a down check stores no response time and is left off the chart. Days follow this computer's local time, and today's bar counts today's checks so far. The chart shows the last 24 hours, and the page refreshes itself every 30 seconds so a new incident shows without reloading.
```

Code Generation and Build and Test then run on their own for about half an hour, with an approval at the end of each.

If it asks you to stop a process, check the process is Status's own server and not Accountable, then stop it yourself: `kill -TERM <id>` on Mac and Linux, `taskkill /PID <id> /T /F` on Windows.

## 8. See it working

Start Accountable with `npm run dev` in its own terminal. Then, in this folder:

```
npm run dev
```

Open http://localhost:5190 to see 90 days of sample history, the response-time chart and the incident list. Press Ctrl+C in Accountable's terminal, and within a minute Status shows Accountable as down with an ongoing incident. Start Accountable again, and the incident closes at the next check.

Commit your build:

```
git add -A
git commit -m "Build Accountable Status with AI-DLC"
```

AI-DLC's records of the run, from the questions to the test results, are in `aidlc/spaces/default/intents/`.

# Intent Statement: Accountable Status

## Problem Statement

- The Accountable suite of apps has no single page that shows whether each service is responding and how fast. [desc]
- The goal is a status page, Accountable Status, that checks each service's address every minute and records whether it responded and how fast. [desc]
- The page shows each service with a row of 90 daily bars colored by uptime, a chart of response times, and a list of incidents. [desc]
- An incident opens when a service stops responding and closes when it comes back. [desc]

## Target Customer

- The team that runs the Accountable suite, checking on its health. [Q1]

## Success Metrics

- On a fresh install, opening the page shows a complete page: 90 days of sample history, with new once-a-minute checks of Accountable appearing on top of it. [Q2]
- Stopping Accountable opens an incident, and the incident closes when Accountable is started again. [Q2]
- The sample history is a new database filled with 90 days of data so the page looks complete on the first run. [desc]

## Initiative Trigger

- The request is to build a status page for the Accountable suite, starting with one service, Accountable, running locally from `../accountable` beside this repo. [desc]

## Initial Scope Signal

- Workflow-selected scope: `poc` (workflow-selected). [scope]
- This first version leaves out alerts and notifications, and screens for adding or editing services. [Q3]
- The first version starts with one service, Accountable. Its code is read from `../accountable`, not copied or changed. [desc]
- The page is to look polished, following the brand skill, and use the tech stack in `docs/TECH_STACK.md`. [desc]
- The person who made this request decides what goes into the page. [Q4]

## Assumptions & Open Questions

None.

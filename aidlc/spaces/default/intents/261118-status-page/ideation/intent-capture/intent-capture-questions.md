# Intent Capture Questions

## Sources

- [desc] Initial description: "Build Accountable Status, a status page for the Accountable suite of apps. Every minute it checks each service's address and records whether it responded and how fast. The page shows each service with a row of 90 daily bars colored by uptime, a chart of response times and a list of incidents, which open when a service stops responding and close when it comes back. Start with one service, Accountable, running locally from ../accountable, beside this repo. Read its code there; don't copy it or change it. Fill a new database with 90 days of sample history so the page looks complete on the first run. Make the page look polished, following the brand skill. Use the tech stack in docs/TECH_STACK.md, which includes how to start and stop Accountable."
- [scope] Workflow-selected scope: `poc`.

## Q1. [Product] Who is this status page for?

The answer decides how the page is worded and what detail it shows (for example, whether raw response times are useful or just "up / down").

A. People who use Accountable and want to know whether it is working
B. The team that runs the Accountable suite, checking on its health
C. Both of the above
D. Not yet defined
X. Other (please specify)

[Answer]: B. The team that runs the Accountable suite, checking on its health

## Q2. [Product] What would make this first version a success?

This sets the check you run at the end to decide the first version works.

A. Opening the page on a fresh install shows a complete page: 90 days of sample history, and new once-a-minute checks of Accountable appearing on top of it
B. Everything in A, and stopping Accountable opens an incident that closes when Accountable is started again
C. Not yet defined
X. Other (please specify)

[Answer]: B. Everything in A, and stopping Accountable opens an incident that closes when Accountable is started again

## Q3. [Product] What should this first version leave out?

The first version starts with one service (Accountable). This asks what the page should not do yet, so it stays small.

A. Alerts and notifications (email, chat messages) when a service goes down
B. Screens for adding or editing services (the service list lives in the code or a config file)
C. Both A and B
D. None, nothing is ruled out yet
X. Other (please specify)

[Answer]: C. Both A and B

## Q4. [Product] Who decides what goes into the page, and does anyone need progress updates?

This tells us who signs off on the scope and whether anyone besides you needs to be kept informed.

A. You decide, and nobody else needs updates
B. You decide, and the Accountable team should see the result when it is done
C. Not yet defined
X. Other (please specify)

[Answer]: A. You decide, and nobody else needs updates

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]: Looks correct

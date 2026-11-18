# Requirements Analysis Questions

## Q1. [Product] What does it take for the Accountable check to count as "responded"?

Accountable has a page (http://localhost:5173) and an API (http://localhost:8765/api/meta). The API answers 401 when nobody is signed in, and that still means it is up. This decides what every once-a-minute check records.

A. Both addresses must answer (any HTTP status, including 401) for a check to count as up
B. Only the page address is checked
C. Only the API address is checked
D. Not yet defined
X. Other (please specify)

[Answer]: A. Both addresses must answer (any HTTP status, including 401) for a check to count as up

## Q2. [Product] When should an incident open and close?

A check can fail once because of a blip. This sets how quickly an incident appears after Accountable is stopped, and when it closes after Accountable is started again.

A. Opens on the first failed check and closes on the first successful check
B. Opens after 2 failed checks in a row and closes after 1 successful check
C. Opens after 3 failed checks in a row and closes after 1 successful check
D. Not yet defined
X. Other (please specify)

[Answer]: A. Opens on the first failed check and closes on the first successful check

## Q3. [Product] What should the 90 days of sample history look like?

The first-run page should look complete. This decides whether the sample data shows the page with only green bars or also shows how bad days and incidents look.

A. Mostly up, with a few past incidents of different lengths, a couple of slow stretches, and varied response times
B. All up, with no incidents
C. Not yet defined
X. Other (please specify)

[Answer]: A. Mostly up, with a few past incidents of different lengths, a couple of slow stretches, and varied response times

## Q4. [Product] How should a daily bar be colored by uptime?

Each of the 90 bars is one day. This sets the colors the team reads at a glance.

A. Green at 99.9% uptime or higher, amber from 99% up to 99.9%, red below 99%
B. Green at 99% or higher, amber from 95% up to 99%, red below 95%
C. Not yet defined
X. Other (please specify)

[Answer]: A. Green at 99.9% uptime or higher, amber from 99% up to 99.9%, red below 99%

## Consolidated Summary Confirmation

- Looks correct
- Request changes

[Answer]: Looks correct

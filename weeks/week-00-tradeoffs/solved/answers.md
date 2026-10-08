# Week 0: My answers to the interview scenarios

> Answer as you would in an interview: **clarify**, then **options**, then **recommend**, then **what it costs**. Bullet points are fine.
> Timebox each scenario to about 15 minutes. Afterwards, compare with `../solutions/answers.md` and fill in the Review table.

## S1. Reports are killing checkout
**Clarify:**


**(a) Why they interfere:**


**(b) Replica vs warehouse:**


**(c) Recommendation (i) today / (ii) in 2 years:**


**Follow-up: numbers don't match:**


## S2. Live dashboards for 300k sellers
**Clarify:**


**(a) Why not OLTP (query rate estimate):**


**(b) Why not the warehouse:**


**(c) Architecture + freshness promise + trade-offs:**


**Follow-up: precompute and cache?:**


## S3. Questions that cross every silo
**Clarify:**


**(a) Why not one query:**


**(b) Data flow (diagram) + ETL or ELT + where clickstream lands:**


**(c) The rename breaks things:**


**(d) System of record vs derived:**


**Follow-up: ticket text for ML:**


## S4. Which price is true?
**(a) Which price is true:**


**(b) How each copy went stale:**


**(c) Update flow + failure handling:**


**(d) Backups? + carts twist:**


**Follow-up: read everything from the DB?:**


## S5. Cloud or own hardware? The maths
**(a) Calculations (show working):**


**(b) Recommendations beyond the numbers:**


**(c) Hybrid for Y:**


**Follow-up: hidden costs:**


## S6. Locked in, and the region is down
**(a) During the outage / designed beforehand / cost:**


**(b) Price tripling: why painful, what would help, what that costs:**


**(c) Multi-cloud for 10 people?:**


**Follow-up: foreign government access:**


## S7. Storage and compute in the cloud
**(a) Postgres on local NVMe:**


**(b) 200 ms write spikes:**


**(c) 80 TB: fixed cluster vs object storage + on-demand compute:**


**(d) Two noisy-neighbour fixes:**


**Follow-up: why Aurora fails over faster:**


## S8. Do we really need to distribute?
**(a) Microservices proposal / Spark proposal:**


**(b) Legitimate reasons + least-distributed fix:**


**(c) Signals it's time to split:**


**Follow-up: single point of failure:**


## S9. The payment timeout
**(a) Possible states:**


**(b) Why not blind retry / why not show an error:**


**(c) Safe retry design:**


**(d) Charged but crashed: recovery:**


**Follow-up: timeout length:**


## S10. Slow checkout and the half-finished order
**(a) Finding the culprit + what every service must do:**


**(b) Why no transaction + 2PC vs saga:**


**Follow-up: merge the two services?:**


## S11. Serverless or not?
**(a) Thumbnails:**


**(b) Video transcoding:**


**(c) Payment API:**


**(d) Admin tool:**


**(e) Weather simulation:**


**Follow-up: no ops work?:**


## S12. Privacy as a design requirement
**(a) Deletion, system by system:**


**(b) Making deletion practical:**


**(c) Pushback + minimization policy:**


**(d) EU residency changes:**


**Follow-up: anonymize instead?:**


---

## Review (fill in after comparing with the model answers)
| Scenario | What I got right | What I missed: reasoning, trade-offs, follow-ups |
|---|---|---|
| S1 | | |
| S2 | | |
| S3 | | |
| S4 | | |
| S5 | | |
| S6 | | |
| S7 | | |
| S8 | | |
| S9 | | |
| S10 | | |
| S11 | | |
| S12 | | |
| MCQs | | |
| B1–B7 | | |
| Design | | |

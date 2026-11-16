# Week 1: My answers to the interview scenarios

> Answer as you would in an interview: **clarify**, then **estimate**, then **options**, then **recommend**, then **what it costs**. Bullet points are fine.
> Timebox each scenario to about 15 minutes. Afterwards, compare with `../solutions/answers.md` and fill in the Review table.

## S1. Sizing the home timeline
**Clarify:**


**(a) Polling: queries/s and lookups/s:**


**(b) Fan-out on write: writes/s average and spike, plus spike plan:**


**(c) Timeline memory estimate and how to hold it:**


**(d) Choice and its cost:**


**Follow-up: push vs polling:**


## S2. Celebrities and other extremes
**(a) What breaks in each case:**


**(b) Hybrid design, threshold, read cost:**


**(c) News junkie, and why not for celebrity followers:**


**(d) The viral user:**


**Follow-up: celebrity follows celebrity:**


## S3. Dashboards say fast, users say slow
**(a) Unseen parts of response time:**


**(b) How the 10 s reports cause it, and the effect's name:**


**(c) Instrumentation and architecture changes:**


**Follow-up: synchronized p99 spikes:**


## S4. Writing the SLOs
**(a) Metrics, percentiles, where, window: (i) payments / (ii) feed:**


**(b) What counts as a valid request:**


**(c) SLA vs SLO:**


**(d) Burn rate, budget left, affordable error rate, action:**


**Follow-up: why not 100%:**


## S5. The percentile dashboard is lying
**(a) Counter-examples: across servers and over time:**


**(b) Raw-data memory estimate:**


**(c) Better pipeline:**


**Follow-up: what to page on:**


## S6. The outage that didn't end
**(a) Why no recovery at 14:05:**


**(b) Client and server mitigations:**


**(c) First fix and why:**


**Follow-up: autoscaling?:**


## S7. Search that waits for every shard
**(a) Slow share with 100 shards and with 20:**


**(b) Three tail-cutting techniques and their trade-offs:**


**Follow-up: cost of hedged requests:**


## S8. How many copies of the photos?
**(a) Failures per day and per year:**


**(b) Loss risk table (2 vs 3 copies, 48 h vs 6 h) and choice:**


**(c) Why too optimistic, plus guards:**


**Follow-up: backups too?:**


## S9. Find the single points of failure
**(a) SPOFs and correlated risks:**


**(b) Fixes in priority order, with cost:**


**(c) Zero-downtime OS patching:**


**Follow-up: safe with multi-AZ?:**


## S10. The config push
**(a) Why not 'be more careful':**


**(b) Five or more postmortem action items:**


**(c) Software vs hardware fault and redundancy:**


**Follow-up: the VP wants discipline:**


## S11. When will the database fall over?
**(a) Months to the limit, now and after scaling up:**


**(b) Options in order, with headroom:**


**(c) When to start designing sharding:**


**Follow-up: microservices to scale?:**


## S12. Choosing a scaling architecture
**(a) Analytics:**


**(b) Chat app:**


**(c) Bank ledger:**


**(d) Two 100 MB/s systems:**


**Follow-up: autoscale everything?:**


## S13. Operability: the automation that made things worse
**(a) Why automation made it worse:**


**(b) Operability features, and why:**


**(c) Automatic vs human-approved, with examples:**


**Follow-up: automate everything?:**


## S14. Simplicity and evolvability
**(a) Essential vs accidental complexity:**


**(b) Reversible migration plan, and the one-way door:**


**(c) Adding multi-currency safely:**


**(d) First boundaries and abstractions:**


**Follow-up: why not rewrite?:**


---

## Review (fill in after comparing with the model answers)
| Scenario | What I got right | What I missed: reasoning, numbers, trade-offs |
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
| S13 | | |
| S14 | | |
| MCQs | | |
| B1–B7 | | |
| Design | | |

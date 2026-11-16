# Week 1 Questions: Defining Nonfunctional Requirements

Questions are scenario-based and test whether you can **apply** the concepts in [../notes.md](../notes.md), the way system design interviews do. Write your answers in [../solved/](../solved/). Don't edit this file.

---

## Part A: Interview scenarios

For each one:
1. Say what you'd **clarify** first.
2. Lay out the **options**.
3. **Recommend** one, and say **what it costs you**.
4. Answer the **follow-up**.

Do the arithmetic where numbers are given. Interviewers expect rough estimates.

---

**S1. Sizing the home timeline**
Your social app has **200M daily users**, with up to **20M online at once**. Users post **500M times a day**, spiking to **150,000 posts/s**. The average user follows 200 accounts. Followers should see new posts within 5 s.
- (a) With fan-out on read and clients polling every 5 s, how many timeline queries and how many post lookups per second would you face?
- (b) With fan-out on write, how many timeline writes per second on average, and at the spike? What do you do during the spike?
- (c) Each user's precomputed timeline keeps the latest 800 post IDs (8 bytes each). How much memory do all the timelines need? How would you hold that?
- (d) Which approach do you choose, and what does it cost you?
- *Follow-up:* "Why push new posts to online clients instead of letting them poll?"

**S2. Celebrities and other extremes**
You chose fan-out on write. Now:
- a pop star with **90M followers** posts 30 times a day
- a "news junkie" account follows **40,000 accounts**
- an unknown user's post goes **viral**, and they gain 5M followers in one day
- (a) What breaks in each case, and why?
- (b) Design the hybrid approach. Where do you set the celebrity threshold, and what does a timeline read cost now?
- (c) How do you handle the news junkie? Why is that answer *not* acceptable for the pop star's followers?
- (d) How does your design cope with the viral user (someone becoming a celebrity mid-day)?
- *Follow-up:* "A celebrity follows another celebrity. Anything special?"

**S3. "Our dashboards say it's fast, users say it's slow"**
Your API's server-side metrics show **p50 = 12 ms and p99 = 40 ms**. Your mobile app's own measurements show **p50 = 180 ms and p99 = 2.5 s** for the same endpoint.
- (a) List every component of the response time the server isn't seeing.
- (b) The servers have 16 cores. Some endpoints occasionally take 10 s (report generation). How could they cause the gap? What's the name of the effect?
- (c) Where would you instrument, and what would you change in the architecture?
- *Follow-up:* "p99 spikes every few minutes, in sync across all instances. Name likely causes."

**S4. Writing the SLOs**
Define SLOs for two services:
- **(i)** a payment authorization API, called by checkout
- **(ii)** a social feed API, called by the mobile app
- (a) For each, which metrics, which percentiles, where measured, and over what window?
- (b) What counts as a "valid request" for the availability target? Do 4xx errors count? Timeouts?
- (c) Your enterprise customers sign an SLA. How do you set the SLA against your internal SLO, and why?
- (d) You're 12 days into a 30-day window with a 99.9% SLO, and the error rate has been 0.15%. What's the burn rate? How much budget is left? What error rate can you afford for the rest of the window? What do you do?
- *Follow-up:* "Why not target 100% availability?"

**S5. The percentile dashboard is lying**
200 API servers each compute a p99 over 1-minute windows. The dashboard then (1) averages the 200 values into a "fleet p99", and (2) averages the 60 per-minute values into an "hourly p99". Traffic is **500,000 requests/s** in total.
- (a) Show with a concrete example why both kinds of averaging can be badly wrong.
- (b) A colleague suggests shipping every raw response time to one server and sorting a 10-minute window. Estimate the memory needed.
- (c) Design a better pipeline. What does each server send? How do you combine across servers and over time?
- *Follow-up:* "Should we page the on-call engineer when the p99 goes over 1 s?" What's better?

**S6. The outage that didn't end**
Incident timeline:
- **14:00** a marketing push doubles traffic for 5 minutes
- **14:02** the API's p99 rises past the clients' 2 s timeout
- **14:05** traffic is back to normal, yet CPU stays at 100% and the success rate is near 0%
- **14:40** someone restarts everything, and it recovers instantly
- (a) Explain exactly why the system didn't recover on its own at 14:05.
- (b) List mitigations on the **client** side and on the **server** side, and explain how each one breaks the cycle.
- (c) Which **one** would you implement first, and why?
- *Follow-up:* "Can't autoscaling just add servers to fix this?"

**S7. Search that waits for every shard**
A search request fans out to **100 shards** in parallel and waits for all of them. Each shard answers in about 20 ms, but 1% of its responses take about 1 s (GC pauses, disk).
- (a) What share of user searches take about 1 s? What if there were 20 shards?
- (b) Give three ways to cut the user-facing tail, with the trade-off of each.
- *Follow-up:* "What do hedged requests cost? When would you *not* use them?"

**S8. How many copies of the photos?**
A photo-storage service runs **50,000 disks** with a **3% annual failure rate**. Re-copying a failed disk's data takes **48 h** today, or **6 h** with faster re-replication.
- (a) How many disk failures should you expect per day, and per year?
- (b) For 2 copies and 3 copies, at both 48 h and 6 h, estimate the chance that a given disk failure leads to data loss, and the expected data-loss events per year. Which setup do you pick?
- (c) Why are these numbers too optimistic? Give two concrete correlated-failure scenarios and how you'd guard against them.
- *Follow-up:* "We have 3 replicas. Do we still need backups?"

**S9. Find the single points of failure**
Architecture:
- DNS points to **1 load balancer VM**
- **8 stateless API servers** in one availability zone
- **1 Postgres primary** plus 1 asynchronous replica in the same zone, with promotion done by hand
- **1 Redis** for sessions
- **1 cron server** that runs billing at midnight
- every deploy goes to all servers at once
- (a) List every SPOF and every correlated risk.
- (b) Propose fixes in priority order, with the cost of each.
- (c) How would you patch the OS on every machine with **zero downtime**?
- *Follow-up:* "We'll be multi-AZ after this. Are we safe now?"

**S10. The config push**
A config change with a typo in a feature-flag rule was pushed to every server at 09:00 and crashed them all. It took 35 minutes to find and revert. The engineer who pushed it followed the documented process.
- (a) Why is "the engineer should have been more careful" the wrong conclusion?
- (b) Write the action items for the postmortem: at least five, technical and organizational.
- (c) How does this incident differ from a hardware fault, in terms of how redundancy helps?
- *Follow-up:* A VP wants the engineer disciplined. What do you say?

**S11. When will the database fall over?**
A B2B SaaS serves **3,000 requests/s**. Its single Postgres is at **70% CPU**, and latency degrades badly above 80%. Load grows **10% a month**. The next instance size doubles the capacity.
- (a) How many months until you hit 80% CPU? And after scaling up once?
- (b) List your options in the order you'd use them, and estimate how much headroom each one buys.
- (c) When must sharding *design* start, and why that early?
- *Follow-up:* "Should we split into microservices so we can scale?"

**S12. Choosing a scaling architecture**
Pick shared-memory (scale up), shared-disk, or shared-nothing (scale out) for each, and justify:
- (a) internal analytics on 5 TB, growing slowly, used by 20 analysts
- (b) a chat app for 50M users across Asia and Europe
- (c) a bank's core ledger: 2 TB, strict consistency, 5,000 transactions/s
- (d) Two systems both move **100 MB/s**. One serves 100,000 requests/s of 1 kB each; the other takes 3 uploads a minute of 2 GB each. How would their designs differ?
- *Follow-up:* "Shouldn't everything just autoscale?"

**S13. Operability: the automation that made things worse**
Your managed-database team automated everything: failover, scaling, and disk replacement. During a partial network partition, the automation **failed the primary over 14 times in 30 minutes**. Each failover dropped connections, and the on-call engineer couldn't tell what the automation was doing or how to stop it.
- (a) Why did automation make *this* incident worse than a manual process would have?
- (b) Redesign it for operability. List the specific features you'd add, and why each one helps operators.
- (c) Where would you draw the line between automatic and human-approved actions? Give concrete examples of each.
- *Follow-up:* "Isn't the goal of SRE to automate everything?"

**S14. Simplicity and evolvability: changing a system you're afraid to touch**
A 7-year-old order-management monolith (a "big ball of mud") stores everything in MongoDB. Every change breaks something unrelated, releases are monthly, and two of the original authors have left. The business now needs **multi-currency pricing** and wants to move to **Postgres** for transactions and reporting.
- (a) What makes this system hard to change? Separate the essential complexity from the accidental.
- (b) Plan the Postgres migration so that **every step is reversible except the last**. What's the one-way door, and when do you walk through it?
- (c) How do you add multi-currency pricing **safely** before the code is cleaned up?
- (d) Which abstractions or boundaries would you introduce first, and why there?
- *Follow-up:* "Why not just rewrite the whole thing from scratch?"

---

## Part B: Hands-on (Python)

Write your code in `../solved/code/`. Stub files with the exact function names are already there.
Run the tests from the week folder: `python3 solved/code/test_week01.py`

### B1. Home timelines: pull vs push vs hybrid (`fanout.py`)
*Concept: fan-out, materialized views, the celebrity problem (§2).*

Implement three strategies with the same interface: `post(user, post_id, ts)` and `home_timeline(user, limit=20)`, which returns post IDs newest first. Each strategy counts `writes` and `reads`, which is the "work" the case study talks about.
1. `followers_of(follows)`: invert the follow graph
2. `PullTimeline`: store each post once, and merge the followees' posts on read
3. `PushTimeline`: insert each post into every follower's timeline
4. `HybridTimeline(follows, celebrity_threshold)`: push for normal users. Celebrity posts are stored once and merged in at read time.
5. In `__main__`:
   - print the book's numbers (400M lookups/s vs 1.16M writes/s)
   - run all three strategies on the given `build_follow_graph()` and `run_workload()`
   - compare their total work

**Answer in a comment:** which strategy did the least work, and when would the answer change?

### B2. Percentiles and tail latency (`percentiles.py`)
*Concepts: percentiles, tail amplification, "don't average percentiles, add histograms" (§5, §7, §8).*
1. `percentile` (nearest-rank), `summarize` (mean, p50, p95, p99, p999, max), `tail_amplification`
2. `average_of_percentiles`: the *wrong* way, built so you can see how wrong it is
3. `Histogram(precision)`:
   - log-sized buckets (how HdrHistogram and DDSketch work)
   - `record`, `merge` (adds counts), and `percentile` (accurate to within `precision`)
4. In `__main__`: two servers, one with 5% very slow requests. Compare the average of their p99s, the true p99, and the merged-histogram p99.

### B3. Queueing and metastable failure (`overload.py`)
*Concepts: queueing delay, retry storms, metastable failure, load shedding (§3).*
1. `simulate_queue(utilization)`: a single-server queue. Watch the mean and p99 response time explode as utilization approaches 100%.
2. `simulate_retry_storm(...)`: a tick-based server with clients that time out and retry. See the docstring for the exact rules. Show that:
   - **with retries**, a 10-tick spike causes an outage that **never ends**
   - **without retries**, it drains slowly
   - **with load shedding**, it recovers quickly

**Answer in a comment:** why does the default case never recover?

### B4. Reliability maths (`reliability.py`)
*Concepts: hardware fault rates, redundancy, SPOFs, SLO error budgets (§7, §9, §10).*
- Expected failures per day
- Availability in series and in parallel
- The chance of losing data after one disk failure, with N copies and a repair window
- Error budgets and burn rate

**Answer in a comment:** which assumption makes all these numbers too optimistic?

### B5. Capacity planning (`capacity.py`)
*Concepts: understanding load, linear scalability, "no magic scaling sauce" (§15, §16).*
- `months_until_limit`
- `nodes_needed` (target utilization plus a spare node)
- `scaling_efficiency` and `classify_scaling`
- `data_rate_mb_per_s`

### B6. (Stretch, no tests) Fault injection (`chaos.py`)
*Concepts: chaos engineering; independent vs correlated faults (§9, §11).*
Three replicas with a "chaos monkey" that kills each one 10% of the time. Compare:
1. no failover
2. failover
3. failover, plus a bug that hits *every* replica on 1% of requests

Explain the results.

### B7. Reversible database migration (`migration.py`)
*Concepts: evolvability, irreversibility (§17).*

`MigratingStore(old, new)` moves through the phases `old_only → dual_write → shadow_read → new_primary → new_only`:
- implement `put`, `delete`, and `get` (each routes to the right store for the current phase)
- implement an idempotent `backfill`
- `advance()` **refuses to cut over** while shadow reads disagree
- `rollback()` works in every phase **except** `new_only`, which is the one irreversible step

The docstring gives the exact routing rules.

**Answer in a comment:** why does dual-writing keep the migration reversible?

---

## Part C: Design problem (full interview round, 45 minutes)

**"Design the home timeline for a Twitter/X-style social network."**
**Scale:**
- 200M daily users, 20M online at peak
- 500M posts a day, spiking to 150k/s
- 200 follows on average, up to 100M followers for celebrities
- a large company with many engineering teams

Spend 30 minutes on your own attempt **before** watching any video. Then answer the follow-ups out loud.
1. **Requirements:** list the functional requirements, and then the **nonfunctional** ones as concrete SLOs: timeline load latency (p50/p99), post-delivery delay, availability, and durability of posts.
2. **Estimates:** posts/s, timeline reads/s, fan-out writes/s (average and peak), and timeline cache memory.
3. **Data model:** what's the system of record, and what's derived?
4. **Write path:** posting, fan-out workers, queues, the celebrity hybrid, and sampling for heavy followers.
5. **Read path:** serving a timeline (cache plus merging celebrity posts), and pushing new posts to online clients.
6. **Fault tolerance:**
   - a fan-out worker crashes mid-delivery: how do you avoid both missing and duplicating posts?
   - the timeline cache loses a node
   - a whole availability zone goes down
7. **Overload protection:** what happens when a celebrity posts during a World Cup final? Cover backoff, load shedding, backpressure, and queue limits.
8. **Observability:** which metrics, which percentiles, and where they're measured.
9. **Evolution:** what changes when you reach 10× the users?
10. **Maintainability:** what makes this system operable (runbooks, overrides, dashboards), simple (which abstractions), and evolvable? Example: how would you switch from chronological to ranked timelines without a risky big-bang change?

**Interviewer follow-ups** (answer each in 2–3 sentences):
- F1. "A user deletes a post. How does it disappear from 50M timelines?"
- F2. "Timelines need ranking, not just chronological order. What changes?"
- F3. "The timeline cache cluster restarts cold. What happens to the database, and how do you protect it?"
- F4. "Why not compute everything on read with a really fast database?"

Write it in [../solved/design.md](../solved/design.md).

# Week 1: Model answers to the interview scenarios

> Only open this after writing your own answers in `../solved/answers.md`.
> These are *strong* answers, not the only answers. Compare your **reasoning**: did you clarify, estimate, weigh the options, commit to a recommendation, and name its cost?
> Reference code: [code/](code/). It passes all tests: `WEEK_IMPL=solutions python3 solved/code/test_week01.py`

---

## S1. Sizing the home timeline
**Clarify:**
- Is the timeline chronological or ranked?
- How many posts does a timeline hold?
- What's the read:post ratio?
- Is "within 5 s" the p99, or the median?

**(a) Fan-out on read with polling.**
- 20M online ÷ 5 s = **4M timeline queries/s**.
- × 200 followed accounts = **800M post-list lookups/s**, plus the merge-sort for each query.
- And that's the *average* user. People following 10k+ accounts are far worse.

**(b) Fan-out on write.**
- 500M ÷ 86,400 ≈ **5,800 posts/s**, × 200 followers ≈ **1.16M timeline writes/s** on average.
- At the spike: 150k × 200 = **30M writes/s**. Don't try to do those in real time.
  - **Enqueue** the deliveries (e.g. in Kafka, partitioned by follower) and let workers drain the queue.
  - Delivery lag rises from about 1 s to maybe tens of seconds, but **timeline reads stay fast**, because they're served from the precomputed cache.
  - Prioritize delivery to **online** users. Offline users can be filled in lazily when they log in.

**(c) Memory:** 200M users × 800 IDs × 8 B ≈ **1.28 TB**, IDs only (the post bodies live elsewhere).
- That's about 20 nodes with 64 GB of RAM each, or **~40 with 2× replication** for fault tolerance: a Redis/Memcached-style cluster sharded by user ID.
- **Optimization:** materialize timelines only for *active* users (say the last 30 days). Rebuild inactive ones on demand.

**(d) Recommendation:** **fan-out on write, with the hybrid for celebrities** (S2).
- **Why:** reads vastly outnumber posts, and 1.16M cheap writes/s beats 800M lookups/s by about 700×.
- **What it costs:**
  - write amplification and a big cache cluster to run
  - delivery delay during spikes
  - complexity: the queues, the workers, and keeping derived timelines consistent with the posts (deletes!)

**Follow-up: push vs polling.**
- Polling does the work **even when nothing changed**. With 20M clients that's 4M requests/s just to say "nothing new".
- Pushing (WebSocket or SSE subscriptions to the user's timeline stream) sends data **only when there's a new post**, and delivers it faster.
- The cost: millions of long-lived connections to manage. But an idle connection is far cheaper than a constant stream of poll queries.

---

## S2. Celebrities and other extremes
**(a) What breaks:**
- **Pop star:** each post means **90M timeline writes**, and 30 posts a day is 2.7B writes. A single post takes minutes or hours to fan out, delaying everyone else's deliveries behind it in the queue.
- **News junkie:** ~40k accounts × their posting rates means **thousands of writes a minute** into one timeline: a hot key in the cache and wasted work, since nobody reads that much.
- **Viral user:** they were a "normal" user, so the system fans out to **5M followers** they didn't have this morning. Their follower count crosses any celebrity threshold mid-day.

**(b) The hybrid:**
- **Celebrity:** a follower count above a threshold, **e.g. ~100k–1M**. Tune it from measurements: the cost of fan-out vs the cost of extra reads.
- Celebrity posts are written **once**, to a per-celebrity recent-posts list (heavily cached, since everyone reads it).
- **Timeline read** = the user's materialized timeline **+** recent posts from each followed celebrity, **merged by timestamp**.
- **Read cost:** 1 cache read + k extra reads (k = celebrities followed, usually a handful), then a small merge.
  - Mitigation: cache the merged result for a few seconds, and cap k by grouping celebrity lists.

**(c) The news junkie:** **sample or drop writes** into their timeline. Keep the most recent N per followed account, or a random sample. They can't read it all anyway.
- **Not acceptable for celebrity followers:** each follower follows just one or a few celebrities and **expects to see every post** from them. Dropping posts would be a correctness bug, not a harmless trade-off.

**(d) The viral user:**
- Recompute "is a celebrity" **dynamically**: follower count, or **fan-out cost per post**.
- Once above the threshold, **new posts** take the celebrity path. Posts already fanned out stay where they are.
- Add **rate limiting on fan-out work per author**: if one author's fan-out is flooding the queue, switch them to the celebrity path automatically.
- Hysteresis (different up and down thresholds) stops accounts flapping back and forth.

**Follow-up: a celebrity following a celebrity.** Nothing new:
- The follower side is just a user whose timeline read merges in celebrity lists.
- The *posting* side is handled by the author's own celebrity status.
- One edge: a celebrity who also follows *many* accounts has a heavy read-time merge, which is solved by caching their merged timeline.

---

## S3. "Our dashboards say it's fast, users say it's slow"
**(a) Parts of response time the server doesn't see:**
- DNS lookup, TCP and TLS handshakes, especially on mobile networks
- **network latency** both ways, plus retransmissions after packet loss (common on mobile)
- **queueing before the measured part starts:**
  - at the load balancer
  - in the kernel's accept and socket buffers
  - in the server's request queue, waiting for a free thread or worker
- queueing on the way out (outbound buffers)
- client-side time: app processing, JSON parsing, and retries the app makes on errors

**(b) Head-of-line blocking:**
- With 16 cores (or 16 workers), a few 10-second report requests can **occupy several workers**.
- Fast requests then **wait in the queue behind them**. Their service time is still 12 ms, so the server's metrics look perfect, but the client waited seconds.

**(c) Instrumentation:**
- Measure **client-side** response time (real user monitoring in the app) **and** queue wait time on the server: record when a request is *received*, not just when processing *starts*.
- Track a "time in queue" metric, and the load balancer's own latency.
- **Architecture fixes:**
  - isolate slow endpoints: **separate worker pools or queues**, or move reports to an **async job** (return 202, then a download link)
  - per-endpoint concurrency limits
  - timeouts
  - keep utilization well below 100% (queueing grows sharply near capacity)

**Follow-up: periodic p99 spikes in sync across instances.** The likely causes are things on a shared schedule, or shared dependencies:
- **garbage-collection** pauses (often in sync, triggered by the same traffic pattern)
- cron jobs or batch jobs running on the hosts or the database
- cache expiries at the same TTL (a stampede)
- the database's checkpoint, vacuum, or compaction
- a shared dependency's periodic hiccup, e.g. a config or token refresh
- the noisy neighbour's schedule on the cloud host

---

## S4. Writing the SLOs
**(a) Metrics:**

| | (i) Payment authorization API | (ii) Social feed API |
|---|---|---|
| Latency | **p50 < 150 ms, p99 < 800 ms, p99.9 < 2 s**, measured at the *calling service* (checkout), over a rolling 30 days, plus a 5-minute view for alerting | **p50 < 200 ms, p99 < 1 s**, measured **in the app** (real user monitoring) and at the edge |
| Availability | **99.95–99.99%** of valid requests succeed. Money is involved, and every failure loses a sale. | **99.9%**. A failed refresh is annoying but recoverable (show the cached feed). |
| Extra | **Correctness:** zero double charges. Reconciliation mismatches are counted separately. | **Freshness:** 99% of posts delivered to online followers within 5 s |

The percentiles differ because users wait synchronously at checkout, and the slow tail at checkout often belongs to the biggest baskets.

**(b) What counts as "valid":**
- **Count** 5xx errors, timeouts (from the *client's* perspective), and dropped connections as failures.
- **Exclude** client errors (4xx such as bad input or auth failures) from the *denominator*, since they're the user's fault. **But** watch for 4xx spikes caused by *your* bugs, e.g. a deploy that wrongly rejects valid tokens. Track 4xx rates separately.
- A **card declined by the bank** is a *successful* response.

**(c) SLA vs SLO:** the **SLA is looser than the internal SLO**, e.g. SLA 99.9% with a 10% credit, against an internal SLO of 99.95%. The gap is a **safety margin**: you notice and react when you breach the SLO, *before* it costs money and reputation. Define in the SLA exactly how it's measured (which requests, what window, who measures it), because ambiguity there turns into disputes.

**(d) The error budget:**
- The budget is **0.1%** of requests. You're running at **0.15%**, so the **burn rate is 1.5×**.
- 12 days at 1.5× used **18 days' worth** of budget, leaving **12 days' worth** (40%) for the remaining **18 days**.
- To end on budget, the error rate must average **≤ 0.067%** for the rest of the window.
- **Action:**
  - investigate what's driving the extra errors
  - **slow down risky releases**, adding canaries and extra review
  - put reliability fixes ahead of features until the burn rate is below 1×
  - set up **burn-rate alerts**, e.g. page if the 1-hour burn rate is above 14× or the 6-hour rate above 6×

**Follow-up: why not 100%?**
- It's **impossible**: networks, clients, and dependencies all fail.
- It's **extremely expensive**, since each extra nine costs roughly 10× more.
- It **freezes change**: with no error budget, every deploy is a risk you can't afford.
- And users can't tell 99.99% from 100%, because their own Wi-Fi and phones fail more often than that.

The error budget is what makes it **safe to ship**: spend it on deploys and experiments.

---

## S5. The percentile dashboard is lying
**(a) Why averaging fails:**
- **Across servers:**
  - 199 servers have p99 = 50 ms; 1 server (a bad host) has p99 = 5 s and handles 0.5% of traffic.
  - Average of p99s = (199 × 50 + 5,000) ÷ 200 ≈ **75 ms**.
  - The true fleet p99 depends on how many slow requests there are in total. Here it's probably still around 50 ms, with the problem showing up at p99.5.
  - Or the reverse: one *busy* slow server can drag the true p99 far above the average. **Averages ignore request counts.**
- **Over time:** 59 quiet minutes at 50 ms, plus 1 minute of an outage at a p99 of 10 s that carried 30% of the hour's traffic. Averaging the 60 minutes gives ≈ **215 ms**, but the true hourly p99 is about **10 s**.
- **Bottom line:** percentiles are **not additive**, so you can't average or sum them.

**(b) Shipping raw response times:** 500k/s × 600 s = 300M values × 8 B ≈ **2.4 GB** per 10-minute window, re-sorted every minute. That's feasible but wasteful: network-heavy, CPU-heavy, and fragile.

**(c) A better pipeline:**
- Each server keeps a **mergeable histogram or sketch** (HdrHistogram, DDSketch, t-digest) per endpoint per 10 s or 1 minute: a few KB.
- Servers ship sketches, not raw values. The aggregator **merges them** by adding bucket counts across servers and over time, then reads any percentile from the merged sketch, with a known error (e.g. 1%).
- Store the sketches, so you can **re-aggregate** later: per hour, per region, per endpoint.
- Also keep the **request counts** and **error counts** per window, for availability.

**Follow-up: paging on "p99 > 1 s".**
- Raw percentile thresholds are noisy: they flap on low traffic and trigger at night when 10 requests decide the p99.
- Better: alert on **SLO burn rate**, the fraction of requests slower than the latency target (e.g. "more than 1% of requests over 1 s") or failing, over **two windows** (short and long).
- That pages only when the **error budget** is actually being burned fast. The p99 graph stays as a diagnostic tool.

---

## S6. The outage that didn't end
**(a) Why it didn't recover:**
1. The spike filled the queue, so waiting times went past the **2 s client timeout**.
2. Clients timed out and **retried**, while the server kept working on the abandoned originals: **wasted capacity**.
3. Every new request now waited behind a backlog of dead requests, so it **also timed out**, which produced **more retries**.
4. At 14:05, real demand was normal, but **effective load = real requests + retries**, and that was still above capacity. The server spent 100% of its CPU on answers nobody was waiting for, so the success rate was about 0%.

That's a **retry storm** causing a **metastable failure**: a self-sustaining state that needs an external reset. The restart cleared the queue of dead requests.

**(b) Mitigations:**

| Side | Mitigation | How it breaks the cycle |
|---|---|---|
| Client | **Exponential backoff with jitter** | Retries spread out and slow down instead of piling in |
| Client | **Retry budget**, e.g. retries ≤ 10% of requests | Caps the extra load |
| Client | **Circuit breaker** | Stops calling a failing service for a while, giving it room to drain |
| Server | **Deadline propagation**: drop requests whose client deadline has passed | Stops wasting capacity on abandoned work (see B3) |
| Server | **Load shedding**: reject early, with a quick 503, when the queue is too deep or the work too old | Cheap rejections instead of expensive timeouts |
| Server | **Backpressure**: 429 with Retry-After | Tells well-behaved clients to slow down |
| Server | Bounded queues, maybe **LIFO** under overload | Serves fresh requests that still have a waiting client first |
| Both | Capacity headroom, and autoscaling triggered **early** | Keeps you out of the steep part of the queueing curve |

**(c) First fix:** **server-side load shedding with deadline-aware queueing.** It protects the service **whatever the clients do**: you don't control every client, and old app versions retry aggressively. Close behind: client backoff with jitter plus retry budgets in your SDK.

**Follow-up: autoscaling.** It might help, but it's not a fix:
- new instances take minutes to start, while the storm builds in seconds
- the retry multiplier can grow faster than you can add capacity
- the bottleneck is often **downstream** (the database), where more API servers just add more load
- autoscaling on CPU can be fooled when the CPU is busy doing wasted work

Fix the feedback loop first. Autoscaling is a supplement.

---

## S7. Search that waits for every shard
**(a)** With 100 shards: 1 − 0.99¹⁰⁰ ≈ **63%** of searches take about 1 s, so the shards' **p99 becomes the users' median**. With 20 shards: 1 − 0.99²⁰ ≈ **18%**.

**(b) Three ways to cut the tail:**
1. **Hedged requests:** if a shard hasn't answered by its ~p95 (say 30 ms), send the same request to a **replica** and use whichever answers first. This cuts the tail sharply, at the cost of a few % extra load.
2. **Partial results with a deadline:** return at 100 ms with whatever shards have answered, and mark the result "approximate". The tail is capped, at the cost of **completeness**, which is acceptable for search but not for a bank balance.
3. **Reduce fan-out:** fewer, bigger shards, or route queries only to the relevant shards (e.g. by language or region), so fewer calls each have a chance to be slow. The cost: bigger shards are slower per query, and rebalancing is harder.

Others:
- fix the **sources of the tail**: GC tuning, avoiding disk reads by keeping hot data in memory, isolating background compaction
- **tied requests**: send to two replicas, and cancel the second when the first starts processing

**Follow-up: cost of hedging.**
- It adds load (usually a few %, if you hedge only after the p95).
- It can amplify an overload: if *every* shard is slow because the system is overloaded, hedging doubles the load exactly when that hurts most.
- **Don't** hedge **non-idempotent** requests (writes), and **disable** hedging when the cluster is overloaded.

---

## S8. How many copies of the photos?
**(a)** 50,000 × 3% = **1,500 failures a year ≈ 4.1 a day**. Disk replacement is a daily routine, not an incident.

**(b) Data-loss risk.** The chance that one surviving disk also fails during the repair window is 0.03 × h ÷ 8,760.

| Copies | Repair 48 h | Repair 6 h |
|---|---|---|
| **2** | P = 1.6×10⁻⁴ per failure, so 1,500 × P ≈ **0.25 loss events a year** (about one every 4 years) | 2×10⁻⁵, about **0.03 a year** (one per ~30 years) |
| **3** | P = (1.6×10⁻⁴)² = 2.7×10⁻⁸, about **4×10⁻⁵ a year** | about **6×10⁻⁷ a year** |

**Pick 3 copies, in different availability zones, with fast re-replication.**
- 2 copies loses someone's photos every few years, which is unacceptable for irreplaceable data.
- Faster repair helps a lot, because it shrinks the window of vulnerability.
- **Cost:** 1.5× the storage of 2 copies. (Or use erasure coding to get similar durability with about 1.4× overhead, at a CPU and repair-complexity cost.)

**(c) Why these numbers are too optimistic.** They assume **independent** failures:
- **The same batch or model of disk** failing together (the 32,768-hour firmware bug). *Guard:* mix vendors and batches, and stagger installation dates.
- **The same rack, power, or zone:** a power or cooling failure kills many disks at once. *Guard:* place replicas in **different availability zones**.
- **A software bug** that corrupts or deletes data on **all replicas**, since replication faithfully copies the bug's writes.
- **Repair storms:** re-replicating after a big failure overloads the remaining disks, so more of them fail.

**Follow-up: do we still need backups?** **Yes.** Replication protects against **hardware loss**, but it **copies deletions and corruption instantly** to every replica: a bug, a bad migration, ransomware, an operator's `DELETE`. Backups or snapshots give you **point-in-time recovery**. Keep them immutable and separate, ideally in another account or region, and **test restores** regularly.

---

## S9. Find the single points of failure
**(a) SPOFs and correlated risks:**
- **SPOFs:**
  - the **single load balancer VM**
  - the **Postgres primary**, since manual promotion means an outage of perhaps an hour
  - **Redis for sessions**: if it's lost, every user is logged out, or logins break entirely
  - the **cron server**: no billing, silently
- **Correlated risks:**
  - everything is in **one availability zone**, so one zone outage takes it all
  - the **all-at-once deploy** means one bad build or config kills all 8 servers
  - the replica in the same zone dies along with the primary
  - DNS with a long TTL slows failover

**(b) Fixes, in priority order:**
1. **Gradual deploys** (canary) plus fast rollback. *Cheap*, and it covers the most common cause of outages (software and config changes).
2. **A managed or redundant load balancer** (a cloud load balancer, or 2 VMs with a floating IP). *Low cost.*
3. **Postgres high availability:** a synchronous (or semi-synchronous) standby in **another zone**, with **automatic failover** (managed database, Patroni). *Moderate:* one more instance, plus testing.
4. **App servers spread across 2–3 zones.** *Low:* they're stateless.
5. **Sessions:** a replicated Redis with failover, or stateless signed tokens (JWT) so losing Redis doesn't log everyone out. *Low to moderate.*
6. **Cron:** run it on a scheduler with leader election, or 2 nodes with a lock, and make the **billing job idempotent and monitored** ("did it run?" alerts). *Low.*
7. **Backups, with tested restores** (see S8).

**(c) Zero-downtime OS patching:** a **rolling upgrade**.
- **API servers:** drain one at a time (the load balancer stops sending it new requests, and in-flight ones finish), patch, reboot, health-check, put it back. Keep enough capacity to run with N−1.
- **Database:** patch the **standby** first, fail over to it (a planned switchover takes seconds), then patch the old primary.

**Follow-up: are we safe with multi-AZ?** Safer, but **not safe**:
- **multi-AZ doesn't protect** against software bugs and bad config deployed everywhere, region-wide outages, a broken shared dependency (DNS, auth provider, the cloud's own control plane), data corruption replicated across zones, or overload and retry storms
- untested failover often fails when it's actually needed, so run **game days and chaos tests**

---

## S10. The config push
**(a) Why "be more careful" is wrong:**
- The engineer **followed the documented process**, so the *process* allowed a typo to take down every server.
- Humans *will* make typos. "Be careful" doesn't change the probability, and blame makes people **hide mistakes**, which destroys the information you need to improve.
- The real causes:
  - **no validation** of the config
  - **no gradual rollout**
  - **no fast automatic rollback**
  - **35 minutes to diagnose**, which is an observability problem

**(b) Action items:**
1. **Validate configs before deploying:** schema checks, plus a test that runs the flag rules against sample inputs (property-based tests over random inputs).
2. **Roll out configs like code:** canary first (1% of servers or one zone), automatic health checks, then gradual expansion.
3. **Automatic rollback** when the error rate or crash rate rises after a change, plus a **one-click revert** for config changes.
4. **Crash isolation:** a bad flag rule should fall back to the **last known good config**, or a default, not crash the process.
5. **Observability:** annotate dashboards with deploys and config changes, so "what changed at 09:00?" takes seconds, not 35 minutes.
6. **Run the blameless postmortem** and share it widely, then track the action items to completion with owners and dates.
7. **Organizational:** give reliability work real priority. If the team asked for config validation months ago and it lost to features, write that down and escalate it.

**(c) How it differs from a hardware fault:**
- A hardware fault hits **one** machine **independently**, so **redundancy** absorbs it.
- A software or config fault is **correlated**: every replica runs the same config, so **all of them fail together**, and more replicas don't help at all.
- The defences are different: **diversity in time** (gradual rollout), validation, and fast rollback.

**Follow-up: the VP wants discipline.**
- Punishing someone for following the process teaches everyone to hide incidents and avoid touching production, so reliability gets *worse*.
- The process failed: the organization didn't fund validation or canaries. Fix those, and you protect against *every* future typo, from anyone.
- Offer the postmortem's action items and their owners as the accountability the VP is looking for.

---

## S11. When will the database fall over?
**(a) Months to the limit:**
- The 80% CPU limit ≈ 3,000 × 80 ÷ 70 ≈ **3,430 requests/s**.
- At 10% a month: log(3,430 ÷ 3,000) ÷ log(1.1) ≈ **1.4 months**. You'll hit it in about **6 weeks**. **This is urgent.**
- **After doubling the instance:** a limit of about 6,860, and log(6,860 ÷ 3,000) ÷ log(1.1) ≈ **8.7 months** from now.

**(b) Options, in the order you'd use them:**
1. **Find the expensive queries:** slow-query log, missing indexes, N+1 queries. Often frees **20–50%** of CPU, in days, very cheaply. Do it now.
2. **Scale up** to the next instance size: **about 7 more months** of headroom. Fast, but cost grows faster than capacity and there's a ceiling.
3. **Read replicas** for read-heavy endpoints, if reads are the majority: maybe **2–3× read capacity**. The cost is **replication lag**, so read-your-writes needs care (Week 9).
4. **Caching** hot reads (Redis): cuts the database load from reads a lot, if the hit rate is high. The cost: invalidation complexity (Week 0, S4).
5. **Move work off the request path:** queues, batch reports into a warehouse.
6. **Sharding** (Week 11): headroom that scales with the number of shards. The cost: high complexity, cross-shard queries, rebalancing. That's why it comes **last**.

**(c) When sharding design must start:**
- **Now, in parallel.** Steps 1–4 buy roughly 12–18 months, and growth compounds: 10% a month is about **3× a year**.
- Sharding means picking a shard key, changing the data model and queries, migrating data with zero downtime, and testing. That takes **months**.
- Planning one order of magnitude ahead is exactly this case: you're about 1–1.5 years from 10× the load.

**Follow-up: microservices to scale?**
- **Not for this problem.** The bottleneck is **one database's capacity**. Splitting the code into services doesn't reduce queries. It adds network calls, and the services would still share, or have to split, the data.
- Microservices solve **team coordination**.
- Scaling a data bottleneck needs **data-level** techniques: query tuning, caching, replicas, sharding, or splitting data by domain *if* it separates cleanly. That last one can coincide with service boundaries, but the scaling comes from the data split, not from the services.

---

## S12. Choosing a scaling architecture
**(a) Internal analytics, 5 TB, growing slowly:**
- **Scale up**, a single node: one big machine (lots of RAM, NVMe) with a columnar engine (DuckDB or ClickHouse), or a managed warehouse.
- 5 TB fits comfortably on a node, there are only 20 users, and it's simple.
- Shared-disk was the traditional on-prem warehouse answer, but locking and contention limit it. Today's cloud warehouses use separate storage and compute, which looks like shared-disk but with a purpose-built storage API.

**(b) Chat for 50M users across Asia and Europe:** **shared-nothing**, scale out.
- A huge number of concurrent connections, data that's naturally **partitioned** by user or conversation, the need to survive a zone or region failure, and servers **near users** for latency.
- The cost: sharding, replication, and the complexity of distributed systems.

**(c) A bank's core ledger, 2 TB, strict consistency, 5,000 transactions/s:**
- **Scale up first**, with high availability. A powerful primary database (one node gives strong consistency and real transactions) plus synchronous standbys in other zones.
- 2 TB and 5,000 transactions/s fit on one modern machine.
- Distributing it means **distributed transactions or consensus** (Ch8, Ch10), which adds latency and risk.
- Go shared-nothing only when you outgrow the biggest machine, e.g. by sharding accounts, or with a distributed SQL database built for this.

**(d) The same 100 MB/s, two very different designs:**
- **100k requests/s × 1 kB:** bound by CPU per request, connections, and lock contention.
  - needs many cores and nodes, connection pooling, efficient serialization, caching
  - a stateless tier scaled out horizontally, and a database that can handle 100k operations/s
- **3 uploads/min × 2 GB:** bound by **streaming bandwidth and durability**.
  - stream the data straight to object storage (resumable, chunked uploads)
  - checksums, long timeouts, and background processing jobs
  - request rate is trivial, so you hardly need a database
- **Same throughput, different architecture: there's no magic scaling sauce.**

**Follow-up: "everything should autoscale?"**
- **No.** With **predictable** load, scaling by hand (or on a schedule) gives **fewer operational surprises**.
- Autoscaling reacts with lag, can oscillate, can be triggered by wasted work (S6), and has trouble with **stateful** systems: you can't add a database replica or rebalance shards in seconds.
- Use it for **stateless, bursty** tiers.
- Plan capacity for **stateful** systems deliberately.

---

## S13. Operability: the automation that made things worse
**(a) Why automation made it worse.**
- **It was designed for clean failures**, like a dead primary. A *partial* partition is an edge case: the primary is alive but unreachable from some places, so health checks flip back and forth, and the automation acts on every flip.
- **It acted fast and repeatedly**, so a human would have caused 1 failover where the automation caused 14, each one dropping connections. It **amplified** the fault.
- **It was opaque.** The operator couldn't see *why* it was acting, or how to stop it.
- That's the chapter's point: **automated systems that go wrong are harder to troubleshoot**, and the leftover cases are the hardest ones.

**(b) Redesigning for operability:**
1. **Damping:** a minimum interval between failovers (e.g. at most 1 per 15 minutes) and **flap detection**. If a second failover is needed soon after the first, **stop and page a human** instead.
2. **A big red button:** a clearly documented way to **pause** the automation and take **manual control** of which node is primary.
3. **Visibility:** an event log of every automated decision with its *reason* ("primary missed 3 health checks from zone b"), shown on the dashboard.
4. **A clear operational model:** a runbook saying "if the automation does X, here's why, and here's what to do".
5. **Better failure detection:** require agreement from multiple observers or zones before declaring the primary dead (quorum-based, Week 16), so one partition can't trigger a failover.
6. **Predictable defaults that can be overridden:** conservative timeouts by default, adjustable per cluster.
7. **Game days:** practise partial partitions on purpose (fault injection), so both the automation and the people have rehearsed it.

**(c) Automatic vs human-approved:**
- **Automatic:** frequent, well-understood, and **reversible**, with a small blast radius.
  - restarting a crashed process
  - replacing a failed disk and re-replicating its data
  - a single failover when the primary is clearly dead
  - scaling a stateless tier
- **Human-approved:** rare, ambiguous, **irreversible**, or with a big blast radius.
  - a second failover within the damping window
  - promoting a replica that might be missing data (risking lost writes)
  - deleting data
  - failing over a whole region
- **Rule of thumb:** automate the **routine**, and make the rare cases **easy for humans** rather than trying to automate them blindly.

**Follow-up: "automate everything"?**
- SRE aims to **eliminate toil**, the repetitive manual work, not human judgement.
- Automate repeatable tasks, but keep humans for ambiguous situations, and give them **observability and override controls**.
- Automation without those turns operators into spectators during the worst incidents. The sweet spot depends on the system and the team.

---

## S14. Simplicity and evolvability: changing a system you're afraid to touch
**(a) What makes it hard to change:**
- **Essential complexity:** billing and order rules, taxes, discounts, regulatory requirements. They're inherent in the domain, and multi-currency adds more of them.
- **Accidental complexity:**
  - **tight coupling:** modules reach into each other's data, so every change has hidden effects
  - **no clear boundaries or abstractions** (the big ball of mud)
  - **few tests**, so nobody knows what a change breaks
  - **lost knowledge** as authors left
  - **monthly releases**: big, risky batches
  - a schemaless store where every document shape is "in the code somewhere"
- The accidental part is what you can actually reduce.

**(b) A reversible migration plan (as in B7):**
1. **An abstraction layer first:** introduce an `OrderRepository` interface so all data access goes through one place. That's reversible, because it's just a refactoring, and it's the precondition for everything else.
2. **Create the Postgres schema.** **Dual-write** new and updated orders to both databases, with MongoDB still the system of record.
3. **Backfill** history into Postgres with an idempotent, resumable job.
4. **Shadow reads:** read from MongoDB, also read from Postgres, and log any mismatches. Fix the bugs until mismatches reach zero over a meaningful period.
5. **Switch reads to Postgres**, behind a feature flag, gradually: per customer, then 1%, 10%, 100%. **Keep dual-writing**, so MongoDB stays current and rollback is just flipping the flag.
6. **The one-way door:** **stop writing to MongoDB.** After that, it goes stale and rolling back means a reverse migration. Walk through it only after weeks at 100% on Postgres with no rollbacks, with reports reconciled and backups verified. Keep a final MongoDB snapshot for a while.

**(c) Adding multi-currency safely before cleanup:**
- Write **characterization tests** first: capture the current pricing behaviour on real orders, so you notice if you change it by accident.
- Build multi-currency **behind a feature flag**, off by default and enabled for internal or test accounts first.
- **Add a new field** (`currency`, defaulting to the existing one) rather than changing the meaning of `amount`. Old code keeps working, and that's backward compatible (Week 8).
- Release **more often and in smaller steps** (canaries) to cut the risk of each change.

**(d) The first boundaries:**
- **Data access** (the repository layer): it's required for the migration, and it untangles the data coupling.
- **Pricing and money as one module** with a clear interface: a `Money` type with amount plus currency, where all conversion happens. That's exactly the area that's about to change.
- Draw boundaries **where change is coming** and where the domain separates naturally (orders, pricing, payments). Don't try to clean the whole mud ball at once.
- Gradually **strangle** the monolith: new functionality goes behind the new interfaces.

**Follow-up: why not rewrite from scratch?**
- A rewrite **throws away years of hidden knowledge**: edge cases, regulatory fixes, bug workarounds that nobody documented.
- It takes far longer than estimated, while the old system still needs features (two systems to maintain).
- And it ends in a **big-bang cutover**, the most irreversible and risky kind of change.
- Incremental change keeps delivering value, and **every step is reversible**.
- **When a rewrite *is* justified:** the system is small and well understood, or the platform is genuinely dead (no hardware, no people). Even then, migrate incrementally.

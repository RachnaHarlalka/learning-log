# Week 0: Model answers to the interview scenarios

> Only open this after writing your own answers in `../solved/answers.md`.
> These are *strong* answers, not the only answers. Compare your **reasoning**: did you clarify, weigh the options, commit to a recommendation, and name its cost?
> Reference code: [code/](code/). It passes all tests: `WEEK_IMPL=solutions python3 solved/code/test_week00.py`

---

## S1. Reports are killing checkout
**Clarify:**
- How fresh must the dashboards be: real-time, hourly, or yesterday?
- Do the reports need data from other systems too?
- Is there already a replica, for high availability?

**(a) Why they interfere.**
- **Checkout** (OLTP) is many tiny **point reads and writes** by key. It needs the hot rows and indexes in memory, and it needs short lock and I/O waits.
- **Dashboards** (OLAP) **scan and aggregate millions of rows**. That uses lots of CPU and disk bandwidth, pushes checkout's hot pages out of the buffer cache, and can hold long-running snapshots.
- Both share one machine's CPU, I/O, and memory, so the long scans starve the short transactions. That's why p99 suffers, not the average.

**(b) Replica vs warehouse.**

| | Read replica | Warehouse (fed by ETL/CDC) |
|---|---|---|
| Fixes the interference | ✅ Scans move off the primary | ✅ |
| Effort | Low: minutes to set up | High: pipelines, a schema, ownership |
| Combines data from many systems | ❌ Only this one database | ✅ Joins across services and SaaS tools |
| Schema | Same OLTP schema (normalized, awkward for analytics) | Analysis-friendly (star schema), keeps history |
| Scan performance | Row store, still slow at TB scale | Column store, built for scans |
| History | Only current state (overwritten rows are gone) | Keeps history and snapshots |
| Side effects | Heavy queries can still lag replication, or get cancelled | Isolated from production |

The **replica is good enough** when there's one database, a modest amount of data, and the questions are about current state. A **warehouse** becomes necessary once you have many sources, need history, or data volume makes row-store scans too slow.

**(c) Recommendation.**
- **(i) Today:** add a **read replica** for the dashboards. It's cheap and quick and fixes the outage. Consider a small columnar copy (e.g. DuckDB or ClickHouse) if queries get slow.
- **(ii) In 2 years:** a **warehouse** fed by CDC or ETL from all 30 databases. A replica can't join 30 separate databases, and 60 analysts need a modelled, documented schema.

**Follow-up: the numbers don't match.**
- **Freshness:** the ETL snapshot was taken at a different time than the production query, or a late-arriving refund wasn't loaded yet.
- **Definitions:** timezone of "yesterday", whether cancelled or test orders are excluded, gross vs net revenue.
- **Pipeline bugs:** dropped or duplicated rows on a rerun.

**Production (the system of record) is right by definition.** The warehouse is derived, so you **reconcile** it: compare row counts and totals per day between source and warehouse. Build that check into the pipeline.

> **What interviewers look for:** you explain the interference mechanically (shared CPU, I/O, and cache), you pick the cheap fix first, and you know when it stops being enough.

---

## S2. Live dashboards for 300k sellers
**Clarify:**
- Is "live" every 10 s, or would 1 minute do?
- How long is the history (today only, or 90 days)?
- Are the metrics fixed, or do sellers slice the data freely?
- How accurate must returns be?

**(a) Why not the OLTP database?**
20,000 open dashboards ÷ 10 s = **~2,000 aggregate queries per second**, on top of checkout traffic. Each query scans a seller's orders for the day. That's the S1 problem multiplied by 1,000. It would flatten the primary, and replicas would only spread the pain around.

**(b) Why not the warehouse?** It's a **day stale**. It's also built for **a few heavy queries from analysts**, not thousands of small, concurrent, user-facing ones (concurrency limits and per-query cost).

**(c) Architecture:**
- Orders, payments, and returns emit events, through **CDC** from the OLTP databases or the app publishing them, into **Kafka**.
- A **real-time analytics store** (ClickHouse, Pinot, or Druid) ingests them, partitioned by `seller_id` and time, with **pre-aggregated hourly rollups**.
- A dashboard API queries it, behind a short cache (around 5 s).

**Promise:** data no more than ~10–30 s old, and p99 under 300 ms for queries on today's data.

**Trade-offs vs a warehouse:**
- less flexible: queries are pre-shaped around seller and time
- another system to run, with its own pipeline to monitor
- **eventual consistency**: a refund may show a few seconds late
- more expensive per GB than a warehouse

**Follow-up: precompute and cache?** That works when the **set of views is small and fixed**: "orders per hour today" can be **maintained incrementally** (add 1 to the right counter per event). It breaks down when sellers want **arbitrary filters** (category × city × hour), when there are too many combinations, or when you need freshness across many dimensions. That's where an OLAP engine beats a pile of caches. In practice you combine them: incremental rollups for the common views, the OLAP store for the rest.

---

## S3. Questions that cross every silo
**Clarify:**
- One-off answer, or a recurring dashboard?
- How fresh must it be (daily is probably fine)?
- Are there privacy constraints on the ticket text?

**(a) Why not one query?** **Data silos.** The data sits in 4 different database engines plus a SaaS API, each with its own team and schema. No single query engine can join across them, and a script that queried them all would load production and break with every schema change.

**(b) Data flow:**
```
Postgres / MySQL / Mongo --CDC or nightly extract--+
Zendesk API --connector (Fivetran/Airbyte)---------+--> DATA LAKE (raw, S3/Parquet) --> transform (SQL, dbt) --> WAREHOUSE --> BI
App clickstream (2B/day) --Kafka-------------------+                     |
                                                                         +--> data science (pandas, Spark)
```
- Use **ELT**: land raw data first, then transform inside the lake or warehouse.
  - **Raw data is better**: you can't predict tomorrow's question (S3's follow-up proves it).
  - Re-running a transformation is cheap, while re-extracting from sources is expensive or impossible.
- **Clickstream lands in the lake first.** At 2B events a day with a loose, changing JSON schema, forcing it into warehouse tables at ingest is costly and lossy. Load only the curated, aggregated parts, like crash counts per restaurant per day, into the warehouse.

**(c) The rename breaks things.**
- The extract keeps running but `amount` is now null or missing, so refund rates silently go wrong, or the transformation job fails.
- **Prevention:**
  - **Schema contracts**: the source team publishes a versioned schema for the data it shares, as with an API
  - **Schema checks** in the pipeline that fail loudly on unexpected changes
  - **CDC with a schema registry**
  - **data-quality tests**, e.g. "refund total ≥ 0", "row count within ±20% of yesterday"
- **Organizationally:** treat the data the team exports as a **product with an owner**, so changes are announced and versioned rather than discovered later.

**(d) Labels:**
- **Systems of record:** Postgres, MySQL, MongoDB, Zendesk, and the clickstream events at the source
- **Derived:** the lake, warehouse, BI extracts, and anything built from them

**Follow-up: ticket text.** **Yes.** Raw ticket text is already in the lake, and data scientists use Python and NLP there directly. A warehouse-only design would have struggled. Mind the privacy side: tickets contain personal data, so restrict access, mask phone numbers and emails, and remember GDPR deletion applies here too (S12).

---

## S4. Which price is true?
**(a)** **₹599, from the products database.** It's the system of record, so it wins by definition. The search index and the cache are **derived copies** that have fallen behind.

**(b) How each copy went stale:**
- **Redis ₹549:** an earlier price change wrote the database but never **invalidated** the cache key. Or the TTL hasn't expired yet. Or there's a race: a read loaded the old value into the cache just after the invalidation.
- **Elasticsearch ₹499:** the indexing pipeline is **asynchronous and lagging**, or an update event was dropped or failed, or the index was rebuilt from an old snapshot.

**(c) The flow:**
1. Write the new price to the **products database first**, in a transaction.
2. In the **same transaction**, write a "price changed" row to an **outbox table**. (CDC on the database works too.)
3. A relay publishes the outbox rows to Kafka.
4. Consumers then **invalidate the Redis key** (delete it rather than overwrite it, to avoid races) and **reindex the document** in Elasticsearch.

**If a step fails:** the event stays in the log and is **retried**, and the consumers are **idempotent** ("set price = 599" is safe to apply twice). If the database write fails, nothing is published.

**Why not dual writes:** the app writing to the DB, then Redis, then ES directly will eventually crash between steps and leave the copies inconsistent forever.

**Checkout always reads the system of record.**

**(d) Backups:**
- **Redis (cache):** no backup needed, since it's derived. **But** a cold restart sends every read to Postgres (a stampede of requests), so plan for warm-up, rate limits, and request coalescing.
- **Elasticsearch:** rebuildable from the database, but a full **reindex of millions of documents can take hours**, and search would be broken meanwhile. Snapshots are worth it **for recovery time, not correctness**.
- **Twist, carts only in Redis:** Redis is now a **system of record** for carts. It needs persistence (AOF/RDB), replication, and backups. Or, better, move carts to a durable store and cache them.

**Follow-up: why not read everything from the database?**
- Load: search and product pages are the highest-traffic reads, so the database would need far more capacity.
- **Capability:** relational databases are poor at full-text search, typo tolerance, and relevance ranking. That's why the search index exists.

Derived data trades **freshness and complexity** for **speed and new query types**. The right move is to keep it and manage its sync, not to remove it.

---

## S5. Cloud or own hardware? The maths
**(a) Yearly cost (8,760 h):**

| | Cloud | Self-hosted |
|---|---|---|
| **X** | 120 × ₹60 × 8,760 = **₹6.31 Cr** | Sized for the peak, 132 servers (+10%): 132 × ₹25 × 8,760 = **₹2.89 Cr**. No extra staff. |
| **Y** | Base 10 × ₹60 × 8,760 = ₹52.6 L. Peak: 140 extra × 6 h × 61 days = 51,240 server-hours × ₹60 = ₹30.7 L. **Total ₹83.3 L.** | Sized for the peak, 150 servers: 150 × ₹25 × 8,760 = ₹3.29 Cr, plus 2 SREs at ₹80 L = **₹4.09 Cr** |

**(b) Recommendations:**
- **X: self-host, or at least move the steady core off on-demand cloud.** It saves about **₹3.4 Cr a year (54%)**. The load is predictable, the expertise exists, and utilization stays high.
  - Risks: hardware lead times, capacity mistakes, and the work of the migration itself.
  - Middle ground: stay in the cloud but buy **reserved or committed-use capacity** for the steady load, which closes much of the gap without a migration.
- **Y: cloud.** It's about **5× cheaper**, because owned servers would sit **idle about 93% of the year** for a 2-month peak.
  - Three engineers should build product, not run hardware.
  - Autoscaling also protects them if a match goes viral beyond 150 servers.

**(c) Hybrid for Y:** reserved or committed instances for the always-on base of 10, with **autoscaling on-demand or spot capacity** for match peaks. Pre-scale before scheduled matches, since autoscaling reacts with a lag.

**Follow-up: hidden costs.**
- **Cloud:**
  - **data egress** fees
  - managed-service premiums
  - forgotten idle resources
  - vendor lock-in raising future prices
  - quota limits on peak day
- **Self-hosted:**
  - **redundancy**: spare servers, a second site for disaster recovery
  - hardware refresh every 3–5 years
  - hiring risk and on-call burnout
  - lead time to add capacity
  - networking, security, and compliance audits
  - the opportunity cost of engineers not building product

> **What interviewers look for:** you do the arithmetic quickly, then say *"the numbers aren't the whole story"* and name the risks.

---

## S6. Locked in, and the region is down
**(a) During the outage:** there's little you can do except communicate (status page, honest updates), degrade gracefully where possible (serve cached or static pages, queue writes on the client), and wait. **Beforehand:**
- **Multi-AZ** (multiple availability zones): cheap, standard, survives a datacenter failure
- **Multi-region:**
  - *warm standby:* replicate data to a second region and fail over in minutes or hours. That needs cross-region replication, and asynchronous replication can lose recent writes.
  - *active-active:* much harder, with conflict handling (Week 10)
  - costs: duplicated infrastructure, cross-region data transfer, and a lot of engineering and testing (untested failover is the same as no failover)
- **The decision:** compare cost per hour of downtime × probability, against the cost of the standby.

**(b) The price tripling.** Migration hurts because:
- proprietary APIs are woven through the code, with no drop-in alternative
- data must be exported, possibly with egress fees, and reshaped
- the auth service holds users' identities and password hashes, which may not be exportable
- nobody can "keep running the old version"

**Earlier choices that reduce the pain:**
- prefer services with **standard or open interfaces**: managed Postgres, Kafka-compatible queues, S3-compatible storage, OIDC-standard auth
- put a **thin adapter layer** in the code
- keep data exportable in open formats

**What those choices cost:** you give up some proprietary features and convenience, take on some abstraction overhead, and may move slower early on.

**(c) Multi-cloud for 10 people? Usually no.**
- It roughly **doubles** infrastructure and operations work, forces you to the lowest common denominator of features, and slows down a small team.
- Better value: **multi-AZ**, portable choices where they're cheap (Postgres, containers), tested backups stored outside the primary account, and a written exit plan.
- Revisit when customers or regulators demand it, or when the cost of downtime justifies it.

**Follow-up: foreign government access.**
- Be honest: the provider is subject to its home country's laws and could be **compelled** to hand over data. The chapter also notes sanctions risk.
- **Mitigations:**
  - an EU region, and EU-based providers where required
  - encryption with **customer-managed keys**, held outside the provider if needed
  - data minimization
  - a contractual Data Processing Agreement
- This is a legal and compliance question as much as a technical one, so loop in legal.

---

## S7. Storage and compute in the cloud
**(a) Postgres on local NVMe.**
- **Risk:** local disks are **ephemeral**. If the VM is stopped, resized, or moved, or its host fails, the data is gone.
- **Fixes, keeping performance:**
  - run a **replica** (synchronous or asynchronous) on another VM, ideally in another availability zone, and fail over to it
  - continuous **WAL archiving to S3** plus regular backups
  - or switch to a **managed or cloud-native database** that separates storage
- Local NVMe is fine as a *performance tier* **only if** durability comes from replication.

**(b) The 200 ms write spikes.** Network block storage is a **remote service emulating a disk**: every write is a network round trip, replicated across storage nodes. Network jitter, noisy neighbours on the storage backend, or hitting the volume's **IOPS or throughput limits** all show up as disk latency, even with the CPU idle. Databases call **fsync** on every commit, so they're especially sensitive.

**(c) 80 TB, 30 heavy queries a day.**
- **Choose object storage plus on-demand compute** (Snowflake, BigQuery, Athena/Trino, or Spark on demand).
  - Storage is cheap and durable.
  - Compute is paid **only while queries run**, which is probably a small share of the day.
  - Compute can scale up for a heavy query and back to zero.
- **Downsides:**
  - every query pulls data over the network, so first queries are slower; mitigated by caching on local SSDs, columnar formats, and partition pruning
  - per-query costs can surprise you
  - performance is less predictable than a tuned dedicated cluster
- A fixed cluster wins only with **constant, heavy utilization**.

**(d) Noisy-neighbour fixes** (any two):
- **per-tenant quotas or limits** on CPU, memory, concurrency, and query time
- **separate resource pools or queues** per tenant tier
- **dedicated clusters** for the largest tenants (often sold as a premium tier)
- **admission control**: queue or reject queries above a cost estimate
- **pre-aggregation** of the big tenant's common queries

**Follow-up: why Aurora recovers faster.**
- **Storage is a separate, replicated service** (the data is copied across availability zones by the storage layer).
- When a compute node dies, a new or standby node **attaches to the same storage** and only replays a little log. No data copy, no full recovery from the local disk.
- Postgres on a VM must fail over to a replica that has its *own* full copy (with possible lag), or restore from backup.

---

## S8. Do we really need to distribute?
**(a) Evaluating the two proposals.**
- **Microservices on Kubernetes:**
  - Gain: little. One 32-core machine handles 1,500 requests/s comfortably, and one team has no coordination problem to solve.
  - Pay:
    - network calls replace function calls (more latency, and new partial failures)
    - cross-service consistency problems (S10)
    - distributed debugging (tracing)
    - Kubernetes and per-service deployment, monitoring, and on-call work
    - slower feature work
  - **Verdict:** no. Use a **modular monolith** (clear internal modules), which keeps the option to split later.
- **20-node Spark for the nightly job:**
  - The job takes 12 minutes on one machine, overnight. There's no problem to solve.
  - Spark adds cluster operations, shuffle overhead (it may even be *slower*, as in MCQ 20), and cost.
  - **Verdict:** no. If it grows, use a bigger machine, DuckDB or Polars, or partition the work by date.

**(b) Legitimate reasons to distribute anyway, with the least distribution for each:**
- **High availability:** a single server is a single point of failure. Fix: a **standby replica plus failover** (2 nodes, still one app). Run 2–3 stateless app instances behind a load balancer.
- **Latency for global users:** a CDN for static content first, then a regional read replica.
- **Data residency:** a separate regional deployment (S12d).
- **Genuinely outgrowing one machine:** scale up first, then read replicas, then shard.

**(c) Signals that it's time to split into services:**
- many teams (several of 6–8 people) **stepping on each other's** deploys and merge queues
- different parts needing very different **scaling or hardware** (e.g. GPU inference vs CRUD)
- one module's failures or releases **repeatedly endangering** unrelated features
- clear, stable domain boundaries with little shared data
- build and test times hurting productivity

These are **organizational and operational** pain, not "it's 2026 and everyone uses microservices".

**Follow-up: single point of failure.** **Yes, high availability is a valid reason to distribute**, but it needs *redundancy*, not *microservices*. Two app instances behind a load balancer plus a Postgres primary with a standby gives fault tolerance with almost no architectural change. Don't confuse "more than one machine" with "split the codebase".

---

## S9. The payment timeout
**(a) Possible states after the timeout:**
1. The request was lost before reaching the payment service, so **not charged**.
2. It arrived, but the service crashed or queued it before processing, so **not charged** (or charged later, from a queue).
3. It's **still processing** (slow bank), so the outcome is **unknown for now**.
4. It **was charged**, but the response was lost or late.

You **cannot tell** these apart from the client side.

**(b) Neither obvious response is safe.**
- **A blind retry** in state 4 (or 3) charges the customer **twice**.
- **"Show an error"** is also wrong. In state 4 the user was charged, so if they pay again they're double-charged, and if they leave, you've taken money for an order you never record. Either way they lose trust.

**(c) A safe retry:**
- The **order service generates an idempotency key** per payment attempt, e.g. `order-81-attempt-1` or a UUID, and stores it with the order *before* the first call.
- It sends the key with each request (an `Idempotency-Key` header) and **retries with the same key**, using exponential backoff with jitter.
- **The payment service** keeps an idempotency table `{key → status, result}` with a unique constraint, written **in the same transaction** as the charge record.
  - On a **duplicate key**, it **returns the stored result** without charging again.
  - If the first request with that key is still in flight, it returns "in progress".
- Meanwhile, the UI shows **"payment processing"**, not "failed".

**(d) Charged, but the order service crashed before recording it.**
- **Reconciliation:** because the key was stored with the order beforehand, a background job finds orders stuck in "payment pending". It **queries the payment service by idempotency key or order ID** and completes or cancels the order.
- Alternatively, the payment service sends a **webhook or event**, "payment succeeded for order 81", which the order service handles idempotently.
- Run a periodic **ledger reconciliation**: payments vs orders.
- **The principle: never rely on a single synchronous response for money.** Design for the unknown outcome.

**Follow-up: how long a timeout?**
- Base it on the dependency's **latency distribution**: somewhat above its p99 or p99.9, e.g. 2–3 s if p99 is 800 ms. Fit it within the user-facing deadline.
- **Too short:** you time out on healthy-but-slow requests and create needless retries, which can overload the dependency (a retry storm).
- **Too long:** threads pile up waiting and the user waits.
- Add a **retry budget**, plus a **circuit breaker** so you stop hammering a dependency that's down.

---

## S10. Slow checkout and the half-finished order
**(a) Finding the culprit.**
- Use **distributed tracing** (OpenTelemetry, with Jaeger or Zipkin).
- Pull traces of **slow checkouts** (filter for p99 or slower) and look at the **span tree**: which hop's duration grew, and whether calls are sequential that used to run in parallel. Compare with traces from before Tuesday. Often it's one dependency, a new N+1 query loop, or a retry loop.
- **Requirements:**
  - every service **propagates the trace context** (trace ID and parent span ID headers) on every outgoing call, including through queues
  - every service is instrumented to emit spans
  - consistent sampling (keep the slow and error traces)
- Correlate with the **deploy log**: which of the Tuesday deploys touched the slow hop?
- **Why per-service graphs missed it:** each service can look fine on average while one call path is slow, or the time is spent *between* services (network, queueing, connection pools).

**(b) The half-finished order.**
- **Why no transaction can prevent it:** a database transaction is atomic **within one database**. Orders and Inventory each own their own database, so no single transaction covers both.
- **Two-phase commit (2PC):** a coordinator asks both databases to *prepare*, then *commit*.
  - ✅ atomic
  - ❌ couples the services' availability (if either is down, both block)
  - ❌ locks are held while waiting
  - ❌ the coordinator becomes a single point of failure
  - ❌ many databases and message queues don't support it
  - So it's rarely used with microservices.
- **Saga / compensating actions:** run the steps in sequence, each a local transaction, and **compensate** on failure (inventory fails, so cancel the order and refund).
  - ✅ services stay independent
  - ❌ **intermediate states are visible** (an order briefly exists without stock)
  - ❌ compensations must be designed and made idempotent
  - ❌ more application logic
  - Usually event-driven, using the outbox pattern.
- **Better step order:** reserve stock *first* (with a time limit), then create the order, then charge, so a failure leaves the cheapest thing to undo.

**Follow-up: merge Orders and Inventory?**
- **Often yes:** if they're always changed together, owned by the same team, and need to be strongly consistent, then they're one domain and the split was premature. One database gives a real transaction.
- Keep them separate when they have **different owners**, very different scaling needs, or Inventory is shared by many other services (warehouses, suppliers).
- Rule of thumb: put boundaries where **consistency requirements are weak**.

---

## S11. Serverless or not?
| Workload | Verdict | Reasoning |
|---|---|---|
| **(a) Thumbnails** | ✅ **Serverless** | Event-driven (one upload triggers one function), short (1 s), bursty from 0 to 5,000 a minute. You pay per execution, so nothing when idle, and scaling is automatic. Cold starts don't matter for a background job. |
| **(b) Video transcoding, 30–60 min** | ❌ Not as single functions | **Execution time limits** (often ~15 min), plus heavy CPU, memory, and temp disk needs. Use **containers or batch jobs** (a queue plus autoscaled workers, or spot instances). Alternatively, **split the video into chunks** and transcode them in parallel functions, then stitch them together. |
| **(c) Payment API, <100 ms p99, steady 3k req/s** | ❌ Use always-on services | **Steady 24/7 load** means per-invocation pricing usually costs *more* than reserved instances. **Cold starts** and per-invocation overhead threaten the p99. You also need connection pooling to the database, which is hard with ephemeral functions. |
| **(d) Admin tool, 20 uses a day** | ✅ **Serverless** | Idle 99.9% of the time, so you pay almost nothing and there are no servers to patch. A 1–2 s cold start is fine for internal users. |
| **(e) Weather simulation, 4 h on 500 cores** | ❌ This is an **HPC/batch** workload | Compute-heavy and tightly coupled, using **checkpoint-and-restart** for fault tolerance. Use **batch compute**: spot or preemptible VMs (cheap, since you can restart from checkpoints), or an HPC service with fast interconnects if the nodes talk to each other a lot. Pay for 4 hours a night, not 24. |

**Follow-up: "no ops work"?** **No.** You don't manage servers, but you still own:
- monitoring and alerting
- function timeouts and retries (and making them **idempotent**, since functions may be retried)
- concurrency limits and **quotas**
- cost control (a runaway loop costs real money)
- security and IAM permissions, dependencies and patching
- cold-start tuning
- debugging distributed event flows (tracing again)

Ops shifts; it doesn't vanish.

---

## S12. Privacy as a design requirement
**(a) A deletion request, system by system:**

| System | What must happen | Difficulty |
|---|---|---|
| Postgres profile | Delete or anonymize the rows, in a transaction | Easy |
| Kafka (7-day retention) | Events expire within 7 days, so document it and make sure downstream consumers delete too. Or use log compaction with tombstones on keyed topics. | Medium |
| S3 lake (append-only Parquet) | **Hard.** Files are immutable and the user's GPS points are spread across thousands of files. You must rewrite every affected file. | **Hard** |
| Warehouse | Delete the rows (DELETE or MERGE). Rebuild aggregates if needed. | Medium |
| Recommendation model | **Hard.** The data is baked into the trained weights. Remove it from the training set and retrain at the next cycle (monthly), and document that timeline. Use aggregate or anonymized features where possible. | **Hard** |
| Backups (1 year) | **Hard.** You can't easily edit backups. Common approach: keep a **deletion list** and reapply deletions on any restore, and let backups age out. Or crypto-shred (below). | **Hard** |

Also: caches, search indexes, logs, analytics tools, and **third parties** you shared data with. Keep an auditable record that the request was completed, without the data itself.

**(b) Making deletion practical:**
- **Crypto-shredding:** encrypt each user's sensitive data, like GPS traces, with a **per-user key** held in a key service. To delete, **destroy the key**: every copy in the lake and the backups becomes unreadable at once, with no file rewrites. It costs key management, encryption overhead, and some loss of query convenience.
- **Partition the lake by user**, or by user bucket and date, so deleting means rewriting only a few small files. Use a table format that supports deletes (Iceberg, Delta, Hudi), which handles the rewrite and compaction for you.
- **Short retention** on raw data limits how far back deletion has to reach.

**(c) Pushing back on "keep raw GPS forever":**
- **Risks beyond storage cost:**
  - GPS traces reveal **home, workplace, routines, and sensitive locations** (clinics, places of worship)
  - a breach means severe **reputational damage** and **GDPR fines** (up to 4% of global turnover)
  - **compelled disclosure** to governments
  - a larger deletion burden (S12a)
  - it breaks GDPR's **purpose limitation** and **storage limitation** rules
- **A minimization policy that still serves the product:**
  - keep **raw traces 30–90 days** (enough for the user's history and for fixing bugs)
  - then keep only **derived, coarse features**: distance, pace, elevation, a city-level region, aggregated heatmaps with k-anonymity
  - blur the start and end points near home
  - use explicit **opt-in** for research use
  - a new ML feature that needs raw data gets a **new, explicit purpose and consent**, not a speculative hoard

**(d) EU data residency:**
- **Partition users by region**: EU users' data (Postgres, lake, Kafka, warehouse, backups, model training) lives in **EU regions**, and processing happens there too.
- **Routing:** a user's "home region" decides where requests go.
- **Global features** (leaderboards, cross-region friends) work only on **non-personal or aggregated** data, or need legal review.
- Ops cost: two deployments to run, cross-region analytics becomes harder, and keys must stay in the EU.

**Follow-up: anonymize instead of delete?**
- Real anonymization is **hard**. Location traces are famously **re-identifiable**: a few points (where the trace starts at night, where it stops in the day) pinpoint a person.
- Removing the user ID is only **pseudonymization**, and GDPR still treats pseudonymized data as personal data.
- Anonymization can be acceptable for **coarse aggregates** (e.g. city-level counts with minimum group sizes), not for raw traces.
- So: delete the raw data, and keep only aggregates that are genuinely anonymous.

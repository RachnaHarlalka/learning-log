# Week 0 MCQs: Answer key

> Check your score first with `python3 tools/check_mcqs.py weeks/week-00-tradeoffs`. Read the "Why" column only for the ones you missed, after working out your own reason.

| Q | Answer | Why the best answer wins (and the trap) | Concept (notes §) |
|---|---|---|---|
| 1 | C | Scan-heavy analytics competes with point queries for CPU, I/O, and cache. Separating the workloads fixes the cause. **Trap:** D only moves the clash, an index (A) doesn't help a full aggregation, and B just postpones it. | OLTP vs OLAP (3–4) |
| 2 | A | It's an analytical query, but user-facing, needing low latency and fresh data at huge query volume. That's what real-time analytics stores are for. **Trap:** B would hammer the primary; C and D are hours stale. | Product analytics (3) |
| 3 | D | It needs fresh data *and* a per-request answer within milliseconds. A nightly, scan-optimized warehouse provides neither, so you need a stream processor or an online feature store. | OLTP vs OLAP, streams (3, 5) |
| 4 | B | This is why warehouses exist: no load on production, history and consistent snapshots, and decoupling from each service's internal schema. | Data warehousing (4) |
| 5 | A | Keeping data raw (the "sushi principle") means future consumers can derive what they need. Once a transformation has thrown data away, it's gone. | Data lake, ELT (5) |
| 6 | C | One application needing both large scans and low-latency writes is the HTAP sweet spot. **Trap:** A needs data from many systems combined, which is the warehouse's job. | HTAP (4) |
| 7 | D | When copies disagree, the system of record wins. Search indexes are derived and update asynchronously, so they can lag. Charge using the system of record. | System of record vs derived (6) |
| 8 | C | Derived data can be rebuilt, so backups are optional. But rebuilding has a cost: a cold cache sends a wave of reads to Postgres. Mention that in an interview. | Derived data (6) |
| 9 | B | Being a system of record depends on **how** you use a tool, not what the tool is. The moment carts live only in Redis, Redis is their source of truth. | Tool vs usage (6) |
| 10 | D | Spiky load plus no ops skills is the textbook case for the cloud. A pays all year for a 3-day peak; B loses the most valuable days. | Cloud vs self-host (7) |
| 11 | A | Predictable, high-utilization load plus in-house expertise is when owning hardware usually wins. **Trap:** D is false, since self-hosting needs *more* ops. | Cloud vs self-host (7) |
| 12 | C | A proprietary API means switching costs are high, so the vendor has pricing power over you. | Vendor lock-in (7) |
| 13 | B | The cloud removes machine-level work, but the ops *role* moves to integration, cost, quotas, security, monitoring, and incident debugging. | Ops in the cloud era (9) |
| 14 | D | With metered billing, waste costs money immediately. Capacity planning becomes financial planning. | Ops in the cloud era (9) |
| 15 | B | A VM's local disk is ephemeral and tied to the physical host. Durable data needs replicated storage, database replicas, or a cloud-native database. | Storage and compute (8) |
| 16 | D | Virtual block devices are network services that emulate a disk, so network jitter turns into disk latency. | Storage and compute (8) |
| 17 | A | Bursty heavy compute over big, rarely queried data: keep it cheap in object storage and pay for compute only while queries run. **Trap:** B pays for 50 idle servers most of the day. | Separating storage and compute (8) |
| 18 | C | Shared hardware means one tenant can starve the others ("noisy neighbour"). Fix with per-tenant quotas, isolation, or dedicated tiers. | Multitenancy (8) |
| 19 | A | One machine copes fine with this load. Microservices are an *organizational* tool and add network calls, operational overhead, and consistency problems. A standby replica covers availability without splitting the app. | Single node vs distributed, microservices (10–11) |
| 20 | C | More nodes aren't always faster. Shuffling data over the network and coordinating the nodes can cost more than the extra parallelism saves. | Distributed overheads (10) |
| 21 | B | After a timeout the outcome is unknown. An idempotent retry is safe whatever happened. **Traps:** A and C risk double-charging, and D risks shipping an unpaid order. | Timeouts, unsafe retries (10) |
| 22 | D | Each service looks fine on its own; you need the *end-to-end* picture of where time is spent per hop. That's what distributed tracing gives you. | Observability (10) |
| 23 | A | One database per service means no single transaction covers both, so consistency becomes the application's job (sagas or compensating actions). 2PC exists but is rarely used because it couples services together. | Cross-service consistency (10) |
| 24 | C | Sharing a database turns its schema into a hidden API between teams. That's why each service should own its data. | Microservices (11) |
| 25 | B | Event-driven, short, bursty work is the ideal serverless workload: no idle cost, automatic scaling. | Serverless (11) |
| 26 | D | Serverless platforms impose execution time limits. Long jobs must be chunked, or run on containers or batch infrastructure. | Serverless limits (11) |
| 27 | A | A cold start is the delay when a new instance spins up after idle time. Mitigate with pre-warmed (provisioned) capacity, or move latency-critical paths to always-on services. | Serverless limits (11) |
| 28 | C | Checkpoint-and-restart suits batch HPC jobs. Online services must stay available, so they use redundancy rather than stopping everything. | Cloud vs HPC (12) |
| 29 | B | Erasure must reach every derived copy: caches, indexes, warehouse, lake, backups, and models. The immutable lake and the trained model are the hard parts. | Right to be forgotten (13) |
| 30 | D | Data that has no explicit purpose is pure risk (leaks, fines, compelled disclosure). **Trap:** C fails because precise GPS traces re-identify people (home and work locations). | Data minimization (13) |
| 31 | A | With crypto-shredding, deleting a small key makes all of that user's encrypted data unreadable, with no petabyte rewrites. (Compacting segments with tombstones is another option, covered in Week 5.) | Deleting from immutable logs (13) |
| 32 | B | Data residency laws are a legitimate reason to distribute. Encryption (A) doesn't change *where* data is stored and processed, and a CDN (C) only caches. | Distribution for legal compliance (10, 13) |

**Score guide:** 30–32 excellent · 26–29 good, review your misses · below 26, re-read the sections in the last column, then retry.

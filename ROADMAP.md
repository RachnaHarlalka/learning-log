# System Design + Python Roadmap

**Main source:** *Designing Data-Intensive Applications*, 2nd edition (DDIA)
**Supporting sources:** Engineering Digest, Shreyansh (HLD), Gaurav Sen
**Pace:** ~8–10 hrs/week (1 hr on weekdays, ~3 hrs on weekends). If you fall behind, push the whole schedule back. Don't skip weeks.

---

## How to use this roadmap

### Each channel has one job
| Source | Job | When |
|---|---|---|
| **DDIA** | Main source. It sets the order of topics. | Every week |
| **Engineering Digest** | Warm-up / vocabulary | Before a chapter, only if the topic is new. If you've already watched it, it counts. Don't rewatch. |
| **Gaurav Sen** | Intuition for one hard concept | After reading, only for something that didn't click |
| **Shreyansh (HLD)** | Design problems, interview style | Sunday, *after* you've tried the problem yourself |

### Rules
1. **Lock to one topic.** Everything in a week is about that week's topic.
2. **One video per concept.** Never watch three channels on the same thing.
3. **Keep a parking lot.** Interesting but off-topic? Write it in `parking-lot.md` and move on.
4. **Hands-on first.** If a topic can be built in Python, build it. Use conceptual questions only when a build doesn't make sense.
5. **Design problems:** spend 30 minutes on your own design first, list which chapter concepts it uses, *then* watch a video.

### Weekly rhythm
| Day | Activity |
|---|---|
| Mon–Wed | Read the DDIA section and write rough notes |
| Thu | At most 1 supporting video, then tidy up your notes |
| Fri | Learn the Python features the build needs |
| Sat | Python build |
| Sun | Practice questions and the design problem |

### Folder structure
```
learning-log/
  ROADMAP.md
  parking-lot.md
  weeks/
    week-01-latency-availability/
      notes.md
      questions.md      # your answers to the practice questions
      design.md         # your design-problem attempt
      code/
```

---

## Progress tracker

| Week | Topic | Read | Build | Questions | Design |
|---|---|---|---|---|---|
| 0 | Trade-offs and setup (Ch1) | [ ] | [ ] | [ ] | [ ] |
| 1 | Latency and availability (Ch2) | [ ] | [ ] | [ ] | [ ] |
| 2 | Scalability and load balancing (Ch2) | [ ] | [ ] | [ ] | [ ] |
| 3 | Relational vs document (Ch3) | [ ] | [ ] | [ ] | [ ] |
| 4 | Graphs and event sourcing (Ch3) | [ ] | [ ] | [ ] | [ ] |
| 5 | Logs and hash indexes (Ch4) | [ ] | [ ] | [ ] | [ ] |
| 6 | LSM trees, B-trees and caching (Ch4) | [ ] | [ ] | [ ] | [ ] |
| 7 | Analytics storage and search indexes (Ch4) | [ ] | [ ] | [ ] | [ ] |
| 8 | Encoding, APIs and rate limiting (Ch5) | [ ] | [ ] | [ ] | [ ] |
| 9 | Single-leader replication (Ch6) | [ ] | [ ] | [ ] | [ ] |
| 10 | Multi-leader and leaderless replication (Ch6) | [ ] | [ ] | [ ] | [ ] |
| 11 | Sharding and consistent hashing (Ch7) | [ ] | [ ] | [ ] | [ ] |
| 12 | Transactions: isolation basics (Ch8) | [ ] | [ ] | [ ] | [ ] |
| 13 | Transactions: serializability and 2PC (Ch8) | [ ] | [ ] | [ ] | [ ] |
| 14 | Distributed systems trouble (Ch9) | [ ] | [ ] | [ ] | [ ] |
| 15 | Linearizability, CAP and ordering (Ch10) | [ ] | [ ] | [ ] | [ ] |
| 16 | Consensus and leader election (Ch10) | [ ] | [ ] | [ ] | [ ] |
| 17 | Batch processing (Ch11) | [ ] | [ ] | [ ] | [ ] |
| 18 | Message queues and logs (Ch12) | [ ] | [ ] | [ ] | [ ] |
| 19 | Stream processing (Ch12) | [ ] | [ ] | [ ] | [ ] |
| 20 | Final chapters and capstone | [ ] | [ ] | [ ] | [ ] |

---

## Week 0: Trade-offs and setup (3–4 days)
**Read:** DDIA Ch1, *Trade-offs in Data Systems Architecture*
**Concepts:** operational (OLTP) vs analytical (OLAP) systems, data warehouses and data lakes, cloud vs self-hosting, distributed vs single-node, systems of record vs derived data

**Hands-on (Python):**
- Set up Python 3.12+, a virtual environment (`python -m venv .venv`), `pytest`, and git.
- **OLTP vs OLAP feel test:** use `sqlite3` to insert 1M fake orders. Time a *point lookup* (`WHERE id = ?`) against an *aggregate* (`SUM(amount) GROUP BY city`). Then add an index and time both again. Write down why one query speeds up and the other doesn't.
- *Python skills:* venv, modules, `sqlite3`, `time.perf_counter`, `random`, f-strings

**Practice questions:**
1. Give 2 examples of OLTP queries and 2 of OLAP queries from an app like Swiggy.
2. Why do companies copy data into a separate warehouse instead of running analytics on the main database?
3. List 3 reasons to self-host and 3 to use a cloud service.
4. When is a single machine better than a distributed system?

**Design:** none this week. Ch1 is context.

---

## Week 1: Latency and availability
**Read:** DDIA Ch2, the sections on performance and on reliability/fault tolerance
**Your existing Engineering Digest videos on latency and availability count as this week's warm-up.**
**Concepts:** response time vs latency, throughput, percentiles (p50/p95/p99), tail latency, head-of-line blocking, SLOs/SLAs, faults vs failures, hardware/software/human faults, availability "nines"

**Hands-on (Python):**
- **Latency simulator:** generate 10,000 request times, mostly 20–80 ms with ~1% at 1–3 s. Calculate the mean and p50/p95/p99 yourself (sort the list and index into it), then check your numbers against `statistics.quantiles`. Show that the mean hides the slow requests.
- **Tail-latency amplification:** a page calls 10 backends in parallel and waits for all of them. Simulate how often the page is slow even though each backend is only slow 1% of the time.
- **Availability calculator:** convert nines into downtime per year/month. Calculate availability for components in series (all must work) and in parallel (any one is enough).
- *Python skills:* lists, sorting, functions, `random`, `statistics`, list comprehensions

**Practice questions:**
1. Why do companies set targets on p99 rather than the average?
2. Your service is at 99.9% availability. How many minutes of downtime is that per month?
3. Three services in series, each at 99.9%: what's the total availability? What if two replicas run in parallel?
4. What's the difference between a fault and a failure? Give an example of each.
5. Why is human error a bigger cause of outages than hardware?

**Design:** set latency and availability targets for a social media home timeline. What gets measured, and where?

---

## Week 2: Scalability and load balancing
**Read:** DDIA Ch2, the sections on scalability and maintainability, plus the home-timeline case study
**Supporting topic:** load balancers (round robin, least connections, health checks). One short video.
**Concepts:** describing load, fan-out, vertical vs horizontal scaling, shared-nothing architecture, operability, simplicity, evolvability

**Hands-on (Python):**
- **Fan-out simulator:** users follow each other, and some celebrities have 100k+ followers. Implement both:
  - *pull:* build the timeline at read time
  - *push:* write each post into every follower's timeline

  Count the work for each approach on reads and writes, then try a hybrid (push for normal users, pull for celebrities).
- **Load balancer simulator:** 5 servers with different speeds. Compare round robin, random, and least connections on p99 latency.
- *Python skills:* dicts, sets, classes, `collections.defaultdict`, `heapq`

**Practice questions:**
1. Why is "it handles 10k users" a bad way to describe scalability?
2. Push vs pull fan-out: which is better for a celebrity, and which for a normal user?
3. When is vertical scaling the right answer?
4. What's a health check, and what happens if the load balancer doesn't have one?
5. What makes a system easy to maintain?

**Design:** **home timeline for Twitter/X**, covering fan-out strategy, load balancers, and handling celebrities.

---

## Week 3: Relational vs document models
**Read:** DDIA Ch3, the sections on the relational and document models
**Concepts:** object-relational mismatch, normalization vs denormalization, one-to-many vs many-to-many, joins, schema-on-read vs schema-on-write, SQL vs NoSQL

**Hands-on (Python):**
- Model **LinkedIn profiles** (user, jobs, education, skills, companies) two ways:
  1. normalized tables in `sqlite3`
  2. one JSON document per user (`json` module, stored in files or a dict)
- Run the same queries on both: "show a profile", "all users who worked at Company X", "rename a company". Note which model makes each query easy or painful.
- *Python skills:* `json`, nested dicts/lists, SQL joins from Python, `dataclasses`

**Practice questions:**
1. When would you choose MongoDB over PostgreSQL? Give a concrete case.
2. What problem does normalization solve, and what does it cost?
3. Why are many-to-many relationships awkward in document databases?
4. Schema-on-read vs schema-on-write: which is better for fast-changing data?

**Design:** data model for **LinkedIn profiles and company pages**. Which database, and why?

---

## Week 4: Graphs and event sourcing
**Read:** DDIA Ch3, the sections on graph models, event sourcing/CQRS, and dataframes
**Concepts:** property graphs, triple stores, Cypher/SPARQL (just read them), recursive queries, event sourcing, CQRS, materialized views

**Hands-on (Python):**
- **Social graph:** store connections as an adjacency list. Write a BFS for "friends of friends" and "degrees of separation". Then try the same query in SQL with a recursive CTE in `sqlite3`.
- **Event-sourced bank account:** an append-only list of events (`Deposited`, `Withdrew`, `Transferred`). Rebuild the balance by replaying events, and build two read models (current balance, monthly statement) from the same events.
- *Python skills:* `collections.deque`, BFS, recursion, classes, `Enum`

**Practice questions:**
1. What kinds of queries are graph databases much better at?
2. Event sourcing: what are the advantages of storing events instead of the current state? What are the costs?
3. What is CQRS, and why separate reads from writes?
4. How do you "fix" a wrong event in an event-sourced system?

**Design:** **"People you may know"** for LinkedIn. Which data model, and how does the query work?

---

## Week 5: Logs and hash indexes
**Read:** DDIA Ch4, from the start through log-structured storage and hash indexes
**Concepts:** append-only logs, hash index, segments, compaction and merging, tombstones, crash recovery

**Hands-on (Python): your first real database (Bitcask-style key-value store)**
- `set(key, value)` appends to a log file, and an in-memory dict maps each key to its byte offset.
- `get(key)` seeks to the offset and reads the value.
- `delete(key)` writes a tombstone.
- Start a new segment file after N bytes, and write **compaction** that keeps only the latest value for each key.
- On startup, rebuild the index by scanning the segments (crash recovery).
- Write `pytest` tests for each operation.
- *Python skills:* file I/O in binary mode, `seek`/`tell`, `struct`, classes, `pytest`

**Practice questions:**
1. Why is appending to a file faster than updating it in place?
2. Why must the hash index fit in memory? What breaks if it doesn't?
3. Why can't a hash index do range queries (`keys between a and f`)?
4. What happens to deleted keys during compaction?

**Design:** a **key-value store like Redis**, single node. How does it survive a crash?

---

## Week 6: LSM trees, B-trees and caching
**Read:** DDIA Ch4, the sections on SSTables/LSM trees, B-trees, the comparison, secondary indexes, and in-memory databases
**Supporting topic:** caching strategies (cache-aside, write-through, write-back), eviction (LRU), CDNs. One short video.
**Concepts:** memtable, SSTable, LSM compaction, Bloom filters, B-tree pages, write-ahead log, write amplification, in-memory stores

**Hands-on (Python):**
- **LSM-lite:** keep writes in a sorted memtable. When it's full, flush it to a sorted SSTable file. Reads check the memtable first, then SSTables from newest to oldest. Add a simple **Bloom filter** per SSTable to skip files.
- **LRU cache:** implement it with `OrderedDict`, then wrap a slow function. Measure the hit rate and speed-up.
- *Python skills:* `bisect`, sorted structures, `hashlib`, `OrderedDict`, decorators

**Practice questions:**
1. LSM tree vs B-tree: which suits write-heavy workloads, and which read-heavy? Why?
2. What does a Bloom filter tell you, and what can it never tell you?
3. Why does a B-tree need a write-ahead log?
4. Cache-aside vs write-through: what goes wrong with each when the database is updated?
5. What does a CDN cache, and where?

**Design:** **caching for an e-commerce product page**, covering the cache layer, invalidation, and the CDN for images.

---

## Week 7: Analytics storage and search indexes
**Read:** DDIA Ch4, the sections on analytical storage, column-oriented storage, materialized views, full-text search, and vector indexes
**Concepts:** column storage, compression, vectorized execution, data cubes, inverted index, vector embeddings (overview)

**Hands-on (Python):**
- **Row vs column:** store 1M rows as a list of dicts (row layout) and as a dict of lists (column layout). Time `SUM(price)` on each. Then try the same query in **DuckDB** (`pip install duckdb`) against SQLite.
- **Mini search engine:** build an inverted index (word → set of document IDs) over ~100 text files. Support AND/OR queries and simple ranking by word frequency.
- *Python skills:* pip packages, `pathlib`, string processing, `re`, `Counter`

**Practice questions:**
1. Why are column stores faster for analytics but slow for single-row updates?
2. Why does column data compress so well?
3. How does an inverted index find documents containing "distributed systems"?
4. What is a vector index used for? (Think semantic search.)

**Design:** **search for an e-commerce site**, covering autocomplete and keyword search over product titles.

---

## Week 8: Encoding, APIs and rate limiting
**Read:** DDIA Ch5, *Encoding and Evolution*
**Supporting topic:** rate limiting (token bucket, sliding window), API gateways. One short video.
**Concepts:** JSON/XML vs binary encodings (Protobuf, Avro), schema evolution, backward/forward compatibility, REST vs RPC, dataflow through databases, services and messages

**Hands-on (Python):**
- **Encoding comparison:** encode the same record as JSON, MessagePack (`pip install msgpack`), and a hand-rolled binary format with `struct`. Compare sizes and encode/decode speed.
- **Schema evolution test:** v1 and v2 of a `User` record, where v2 adds a field and drops one. Write tests proving new code reads old data (backward compatibility) and old code reads new data (forward compatibility).
- **Rate limiter:** implement a token bucket and a sliding-window counter. Simulate bursts of requests.
- *Python skills:* bytes, `struct`, `dataclasses`, versioning, time-based logic

**Practice questions:**
1. Backward vs forward compatibility: which one do mobile apps need most, and why?
2. Why does Protobuf use field *numbers* instead of field names?
3. REST vs gRPC: when would you choose each?
4. Token bucket vs fixed window: what problem does fixed window have at window edges?

**Design:** **public API for a mobile app** where old app versions stay in use for years, covering versioning, the API gateway, and rate limits.

---

## Week 9: Single-leader replication
**Read:** DDIA Ch6, the sections on single-leader replication and replication lag
**Concepts:** leader/follower, synchronous vs asynchronous replication, adding followers, failover, split brain, replication logs, read-your-writes, monotonic reads, consistent prefix reads

**Hands-on (Python):**
- **Replication simulator:** a leader plus 3 followers, each holding a dict. Writes go to the leader and are copied to followers after a random delay.
  - Show a **stale read**: write, then immediately read from a lagging follower.
  - Fix it with **read-your-writes**: route a user's reads to the leader for a few seconds after they write.
  - Simulate **leader failure and failover**, and show which unreplicated writes are lost.
- *Python skills:* `threading` or `asyncio`, `queue.Queue`, `time.sleep`, classes

**Practice questions:**
1. Synchronous vs asynchronous replication: what's the trade-off?
2. What is split brain, and how can failover cause it?
3. A user updates their profile picture, refreshes, and sees the old one. Why, and how do you fix it?
4. Why can async replication lose writes even though the client got an "OK"?

**Design:** **chat app (WhatsApp)** message storage. Make sure users always see their own sent messages.

---

## Week 10: Multi-leader and leaderless replication
**Read:** DDIA Ch6, the sections on multi-leader, leaderless replication, quorums, and conflict resolution
**Concepts:** multi-datacenter setups, offline clients, write conflicts, last-write-wins, CRDTs, quorums (N, W, R), sloppy quorums, read repair, version vectors

**Hands-on (Python):**
- **Quorum simulator:** N=5 replicas with configurable W and R. Randomly fail replicas. Show when reads return stale data (W+R ≤ N) and when they can't (W+R > N).
- **CRDTs:** implement a G-Counter (likes counter) and an LWW-register. Two "offline devices" edit independently and then merge, with no conflicts.
- *Python skills:* more OOP, `random`, merge logic, writing tests for edge cases

**Practice questions:**
1. Why do offline-first apps behave like multi-leader systems?
2. N=3, W=2, R=2: why does this give you up-to-date reads? What if W=1, R=1?
3. Why can last-write-wins silently lose data?
4. What makes a CRDT always merge without conflicts?

**Design:** **Google Docs / offline-first notes app**. What happens when two people edit the same line offline?

---

## Week 11: Sharding and consistent hashing
**Read:** DDIA Ch7, *Sharding*
**Concepts:** key-range vs hash sharding, hot spots, skew, consistent hashing, rebalancing, request routing, secondary indexes (local vs global)

**Hands-on (Python):**
- **Mod-N vs consistent hashing:** distribute 100k keys over 4 nodes using `hash(key) % N`, add a 5th node, and count how many keys move. Repeat with a **consistent hash ring with virtual nodes** and compare.
- **Hot spot demo:** shard by a celebrity user ID and show the load skew. Fix it with key salting.
- *Python skills:* `hashlib`, `bisect` for the ring, `Counter`, simple text-based charts

**Practice questions:**
1. Key-range vs hash sharding: which supports range queries, and which spreads load better?
2. Why does `hash % N` reshuffle almost everything when N changes?
3. What do virtual nodes fix?
4. Local vs global secondary indexes: what's the read/write trade-off?

**Design:** **sharding Instagram's users and posts**. Pick a shard key, and decide how to handle celebrity accounts.

---

## Week 12: Transactions: isolation basics
**Read:** DDIA Ch8, the sections on ACID, read committed, snapshot isolation, and preventing lost updates
**Concepts:** atomicity, consistency, isolation, durability; dirty reads/writes; read committed; snapshot isolation/MVCC; lost updates; atomic operations; explicit locks; compare-and-set

**Hands-on (Python):**
- **Lost update:** 10 threads each increment a shared counter (read → +1 → write) 1,000 times. Show the final count is wrong.
- Fix it 3 ways: a `threading.Lock`, an atomic SQL update (`UPDATE ... SET n = n + 1`) in `sqlite3`, and compare-and-set with retry.
- *Python skills:* `threading`, race conditions, locks, context managers (`with`)

**Practice questions:**
1. What does the "C" in ACID really mean, and who is responsible for it?
2. Dirty read vs non-repeatable read: give an example of each.
3. Why does snapshot isolation help long-running reports?
4. Two users click "like" at the same moment. How can a like get lost?

**Design:** **wallet/payment balance updates**, with no double spending and no lost updates.

---

## Week 13: Transactions: serializability and 2PC
**Read:** DDIA Ch8, the sections on write skew, phantoms, serializability (serial execution, 2PL, SSI), and distributed transactions
**Concepts:** write skew, phantoms, two-phase locking, serializable snapshot isolation, two-phase commit (2PC), coordinator failure

**Hands-on (Python):**
- **Mini MVCC store:** each write creates a new version tagged with a transaction ID, and readers see a consistent snapshot.
- **Write-skew demo:** the book's "doctors on call" example. Two transactions each check that someone else is on call, then both go off call. Show it happening under snapshot isolation, then prevent it.
- **2PC simulator** (stretch goal): a coordinator and 3 participants. Crash the coordinator after "prepare" and see the participants get stuck.
- *Python skills:* versioned data structures, transaction IDs, state machines

**Practice questions:**
1. What is write skew, and why doesn't snapshot isolation prevent it?
2. Two-phase locking vs SSI: pessimistic vs optimistic. When does each win?
3. Why is 2PC called a "blocking" protocol?
4. Why do microservices often avoid distributed transactions? What do they use instead? (Read up on the saga pattern.)

**Design:** **movie seat booking (BookMyShow)**, with no double booking under heavy load.

---

## Week 14: Distributed systems trouble
**Read:** DDIA Ch9, *The Trouble with Distributed Systems*
**Concepts:** partial failures, unreliable networks, timeouts, unreliable clocks (time-of-day vs monotonic), clock skew, process pauses (GC), leases, fencing tokens, Byzantine faults

**Hands-on (Python):**
- **Unreliable network:** a fake network layer that randomly drops, delays, and duplicates messages. Build a client with timeouts, **retries with exponential backoff and jitter**, and **idempotency keys** so duplicate requests don't double-charge.
- **Clock skew bug:** two nodes with clocks 50 ms apart use last-write-wins. Show the later write getting lost.
- **Fencing tokens:** a client holding an expired lease tries to write. Show storage rejecting it based on the token number.
- *Python skills:* `asyncio`, `asyncio.wait_for`, exceptions, retry decorators, `time.monotonic` vs `time.time`

**Practice questions:**
1. A request times out. Did it fail? List every possibility.
2. Why add jitter to retries?
3. Why must you never use `time.time()` to measure durations?
4. How does a GC pause break a lease-based lock, and how do fencing tokens fix it?
5. What is an idempotency key?

**Design:** **job scheduler that never runs a job twice**, even when workers pause or networks drop.

---

## Week 15: Linearizability, CAP and ordering
**Read:** DDIA Ch10, the sections on linearizability and ordering/logical clocks
**Supporting topic:** CAP theorem. You may have seen this on Engineering Digest already; if so, it counts.
**Concepts:** linearizability, the cost of linearizability, CAP (and why it's often misunderstood), causality, Lamport timestamps, vector clocks, total order broadcast

**Hands-on (Python):**
- **Lamport clocks:** 3 processes exchanging messages. Assign timestamps and produce a total order.
- **Vector clocks:** detect whether two events are causally related or concurrent.
- *Python skills:* tuples/lists comparison, classes, message-passing simulation

**Practice questions:**
1. Explain linearizability with a real example (e.g. a username being claimed).
2. What does CAP actually say? Why is "pick 2 of 3" misleading?
3. Lamport clocks vs vector clocks: what can vector clocks detect that Lamport clocks can't?
4. Why is linearizability slow in geographically distributed systems?

**Design:** **unique username registration** across multiple regions.

---

## Week 16: Consensus and leader election
**Read:** DDIA Ch10, the sections on consensus, Raft/Paxos (concepts), and coordination services
**Concepts:** consensus, leader election, terms/epochs, quorums, Raft basics, ZooKeeper/etcd, distributed locks, unique ID generation

**Hands-on (Python):**
- **Raft leader election:** 5 nodes with random election timeouts, terms, and `RequestVote` messages, using `asyncio`. Kill the leader and watch a new election. (Leader election only, not full log replication.)
- **Snowflake ID generator:** 64-bit IDs made of timestamp + machine ID + sequence. Generate 1M IDs and check they're unique and roughly time-ordered.
- *Python skills:* `asyncio` tasks, state machines, bit manipulation (`<<`, `|`)

**Practice questions:**
1. Why does Raft need a majority to elect a leader?
2. What are terms for, and what happens to an old leader that comes back?
3. Why not use the database auto-increment ID in a sharded system?
4. What do ZooKeeper/etcd provide that apps use them for?

**Design:** **distributed ID generator** and **distributed lock service**.

---

## Week 17: Batch processing
**Read:** DDIA Ch11, *Batch Processing*
**Concepts:** Unix philosophy, MapReduce, distributed file systems, sort-merge joins, broadcast joins, dataflow engines (Spark), batch outputs

**Hands-on (Python):**
- **MapReduce from scratch:** word count over a folder of large text files. Write map, shuffle (group by key), and reduce steps, then parallelize with `multiprocessing.Pool`.
- **Join in batch:** join users and page-views files with a sort-merge join.
- Do the same job in pandas or DuckDB and compare code size and speed.
- *Python skills:* generators (`yield`), `multiprocessing`, `itertools.groupby`, reading large files lazily

**Practice questions:**
1. Why is "move computation to the data" important in batch systems?
2. Sort-merge join vs broadcast join: when do you use each?
3. Why is batch processing easy to retry after failure?
4. What did Spark improve over MapReduce?

**Design:** **daily analytics pipeline** (e.g. top 10 products per city each day).

---

## Week 18: Message queues and logs
**Read:** DDIA Ch12, the sections on transmitting events, message brokers, log-based brokers, and change data capture
**Supporting topic:** message queues vs pub/sub (RabbitMQ vs Kafka). One short video.
**Concepts:** producers/consumers, queues vs logs, partitions, offsets, consumer groups, acknowledgments, change data capture (CDC), log compaction

**Hands-on (Python): mini Kafka**
- Topics with N partitions, each an append-only file. Producers choose a partition by key hash.
- Consumers track their **offsets**. Consumer groups split partitions between members.
- Kill a consumer, restart it, and confirm it resumes from its committed offset.
- **CDC demo:** turn writes to a `sqlite3` table into events that keep a separate search index (from Week 7) in sync.
- *Python skills:* file-based design, `asyncio` or threads, project structure (multiple modules)

**Practice questions:**
1. RabbitMQ-style queue vs Kafka-style log: what happens to a message after it's consumed in each?
2. Why does ordering only hold *within* a partition?
3. What is CDC, and why is it better than the app writing to both the DB and the search index?
4. At-most-once vs at-least-once delivery: what does each cost?

**Design:** **notification system** (email/SMS/push) using queues, and **keeping search in sync with the DB**.

---

## Week 19: Stream processing
**Read:** DDIA Ch12, the sections on processing streams, time and windows, stream joins, and fault tolerance
**Concepts:** event time vs processing time, tumbling/hopping/sliding/session windows, late events, stream joins, exactly-once semantics, idempotence, checkpointing

**Hands-on (Python):**
- **Windowed aggregation:** a stream of ride requests with timestamps. Count requests per area per 1-minute tumbling window, then sliding windows. Add **late events** and handle them with a watermark.
- **Idempotent consumer:** reprocess the same events after a crash and get the same result (deduplicate by event ID).
- *Python skills:* generators as streams, `datetime`, windowing logic, `dict` state

**Practice questions:**
1. Event time vs processing time: why do results differ?
2. How do you handle an event that arrives 5 minutes late?
3. What does "exactly-once" really mean in practice?
4. Stream-table join: give an example (e.g. enrich clicks with user profiles).

**Design:** **Uber live location and surge pricing**.

---

## Week 20: Final chapters and capstone
**Read:** the remaining DDIA chapters after Ch12 (check your table of contents). They cover the future of data systems: combining tools, derived data, correctness, and ethics/privacy.
**Supporting topic:** microservices vs monolith. One video.
**Concepts:** derived data, unbundling databases, end-to-end correctness, privacy and responsibility

**Hands-on (capstone, optional but recommended):** clean up your best 2–3 builds (e.g. KV store + replication + sharding) into one small project with a README, tests, and a diagram. This becomes a portfolio piece.

**Practice questions (no hands-on, this part is conceptual):**
1. What does "unbundling the database" mean?
2. What's the difference between a system of record and derived data, and why does it matter?
3. What responsibilities do engineers have when building systems that store personal data?
4. Monolith vs microservices: when is a monolith the better choice?

**Design (review everything):** **YouTube/Netflix**, covering upload, storage, encoding pipeline, CDN, recommendations, and view counts. Label which week's concept each part uses.

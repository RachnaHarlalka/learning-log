# Week 0 Questions: Trade-offs in Data Systems Architecture

Questions are scenario-based and test whether you can **apply** the concepts in [../notes.md](../notes.md), the way system design interviews do. Write your answers in [../solved/](../solved/). Don't edit this file.

---

## Part A: Interview scenarios

These are the kind of open-ended questions asked in system design rounds. There's no single right answer: you're graded on **reasoning about trade-offs**.

For each one:
1. Say what you'd **clarify** first.
2. Lay out the **options**.
3. **Recommend** one, and say **what it costs you**.
4. Answer the **follow-up**.

Some include numbers, so do the arithmetic. Interviewers expect rough estimates.

---

**S1. Reports are killing checkout**
Your e-commerce site runs on a single PostgreSQL primary (2 TB of data, 3,000 writes/s at peak). Every day at 10:00, the finance and growth teams run dashboards (revenue by city, cohort retention) directly against it, and checkout p99 latency jumps from 120 ms to 3 s.
- (a) Explain *why* these two workloads interfere, in terms of what each one does to the database.
- (b) Option 1: add a read replica and point the dashboards at it. Option 2: build a warehouse fed from production. When is the replica *good enough*? What problems remain that only a warehouse solves?
- (c) What do you recommend (i) today, with 5 analysts and one database, and (ii) in 2 years, with 30 microservices each owning a database and 60 analysts?
- *Follow-up:* "Finance says the warehouse's revenue for yesterday doesn't match production." How could that happen, and which number is right?

**S2. Live dashboards for 300k sellers**
Your marketplace has 300,000 sellers. Each wants a dashboard showing "orders, revenue, and returns per hour, today", refreshing every 10 s. At peak, about 20,000 dashboards are open at once.
- (a) Why not run these queries on the OLTP database? Estimate the query rate it would face.
- (b) Why not use the existing warehouse, refreshed nightly?
- (c) Propose an architecture. What freshness and latency would you promise, and what do you give up compared with a traditional warehouse?
- *Follow-up:* "Can't we just precompute the numbers and cache them?" When does that work, and when doesn't it?

**S3. Questions that cross every silo**
A food-delivery company stores:
- orders in Postgres (orders service)
- payments in MySQL (payments service)
- restaurants in MongoDB
- support tickets in Zendesk (a SaaS product)
- app clickstream events, about 2 billion a day

Leadership asks: *"What's the refund rate per restaurant, and does it correlate with support tickets and app crashes?"*
- (a) Why can't anyone answer this today with one query?
- (b) Design the data flow. ETL or ELT, and why? Where do the clickstream events land, and why not straight into warehouse tables?
- (c) The orders team renames `amount` to `total_amount`. What breaks? How would you design the pipeline, or the organization, so this is caught?
- (d) Label each component of your design as a system of record or derived data.
- *Follow-up:* "Data scientists now want to train a model on the support-ticket text." Does your design support that?

**S4. Which price is true?**
A product shows ₹499 in search results (Elasticsearch), ₹549 on the product page (served from a Redis cache), and ₹599 in the products database. A customer complains.
- (a) Which price is correct, and what does that make the other two?
- (b) Give a plausible way each stale copy could have happened.
- (c) Design how a price change should flow so the derived copies stay in sync. What's the order of operations, and what happens if one step fails?
- (d) Ops asks: *"Do we need backups for Redis and Elasticsearch?"* Answer for each, weighing the cost of rebuilding. Then a twist: a team has started storing **shopping carts only in Redis**. Does your answer change?
- *Follow-up:* "Why not send every read to the products database and delete the cache and search index?"

**S5. Cloud or own hardware? Do the maths**
- **Company X:** B2B SaaS needing **120 servers**, steady (±10%) 24/7, with 4 experienced SREs already.
- **Company Y:** consumer app with **3 engineers**. It needs **10 servers** normally, peaking at **150** during cricket matches (about 6 hours a day, for 2 months a year).

Assume:
- **Cloud:** ₹60 per server-hour, paying only for what you use
- **Own hardware:** ₹25 per server-hour (hardware, power, and colocation), and you must own enough servers for the **peak**
- **Staff:** an SRE costs ₹40 lakh a year. Self-hosting means 2 more SREs for Y, and none extra for X.
- **Time:** 8,760 hours in a year, and 2 months ≈ 61 days

Questions:
- (a) Calculate the yearly cost of both options for X and for Y.
- (b) Recommend an option for each company, arguing **beyond** the numbers (risk, speed, expertise).
- (c) What hybrid setup would you suggest for Y?
- *Follow-up:* "What hidden costs does your calculation miss, on each side?"

**S6. Locked in, and the region is down**
Your startup is built entirely on one cloud provider's proprietary database, queue, and authentication services, in a single region.
- (a) That region goes down for 5 hours. What can you do *during* the outage? What could you have designed beforehand, and what would it have cost?
- (b) The vendor triples its prices. What makes migrating painful? Which earlier design choices would have reduced the pain, and what would *they* have cost?
- (c) Is multi-cloud worth it for a 10-person startup? Argue your position.
- *Follow-up:* An EU customer asks: *"Could a foreign government get our data through your cloud provider?"* What do you say?

**S7. Storage and compute in the cloud**
- (a) A junior engineer runs a self-managed Postgres on a cloud VM, storing its data on the VM's local NVMe disk "because it's fastest". What can go wrong? How do you fix it while keeping good performance?
- (b) After moving to network block storage (like EBS), writes sometimes take 200 ms while the CPU is idle. Explain why.
- (c) You have 80 TB of event data and analysts run about 30 heavy queries a day. Compare a fixed cluster with data on its local disks against object storage plus on-demand compute. Which do you choose, and what's its downside?
- (d) In your multi-tenant analytics SaaS, one large customer's queries slow everyone down. Give two ways to fix it.
- *Follow-up:* "Why do cloud-native databases like Aurora recover from failures faster than Postgres on a VM?"

**S8. Do we really need to distribute?**
An 8-person startup runs a monolith on one 32-core server: a 400 GB Postgres, 1,500 requests/s, and a nightly job over a 150 GB file that takes 12 minutes. The CTO wants to (1) split the app into microservices on Kubernetes, and (2) move the nightly job to a 20-node Spark cluster.
- (a) Evaluate each proposal: what do they gain, and what do they pay?
- (b) Which *legitimate* reasons could force them to distribute anyway? How would you meet each one with the **least** distribution possible?
- (c) List concrete signals that would tell you it's time to split into services.
- *Follow-up:* "A single server is a single point of failure. Doesn't that force us to distribute?"

**S9. The payment timeout**
The order service calls the payment service with `POST /charge {order_id: 81, amount: 2000}`, and the call times out after 3 seconds. The user is waiting.
- (a) List every possible state of the world after the timeout.
- (b) Why is retrying blindly dangerous? And why is "show the user an error" also a bad answer?
- (c) Design a safe retry. Who generates the idempotency key? Where is it stored? What does the payment service do when it sees a duplicate?
- (d) The charge succeeded, but the order service crashed before recording that. How does the system recover?
- *Follow-up:* "How long should the timeout be?"

**S10. Slow checkout and the half-finished order**
- (a) After Tuesday's deploys, checkout p99 went from 300 ms to 2.5 s. A checkout touches 7 services, and each one's logs and CPU graphs look normal. How do you find the culprit? What must every service do for your approach to work?
- (b) Later, an order is created in the Orders database, but the Inventory service fails to reserve stock in its own database. Now there's an order with no stock. Why can't an ordinary database transaction prevent this? Compare two-phase commit with compensating actions (sagas).
- *Follow-up:* "Why not merge Orders and Inventory into one service with one database?" When is that the right call?

**S11. Serverless or not?**
For each workload, decide and justify it on both cost and technical fit:
- (a) Making thumbnails of uploaded photos: bursty, 0–5,000 uploads a minute, 1 s each
- (b) Transcoding uploaded videos: 30–60 minutes each
- (c) A payment API that must answer in under 100 ms at p99, with a steady 3,000 requests/s, 24/7
- (d) An internal admin tool used about 20 times a day
- (e) A nightly weather simulation for an agri-tech startup: CPU-heavy, 4 hours on 500 cores, able to restart from checkpoints. What kind of workload is this really, and what infrastructure suits it?
- *Follow-up:* "Serverless means no ops work, right?"

**S12. Privacy as a design requirement**
An Indian fitness app stores:
- profiles in Postgres
- workout GPS traces (one point every 5 s) in an append-only data lake of Parquet files on S3
- events in Kafka (7-day retention)
- a nightly warehouse copy
- a recommendation model retrained monthly
- daily backups, kept for a year

It's expanding to the EU.
- (a) A user requests deletion under GDPR. Walk through each system: what must happen, which systems are hard, and why?
- (b) Propose designs that make deletion practical for the immutable lake and the backups.
- (c) Product wants to keep raw GPS forever "for future ML features". Push back with the risks *beyond* storage cost, and propose a minimization policy that still serves the product.
- (d) The EU regulator requires EU users' data to stay in the EU. What changes in the architecture?
- *Follow-up:* "We'll anonymize the data instead of deleting it. Problem solved?"

---

## Part B: Hands-on (Python)

Write your code in `../solved/code/`. Stub files with the exact function names are already there.
Run the tests from the week folder: `python3 solved/code/test_week00.py`

### B1. Feel the OLTP vs OLAP difference: `oltp_vs_olap.py`
*Concept: point queries vs aggregates (Table 1-1).*
Use `sqlite3` with an in-memory database.
1. `create_orders_db(conn, n_orders=200_000, n_customers=20_000, seed=0)`
   Create the table `orders(id INTEGER PRIMARY KEY, customer_id, store, amount_paise, created_at)` and insert random rows. `store` is one of `STORES`. Store money as **integer paise**, never floats.
2. `get_order(conn, order_id)`: point query by primary key. Returns the row, or `None` if not found.
3. `orders_for_customer(conn, customer_id)`: all of a customer's orders
4. `revenue_by_store(conn) -> dict`: `{store: total_paise}`, an aggregate query
5. `add_customer_index(conn)`: create an index on `customer_id`
6. `best_time(fn, *args, repeat=5) -> float`: the fastest of `repeat` runs, in seconds
7. In `__main__`, time all three queries **before and after** adding the index, and print a table.

**Answer in a comment:** which query sped up, which didn't, and why? What does this suggest about why analytical systems use different storage?

### B2. Mini ETL pipeline: `etl_pipeline.py`
*Concept: data silos → ETL → data warehouse → analyst query.*
`setup_sources()` is already written for you. It creates **two separate operational databases** (a stores service and an orders service) with deliberately messy data: amounts stored as text, cancelled and test orders, and orders pointing to a store that doesn't exist.
1. `extract(orders_db, stores_db) -> (orders, stores)`: lists of dicts
2. `transform(orders, stores) -> list[dict]`. For each order:
   - keep only `status == "completed"`
   - drop orders whose `store_id` doesn't exist
   - convert `amount` text (e.g. `"1234.50"`) to integer `amount_paise` (`123450`), using `Decimal` and not `float`
   - add `store_name` and `city` from the stores data (this join across silos is impossible in a single OLTP query)
   - output the keys: `order_id, store_name, city, amount_paise, order_date (YYYY-MM-DD), month (YYYY-MM)`
3. `load(warehouse, rows) -> int`: create the `sales` table and insert the rows. **Running it twice must not duplicate rows.**
4. `revenue_by_store_for_month(warehouse, month) -> dict`: the analyst's question, "total revenue of each store in January?"
5. `run_pipeline(n_orders=2_000, seed=0)`: wire everything together and return the warehouse connection.

**Answer in a comment:** is the warehouse a system of record or derived data? If you deleted it, what would you do?

### B3. System of record vs derived data: `derived_data.py`
*Concept: derived data is redundant, can be re-created, and needs a process to stay up to date.*
`ProfileStore` (the system of record) is already written.
1. `build_city_index(store) -> dict[city, set[user_id]]`: a derived index
2. `ProfileCache(store)` with `get(user_id)` (cache-aside: check the cache, otherwise read the store and remember the result), `invalidate(user_id)`, and `hits`/`misses` counters
3. `update_profile(store, cache, city_index, user_id, profile)`: write to the **system of record first**, then bring **both** derived systems up to date. Remove a city key from the index once it has no users left.
4. In `__main__`, demonstrate all three:
   - (a) updating the store *without* propagating leaves the cache stale
   - (b) `update_profile` fixes it
   - (c) delete the index entirely, rebuild it from the store, and show it matches

### B4. Cloud vs self-hosting cost model: `cloud_cost.py`
*Concept: predictable load → self-host is cheaper; variable load → cloud elasticity wins.*
1. `machines_needed(load_rps, capacity_per_machine) -> int`: round up
2. `self_hosted_cost(hourly_load, capacity_per_machine, cost_per_machine_hour)`: you must own enough machines for the **peak**, every hour
3. `cloud_cost(hourly_load, capacity_per_machine, cost_per_machine_hour, markup=1.5)`: pay only for the machines needed **each hour**, but at a markup
4. `utilization(hourly_load, capacity_per_machine) -> float`: average load divided by the capacity of the owned (peak-sized) fleet
5. In `__main__`, compare 30 days of a **steady** web app against a **spiky** analytics workload, and print which option is cheaper for each.

**Answer in a comment:** what real-world costs does this model ignore that could change the answer? (Think about the chapter's points on skills and staff.)

### B5. (Stretch, no tests) Network call vs function call: `network_vs_function.py`
*Concept: "a call to another service is vastly slower than calling a function in the same process."*
Time 100,000 calls to a local `add(a, b)` function, then 500 HTTP requests to a tiny local server (`http.server` in a thread) that does the same addition. Print the time per call for each, and the ratio between them. This is even on the *same machine*, with no real network.

### B6. Right to be forgotten in an append-only log: `user_events.py`
*Concept: GDPR erasure vs immutable logs and derived data; data minimization (§13).*
Events are stored as **one JSON object per line**, appended to a file. Each event looks like `{"user_id": 7, "type": "view", "ts": "2026-03-01", "data": {...}}`.
1. `append_event(log_path, event)`: append one line, never modifying existing lines
2. `read_events(log_path) -> list[dict]`: return an empty list if the file doesn't exist
3. `build_event_counts(log_path) -> dict[user_id, int]`: **derived data**, the number of events per user
4. `forget_user(log_path, user_id) -> int`: erase every event of that user and return how many were removed. You can't edit lines in place in an append-only file, so **rewrite the file without them**: write a temporary file, then swap it in with `os.replace` so a crash never leaves a half-written log.
5. `forget_everywhere(log_path, derived_counts, user_id) -> int`: erase from the log **and** from the derived counts dict. Forgetting the source isn't enough.
6. `purge_older_than(log_path, cutoff) -> int`: **data minimization**. Delete events whose `ts` is before `cutoff` (`"YYYY-MM-DD"` strings compare correctly as text), and return the number removed.

**Answer in a comment:** your `forget_user` rewrites the *whole file* to delete one user. Why would that be a problem with 10 TB of logs? Can you think of a better approach? (Week 5 has one answer.)

### B7. (Stretch, no tests) Mini distributed tracing: `tracing.py`
*Concept: observability. A tracer records "which client called which server for which operation and how long each call took" (§10).*
Write a decorator `@traced(service, operation)` that records a **span** for every call: `trace_id, span_id, parent_id, service, operation, duration_ms`. Use `contextvars` to remember the current span, so nested calls get the right parent.
Simulate a `checkout` request in the `frontend` service that calls `auth`, `inventory` (which calls `db`), and a slow `payment` service, using `time.sleep` for fake latency. Print the spans as an indented tree, then print which span was slowest. This is how a tracing tool finds the problem in a 6-service request.

---

## Part C: Design problem (full interview round, 45 minutes)

**"Design the data platform for a supermarket chain."**
**Scale:**
- 200 stores, about 3 million receipts a day (≈40 million line items)
- a website and app with about 50,000 online orders a day
- 6 engineers

Spend 30 minutes on your own attempt **before** watching any video, then answer the follow-ups out loud as if an interviewer asked them.
0. **Estimate:** how much raw sales data per day and per year? (Assume ~100 bytes per line item.) Does that change what kinds of systems you need?
1. **Operational systems:** list at least 4 (e.g. checkout/POS, inventory, website orders, suppliers). Does each get its own database? Why?
2. **Analytics:** how do analysts answer *"total revenue per store in January"* and *"how many more bananas did we sell during the promotion?"* Draw the data flow from operational systems to the warehouse. ETL or ELT?
3. **Data science:** the team wants to analyse product-review text and shelf photos. Where does that data live?
4. **Back to the product:** a "people who bought X also bought Y" model is trained on analytics data. How does it reach the website?
5. **Fraud:** card fraud at checkout must be blocked within seconds, not tomorrow. What changes?
6. **Label** every box in your diagram as *system of record* or *derived*.
7. **Cloud or self-host** for (a) the warehouse and (b) the checkout systems in stores. Justify your choices.
8. **Architecture style:** should 6 engineers use microservices? Would serverless suit the nightly ETL job?
9. **Privacy:** a loyalty-card customer invokes the **right to be forgotten**. List every place their data lives, including derived data and the ML model. How do you erase it? Which data would you **not collect or keep at all**? Which compliance standard applies to card payments?

**Interviewer follow-ups** (answer each in 2–3 sentences):
- F1. "A store's internet link goes down for 2 hours. What happens at its tills?"
- F2. "The banana-promotion numbers in the warehouse are 3% lower than the POS system's. How do you investigate?"
- F3. "Finance wants yesterday's numbers by 7 AM, but the ETL takes 5 hours and starts at midnight. Then they want them hourly. What changes?"
- F4. "Why not run the whole thing on one big Postgres?" At this scale, where exactly would that break?

Write it in [../solved/design.md](../solved/design.md).

# Week 0 MCQs: Trade-offs in Data Systems Architecture

32 scenario questions, each with one correct answer. They test whether you can **apply** the ideas, not recall the book's wording. Several options are partly true; pick the **best** one, the answer a senior engineer would defend.

- Write your answers in [../solved/mcq-answers.md](../solved/mcq-answers.md)
- Check your score from the repo root: `python3 tools/check_mcqs.py weeks/week-00-tradeoffs`. It shows which questions you got wrong, not the right answers.
- Target: **26/32 or better**. For each miss, work out *why* the right answer beats the one you picked before reading the key.

---

### Operational vs analytical

**1.** Your e-commerce site runs on a single PostgreSQL primary. Every morning at 10:00, when the finance team runs its revenue dashboards directly on it, checkout p99 latency jumps from 80 ms to 2 s. What's the best **long-term** fix?
- A) Add an index on `orders.amount`
- B) Double the Postgres server's CPU and RAM
- C) Move reporting off the primary, onto a replica or a warehouse fed from it
- D) Ask finance to run the reports at midnight

**2.** Product wants each of your 200,000 marketplace sellers to see a live "orders per hour today, by category" dashboard that refreshes every few seconds. Which design fits best?
- A) A real-time analytics store (e.g. ClickHouse, Pinot, Druid) fed by an event stream of orders
- B) Run the aggregate query on the OLTP primary for every refresh
- C) A nightly ETL job into the data warehouse
- D) Compute the numbers once a day and cache them in Redis for 24 hours

**3.** Each card payment must be scored against the customer's last 90 days of behaviour, then approved or declined **within 100 ms**. The data warehouse is refreshed nightly. Why is the warehouse alone not enough?
- A) Warehouses can't store 90 days of data
- B) Warehouses don't support aggregate functions
- C) Fraud models can only be trained on OLTP databases
- D) Its data is up to a day stale, and it's built for big analytical scans, not low-latency answers to individual requests

**4.** To join orders (Postgres), payments (MySQL), and refunds (a SaaS payments provider), an analyst's Python script queries all three **production** systems at 2 PM every day. What's the biggest problem?
- A) Python is too slow for analytics
- B) It loads production systems at peak time, gets no consistent snapshot or history, and breaks whenever any team changes its schema
- C) You can't query MySQL and Postgres from the same script
- D) SaaS providers don't offer APIs

**5.** A data scientist says: *"The warehouse kept only 8 columns of the clickstream, and I need the `referrer` field they threw away last year."* What practice would have prevented this?
- A) Keep the raw events in a data lake, and let each consumer derive the views it needs
- B) Normalize the warehouse schema further
- C) Switch the warehouse to an HTAP database
- D) Increase the warehouse's retention period

**6.** Which situation is the **best** fit for an HTAP database instead of a data warehouse?
- A) The CFO's quarterly report, which combines data from 40 microservices
- B) Data scientists training a model on product photos
- C) A loan app that, for each application, scans the applicant's last 10,000 transactions and immediately writes a decision record
- D) A nightly batch export of data to partners

### Systems of record vs derived data

**7.** Search results (Elasticsearch) show a product at ₹499, but the products database says ₹599. The customer is checking out. Which price should checkout use?
- A) ₹499, because the search index was updated more recently
- B) The average of the two
- C) Whichever system answers faster
- D) ₹599, because the products database is the system of record; the search index is derived and can lag

**8.** Redis is used **purely as a cache** in front of Postgres. An engineer proposes cancelling the Redis backups to save money. Is that safe?
- A) No, losing Redis would lose customer data
- B) No, Redis is always a system of record
- C) Yes. The cache is derived and can be rebuilt from Postgres, but expect a load spike on Postgres while it refills
- D) Caches can't be backed up anyway

**9.** Later, a team starts storing shopping carts **only** in that same Redis, not in Postgres. What changes?
- A) Nothing. Redis is a caching tool, so its data is always derived.
- B) Redis is now the system of record for carts, so it needs durability, replication, and backups
- C) Postgres becomes derived from Redis
- D) Carts are automatically copied to Postgres

### Cloud vs self-hosting

**10.** A 3-engineer startup sees 10× traffic for the 3 days of a Diwali sale and is quiet the rest of the year. A hosting provider offers dedicated servers that are cheaper per hour than the cloud. What's the best choice?
- A) Buy enough servers for the Diwali peak
- B) Buy servers for normal load and accept outages during Diwali
- C) Build their own datacenter, for full control
- D) Use cloud managed services with autoscaling. Elasticity and needing no ops team outweigh the higher hourly price.

**11.** A mature company runs 400 servers at about 75% utilization, 24/7, with stable load and an experienced infrastructure team. Its cloud bill is ₹20 crore a year. What's the strongest argument for moving **some** workloads to self-hosted hardware?
- A) Steady, high-utilization load plus existing ops skills is exactly when owning hardware tends to be cheaper
- B) Self-hosted hardware never fails
- C) Clouds can't run 400 servers
- D) Self-hosting means you no longer need an operations team

**12.** You built on a proprietary cloud database with a non-standard API, and the vendor announces a 3× price increase. Which risk did you underestimate?
- A) Multitenancy
- B) Cold starts
- C) Vendor lock-in: with no compatible alternative, migrating is expensive, and you can't keep running the old version yourself
- D) Data silos

**13.** A manager says: *"We're moving to the cloud, so we can let the ops team go."* What's wrong with that?
- A) Nothing. The cloud does all operations.
- B) Operations changes rather than disappearing: choosing and integrating services, cost control, quotas, security, monitoring, and debugging outages all remain
- C) The cloud needs more hardware maintenance than on-prem
- D) Cloud providers require customers to have staff on site

**14.** Your monthly cloud bill doubled while traffic stayed flat. Which practice was most likely neglected?
- A) RAID configuration
- B) OS patching
- C) Planning disk purchases
- D) Cost visibility: knowing which resources are used for what (idle instances, forgotten test clusters, oversized machines)

### Cloud-native architecture

**15.** A self-managed Postgres on a cloud VM keeps its data on the VM's **local NVMe disk**. The VM is resized to a bigger instance type. What's the risk?
- A) None. The local disk moves with the VM.
- B) The data can be lost, because a resized VM may move to a different physical machine and local disks don't come with it
- C) Bigger VMs have smaller disks
- D) Postgres can't use NVMe disks

**16.** A database on network-attached block storage (like EBS) shows occasional 200 ms spikes on simple writes, while CPU sits idle. What's the most likely cause?
- A) Too many indexes
- B) The CPU is too slow
- C) Missing RAID
- D) Every disk I/O is really a network call, so hiccups on the storage network show up as I/O latency

**17.** You have 50 TB of event data. Analysts run about 20 heavy queries a day, each needing lots of CPU for a few minutes. Which architecture fits best?
- A) Keep the data in object storage and start compute only when a query runs (storage and compute separated)
- B) A fixed cluster of 50 large servers, with the data copied to their local disks
- C) Put all 50 TB on one VM's virtual disk
- D) Load it into the OLTP database

**18.** In your multi-tenant analytics SaaS, one customer's massive query makes every other customer's dashboards slow. This is mainly a problem of:
- A) Data residency
- B) Vendor lock-in
- C) Multitenancy: tenants need resource isolation and limits
- D) ETL

### Distributed vs single node

**19.** An 8-person team's monolith handles 2,000 requests/s on one 16-core server with a 300 GB Postgres. An architect proposes splitting it into 12 microservices on Kubernetes "for scalability". What's the best response?
- A) Scale isn't a problem on one machine, and microservices solve team coordination, which 8 people don't need. Keep the monolith and add a standby replica for availability.
- B) Do it now, because microservices always scale better
- C) Split into exactly 2 services as a compromise
- D) Rewrite in a faster language instead

**20.** A batch job processes a 200 GB file. DuckDB on one 64 GB machine finishes in 6 minutes; a 20-node Spark cluster takes 9. What's the most plausible explanation?
- A) Spark can't read files bigger than 100 GB
- B) DuckDB caches the answer in advance
- C) Distributed overhead (moving data between nodes, coordination, serialization) outweighs the extra cores at this size
- D) The cluster must have had a failed node

**21.** The order service calls the payment service: "charge ₹2,000". The call times out after 5 seconds. What's the safest thing for the order service to do?
- A) Mark the payment as failed and ask the user to pay again
- B) Retry with the same idempotency key, so the payment service can recognize a duplicate and won't charge twice
- C) Retry immediately as a new request
- D) Assume it succeeded and ship the order

**22.** After Tuesday's deploys, checkout p99 rose from 300 ms to 2.5 s. A checkout touches 7 services, and none of them show anything unusual in their own logs or CPU graphs. What do you need?
- A) Bigger servers for all 7 services
- B) More detailed logging in each service
- C) Roll back every deploy from the past month
- D) Distributed tracing with a trace ID passed through every call, to see how long each hop takes

**23.** An order is committed in the Orders database, then the Inventory service fails to reserve stock in its own database. Now there's an order with no stock behind it. What's the core issue, and what's the typical fix?
- A) No single transaction spans both databases, so the application must restore consistency, e.g. with a compensating action that cancels the order, or a saga
- B) Postgres has a bug
- C) The inventory database needs more replicas
- D) Use a bigger timeout

**24.** Two microservice teams share one Postgres database to "avoid duplicating data". Six months later, the Orders team can't rename a column. Why?
- A) Postgres doesn't allow renaming columns
- B) The database is too large to change
- C) The shared schema has become part of the other team's API, so any change can break their service
- D) Renaming needs a distributed transaction

### Microservices, serverless, HPC

**25.** Users upload photos in bursts: some hours have none, others have 5,000 a minute. Making a thumbnail takes about 1 second. Is serverless a good fit?
- A) No, serverless can't handle images
- B) Yes. It's event-driven, bursty, and short, so you pay only per execution and scaling is automatic.
- C) No, you need a fixed fleet sized for the peak
- D) Only if the photos are smaller than 1 KB

**26.** The team wants to transcode uploaded videos with serverless functions, and each video takes about 40 minutes. What's the main concern?
- A) Serverless can't read video files
- B) It's always more expensive than VMs
- C) Cold starts would add 40 minutes
- D) Execution time limits: functions are usually capped well below 40 minutes, so split the work into chunks or use containers or batch jobs

**27.** A customer-facing API on serverless has p99 latency of 3 seconds, but only for the first requests after a quiet period. What's the cause?
- A) Cold starts: a new function instance has to be started after idling
- B) The database is full
- C) The CDN is misconfigured
- D) The functions are too small

**28.** A bank trains its credit-scoring model on an HPC-style cluster that checkpoints every hour; when a node fails, the job restarts from the last checkpoint. Should the bank's **online loan-approval API** handle failures the same way?
- A) Yes, checkpointing works for everything
- B) Yes, losing an hour is fine for an API
- C) No. An online service must keep serving through failures using redundancy and failover, not by stopping and restarting.
- D) No, because APIs can't be checkpointed

### Law, privacy, compliance

**29.** A user requests deletion under GDPR. Their data lives in Postgres (system of record), Elasticsearch, Redis, nightly warehouse copies, append-only Parquet files in S3, backups, and an ML model trained on last year's data. An engineer deletes the Postgres row and closes the ticket. What's wrong?
- A) Nothing. Deleting from the system of record is enough.
- B) Copies remain in the derived systems, the immutable lake files, and the backups, and the model was trained on the data. Deletion must be carried through to all of them.
- C) They should have deleted the Elasticsearch document instead
- D) GDPR deletion only applies to backups

**30.** Your mobile app records precise GPS every minute "in case it's useful for future features". Legal flags it. Which principle applies?
- A) Encrypt it and keep it forever
- B) Move it to cheaper storage
- C) Anonymize the user ID and keep everything
- D) Data minimization: collect only what an explicit purpose needs (e.g. coarser location, less often), and delete it when that purpose is served

**31.** Logs are kept forever in append-only files in S3, which are petabytes in size. Which design lets you honour deletion requests **without rewriting petabytes** each time?
- A) Encrypt each user's data with their own key, and delete the key on request (crypto-shredding)
- B) Delete the whole bucket
- C) Add a `deleted=true` flag in Postgres
- D) Keep the logs but make the bucket private

**32.** An Indian fintech expands to Germany, and the regulator requires German users' personal data to be stored and processed in the EU. What's the right architectural change?
- A) Keep the single Mumbai database, but encrypt German users' data
- B) Add an EU region and keep German users' data and processing there (data residency forces distribution)
- C) Put a CDN node in Frankfurt
- D) Store German users' data only in the warehouse

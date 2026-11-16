# Week 1 Notes: Defining Nonfunctional Requirements (DDIA Ch2)

> Summarized from the chapter text you shared (the full chapter). Add your own thoughts in **My additions** at the end.

---

## 1. Functional vs nonfunctional requirements
- **Functional:** *what* the app does: its screens, buttons, and operations.
- **Nonfunctional:** *how well* it does it: fast, reliable, secure, legally compliant, maintainable. These are often **not written down** because they seem obvious, but an app that's unbearably slow or unreliable *might as well not exist*.
- This chapter covers four of them: **performance**, **reliability**, **scalability**, and **maintainability**.

## 2. Case study: social network home timelines
**Load assumptions** (X/Twitter-style):

| Quantity | Value |
|---|---|
| Posts | **500M/day ≈ 5,800/s** on average, spiking to **150,000/s** |
| Follows per user | **200** on average, followed by 200 on average (a very wide range: celebrities have **100M+** followers) |
| Users online at once | **10M** |
| Freshness goal | Followers see a post **within 5 s** |

**Approach 1: query at read time, with polling.**
- One SQL query joins `follows`, `posts`, and `users`, sorts by timestamp, and takes the latest 1,000 posts.
- **Polling** every 5 s with 10M users online means **2M queries/s**.
- Each query looks up the recent posts of ~200 followed accounts, so **2M × 200 = 400M lookups/s**.
- Users who follow tens of thousands of accounts make it far worse.

**Approach 2: materialize the timelines (fan-out on write).**
- **Push** new posts to online followers instead of making them poll.
- **Precompute** each user's home timeline, like **delivering a letter to each follower's mailbox**. Reading a timeline is then just a cache read, and clients **subscribe** to a stream of new posts.
- **Fan-out:** the factor by which one request multiplies into downstream requests.
- **Cost:** 5,800 posts/s × 200 followers = **~1.16M timeline writes/s**. That's a lot, but **far less than 400M lookups/s**.
- During spikes, **enqueue** the deliveries: posts show up a bit later, but **reads stay fast** because they come from the cache.
- **Materialization:** precomputing and updating a query's results. The timeline cache is a **materialized view**. It **speeds up reads at the cost of more work on writes**, and the timelines are **derived data**.

**The extreme cases:**
- **A user following a huge number of active accounts** has a very high write rate into their timeline. They can't read it all anyway, so it's **OK to drop some writes** and show a sample.
- **A celebrity with millions of followers:** dropping writes is *not* OK. Instead, **store celebrity posts separately and merge them in at read time** (a hybrid approach). Celebrities still need a lot of infrastructure.

## 3. Describing performance
| Metric | Definition | Unit | Case-study example |
|---|---|---|---|
| **Response time** | Time from the user's request until they get the answer | seconds / ms / µs | Time to load the home timeline; time until a post reaches followers |
| **Throughput** | Requests (or data volume) processed per second. The hardware sets a maximum. | "somethings per second" | Posts/s, timeline writes/s |

- **They're linked through queueing.** At low load, response time is low. As throughput approaches the maximum, new requests **wait behind earlier ones**, and response time **rises sharply**.
- **Users care about response time. Throughput determines how many servers you need, and so the cost.**
- **Scalable** means the maximum throughput can be **significantly increased by adding resources**.

### When an overloaded system won't recover
- **Vicious cycle:** a long queue makes response times so slow that clients **time out and resend** their requests. That raises the load further: a **retry storm**.
- **Metastable failure:** even after the original load drops, the system **stays overloaded** until it's rebooted or reset. This causes serious production outages.

| Defence | Side | What it does |
|---|---|---|
| **Exponential backoff** (with randomization) | Client | Wait longer, and a random amount, between retries |
| **Circuit breaker** / **token bucket** | Client | Temporarily stop calling a service that recently failed or timed out |
| **Load shedding** | Server | Proactively **reject** requests when nearing overload |
| **Backpressure** | Server | Tell clients to **slow down** |
| Queueing and load-balancing algorithms | Both | The choice of algorithm affects behaviour under load |

## 4. Latency and response time: precise terms
```
client ──request──>  [queue] ──> [service processing] ──> [queue] ──response──> client
       network latency  queueing delay    service time      queueing delay   network latency
<──────────────────────────── response time (what the client sees) ────────────────────────>
```
- **Response time:** what the client sees, including **every delay anywhere**.
- **Service time:** how long the service is **actively processing** the request.
- **Queueing delay:** waiting for a CPU, or for an outbound network buffer, at any point along the way.
- **Latency:** a catch-all for time when the request is **not being actively processed** (it's *latent*). **Network latency** is the time spent travelling through the network.
- **Why the same request varies:** context switches, lost packets and TCP retransmission, **garbage-collection pauses**, page faults, even rack vibration.
- **Head-of-line blocking:** a server handles only a few things in parallel (limited by its cores), so **a few slow requests hold up the fast ones behind them**. The client sees a slow response even though its own service time was short.
- Queueing delay is **not** part of service time, so **measure response time on the client side**.

## 5. Mean, median, and percentiles
- Response time is a **distribution**, not a single number. Variation in network delay is called **jitter**.
- **Mean (average):** useful for **estimating throughput limits**, but not the "typical" experience, because it doesn't tell you how many users actually saw that delay.
- **Median = p50:** half of requests are faster, half slower. A good measure of the **typical** wait.
- **p95 / p99 / p999 (99.9th):** how bad the outliers are. p95 = 1.5 s means 5 in 100 requests take 1.5 s or longer.
- **Tail latencies** (high percentiles) directly hurt user experience.
  - **Amazon** sets internal targets at **p99.9**, because the slowest requests often belong to customers with the **most data, meaning the most purchases, meaning the most valuable customers**.
  - **p99.99 was judged too expensive.** Very high percentiles are dominated by random events outside your control, with **diminishing returns**.

## 6. The user impact of response times
- Faster is better, but **reliable data quantifying it is hard to find**. Many famous statistics are shaky:
  - **Google 2006:** 400 ms → 900 ms gave −20% traffic. **Google 2009:** +400 ms gave only −0.6% searches. **Bing 2009:** +2 s gave −4.3% ad revenue.
  - **Akamai:** +100 ms gave up to −7% conversions, **but** very fast pages *also* converted worse, because the fastest pages were often 404s with no content. The study **didn't separate content from speed**, so it's probably meaningless (a **confounding variable**).
  - **Yahoo**, controlling for result quality: **20–30% more clicks** when results were ≥ 1.25 s faster.
- **Lesson:** be sceptical of latency statistics; check whether the study controlled for confounders.

## 7. Using response time metrics
- **Tail latency amplification:** one user request calls **many backends** (even in parallel) and must wait for the **slowest**. One slow call makes the whole request slow, so the more calls, the higher the share of slow user requests.
- **SLO (service level objective):** a target, e.g. **p50 < 200 ms, p99 < 1 s, and ≥ 99.9% of valid requests succeed**.
- **SLA (service level agreement):** a **contract** saying what happens if the SLO is missed, e.g. refunds.
- Defining good availability metrics for SLOs and SLAs is harder than it looks.

## 8. Computing percentiles
- Dashboards use a **rolling window**, e.g. the last 10 minutes of response times, recomputed every minute.
- **Simplest method:** keep every response time in the window and sort the list each minute.
- **Cheaper approximations:** **HdrHistogram, t-digest, OpenHistogram, DDSketch**. Good accuracy with little CPU and memory.
- ⚠️ **Averaging percentiles is mathematically meaningless**, whether across time or across machines. The right way to combine is to **add the histograms**, then read the percentile from the combined histogram.

## 9. Reliability and fault tolerance
**"Working correctly" means:**
1. it does what the user expected
2. it tolerates user mistakes and unexpected use
3. performance is good enough under the expected load and data volume
4. it prevents unauthorized access and abuse

**Reliability ≈ continuing to work correctly, even when things go wrong.**

| | Meaning |
|---|---|
| **Fault** | One **part** stops working correctly: a disk, a machine, an external dependency |
| **Failure** | The **system as a whole** stops providing the required service, i.e. **misses its SLO** |

- It's the **same event viewed at different levels**. A failed disk is a *failure* for the disk, but only a *fault* for a system that keeps copies elsewhere.
- **Fault-tolerant:** keeps providing the service despite **certain** faults.
- **Single point of failure (SPOF):** a part whose fault escalates into a failure of the whole system.
- **Case-study example:** a fan-out machine crashes mid-delivery. Another machine must take over **without missing or duplicating posts**. That's **exactly-once semantics** (Ch12).
- Fault tolerance is **always limited** to certain numbers and types of faults, e.g. 2 disks, or 1 of 3 nodes. (Surviving a black hole would need "web hosting in space".)
- **Fault injection:** deliberately trigger faults, e.g. randomly kill processes. Many critical bugs are in **poor error handling**, and this keeps the recovery paths exercised. **Chaos engineering** is the discipline built around such experiments.
- **Prevention beats cure when there's no cure**, as with **security**: leaked data can't be un-leaked.

## 10. Hardware faults
| Component | Failure rate |
|---|---|
| Magnetic hard disks | **2–5% per year**, so 10,000 disks means **about 1 failure a day** |
| SSDs | **0.5–1% per year**. Uncorrectable errors about **once per year per drive**, even when new, which is more often than HDDs. |
| Other parts | Power supplies, RAID controllers, and memory fail less often |
| CPUs | **~1 in 1,000 machines** has a core that sometimes **computes wrong results**: maybe a crash, maybe a **silently wrong answer** |
| RAM | Cosmic rays or defects. **>1% of machines with ECC** hit an uncorrectable error each year (usually a crash). Some access patterns can flip bits (rowhammer). |
| Whole datacenter | Power or network misconfiguration, or destruction (fire, flood, earthquake). Solar storms can damage grids and undersea cables. |

These are rare on a small system, but **at large scale hardware faults are part of normal operation**.

**Tolerating hardware faults through redundancy:**
- **Within a machine:** RAID, dual power supplies, hot-swappable CPUs, datacenter batteries and diesel generators. These can keep one machine up for years.
- Redundancy works best when faults are **independent**, but **component failures are correlated** in practice. Whole racks and datacenters still go down.
- **Cloud approach:** care less about individual machines and **tolerate node loss in software**.
  - **Availability zones** tell you which resources are physically together, and therefore likely to fail together.
  - The techniques in this book survive the loss of **machines, racks, or whole zones** (Ch6, Ch10).
- **Operational bonus: rolling upgrades.** Patch and restart one node at a time with no downtime. A single server needs **planned downtime** to reboot (Ch5).

## 11. Software faults
**Highly correlated:** every node runs the same code with the same bugs. That makes them harder to anticipate, and they cause **more system failures than hardware faults do**.

**Examples:**
- **A bug that hits every node at once:**
  - **June 30, 2012:** a **leap second** hung many Java apps at the same time, through a Linux kernel bug.
  - Certain **SSD models all die after exactly 32,768 hours** of operation (a firmware bug), and the data is unrecoverable.
- **A runaway process** exhausting a shared resource: CPU, memory, disk, bandwidth, threads. Or a client-library bug that sends far more requests than expected.
- **A dependency** that slows down, hangs, or returns **corrupted** responses.
- **Emergent behaviour** from interactions between systems that each pass their tests in isolation.
- **Cascading failures:** one component's problem overloads the next, which slows down and brings down the one after.

**Root cause pattern:** a **dormant bug** plus an **assumption about the environment** that is usually true, until one day it isn't.

**No quick fix, but many small things help:**
- think carefully about assumptions and interactions
- thorough testing
- process isolation
- **let processes crash and restart**
- avoid feedback loops such as retry storms
- measure, monitor, and analyse in production

## 12. Humans and reliability
- **Configuration changes by operators were the leading cause of outages.** Hardware played a role in only **10–25%**.
- **"Human error" is a symptom, not a cause.** It points to a problem in the **sociotechnical system**. Complex systems also have **emergent behaviour**.
- **Technical measures:**
  - thorough testing, including **property testing** on many random inputs
  - **fast rollback** of config changes
  - **gradual rollouts**
  - clear monitoring and **observability**
  - **interfaces that make the right thing easy and the wrong thing hard**
- **Reality:** these cost time and money, and businesses often choose features over testing. When a preventable mistake happens, **blaming the individual makes no sense**: the problem is the **organization's priorities**.
- **Blameless postmortems:** people share full details without fear of punishment, so the organization learns. The outcome may be changed priorities, investment, or incentives.
- **Be suspicious of simplistic answers:**
  - ❌ "Bob should've been more careful."
  - ❌ "Rewrite it in Haskell."
  - ✅ Learn how the system really works from the people who run it every day, then improve it.

## 13. How important is reliability?
- It isn't only for nuclear plants. Business bugs cost productivity (and **legal risk** when figures are reported wrong), and e-commerce outages cost **revenue and reputation**.
- **A few minutes or hours of outage is often tolerable, but permanent data loss or corruption is catastrophic.** Think of a parent's lifetime of family photos.
- **The Post Office Horizon scandal (UK, 1999–2019):** accounting-software bugs showed shortfalls, and **hundreds of branch managers were convicted** of theft or fraud. It's probably the **largest miscarriage of justice in British history**, enabled by the legal **presumption that computers work correctly**.
- **Cutting reliability is sometimes OK** (e.g. a prototype for an unproven market), but **do it consciously** and keep the consequences in mind.

## 14. Scalability
- **Scalability** is a system's **ability to cope with increased load** (e.g. 10k → 100k concurrent users, or 1M → 10M).
- **"You're not Google, just use a relational database."** Whether that's right depends on the app.
  - **Startup / new product:** keep things **simple and flexible** so you can change as you learn. Building for hypothetical scale is **premature optimization** at best, and at worst **locks you into an inflexible design**.
- **"X is scalable" is meaningless.** Ask instead:
  - If the system grows **in this particular way**, what are our options?
  - How do we add computing resources for the extra load?
  - With current growth projections, **when do we hit the limits** of the current architecture?
- Once you're popular, you'll learn **where the bottlenecks actually are**. Optimize then.

## 15. Understanding load
- **First describe the current load**, then ask "what if it doubles?"
  - Usually **throughput**: requests/s, GB of new data per day, checkouts per hour.
  - Sometimes the **peak** of something, e.g. users online at the same time.
- **Other characteristics that shape scaling:** read/write ratio, **cache hit rate**, **items per user** (followers in the case study). **Is your bottleneck the average case or a few extreme cases?** (Think of celebrities.)
- **Two ways to ask about growth:**
  1. Load goes up and resources stay the same: **what happens to performance?**
  2. Load goes up and performance must stay the same: **how many more resources do you need?**
- **Goal:** stay within the SLA **at minimum cost**. Some hardware is more cost-effective than others, and that changes over time.
- **Linear scalability:** 2× resources handles 2× load. Occasionally you get *better* than linear (economies of scale, smoother peaks). **Usually cost grows faster than linear**, e.g. a single write does more work when there's more data.

## 16. Shared-memory, shared-disk, and shared-nothing architectures
| Architecture | What it is | ✅ | ❌ |
|---|---|---|---|
| **Shared-memory** (**vertical scaling / scaling up**) | One bigger machine, with threads and processes sharing RAM | Simple | **Cost grows faster than linear** (2× the hardware costs ≫ 2×), bottlenecks mean it won't handle 2× the load, and individual cores aren't getting much faster |
| **Shared-disk** | Several machines (own CPU and RAM) sharing a disk array over a fast network (**NAS / SAN**) | Traditional on-prem warehousing | **Contention and locking overhead** limit scaling |
| **Shared-nothing** (**horizontal scaling / scaling out**) | Many nodes, each with its own CPU, RAM, and disks, coordinating in software over a normal network | Can scale **linearly**, uses the best price/performance hardware, adjusts to load easily, **fault tolerance across datacenters and regions** | Needs explicit **sharding** (Ch7) and brings all the complexity of distributed systems (Ch9) |

- **Cloud-native databases** (separate storage and compute) look *like* shared-disk: many compute nodes, one storage service. But the storage service has a **specialized database API**, not a generic filesystem or block device, so it avoids the old scaling problems.

### Principles for scalability
- **There's no "magic scaling sauce".** Architecture at scale is **specific to the application**.
  - 100,000 requests/s × 1 kB and 3 requests/min × 2 GB are **both ~100 MB/s**, yet need **very different** systems.
- **Expect to rethink the architecture at every order-of-magnitude (10×) increase in load.** Don't plan more than **one order of magnitude ahead**.
- **Break the system into components that can run largely independently.** That's the idea behind microservices, sharding, stream processing, and shared-nothing. The hard part is **where to draw the lines**.
- **Don't make things more complicated than necessary:**
  - one machine beats a complex distributed setup if it does the job
  - with **predictable** load, **manual scaling** may cause fewer surprises than **autoscaling**
  - **5 services are simpler than 50**
  - good architectures are a **pragmatic mixture**

## 17. Maintainability
- Software doesn't wear out, but **requirements change, environments change** (dependencies, platforms), and **bugs need fixing**.
- **Most of the cost of software is maintenance**, not initial development: fixing bugs, keeping it running, investigating failures, adapting to new platforms and use cases, repaying **technical debt**, adding features.
- **Legacy systems:** outdated technologies (mainframes, COBOL), lost institutional knowledge as people leave, and other people's mistakes to fix. **Maintenance is as much a people problem as a technical one.**
- **Every valuable system becomes legacy one day**, so **design with maintenance in mind**. There are three principles:

| Principle | Goal |
|---|---|
| **Operability** | Easy for the organization to **keep it running smoothly** |
| **Simplicity** | Easy for **new engineers to understand**: well-understood, consistent patterns, no unnecessary complexity |
| **Evolvability** | Easy to **change in the future**, for unanticipated use cases |

### Operability: making life easy for operations
- *"Good operations can often work around the limitations of bad (or incomplete) software, but good software cannot run reliably with bad operations."*
- **Automation is a two-edged sword:**
  - At thousands of machines, manual work is too expensive, so **automation is essential**.
  - But the cases automation *can't* handle are the **hardest ones**. More automation needs a **more skilled** ops team.
  - **A misbehaving automated system is harder to troubleshoot** than one where an operator performs the steps by hand.
  - So **more automation isn't always better**. The sweet spot depends on the application and the organization.
- **Good operability means routine tasks are easy**, so ops can focus on high-value work. Data systems help by:
  1. supporting **monitoring** of key metrics and **observability** of runtime behaviour
  2. **not depending on individual machines**: any machine can be taken down for maintenance while the system keeps running
  3. **good documentation** and an easy-to-understand **operational model** ("if I do X, Y will happen")
  4. **good defaults**, with the freedom to **override** them
  5. **self-healing** where appropriate, but with **manual control** available
  6. **predictable behaviour**, with few surprises

### Simplicity: managing complexity
- Small projects can be simple. Large ones tend to become complex, which **slows everyone down** and raises maintenance cost. The extreme is a **"big ball of mud"**.
- **Complexity causes:** overrun budgets and schedules, and **more bugs per change**, because hidden assumptions, unintended consequences, and unexpected interactions are easy to miss.
- **Simplicity is subjective.** There's no objective standard. Is a complex implementation behind a simple interface simpler than a simple implementation that exposes its internals?
- **Essential vs accidental complexity:**
  - **Essential:** inherent in the problem domain.
  - **Accidental:** comes only from the limitations of our tools.
  - The distinction is flawed too: **the boundary shifts as tools evolve**.
- **Abstraction is the best tool we have.** It hides lots of implementation detail behind a clean façade.
  - It's **reused** widely, so improvements to the abstracted component **benefit every user**.
  - Examples:
    - **high-level languages** hide machine code, registers, and system calls
    - **SQL** hides on-disk and in-memory data structures, concurrent clients, and inconsistencies after crashes
  - Application-level abstractions come from **design patterns** and **domain-driven design (DDD)**. This book is about **general-purpose** abstractions instead: **transactions, indexes, event logs**. DDD can be built on top of them.

### Evolvability: making change easy
- Requirements are **constantly in flux**: new facts, unanticipated use cases, changing business priorities, feature requests, new platforms, **new legal or regulatory rules**, and growth that forces architectural change.
- **Agile** provides the process. **TDD** and **refactoring** provide the technical tools at the level of code. This book looks for agility at the level of a **whole data system** made of several services. The book calls that **evolvability**.
- **Evolvability depends on simplicity and good abstractions:** **loosely coupled, simple** systems are easier to change than tightly coupled, complex ones.
- **Irreversibility makes change hard.** If a database migration **can't be switched back**, the stakes are much higher.
  - Take **irreversible actions very carefully**.
  - **Minimize irreversibility** to keep flexibility: keep the ability to roll back, run the old and new systems side by side, and keep reversible steps.

## 18. Chapter summary
1. **Nonfunctional requirements** covered here: **performance, reliability, scalability, and maintainability**.
2. **The timeline case study** showed the challenges of scale: fan-out, materialization, and celebrities.
3. **Performance** is measured with **response time percentiles**, and **load** with **throughput**. Both feed into **SLAs**.
4. **Scalability** means keeping performance the same as load grows. The general principle is to **break tasks into parts that can operate independently**.
5. **Reliability** comes from **fault tolerance**:
   - hardware faults are mostly independent
   - **software faults are strongly correlated**, which makes them harder
   - human mistakes are handled with resilience, and learned from through **blameless postmortems**
6. **Maintainability** means operability, simplicity, and evolvability. There are no easy answers, but **well-understood building blocks with useful abstractions** help, and that's what the rest of the book covers.

## 19. Key terms
| Term | One-line meaning |
|---|---|
| Functional requirement | What the system does |
| Nonfunctional requirement | How well it does it: speed, reliability, scalability, maintainability, security, compliance |
| Home timeline | Recent posts from the accounts a user follows |
| Polling | The client repeatedly asks the server for updates |
| Fan-out | The factor by which one request multiplies into downstream requests |
| Materialization / materialized view | Precomputed and maintained query results (faster reads, more writes) |
| Response time | Total time the client waits |
| Service time | Time the service actively spends processing |
| Queueing delay | Time spent waiting for a CPU, buffer, and so on |
| Latency | Time a request is not being processed. Network latency is time in transit. |
| Throughput | Requests or data per second |
| Head-of-line blocking | Slow requests at the front of a queue delay the fast ones behind them |
| Jitter | Variation in network delay |
| Percentile (p50/p95/p99/p999) | X% of requests are faster than this value |
| Tail latency | High-percentile response times |
| Tail latency amplification | Many backend calls per request, so slow requests become more likely |
| SLO / SLA | Performance and availability target / the contract with penalties |
| HdrHistogram, t-digest, DDSketch | Libraries that estimate percentiles cheaply |
| Retry storm | Timed-out clients retry, which adds load, which causes more timeouts |
| Metastable failure | The system stays overloaded even after the trigger is gone |
| Exponential backoff | Increasing, randomized waits between retries |
| Circuit breaker | Stop calling a failing dependency for a while |
| Load shedding | The server rejects requests when near overload |
| Backpressure | The server tells clients to slow down |
| Fault / failure | A part breaks / the whole system misses its SLO |
| SPOF | Single point of failure |
| Fault injection / chaos engineering | Deliberately cause faults to test fault tolerance |
| Exactly-once semantics | Each item processed once: none lost, none duplicated |
| ECC memory | RAM that corrects some bit errors |
| Availability zone | A group of physically co-located resources, likely to fail together |
| Rolling upgrade | Restart nodes one at a time, with no downtime |
| Cascading failure | One overloaded component takes down the next |
| Blameless postmortem | Incident review focused on systems, not blame |
| Property testing | Testing invariants against many random inputs |
| Linear scalability | 2× resources handles 2× load |
| Vertical / horizontal scaling | Bigger machine / more machines |
| Shared-memory / shared-disk / shared-nothing | Architectures for adding hardware |
| NAS / SAN | Network-attached storage / storage area network |
| Technical debt | Shortcuts that make future changes costlier |
| Legacy system | An old, valuable system with outdated tech or lost knowledge |
| Operability / simplicity / evolvability | Easy to run / easy to understand / easy to change |
| Operational model | Predictable "if I do X, Y happens" behaviour |
| Self-healing | The system recovers automatically, with a manual override available |
| Big ball of mud | A system with no clear structure, where every change is risky |
| Essential / accidental complexity | Inherent in the problem / caused by our tools |
| Abstraction | A clean interface hiding implementation details (SQL, languages, transactions) |
| Domain-driven design (DDD) | A method for building application-level abstractions |
| TDD / refactoring | Test-first development / restructuring code without changing behaviour |
| Irreversibility | Changes you can't roll back. Minimize them. |

## 20. How this connects to other weeks
- Derived data and materialized views: Week 0 (system of record vs derived), Week 4 (event sourcing, CQRS)
- Caching the timelines: Week 6
- Replication and failover (tolerating machine and zone loss): Weeks 9–10
- Sharding (needed for shared-nothing): Week 11
- Timeouts, unbounded delays, GC pauses: Week 14
- Consensus for fault tolerance: Weeks 15–16
- Exactly-once fan-out: Week 19
- Rolling upgrades, compatibility, and evolvable schemas: Week 8
- General-purpose abstractions (transactions, indexes, event logs): Weeks 5–6, 12–13, 18

---

## My additions
(Your own thoughts, work examples, and notes from the videos.)
-

# Week 1 MCQs: Answer key

> Check your score first with `python3 tools/check_mcqs.py weeks/week-01-nonfunctional-requirements`. Read the "Why" column only for the ones you missed, after working out your own reason.

| Q | Answer | Why the best answer wins (and the trap) | Concept (notes §) |
|---|---|---|---|
| 1 | C | 10M ÷ 5 s = 2M timeline queries/s, × 200 accounts each = **400M lookups/s**. **Trap:** A counts queries, not lookups. | Polling cost (2) |
| 2 | A | Very read-heavy with modest fan-out: do the work once per post (×200), not on every read. Reads become cache lookups. | Materialization (2) |
| 3 | D | That's the hybrid approach. Celebrity posts are stored once and merged at read time. Dropping (A) isn't acceptable for posts people expect to see. | Celebrity problem (2) |
| 4 | B | That user can't read thousands of posts a minute, so sampling loses nothing they'd notice. It's acceptable here but **not** for celebrities' followers (Q3). | Extreme cases (2) |
| 5 | A | Fan-out on write separates writes from reads. A spike delays delivery a little while reads stay fast. Queues absorb bursts. | Spikes (2) |
| 6 | C | It's "how long until X happens", which is response time. Posts per second would be throughput. | Response time vs throughput (3) |
| 7 | D | Same work per request, but near capacity requests wait behind each other. Queueing delay grows non-linearly (see B3). | Queueing (3) |
| 8 | B | It stays broken after the trigger is gone, which is the signature of metastable failure. Fix: backoff with jitter and retry limits on clients, load shedding and backpressure on the server. | Metastable failure (3) |
| 9 | B | Server-side timing covers only service time. Queueing before processing and network time are invisible to it, so measure on the client. | Response time components (4) |
| 10 | D | The fast requests wait behind slow ones (head-of-line blocking). Isolating the slow work removes the cause. | Head-of-line blocking (4) |
| 11 | A | The average hides the tail and describes nobody. p50 shows the typical experience and p99/p99.9 the bad cases, measured where the user is. | Percentiles (5) |
| 12 | C | Amazon's reasoning: the slowest requests are often from customers with the most data, who are the most valuable. | Tail latency (5) |
| 13 | D | Percentiles don't add up or average. Merge the distributions (histograms), weighted by how many requests each server handled. | Computing percentiles (8) |
| 14 | A | Sketches and histograms are tiny, cheap, and **mergeable** across servers and time. Raw sorting is too expensive at that volume. | Computing percentiles (8) |
| 15 | B | 1 − 0.99⁴⁰ ≈ 33%. One slow backend makes the whole page slow. | Tail latency amplification (7) |
| 16 | C | The SLA is the contract with consequences. An internal SLO set stricter than the SLA lets you react before you owe customers money. | SLO vs SLA (7) |
| 17 | A | The budget is 0.1% of requests. Running at 0.3% is a 3× burn, so 10 days at 3× uses 30 days' worth: it's all gone. | SLOs, error budgets (7) |
| 18 | B | A fault is one component; a failure is the system missing its SLO. Tolerating the fault means no failure. | Fault vs failure (9) |
| 19 | D | A single load balancer is a SPOF. A primary that needs an hour of manual promotion is, in practice, a SPOF too. | Single point of failure (9) |
| 20 | C | That's fault injection, or chaos engineering. Rarely run error-handling code is where critical bugs hide, so exercise it constantly. | Fault injection (9) |
| 21 | C | 50,000 × 4% ÷ 365 ≈ **5.5 a day**. At scale, hardware faults are routine operations, not emergencies. | Hardware faults (10) |
| 22 | B | Multiplying availabilities assumes independent failures. A shared rack, power supply, zone, or the same software breaks that assumption. | Correlated faults (10) |
| 23 | D | Software faults are correlated (same bug everywhere). A canary rollout limits the blast radius, and rollback makes the fault short. | Software and human faults (11–12) |
| 24 | A | It's the real SSD firmware bug the chapter describes. Identical twins fail together, so redundancy needs diversity. | Software faults (11) |
| 25 | B | One component's trouble overloads the next, which overloads the next. Headroom, timeouts, circuit breakers, and shedding stop the chain. | Cascading failures (11) |
| 26 | D | "Human error" is a symptom of the system. Blameless postmortems lead to guardrails; blame leads to people hiding mistakes. | Humans and reliability (12) |
| 27 | A | Outages are recoverable; permanent data loss isn't. The chapter's family-photos example. | How important is reliability (13) |
| 28 | C | Premature scaling wastes effort and locks in an inflexible design. Plan about one order of magnitude ahead. | Scalability (14, 16) |
| 29 | D | "X is scalable" is meaningless. Ask how the load grows and what your options are along that dimension. | Scalability (14) |
| 30 | A | Fan-out (followers per user), and especially the celebrity extreme, drove the push/pull/hybrid design. | Understanding load (15) |
| 31 | C | 800 → 600 requests/s per server is sublinear. Find the shared bottleneck rather than throwing hardware at it. | Linear scalability (15) |
| 32 | B | Scaling up is maxed out and growth is steady: buy time with replicas, caching, and tuning, and design sharding while there's headroom (log(1.25)/log(1.05) ≈ 4.6 months). | Vertical vs horizontal scaling (16) |
| 33 | B | Automation takes the easy cases and leaves the hardest for humans, and a misbehaving automated system is harder to debug. Keep it visible and overridable, and keep operators skilled. **Trap:** A throws away the benefits of automation. | Operability (17) |
| 34 | D | Operability comes from predictability, good overridable defaults, and not depending on individual machines. Hiding or forbidding control (A, C) hurts operators in edge cases. | Operability (17) |
| 35 | A | It existed only because of a tool's limitation, so when the tool improved, it vanished. That's accidental complexity, and it shows the boundary shifts as tools evolve. | Essential vs accidental complexity (17) |
| 36 | C | Good abstractions are reused widely, so a quality improvement in the component improves every application built on it. | Abstraction (17) |
| 37 | D | Every step stays reversible until the last one. Stopping writes to the old database is the only one-way door, so take it last (see B7). | Evolvability, irreversibility (17) |
| 38 | A | Most cost is in maintenance, and simplicity and well-understood building blocks reduce it. A 30% speed gain rarely pays for a lifetime of custom maintenance. | Maintainability, simplicity (17) |
| 39 | C | Legacy maintenance is a people and knowledge problem. Pin down the existing behaviour first, then change it in small, reversible steps. A rewrite (A) loses the hidden knowledge built into the old code. | Legacy systems (17) |
| 40 | B | Tight coupling and no clear abstractions mean hidden interactions everywhere, so every change is risky. That's a big ball of mud, and the fix is better boundaries and abstractions. | Simplicity (17) |

**Score guide:** 37–40 excellent · 32–36 good, review your misses · below 32, re-read the sections in the last column, then retry.

# Week 1 MCQs: Defining Nonfunctional Requirements

40 scenario questions, each with one correct answer. They test whether you can **apply** the ideas. Several options are partly true; pick the **best** one, the answer a senior engineer would defend.

- **Answer right here:** type the letter after **Your answer:** under each question, e.g. `> **Your answer:** C · **Sure?** Y`. Mark **Sure?** Y or N, because a correct guess still means you should revisit that topic.
- Check your score from the repo root: `python3 tools/check_mcqs.py weeks/week-01-nonfunctional-requirements`. It shows which questions you got wrong, not the right answers.
- Target: **32/40 or better**. For each miss, work out *why* the right answer beats the one you picked before reading the key.

---


### Timelines and fan-out

**1.** Clients poll the home timeline every 5 s. 10 million users are online, and each follows about 200 accounts. With fan-out on read, roughly how many per-account post lookups per second does the backend face?
- A) 2 million
- B) 50 million
- C) 400 million
- D) 2 billion

> **Your answer:**   · **Sure?** 

**2.** A social app has about 1,000 timeline reads per post, and almost every account has a few hundred followers. Which timeline strategy fits best?
- A) Fan-out on write: precompute each user's timeline when posts are made
- B) Fan-out on read: build each timeline with a join when it's requested
- C) Poll the posts table every second from every client
- D) Recompute everyone's timeline in a nightly batch job

> **Your answer:**   · **Sure?** 

**3.** You use fan-out on write. A celebrity with 80 million followers posts 20 times a day, and the delivery workers fall hours behind. What's the standard fix?
- A) Drop most of the celebrity's deliveries
- B) Add 80× more delivery workers
- C) Make every user switch to fan-out on read
- D) Store celebrity posts separately and merge them into followers' timelines at read time

> **Your answer:**   · **Sure?** 

**4.** One user follows 50,000 very active accounts, so their materialized timeline receives thousands of writes per minute. What's an acceptable trade-off?
- A) Block the user from following more accounts
- B) Drop or sample some of that user's timeline writes, since nobody reads thousands of posts a minute
- C) Rebuild their timeline from scratch on every read
- D) Give that user a dedicated database

> **Your answer:**   · **Sure?** 

**5.** On New Year's Eve, posts spike from 6,000/s to 150,000/s and fan-out on write can't keep up. What should happen?
- A) Enqueue the deliveries and accept that posts appear a little later. Timeline reads stay fast because they come from the precomputed cache.
- B) Reject new posts until the spike ends
- C) Switch every client to polling
- D) Temporarily stop serving timelines

> **Your answer:**   · **Sure?** 


### Performance basics

**6.** "Time until a new post appears in followers' timelines" is best described as a:
- A) Throughput metric
- B) Availability metric
- C) Response time metric
- D) Utilization metric

> **Your answer:**   · **Sure?** 

**7.** An API's p99 is 50 ms at 40% CPU and 900 ms at 90% CPU. The CPU work per request hasn't changed. What's the main cause?
- A) The database got slower
- B) Garbage collection
- C) Network congestion
- D) Queueing delay grows sharply as utilization approaches capacity

> **Your answer:**   · **Sure?** 

**8.** A 5-minute traffic spike ends, but the service stays at 100% CPU with nearly every request timing out, until someone restarts it. What happened, and what prevents it?
- A) A memory leak: add more RAM
- B) A retry storm causing metastable failure: add client backoff with jitter and retry limits, and have the server shed requests whose clients have already given up
- C) Disk failure: add RAID
- D) A bad deploy: roll back

> **Your answer:**   · **Sure?** 

**9.** Server-side metrics show p99 = 40 ms, but users' apps measure a p99 of 3 s for the same calls. What's the most likely explanation?
- A) Users' phones are slow
- B) Time spent queueing, and on the network, before and after the service processes the request isn't counted in server-side service time
- C) The p99 calculation is wrong
- D) A cache is serving stale data

> **Your answer:**   · **Sure?** 

**10.** An 8-core server mostly handles 5 ms requests, but occasionally gets 20-second report exports. During exports, the simple requests also take seconds. Which fix targets the cause?
- A) Add a CDN
- B) Increase the client timeout
- C) Add more RAM
- D) Run slow exports in a separate queue or worker pool, so fast requests don't wait behind them (head-of-line blocking)

> **Your answer:**   · **Sure?** 


### Percentiles and SLOs

**11.** A team reports "average latency 120 ms" every month, but users complain the app feels slow. What should the SLO use instead?
- A) Client-measured p50 for the typical experience, plus p99 or p99.9 for the tail
- B) The maximum latency
- C) Server CPU utilization
- D) The average, measured more often

> **Your answer:**   · **Sure?** 

**12.** At an e-commerce company, whose requests usually land in the p99.9?
- A) Bots
- B) New users with empty accounts
- C) Heavy customers with lots of order history and data, often the most valuable ones
- D) Users on fast connections

> **Your answer:**   · **Sure?** 

**13.** Three servers report p99s of 100 ms, 120 ms, and 900 ms. The dashboard shows their average, 373 ms, as the "fleet p99". What's wrong?
- A) Nothing
- B) It should use the median of the three
- C) It should use the maximum, 900 ms
- D) Averaging percentiles is meaningless. Merge the servers' latency histograms (which accounts for their different request counts) and read the p99 from the result.

> **Your answer:**   · **Sure?** 

**14.** You need fleet-wide percentiles at 1 million requests/s with little memory and CPU. What's the best approach?
- A) Each server keeps a mergeable histogram or sketch (HdrHistogram, t-digest, DDSketch). Ship and merge those.
- B) Store every response time centrally and sort the list every minute
- C) Sample 10 requests per minute
- D) Log only the average

> **Your answer:**   · **Sure?** 

**15.** A page calls 40 backend services in parallel and waits for all of them. Each is slower than 200 ms 1% of the time. Roughly what share of page loads take longer than 200 ms?
- A) 1%
- B) About 33%
- C) 40%
- D) About 4%

> **Your answer:**   · **Sure?** 

**16.** Your customer contract promises 99.9% monthly uptime or a 10% credit. Your team aims for 99.95% internally. Which statement is right?
- A) Both are SLAs
- B) The internal target should be lower than the contract
- C) The contract is the SLA. The stricter internal SLO leaves a safety margin before the SLA is breached.
- D) SLOs only apply to latency

> **Your answer:**   · **Sure?** 

**17.** Your SLO is 99.9% success over 30 days. For the first 10 days, the error rate has been 0.3%. What's the situation?
- A) The burn rate is 3×, so the whole 30-day error budget is already spent. Prioritize reliability over risky releases.
- B) You're on track, since 0.3% is under 1%
- C) About a third of the budget is used
- D) SLOs reset weekly, so it doesn't matter

> **Your answer:**   · **Sure?** 


### Reliability

**18.** One of three database replicas loses its disk. The service keeps meeting its SLO while a new replica is built. This is:
- A) A failure
- B) A fault that was tolerated, not a failure
- C) An SLA breach
- D) A single point of failure

> **Your answer:**   · **Sure?** 

**19.** Setup: 6 app servers behind **one** load balancer instance, and one primary database with an asynchronous replica that takes about an hour to promote by hand. What are the single points of failure?
- A) The app servers
- B) The replica
- C) None, since everything is replicated
- D) The load balancer and the primary database (manual promotion means a long outage)

> **Your answer:**   · **Sure?** 

**20.** Why would a bank deliberately kill production instances at random?
- A) To save money
- B) To test new hardware
- C) To keep exercising failover and error-handling code, which runs rarely and is where many critical bugs hide
- D) Regulators require it

> **Your answer:**   · **Sure?** 

**21.** You run 50,000 hard disks with a 4% annual failure rate. About how many disk failures per day should you plan for?
- A) 0.05
- B) 0.5
- C) About 5
- D) About 50

> **Your answer:**   · **Sure?** 

**22.** Two servers at 99.9% each "should" give 99.9999% when combined, but in practice outages often take out both. Why?
- A) The maths is wrong
- B) Their failures are correlated: same rack, power, zone, or the same software. Spread them across availability zones and roll out changes gradually.
- C) Load balancers add downtime
- D) 99.9% servers don't exist

> **Your answer:**   · **Sure?** 

**23.** A config change with a bug is pushed to all 500 nodes at once, and all of them crash. What would have limited the damage most?
- A) Better hardware
- B) RAID
- C) More nodes
- D) A gradual (canary) rollout with automatic rollback

> **Your answer:**   · **Sure?** 

**24.** All the SSDs in a storage cluster were bought together, and they fail within days of each other after exactly 32,768 hours. What's the lesson?
- A) Identical components installed at the same time can fail together. Redundancy assumes independence, so mix batches or models and stagger installs.
- B) SSDs are worse than HDDs
- C) Use RAID 0
- D) Buy more spares of the same model

> **Your answer:**   · **Sure?** 

**25.** One of four cache nodes dies. Its traffic hits the database, which slows down. Then the API servers' threads all block waiting on the database, and the whole site goes down. This is:
- A) A metastable failure caused by clock skew
- B) A cascading failure. Mitigate with spare capacity, timeouts, circuit breakers, and load shedding.
- C) A hardware fault that can't be avoided
- D) A security incident

> **Your answer:**   · **Sure?** 

**26.** An engineer ran a command that deleted a production table. What's the most productive response?
- A) Fire the engineer
- B) Add a rule that says "be more careful"
- C) Rewrite the system in another language
- D) A blameless postmortem: fix the system with guardrails, confirmation steps, least-privilege access, and backups whose restores are tested

> **Your answer:**   · **Sure?** 

**27.** A photo-storage startup can afford only one of: (i) raising uptime from 99.9% to 99.99%, or (ii) guaranteed durability (checksums, tested backups, multi-zone copies). Which should it choose?
- A) (ii) Durability. Short outages are tolerable, but losing someone's family photos is catastrophic and permanent.
- B) (i) Uptime, because users notice outages
- C) Neither, ship features
- D) Both partially

> **Your answer:**   · **Sure?** 


### Scalability

**28.** A startup with 2,000 users wants to build a sharded multi-region Cassandra cluster "for when we have 100 million users". What's the best advice?
- A) Do it now, since migrating later is hard
- B) Use microservices instead
- C) Keep it simple (e.g. one Postgres) and flexible, track growth, and redesign around each 10× increase in load
- D) Use serverless

> **Your answer:**   · **Sure?** 

**29.** Someone asks, "Is Postgres scalable?" What's the best response?
- A) Yes
- B) No
- C) Only with sharding
- D) It depends on how your load grows: reads or writes, data size, the extreme cases. Scalability is about specific growth dimensions, not a yes/no label.

> **Your answer:**   · **Sure?** 

**30.** In the timeline case study, which load parameter shaped the architecture the most?
- A) The distribution of followers per user (the fan-out), especially the extreme cases
- B) The average post length
- C) The number of servers
- D) The database version

> **Your answer:**   · **Sure?** 

**31.** Going from 8 to 16 servers raised throughput from 6,400 to 9,600 requests/s. What does that tell you?
- A) Linear scaling, so keep adding servers
- B) The load test was broken
- C) Sublinear scaling: per-server throughput fell from 800 to 600. Look for a shared bottleneck (database, lock, hot shard) before adding more.
- D) Superlinear scaling

> **Your answer:**   · **Sure?** 

**32.** Postgres runs on the largest available instance at 80% CPU, and load grows 5% a month. What's the sensible plan?
- A) Shard it across 64 nodes this week
- B) Buy time: move reads to replicas, add a cache, and tune queries. Meanwhile, design sharding before the ~4–5 months of headroom run out.
- C) Do nothing until it hits 100%
- D) Move to a shared-disk SAN

> **Your answer:**   · **Sure?** 


### Maintainability

**33.** Your team fully automated database failover. At 3 AM, a rare network partition makes the automation fail over back and forth repeatedly, and the on-call engineer can't work out what it's doing. What's the lesson?
- A) Automation should be removed entirely
- B) Automation handles the easy cases, which leaves the hardest ones to humans. Automated systems need visibility, a clear operational model, and a manual override, plus skilled operators.
- C) Fail over more often to practise
- D) Add a second automation system to watch the first

> **Your answer:**   · **Sure?** 

**34.** You're building a database product. Which feature does the most for its *operability*?
- A) Hiding every configuration option so admins can't make mistakes
- B) Requiring a human to approve every failover
- C) Never letting administrators override automatic behaviour
- D) Predictable behaviour with a clear operational model ("if I do X, Y happens"), good defaults that can be overridden, and the ability to take any machine down for maintenance

> **Your answer:**   · **Sure?** 

**35.** A team wrote 400 lines of custom retry and serialization code only to work around an old library's limitations. Once they upgraded the library, the code became unnecessary. That code was:
- A) Accidental complexity: caused by tool limitations, not by the problem itself
- B) Essential complexity
- C) Good abstraction
- D) Technical debt that can never be removed

> **Your answer:**   · **Sure?** 

**36.** SQL hides on-disk data structures, concurrency, and crash recovery from application developers. Besides convenience, what's the biggest benefit of such a widely used abstraction?
- A) It makes queries faster than hand-written code in every case
- B) It removes the need for indexes
- C) It's reused by thousands of applications, so every improvement to the database engine benefits all of them
- D) It eliminates all complexity from the system

> **Your answer:**   · **Sure?** 

**37.** You're migrating your main database from MongoDB to Postgres. Which plan keeps the most flexibility?
- A) A big-bang weekend cutover that deletes MongoDB afterwards
- B) Export, import, switch DNS, then decommission the old database the same day
- C) Freeze all writes for a week while you migrate
- D) Dual-write to both, backfill, compare with shadow reads, switch reads to Postgres while still writing both, and only stop writing MongoDB once you're confident

> **Your answer:**   · **Sure?** 

**38.** A startup could build a custom storage engine that's 30% faster for its workload, or use Postgres. Most of the system's lifetime cost will come after launch. What does that point to?
- A) Postgres. A well-understood building block keeps future maintenance, hiring, and operations cheaper, and 30% rarely outweighs that.
- B) The custom engine, because performance is what matters most
- C) Build both and decide later
- D) The custom engine, because it can be replaced later

> **Your answer:**   · **Sure?** 

**39.** You inherit a 20-year-old billing system written in COBOL. Its original authors have left and documentation is thin, and you must add a new tax rule. What's the safest first step?
- A) Rewrite it from scratch in a modern language first
- B) Make the change directly and test in production
- C) Capture its current behaviour first, with characterization tests on real inputs and outputs, monitoring, and notes from the people who run it. Then make small, reversible changes.
- D) Refuse to touch it

> **Your answer:**   · **Sure?** 

**40.** In a large codebase, every small change breaks something seemingly unrelated, and nobody can say what a module is responsible for. What's this a symptom of?
- A) Too many tests
- B) A "big ball of mud": tight coupling and no clear boundaries or abstractions, so hidden interactions make every change risky
- C) Using too many design patterns
- D) Running on old hardware

> **Your answer:**   · **Sure?** 

---

**Score:** __ / 40 · **Topics to revisit:**

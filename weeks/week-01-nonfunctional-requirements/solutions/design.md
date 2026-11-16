# Week 1 Design: Twitter/X home timeline (reference)

> One strong answer, not the only one. Every decision is tied to a nonfunctional requirement from the chapter.

## 1. Requirements
**Functional:**
- post, follow and unfollow
- view the home timeline: recent posts from the accounts you follow, newest first
- receive new posts in real time while online
- delete a post

**Nonfunctional, as SLOs:**

| Requirement | Target | Why |
|---|---|---|
| Timeline load | **p50 < 200 ms, p99 < 1 s** (measured in the app) | The most frequent action, and the first screen people see |
| Post delivery | 99% of posts reach **online** followers **within 5 s**. During extreme spikes, within 60 s. | The book's freshness requirement |
| Post API availability | **99.95%** | Failing to post is very visible |
| Timeline availability | **99.95%**. Serving a slightly stale timeline counts as available. | Graceful degradation |
| Durability of posts | **Never lose an accepted post** (stored in 3 copies across zones) | Data loss is worse than an outage |

## 2. Estimates
- **Posts:** 500M/day ≈ **5,800/s** average, **150k/s** peak.
- **Timeline reads:** 200M daily users × ~20 timeline loads ≈ 4B/day ≈ **46k reads/s** on average, maybe 150k/s at peak. Far more than posts (roughly 8–25× more).
- **Fan-out writes:** 5,800 × 200 ≈ **1.16M/s** on average, **30M/s** at peak if done immediately, so a queue is needed.
- **Timeline cache:** 800 IDs × 8 B × 200M users ≈ **1.3 TB**, about **2.6 TB** with 2× replication. That's about 40 nodes with 64 GB each. Materialize only for active users.
- **Post storage:** ~500 bytes × 500M a day = 250 GB/day ≈ **90 TB/year** of text and metadata (media goes in object storage).

## 3. Data model
- **Systems of record:**
  - the `posts` store, sharded by post ID or author, replicated 3×
  - the `follows` graph, stored in both directions (followee → followers for fan-out, follower → followees for reads)
  - `users`
- **Derived:**
  - **home timelines**: lists of post IDs per user, in the cache
  - per-celebrity recent-post lists
  - follower counts
  - search indexes

  All of these can be **rebuilt from the systems of record**.

## 4. Write path
```
client --POST /posts--> Post API --(1) write post (3 replicas)--> posts DB
                              \--(2) event "post created"--> Kafka (partitioned by author)
                                                              |
                            fan-out workers <-----------------+
                            |- author is a celebrity (>= ~500k followers)? -> append to celebrity list only
                            |- otherwise: for each follower batch -> append post_id to their timeline (cache)
                            |- heavy-following users: sample (keep N most recent per followee)
                            '- online followers: publish to their push channel
```
- Write the post to the database **first** (it's the system of record), then emit the event. Use an **outbox** or CDC so the event is never lost.
- Workers **batch** followers (e.g. 1,000 at a time) and use pipelined cache writes.
- **Prioritization:** online followers first, the rest at lower priority. Inactive users get no fan-out at all; their timelines are rebuilt when they log in.

## 5. Read path
1. Fetch the user's timeline IDs from the cache.
2. Fetch the recent posts of each followed **celebrity** (heavily cached), and merge by timestamp.
3. Hydrate the IDs into posts (post cache, multi-get), and drop deleted posts or blocked authors.
4. Return the first page. New posts arrive over **WebSocket or SSE** pushed from the fan-out workers, so there's no polling.

On a cache miss (the user was inactive), rebuild with pull: query the followees' recent posts, then store the result.

## 6. Fault tolerance
- **A fan-out worker crashes mid-delivery:** the Kafka consumer offset is committed only **after** the batch is written, so another worker re-processes the batch. The appends are **idempotent**: the timeline is a sorted set keyed by post ID, so a duplicate insert does nothing. Nothing is lost and nothing is duplicated, which is effectively exactly-once (Ch12).
- **A timeline cache node is lost:** its shards have replicas, so promote one. If both copies are lost, timelines are rebuilt lazily by pull on the next read. That's slower, but correct, because it's derived data. Protect the database while that happens (F3).
- **An availability zone is lost:** stateless services run in 3 zones. The databases replicate across zones with automatic failover, and the cache has cross-zone replicas. Capacity is planned at **N+1 zones**, so 2 zones can carry the peak.
- **Rolling deploys** with canaries, so no software change hits every node at once.

## 7. Overload protection (World Cup final plus a celebrity post)
- **Queue the fan-out**: delivery lag grows, but reads are unaffected. Autoscale workers on **queue depth**, and alert on delivery lag against the SLO.
- **Load shedding** on the read API under extreme load: serve slightly stale cached timelines, skip non-essential hydration (like counts), and reject the lowest-priority traffic first (prefetches, bots).
- **Client SDK:** exponential backoff with jitter, retry budgets, and circuit breakers. Honour `Retry-After` (backpressure).
- **Bounded queues** with deadlines, so the server drops requests whose clients have already given up. This prevents the metastable retry storm.

## 8. Observability
- **Client-side:** timeline load time p50/p99 by region and app version.
- **Server-side:** per-endpoint latency **histograms** (merged across the fleet, never averaged), error rates, queue depth.
- **Delivery lag:** the time from post creation to its insertion into followers' timelines (p50/p99), and to its push to clients.
- **SLO burn-rate alerts** for timeline availability and latency, and for delivery freshness.
- **Distributed tracing** across Post API → Kafka → workers → cache.

## 9. Evolution at 10×
- **Fan-out cost** grows to about 12M writes/s on average: raise the celebrity threshold, fan out only to recently active users, and store timelines more compactly.
- **The cache** grows to about 13 TB: tiered storage (hot in RAM, warm on SSD), and keep fewer IDs per inactive user.
- **Multi-region:** users are served from the nearest region, with cross-region replication of posts. Expect to **rethink the architecture at this order of magnitude** rather than just add machines.

## 10. Maintainability
- **Operability:**
  - runbooks for each alert
  - an admin override to **pause fan-out** or force a user onto the pull path
  - a manual "rebuild timeline for user X" tool
  - dashboards for delivery lag and queue depth
  - the celebrity threshold as a **config value with a safe default**, not hard-coded
  - any cache node can be drained for maintenance
- **Simplicity:** a few well-understood building blocks: the posts DB (system of record), Kafka (event log), and a cache (derived timelines). One `TimelineService` interface hides whether a timeline is pushed, pulled, or hybrid, so clients never care.
- **Evolvability, e.g. chronological to ranked:**
  - keep fan-out unchanged (it produces candidates)
  - add the ranking step **behind a feature flag**
  - **shadow-rank** (compute rankings without showing them) to compare metrics
  - roll out to 1% → 10% → 100%, keeping chronological as an instant fallback
  - no irreversible step until ranking has proven itself

## Interviewer follow-ups
- **F1. Deleting a post:**
  - Mark it deleted in the posts database (system of record) immediately.
  - Reads already filter deleted posts at **hydration**, so it disappears from every timeline at once, even though the IDs are still in the caches.
  - A background job removes the IDs from timelines lazily, or lets them age out.
  - Celebrity posts live in one list, so they're removed in one place.
  - Don't do a synchronous 50M-timeline deletion.
- **F2. Ranking instead of chronological order:**
  - Fan-out still delivers **candidates** (the recent posts).
  - At read time, a **ranking service** scores the candidates using features such as engagement, affinity, and freshness, and returns the top N.
  - That adds latency (cache the ranked page for a short time, precompute features), and the ranking model is more derived data from the analytical side, delivered by reverse ETL (Week 0).
- **F3. The cache restarts cold:**
  - Every read misses and falls back to pull, which sends a **flood of expensive queries** to the posts database (a thundering herd) and can cause a cascading failure.
  - Protect it:
    - **request coalescing** (one rebuild per user at a time)
    - rate-limit rebuilds, and **shed load** by serving a "recent popular posts" fallback
    - **warm the cache** before taking traffic (replay recent fan-out from Kafka)
    - restart cache nodes **gradually**, never all at once
- **F4. Compute everything on read with a fast database?**
  - At 4M polls/s × 200 accounts that's 800M lookups/s, and even at the real read rate (~50–150k/s) each read is a 200-way merge.
  - Tail latency amplification across many shards makes the p99 terrible. Celebrities' followers also make that database's hot partitions very hot.
  - Precomputation moves the work to the write side, where it's cheaper and can be queued. The trade-off is more storage and more complexity.
  - Pull is fine for **small** apps, and as the **fallback** for inactive users.

## Chapter concepts used
- Functional vs nonfunctional requirements
- SLOs
- Fan-out and materialized views
- The celebrity hybrid, and sampling for heavy followers
- Throughput vs response time
- Queueing
- Metastable failure and its defences
- Percentiles and histograms
- Tail latency amplification
- Faults vs failures, SPOFs
- Exactly-once
- Availability zones
- Rolling upgrades
- Planning one order of magnitude ahead
- Shared-nothing scaling

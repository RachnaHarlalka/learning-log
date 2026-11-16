# Week 1 Videos: Defining Nonfunctional Requirements

All links were found on YouTube in October 2026.
**Rule:** watch **one** video per topic. ⭐ marks the recommended pick; the others are alternatives if that one doesn't click.
Engineering Digest = warm-up before reading · Gaurav Sen = intuition after reading · Shrayansh = design and interview angle.
You've already watched Engineering Digest on latency and availability, so those count as your warm-up. Don't rewatch them.

## From your three channels
| Topic (notes §) | Channel | Video | Length | When |
|---|---|---|---|---|
| Latency (§3–4) | Engineering Digest | [What is latency in networking (Hindi)](https://www.youtube.com/watch?v=cG3LMd2hIXY) | 5:20 | Already watched? Skip it |
| Availability vs redundancy (§9–10) | Engineering Digest | [What is availability? (replication vs redundancy)](https://www.youtube.com/watch?v=Cdh9qAwFNNk) | 5:35 | Already watched? Skip it |
| Timeline / news feed design (§2) | Gaurav Sen | ⭐ [Designing Instagram: System Design of News Feed](https://www.youtube.com/watch?v=QmX2NPkJTKg) | 24:29 | After reading §2. Pairs with B1 and Part C. |
| Cascading failures and overload (§3, §11) | Gaurav Sen | ⭐ [How to avoid cascading failures in a distributed system](https://www.youtube.com/watch?v=xrizarXJgC8) | 18:06 | After reading §3 and §11. Pairs with B3. |
| Vertical vs horizontal scaling (§16) | Gaurav Sen | ⭐ [System Design Basics: Horizontal vs Vertical Scaling](https://www.youtube.com/watch?v=xpDnVSmNFX0) | 7:56 | After reading §16 |
| Vertical vs horizontal scaling (§16) | Engineering Digest | [Difference between horizontal and vertical scaling (Hindi)](https://www.youtube.com/watch?v=dHjHXis1r24) | 4:19 | Warm-up alternative |
| Why relational databases are hard to scale out (§16) | Engineering Digest | [Can RDBMS scale horizontally? (Hindi)](https://www.youtube.com/watch?v=VOrpRnE24KI) | 7:23 | Optional, previews Week 11 |
| Evolvability: the strangler pattern (§17) | Shrayansh | [SAGA, Strangler, CQRS: Microservices Design Patterns](https://www.youtube.com/watch?v=qGlUKtjqaEQ) | 30:55 | The strangler part pairs with S14 |
| Growing a system step by step (§14–16) | Shrayansh | [Scale from ZERO to MILLION Users (Hindi)](https://www.youtube.com/watch?v=rExh5cPMZcI) | 35:14 | Weekend, if you skipped it in Week 0 |

## Topics your channels don't cover (other channels)
| Topic (notes §) | Channel | Video | Length | Why this one |
|---|---|---|---|---|
| Fan-out on write vs read (§2) | Kartikeya Sharma | ⭐ [Timeline Architecture: Fanout on Read vs Fanout on Write](https://www.youtube.com/watch?v=SeeKlGMxyBQ) | 18:12 | Exactly the case study, including the celebrity hybrid |
| Fan-out (§2) | ByteMonk | [Twitter Timeline Architecture: Fanout](https://www.youtube.com/watch?v=FEkXjNFrL1o) | 5:43 | Short alternative |
| p50/p95/p99 (§5) | Hussein Nasser | ⭐ [Percentile Tail Latency Explained (95%, 99%)](https://www.youtube.com/watch?v=3JdQOExKtUY) | 6:15 | Clear and backend-focused |
| p50/p95/p99 (§5) | ByteMonk | [Mastering Latency Metrics: P90, P95, P99](https://www.youtube.com/watch?v=lJ4NEMNBeS4) | 6:41 | Alternative |
| Tail latency amplification (§7) | Vivek Haldar | ⭐ [Read a paper: The Tail at Scale](https://www.youtube.com/watch?v=1Qxnrf2pW10) | 8:53 | The Google paper behind §7, including hedged requests (S7) |
| SLI / SLO / SLA and error budgets (§7) | Tech Tutorials with Piyush | ⭐ [SLO vs SLI vs SLA vs Error Budget: Google SRE in plain English](https://www.youtube.com/watch?v=Akri1BlGp10) | 19:15 | Covers error budgets (S4, B4) |
| SLI / SLO / SLA (§7) | Better Stack | [SLAs, SLOs, and SLIs Explained in 7 Minutes](https://www.youtube.com/watch?v=pouVbehfnqQ) | 7:13 | Shorter alternative |
| Retry storms (§3) | Software Developer Diaries | ⭐ [This is how you protect your backend from a Retry Storm](https://www.youtube.com/watch?v=oQbUOnRhusM) | 6:43 | Pairs with B3 and S6 |
| Backoff and jitter (§3) | Software Developer Diaries | [Every engineer should know this (retries with jitter)](https://www.youtube.com/watch?v=yGO4Igb45V0) | 9:20 | Optional |
| Load shedding and backpressure (§3) | M. Atoar Rahman | ⭐ [Load Shedding & Backpressure Explained](https://www.youtube.com/watch?v=byER136Y968) | 5:18 | Short and clear |
| Chaos engineering (§9) | Why This in Tech? | ⭐ [Chaos Engineering: Why Netflix Breaks Things](https://www.youtube.com/watch?v=zfgAFxln1Lk) | 6:41 | Pairs with B6 |
| Blameless postmortems (§12) | In the Nic of Time | ⭐ [What are Blameless Postmortems?](https://www.youtube.com/watch?v=xGHF5c1xCCA) | 7:08 | Pairs with S10 |
| Essential vs accidental complexity (§17) | Kevlin Henney | ⭐ [Essential versus Accidental Complexity](https://www.youtube.com/watch?v=OFoAHSEDwe8) | 2:01 | Short and sharp |
| Essential vs accidental complexity (§17) | Better Software with Dmitry | [Essential vs accidental complexity in software design](https://www.youtube.com/watch?v=WiX7aIgdviU) | 11:59 | Longer, with examples |
| Big ball of mud (§17) | Smok Code | [What is Big Ball of Mud Software Architecture?](https://www.youtube.com/watch?v=Ygc7Z8UGLhc) | 4:49 | Optional |
| Reversible database migration (§17) | Web Dev Cody | ⭐ [How do projects achieve zero-downtime database migrations?](https://www.youtube.com/watch?v=cw5K2O4AHJc) | 7:06 | Pairs with B7 and S14 |
| Strangler fig pattern (§17) | ByteMonk | [Microservices Strangler Pattern](https://www.youtube.com/watch?v=DpuQ3-7e-rY) | 5:43 | Incremental replacement instead of a rewrite (S14) |
| Shared-nothing architecture (§16) | AGS Tech Tutorials | [Shared Nothing Architecture Explained with Real-Life Example](https://www.youtube.com/watch?v=c9p_rZFoBWQ) | 10:20 | Optional |

## Whole-chapter recaps of DDIA (2nd edition), for revision
Watch **after** finishing the week.

| Channel | Video | Length |
|---|---|---|
| The Insight Haven | ⭐ [DDA Ch 2: Defining Nonfunctional Requirements](https://www.youtube.com/watch?v=9hScmWOfC6U) | 14:40 |
| Kitab & Code | [DDIA Chapter 2: Reliability & Scalability (Hindi & English)](https://www.youtube.com/watch?v=47ljAxQ15Ng) | 21:39 |
| Ben Dicken | [Designing Data-Intensive Applications: Chapters 1 and 2](https://www.youtube.com/watch?v=G7iU2s7LUzA) | 57:48 |

## Suggested minimum for this week (~2 hr)
1. Kartikeya Sharma: fan-out on read vs write (18 min), after §2
2. Hussein Nasser: percentile tail latency (6 min), after §5
3. Vivek Haldar: The Tail at Scale (9 min), after §7
4. Piyush: SLO vs SLI vs SLA and error budgets (19 min), after §7
5. Software Developer Diaries: retry storms (7 min), plus Gaurav Sen: cascading failures (18 min), after §3 and §11
6. Why This in Tech?: chaos engineering (7 min), after §9
7. Gaurav Sen: horizontal vs vertical scaling (8 min), after §16
8. Kevlin Henney: essential vs accidental complexity (2 min), plus Web Dev Cody: zero-downtime migrations (7 min), after §17
9. The Insight Haven: chapter recap (15 min), at the end of the week

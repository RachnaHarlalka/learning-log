# Week 0 Videos: Trade-offs in Data Systems Architecture

All links were found on YouTube in October 2026.
**Rule:** watch **one** video per topic. ⭐ marks the recommended pick; the others are alternatives if that one doesn't click.
Engineering Digest = warm-up before reading · Gaurav Sen = intuition after reading · Shrayansh = design and interview angle.

## From your three channels
These channels don't have videos on OLTP vs OLAP, warehouses, or cloud architecture. They cover the **distributed systems**, **microservices**, **tracing**, and **cross-service transactions** parts of the chapter.

| Topic (notes §) | Channel | Video | Length | When |
|---|---|---|---|---|
| Distributed vs single-node (§10) | Engineering Digest | ⭐ [Distributed systems tutorial](https://www.youtube.com/watch?v=v8jv_6FaqTM) | 5:49 | Warm-up |
| Distributed vs single-node (§10) | Gaurav Sen | [System Design Primer: How to start with distributed systems?](https://www.youtube.com/watch?v=SqcXvc3ZmRU) | 9:22 | After reading |
| Scaling one machine vs many (§10) | Gaurav Sen | ⭐ [Horizontal vs. Vertical Scaling](https://www.youtube.com/watch?v=xpDnVSmNFX0) | 7:56 | After reading |
| Single server to distributed (§10, design) | Shrayansh | ⭐ [Scale from ZERO to MILLION Users (Hindi)](https://www.youtube.com/watch?v=rExh5cPMZcI) | 35:14 | Weekend |
| VMs and IaaS (§7–8) | Engineering Digest | [VM vs Container](https://www.youtube.com/watch?v=ggODipeOBXA) | 3:55 | Optional |
| Microservices (§11) | Engineering Digest | ⭐ [Monolithic vs microservices architecture (Hindi)](https://www.youtube.com/watch?v=MPxr1q8ORuA) | 5:17 | Warm-up |
| SOA → microservices (§11) | Engineering Digest | [REST API, SOA, Microservices, Tier architecture](https://www.youtube.com/watch?v=SvBnrJKzH8k) | 11:13 | Optional, covers SOA as the book does |
| Microservices: when to split (§11) | Gaurav Sen | ⭐ [Moving from monoliths to microservices](https://www.youtube.com/watch?v=rckfN7xFig0) | 19:25 | After reading: the "people problem" angle |
| Microservices (§11) | Gaurav Sen | [What is a microservice architecture and its advantages?](https://www.youtube.com/watch?v=qYhRvH9tJKw) | 8:19 | Shorter alternative |
| Microservices (§11) | Shrayansh | [Microservices Design Patterns, Part 1: Decomposition](https://www.youtube.com/watch?v=l1OCmsBnQ3g) | 29:19 | Optional |
| Observability / tracing (§10) | Shrayansh | [Distributed Tracing in-depth: Micrometer and OpenTelemetry](https://www.youtube.com/watch?v=nf-kyselLHs) | 1:10:34 | Optional deep dive (Java-based) |
| Cross-service consistency (§10) | Shrayansh | [SAGA Pattern, Strangler, CQRS: Microservices Design Patterns](https://www.youtube.com/watch?v=qGlUKtjqaEQ) | 30:55 | Optional, previews Week 13 |

## Topics your channels don't cover (other channels)
| Topic (notes §) | Channel | Video | Length | Why this one |
|---|---|---|---|---|
| OLTP vs OLAP (§3) | IBM Technology | ⭐ [OLAP vs OLTP](https://www.youtube.com/watch?v=iw-5kFzIdgY) | 5:26 | Short and clear, matches Table 1-1 |
| OLTP vs OLAP (§3) | Ben Dicken | [OLTP vs OLAP and the row/column storage trade-off](https://www.youtube.com/watch?v=wdJejI0bZRQ) | 17:33 | Deeper. Also previews Week 7 (column stores) |
| Warehouse, ETL, lake (§4–5) | codebasics | ⭐ [Data Warehouse vs Data Lake vs Data Lakehouse, ETL, OLAP vs OLTP](https://www.youtube.com/watch?v=yRerKDM1h74) | 16:18 | Covers §3–5 in one go, with good examples |
| Warehouse vs lake (§4–5) | IBM Technology | [Data Lake vs Data Warehouse vs Data Lakehouse](https://www.youtube.com/watch?v=PQFWQmL3fLY) | 7:53 | Shorter alternative |
| Cloud vs self-host, hybrid (§7) | TechWorld with Nana | ⭐ [Hybrid Cloud and MultiCloud: why are companies adopting it?](https://www.youtube.com/watch?v=qkj5W98Xdvw) | 13:35 | The trade-offs and the hybrid approach the chapter mentions |
| Separation of storage and compute (§8) | Arpit Bhayani | ⭐ [What the heck is Storage-Compute Separation? (Aurora paper)](https://www.youtube.com/watch?v=DA5W8tO_7Nw) | 17:09 | Aurora is the book's own example (Table 1-2) |
| Distributed tracing (§10) | ByteMonk | ⭐ [Distributed Tracing in Microservices](https://www.youtube.com/watch?v=XYvQHjWJJTE) | 7:02 | Short. Watch before B7 |
| Serverless (§11) | IBM Technology | ⭐ [What is Serverless?](https://www.youtube.com/watch?v=vxJobGtqKVM) | 6:42 | Clear basics |
| Serverless (§11) | Gate Smashers | [What is Serverless? AWS Lambda vs EC2 (Hindi)](https://www.youtube.com/watch?v=SDt36JcxTW4) | 9:08 | Hindi alternative: VM vs serverless |
| Serverless cold starts (§11) | SysSketch | [Serverless Cold Starts Explained](https://www.youtube.com/watch?v=eanGJ9ZOTc8) | 6:15 | Optional |
| Cloud vs supercomputing (§12) | Google Cloud Tech | ⭐ [What is High Performance Computing?](https://www.youtube.com/watch?v=nIBu1EFYmBU) | 5:29 | Short intro to HPC |
| Right to be forgotten (§13) | FIT4Privacy | ⭐ [GDPR Right To Be Forgotten (Right to be deleted)](https://www.youtube.com/watch?v=df_JAQIk1X8) | 7:01 | What the law requires (pairs with B6) |
| Right to be forgotten (§13) | Hemang Doshi | [GDPR Article 17: Right to erasure](https://www.youtube.com/watch?v=rFHO0DtJnP0) | 8:35 | Alternative |
| Separation of storage and compute (§8) | deferstech | [Storage-Compute Separation: the pattern behind Snowflake and BigQuery](https://www.youtube.com/watch?v=jKWfPqAZXbU) | 9:10 | Shorter, analytics-focused |

## Whole-chapter recaps of DDIA (2nd edition), for revision
Watch **after** finishing the week, to check for anything you missed.

| Channel | Video | Length |
|---|---|---|
| The Systematic Engineer | ⭐ [OLAP & OLTP Trade-Offs, DDIA 2nd Ed, Ch 1](https://www.youtube.com/watch?v=Ae4NwMK-Oas) | 17:28 |
| Kitab & Code | [DDIA Chapter 1: Trade-Offs in Data Systems (Hindi & English)](https://www.youtube.com/watch?v=sQ8_pk48q3A) | 18:43 |
| The Insight Haven | [DDA Ch 1: Trade-Offs in Data Systems](https://www.youtube.com/watch?v=6cBkZy3bFKo) | 11:35 |

## Suggested minimum for this week (~1 hr 45 min)
1. IBM: OLAP vs OLTP (5 min), before reading §3
2. codebasics: warehouse vs lake (16 min), after reading §4–5
3. Arpit Bhayani: storage-compute separation (17 min), after reading §8
4. Gaurav Sen: horizontal vs vertical scaling (8 min), after reading §10
5. ByteMonk: distributed tracing (7 min), after reading §10
6. Engineering Digest: monolith vs microservices (5 min), then Gaurav Sen: moving from monoliths to microservices (19 min), around §11
7. IBM: What is Serverless? (7 min), after §11
8. FIT4Privacy: right to be forgotten (7 min), after §13
9. The Systematic Engineer recap (17 min), at the end of the week

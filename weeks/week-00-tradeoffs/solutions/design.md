# Week 0 Design: Supermarket chain data architecture (reference)

> One reasonable answer, not the only one. What matters is that every choice links back to a trade-off from the chapter.

## 0. Estimate
- 40M line items/day × ~100 bytes ≈ **4 GB/day raw**, so **~1.5 TB/year**. Add receipts, inventory movements, clickstream, and indexes, and plan for maybe **5–10 TB/year** across the analytics stack.
- **What this means:** the *operational* side is modest. 3M receipts a day is about 35 a second on average, a few hundred a second at peak, which one good Postgres can handle, but it's spread across 200 stores. The *analytical* side quickly reaches multi-TB history, where row-store scans get slow, so a **columnar warehouse** is justified. It's not "big data" that needs a 100-node cluster, though, so stay simple.

## Diagram
```
 OPERATIONAL (OLTP): systems of record
 ┌──────────┐ ┌───────────┐ ┌──────────────┐ ┌───────────┐ ┌──────────┐
 │ Checkout │ │ Inventory │ │ Website/app  │ │ Suppliers │ │ Staff/HR │
 │ (POS) DB │ │    DB     │ │  orders DB   │ │    DB     │ │   DB     │
 └────┬─────┘ └─────┬─────┘ └──────┬───────┘ └─────┬─────┘ └────┬─────┘
      │  + SaaS: CRM, email marketing, card processor (via Fivetran/Airbyte)
      └─────────────┴──────┬───────┴───────────────┴────────────┘
                           │ extract (nightly dumps + change stream)
                           ▼
                 ┌───────────────────┐   raw files: reviews, shelf photos,
                 │  DATA LAKE (S3)   │◄─ clickstream, sensor data
                 │  raw, any format  │   (DERIVED)
                 └───┬───────────┬───┘
       transform+load│           │ pandas / Spark
                     ▼           ▼
      ┌─────────────────┐   ┌──────────────────────┐
      │ DATA WAREHOUSE  │   │ Data science: NLP on │
      │ (SQL, star      │   │ reviews, vision on   │
      │ schema) DERIVED │   │ photos, ML training  │
      └───────┬─────────┘   └──────────┬───────────┘
              ▼                        │ reverse ETL
      BI dashboards (Looker/           ▼
      Power BI): analysts      "Bought X, also bought Y"
                               model → website/app (DERIVED)

 STREAM path for fraud: checkout events ──► stream processor ──► block card in seconds
```

## 1. Operational systems
- **Checkout/POS, inventory, website/app orders, suppliers, staff/HR**, plus **SaaS** (CRM, email marketing, card processing).
- **Each gets its own database:** each system is complex, has its own team, and runs mostly independently. One database per service is considered good practice. The downside is **data silos**, which the warehouse solves.

## 2. Analytics
- *"Revenue per store in January"* and *"banana sales during the promotion vs normal"* are **aggregates over history**, so they're OLAP. They must **not** run on the checkout databases, because that would slow down real customers at the till.
- Data flows from the OLTP databases (nightly dumps plus a change stream) to the **lake (raw)**, then is transformed into the **warehouse** (a star schema of sales facts with store, product, and date dimensions), then on to BI tools.
- **ELT** is a good fit: load raw data into the lake/warehouse first, then transform inside it. That follows the **sushi principle**: the raw data is kept, so new questions (like the banana promotion) can be answered later without changing the pipeline. ETL is fine too if you want only clean data to enter the warehouse.
- SaaS data (CRM, card processor) is only available through vendor APIs, so pull it with **connector services** (Fivetran/Airbyte).

## 3. Data science
- Review **text** and shelf **photos** don't fit relational tables, so they go in the **data lake** as raw files on object storage, where they're cheap and in any format.
- Data scientists use pandas, scikit-learn, or Spark for NLP (review sentiment) and vision (empty-shelf detection).

## 4. Back to the product
- The "bought X, also bought Y" model is trained on warehouse/lake data, then deployed into the website/app using **reverse ETL** (or an ML deployment tool like MLflow or Kubeflow).
- The model and its recommendations are **derived data**. They can be retrained if lost.

## 5. Fraud in seconds
- Nightly ETL is too slow: by the time it runs, the fraud has already happened.
- Instead, stream checkout events into a **stream processor**, which scores each transaction in seconds and can block the card.
- If one system must both scan recent patterns *and* update or block records with low latency, an **HTAP** system is an option (the chapter's fraud example).

## 6. System of record vs derived
| Box | Type |
|---|---|
| POS, inventory, orders, suppliers, HR databases | **System of record** |
| SaaS (CRM, card processor) | System of record (owned by the vendor) |
| Data lake, warehouse, dashboards | Derived |
| ML model, recommendations | Derived |
| Fraud scores | Derived |

If the warehouse disagrees with the POS database, **the POS database is right** by definition.

## 7. Cloud or self-host?
- **(a) Warehouse: cloud** (e.g. Snowflake or BigQuery). Analytical load is extremely **bursty** (big parallel queries, then idle), so elasticity saves money. Building and operating a warehouse isn't a supermarket's core competency.
- **(b) Checkout systems in stores: largely self-hosted / on-premises, at least partly.** The till must keep working if the internet connection to the cloud drops, which means a local system in each store that syncs to the central database. Load is **predictable** (store opening hours), and there's no dependency on a vendor's outage. Many retailers run a **hybrid**: local POS in each store, cloud for central systems.

## 8. Architecture style
- **No microservices.** 6 engineers are effectively one team, so there's no coordination problem for microservices to solve; they'd only add deploy, monitoring, testing, and API-evolution overhead. Use a **modular monolith** with a database per bounded area if helpful, and split later if the team grows into many teams. (Bought-in SaaS like the CRM is already "someone else's service".)
- **Serverless for the nightly ETL: a good fit, if each step is short.** It runs once a night and is idle the rest of the time, so with metered billing you pay only for the minutes it runs. Watch the **execution time limits**: a multi-hour job must be split into smaller functions, or run on a managed batch service or warehouse ELT instead. Cold starts don't matter for a nightly job.

## 9. Privacy
**Where a loyalty customer's data lives:**
- *System of record:* the loyalty/CRM database and online orders database, plus POS transactions linked to the card
- *Derived:* data lake raw files, warehouse tables, BI extracts, caches, the search index, the **recommendation model and its training data**, and **backups**

**Erasing it:**
- Delete from the systems of record, then **propagate the deletion to every derived system**, just as updates must propagate (B3, B6).
- Raw files in an **append-only** lake can't be edited in place, so rewrite or compact the affected files, or use per-customer encryption keys and delete the key (crypto-shredding).
- Retrain or refresh models built on the customer's data.
- Keep an **audit log** of the deletion request itself, without the personal data.

**Data minimization:**
- Sales analytics don't need *who* bought bananas, so **anonymize or aggregate** POS data for analytics after a short period.
- Don't store precise **location trails** from the app.
- Set **retention periods**: delete raw clickstream after N months, as in B6's `purge_older_than`.
- Collect only what the loyalty programme's stated purpose needs, and don't reuse it for unrelated purposes.

**Card payments:** **PCI** compliance. Better still, use a PCI-certified payment processor so raw card numbers never touch your systems. Buyers of any software you sell to partners may also ask for **SOC 2 Type 2**.

## Interviewer follow-ups
- **F1. Store offline for 2 hours:** tills must keep working, so **each store runs a local POS system of record** (a local database on the store server or the tills themselves). Sales are recorded locally and **synced to the central systems when the link returns**, through an outbox or queue with idempotent upserts keyed by receipt ID. Card payments need an offline mode (floor limits, or deferred authorization), which is a business risk decision. That's why POS is the hybrid / self-hosted part of the design.
- **F2. Warehouse 3% below POS:** **reconcile step by step.** Compare daily counts and totals at each stage (POS → extract → lake → transformed table) to find where rows go missing. Common causes: **late-arriving data** (stores synced after the ETL cut-off; see F1), timezone boundaries, filters (returns, voids, test transactions), a failed partition load, or deduplication removing legitimate repeat purchases. POS is the system of record, so fix the pipeline, and add automated reconciliation checks with alerts.
- **F3. By 7 AM, then hourly:** first make the batch faster: load **incrementally** (only new or changed rows, using CDC or high-water marks) instead of full extracts, parallelize per store, and use ELT inside the warehouse. For **hourly**, switch to **micro-batches or streaming** (store events → Kafka → warehouse tables updated continuously), and accept that recent hours are provisional until late store data arrives.
- **F4. Why not one big Postgres?** OLTP volume would fit, but: (1) **analytics on multi-TB history** would be slow in a row store and would hurt operational traffic (S1); (2) **200 stores must survive WAN outages**, so a single central database can't be in every till's critical path; (3) **data silos**: SaaS tools (CRM, card processor) and the lake data (reviews, photos) don't live in Postgres; (4) one database means one blast radius. One Postgres is a fine *start* for the central operational database, just not the whole platform.

## Chapter concepts used
- OLTP vs OLAP
- Data silos
- Data warehouse and ETL/ELT, SaaS connectors
- Data lake and the sushi principle
- Reverse ETL
- Streams vs batch
- HTAP for fraud
- System of record vs derived data
- Cloud vs self-host (elasticity, core competency, control)
- Hybrid cloud
- Microservices as a people solution
- Serverless billing and limits
- Right to be forgotten vs append-only and derived data
- Data minimization
- PCI

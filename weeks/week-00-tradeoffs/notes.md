# Week 0 Notes: Trade-offs in Data Systems Architecture (DDIA Ch1)

> Summarized from the chapter text you shared (the full chapter). Add your own thoughts in the **My additions** section at the end.

---

## 1. The big idea
> "There are no solutions; there are only trade-offs." (Thomas Sowell)

- **Data-intensive application:** managing data is the *main* challenge (volume, changes, consistency under failures and concurrency, availability).
- **Compute-intensive application:** the challenge is parallelizing a huge computation.
- Apps are built by **gluing standard building blocks** together with application code:

| Building block | Job |
|---|---|
| Database | Store data so it can be found again later |
| Cache | Remember the result of an expensive operation to speed up reads |
| Search index | Search by keyword or filter in various ways |
| Stream processing | Handle events and changes as soon as they happen |
| Batch processing | Periodically crunch large amounts of accumulated data |

- It's easy when you use a tool for exactly what it was designed for. It gets hard when you must **choose between tools** and **combine** them.
- The book's goal is to teach you to *ask the right questions* to compare systems, because no approach is best in general.
- Different teams want different things from the **same data**, and these goals are often unstated, which leads to disagreements.

## 2. Terminology: frontend and backend
- **Frontend:** client-side code (browser or mobile app). It handles *one* user's data.
- **Backend:** server-side code handling requests for *all* users. This is where the hard data problems are.
- Backends are usually reached over HTTP (sometimes WebSocket).
- **Data infrastructure:** databases, caches, message queues, and similar systems.
- **Stateless application code:** the app forgets each request once it's handled. Anything that must persist lives on the client or in the data infrastructure.

## 3. Operational vs analytical systems

### Who uses data
| Role | What they do |
|---|---|
| Backend engineers | Build services that read and update data for users |
| Business analysts | Write reports for management (business intelligence, **BI**) |
| Data scientists | Find insights and build data/ML features (recommendations, fraud scoring, search ranking) |
| Data engineers | Connect operational and analytical systems and own the data infrastructure |
| Analytics engineers | Model and transform data so analysts and scientists can use it |

Analysts and scientists **read** data and **don't modify** it, but they may create **derived datasets**.

- **Operational systems:** where data is *created*. App code both reads and modifies data based on user actions.
- **Analytical systems:** a *read-only copy* of operational data, optimized for analytics.

### OLTP vs OLAP (Table 1-1, most important for exams and interviews)
"Transaction" here loosely means low-latency reads and writes. Chapter 8 defines it properly.

| Property | OLTP (operational) | OLAP (analytical) |
|---|---|---|
| Main read pattern | **Point queries** (fetch records by key) | **Aggregate** over many records |
| Main write pattern | Create/update/delete individual records | Bulk import (ETL) or event stream |
| Human user | End user of a web/mobile app | Internal analyst (decision support) |
| Machine use | Checking whether an action is authorized | Detecting fraud/abuse patterns |
| Queries | Fixed, predefined by the app | Ad-hoc, exploratory |
| Query volume | Lots of small queries | Few complex queries |
| Data represents | **Latest state** (now) | **History** of events over time |
| Dataset size | GB to TB | TB to PB |

- **Why OLTP users can't run custom SQL:** they could read or modify data they aren't allowed to see, and expensive queries would slow the database for everyone else. So OLTP runs *fixed queries baked into the app*.
- **OLAP users** write free-form SQL, or BI tools like Tableau, Looker, or Power BI generate it.
- **Product / real-time analytics** (Pinot, Druid, ClickHouse) are analytical queries *inside user-facing products*. They ingest in real time and are optimized for **low latency**. Traditional OLAP ingests in **batches** and is optimized for **throughput**.

## 4. Data warehousing
At first, one database did both jobs. From the late 1980s, companies moved analytics to a separate **data warehouse**.

**Why analysts shouldn't query OLTP systems directly:**
1. **Data silos:** the data is spread across many operational systems, so you can't join it in one query.
2. **Schemas differ:** a schema that's good for OLTP is poor for analytics (star/snowflake schemas come later).
3. **Performance:** expensive analytical queries slow things down for real users.
4. **Security/compliance:** OLTP systems may sit on networks analysts can't access.

- **Data warehouse:** a separate, read-only copy of data from *all* OLTP systems. Analysts can query it freely without affecting OLTP.
- **ETL (Extract → Transform → Load):** pull data out (periodic dump or continuous stream), transform it to an analysis-friendly schema and clean it, then load it into the warehouse.
- **ELT:** load first, then transform *inside* the warehouse.
- When sources are external **SaaS products** (CRM, email marketing, payments), you only get an API. Connector services like **Fivetran, Singer, or Airbyte** bring that data in.
- **HTAP (hybrid transactional/analytical processing):** OLTP and analytics in one system, with no ETL.
  - Internally it's often an OLTP system plus a separate analytics system behind one interface.
  - **It doesn't replace warehouses.** Good practice is one database per service (possibly hundreds), but **one warehouse** so analysts can combine everything.
  - It's useful when the *same app* needs both large scans and low-latency updates to individual records, e.g. **fraud detection**.
- **Trend:** the larger the scale, the more **specialized** systems become. General-purpose systems are fine at small scale.

## 5. Data lakes and beyond
**Why warehouses don't suit data scientists:**
- **Feature engineering:** turning rows into numerical vectors/matrices for ML needs custom code that's hard to write in SQL.
- **NLP / computer vision:** extracting structure from text (reviews) or images.
- Data scientists prefer **pandas, scikit-learn, R, and Spark**.

**Data lake:** a central store holding a copy of *any* potentially useful data **as files, with no imposed format, model, or schema**: Avro/Parquet records, text, images, video, sensor data, feature vectors, and so on.
- More flexible, and usually **cheaper** because it's built on object storage.
- ETL has generalized into **data pipelines**. A lake is often an intermediate stop on the way into the warehouse.
- **Sushi principle: "raw data is better".** Keep data raw, and let each consumer transform it the way it needs.

**Beyond the lake:**
- **DataOps:** the discipline of managing and operating pipelines. It's driven by governance, privacy, and regulation (GDPR, CCPA).
- **Streams:** file-based analysis reruns periodically (e.g. daily), while stream processing responds in **seconds**. That's valuable for blocking fraud.
- **Reverse ETL:** analytical outputs flowing *back* into operational systems, e.g. an ML model trained in the warehouse serving "people who bought X also bought Y". Tools include TFX, Kubeflow, and MLflow.

```
OLTP DBs ──ETL──> data lake (raw files) ──> data warehouse (SQL) ──> BI dashboards
     ^                         │
     └─────── reverse ETL ─────┘  (e.g. ML recommendations served to users)
```

## 6. Systems of record vs derived data
| | System of record (source of truth) | Derived data system |
|---|---|---|
| What it is | The authoritative version. New data is written here **first**. | Data produced by transforming data from another system |
| Duplication | Each fact stored **exactly once** (normalized) | Redundant: it duplicates existing information |
| If it disagrees with another system | **It wins**, by definition | It's the one that's wrong |
| If lost | Gone | **Can be re-created** from the source |
| Examples | Primary user/orders database | Caches, indexes, denormalized values, materialized views, trained ML models, the warehouse |

- Derived data is redundant **but essential for read performance**, and it lets you see the same data from different angles.
- Analytical systems are usually derived. Operational services mix both.
- **Being a system of record isn't a property of the tool.** It depends on *how you use it*. The same PostgreSQL could be either.
- When the source changes, you need a **process to update the derived data**. Most databases assume they're the only database, which makes this hard. Data pipelines (Ch11) solve it.

## 7. Cloud vs self-hosting
**Build or buy?** Rule of thumb: do your **core competency / competitive advantage** in-house, and outsource routine or commodity things. (Most companies don't make their own CPUs.)

**The spectrum** (Figure 1-2), from more control and more investment to less of both:
```
bespoke software, run in-house → off-the-shelf software you self-host (on-prem or IaaS VM) → SaaS / cloud service
```
- **On premises:** your own hardware, even if it's in a rented datacenter rack.
- **IaaS:** a VM in the cloud that *you* administer.

**When self-hosting is cheaper:** you already have the operational skills **and** your load is **predictable**.

**When cloud wins:**
- You don't know how to run the system, and hiring and training staff is expensive.
- A specialist provider gains expertise from many customers, which can mean better service.
- **Load varies a lot:** scale up and down instead of paying for idle machines sized for the peak. Analytical systems are a classic case: huge parallel bursts, then idle.

**Self-hosting advantage:** you can tune and customize it for your workload, which a vendor won't do for you.

**Cloud downsides: you have no control**
1. A missing feature means you can only ask the vendor.
2. An outage means you wait.
3. Performance bugs are hard to diagnose, with no access to OS metrics or server logs.
4. The service may shut down, get expensive, or change. You can't keep running an old version, so you're forced to migrate. With no standard APIs, that's **vendor lock-in**.
5. **Sanctions/geopolitics** can lock you out.
6. You must trust the provider with your data, which complicates privacy compliance.

**Reality:** cloud adoption keeps growing, often **hybrid**. In-house remains necessary for older systems and special requirements, e.g. **high-frequency trading** needs full control of the hardware.

## 8. Cloud-native architecture
**Cloud native** means designed from the start to use cloud services. It brings better performance on the same hardware, faster recovery, fast scaling, and support for bigger datasets.

| | Self-hosted | Cloud native |
|---|---|---|
| OLTP | MySQL, PostgreSQL, MongoDB | AWS Aurora, Azure SQL DB Hyperscale, Google Spanner |
| OLAP | Teradata, ClickHouse, Spark | Snowflake, BigQuery, Azure Synapse |

**Layering of services:**
- Self-hosted software uses generic resources: CPU, RAM, a filesystem, and an IP network. On IaaS it runs on VMs you administer.
- Cloud-native services **build on lower-level cloud services**. For example, **object storage** (S3, Azure Blob, Cloudflare R2):
  - Has a limited API (read/write whole files), but **hides the machines**.
  - Data is automatically spread across machines, so you don't run out of disk, and failed disks lose no data.
  - Snowflake is built on S3, and other services are built on Snowflake.
- **Rule:** higher-level abstractions are tied to specific use cases. If your need matches, use them; it's far less hassle. If nothing fits, build from lower-level parts.

**Separation of storage and compute:**
- **Traditionally**, a disk is durable, and **RAID** copies data across several disks in one machine.
- **In the cloud**, a VM's local disk is treated as an **ephemeral cache**. It's gone if the instance fails or is replaced with a different size.
- **Virtual disks** (EBS, Azure managed disks, GCP persistent disks) can be detached and reattached. They emulate a block device (4 KiB blocks) using other machines. This lets old disk-based software run in the cloud, **but** it adds overhead, and since **every I/O is a network call**, it's sensitive to network glitches.
- Cloud-native systems instead use **specialized storage services**. Object stores suit large files (hundreds of KB to GB), so databases keep **small values in a separate service** and pack many values into **large blocks in object storage** (Ch4).
- Storage and compute become **disaggregated**: S3 only stores, so computing on the data means moving it over the network.
- **Multitenancy:** many customers share the same hardware and service. That gives better utilization, easier scaling, and easier management, **but** requires careful isolation so one customer can't hurt another's performance or security.

## 9. Operations in the cloud era
- **DBAs/sysadmins → DevOps → SRE** (Google's version of DevOps).
- **Operations' job:** deliver services reliably (configure, deploy) and keep production stable (monitor, diagnose).
- **Self-hosted ops** is machine-level work: capacity planning, provisioning, moving services, OS patches.
- **The cloud hides machines** behind APIs. **Metered billing** replaces fixed-size disks, and services stay available despite machine failures.

**DevOps/SRE emphasizes:**
- automation (repeatable processes over manual one-off jobs)
- ephemeral VMs and services over long-running servers
- frequent application updates
- learning from incidents
- preserving knowledge as people come and go

**A split in roles:** infrastructure companies' ops teams run services for many customers, while their customers try to spend as little effort as possible on infrastructure.

**What cloud customers' ops still do:** choose services, integrate them, and migrate between them.
- **Capacity planning becomes financial planning, and performance optimization becomes cost optimization.**
- Know the **quotas and limits** before you hit them.
- **Integration** across vendors is hard because there are no standards, so it's often manual work.
- **Can't be outsourced:** application and library security, interactions between your own services, load monitoring, and debugging slowdowns or outages.

**The need for operations is as great as ever.**

## 10. Distributed vs single-node systems
**Distributed system:** several machines communicating over a network. Each participating process is a **node**.

**Reasons to distribute:**
| Reason | Meaning |
|---|---|
| Inherent distribution | Multiple users on their own devices must communicate over a network |
| Requests between cloud services | Data stored in one service and processed in another. Cloud-native systems and microservices are distributed by nature. |
| Fault tolerance / high availability | Redundancy: if one machine fails, another takes over (Ch6) |
| Scalability | Load bigger than one machine can handle |
| Latency | Servers near users around the world |
| Elasticity | Scale up and down with demand. A single machine must be sized for the peak. |
| Specialized hardware | Disk-heavy storage nodes, CPU/RAM-heavy analytics nodes, GPU nodes for ML |
| Legal compliance | **Data residency laws** require data to stay in-country |
| Sustainability | Run jobs where and when renewable power is plentiful |

### Problems with distributed systems
| Problem | Detail |
|---|---|
| **Any request can fail** | The network drops, or the service is overloaded or crashed, so the request **times out**. You then **don't know whether it was processed**, so a blind **retry may not be safe** (e.g. charging twice). Ch9 covers this. |
| **Network calls are slow** | A call to another service is **vastly slower** than a function call in the same process. With large data, it can be faster to **bring the computation to the data** than to move the data to the computation. |
| **More nodes ≠ faster** | A simple single-threaded program on one computer can beat a **cluster with 100+ CPU cores**. |
| **Hard to troubleshoot** | If it's slow, *where* is the problem? **Observability** means collecting data about the system's execution so you can query both high-level metrics and individual events. **Tracing tools** (OpenTelemetry, Zipkin, Jaeger) record which client called which server, for which operation, and how long each call took. |
| **Consistency across services** | Databases guarantee consistency within themselves (Ch6, Ch8). When each service has its own database, **keeping data consistent across services becomes the application's problem**. **Distributed transactions** (Ch8) are rarely used with microservices: they go against service independence, and many databases don't support them. |

**Conclusion:** a single machine is often **much simpler and cheaper**. CPUs, memory, and disks keep getting bigger, faster, and more reliable. With single-node databases like **DuckDB, SQLite, and KùzuDB**, many workloads now fit on one node (Ch4).

## 11. Microservices and serverless

### Client/server, SOA, and microservices
- The most common way to distribute a system: **clients send requests to servers**, usually over HTTP (Ch5, REST and RPC). A process can be both a server (handling incoming requests) and a client (calling other services).
- Traditionally this was called **service-oriented architecture (SOA)**. It has since been refined into **microservices**:
  - each service has **one well-defined purpose** (e.g. S3 = file storage)
  - each exposes an **API** called over the network
  - each has **one team** responsible for it
- Cloud-native systems decompose heavily into services, but on-premises systems can be service-oriented too.

| ✅ Advantages | ❌ Costs |
|---|---|
| Each service can be **updated independently**, so teams coordinate less | **Testing is hard**: you need to run all the services it depends on |
| Each service gets the **hardware it needs** | **Every service needs infrastructure**: deploys, scaling, logs, health monitoring, on-call alerts. **Kubernetes** became popular as a foundation for this. |
| The API **hides implementation**, so owners can change internals freely | **APIs are hard to evolve**: adding or removing fields can break clients, often discovered late (in staging or production). **OpenAPI** and **gRPC** help (Ch5). |

**Each service has its own database, never shared:**
1. A shared database makes its **whole structure part of the API**, so it becomes hard to change.
2. One service's queries could **hurt another's performance**.

> **Microservices are a technical solution to a *people* problem:** they let teams make progress without coordinating. That's valuable in a **large company**. In a **small company**, it's usually unnecessary overhead, so build the simplest thing.

### Serverless (FaaS, function as a service)
- Infrastructure management is outsourced to the cloud vendor.
- With **VMs**, *you* decide when to start or stop instances. With **serverless**, the provider **allocates and frees resources automatically** based on incoming requests.
- **Analogy:** cloud storage replaced capacity planning with metered billing. Serverless brings **metered billing to code execution**: you pay only while your code is running.
- **Limitations:**
  - **time limits** on execution
  - **restricted runtime environments**
  - **slow start times** on the first invocation (cold starts)
- **The name is misleading:** functions still run on servers, but each execution might run on a *different* server.
- "Serverless" is also used loosely (BigQuery, Kafka offerings) to mean **autoscales and bills by usage** rather than by machine instance.

## 12. Cloud computing vs supercomputing (HPC)
| | Supercomputing / HPC | Cloud computing |
|---|---|---|
| **Used for** | Compute-intensive science: weather, climate, molecular dynamics, optimization, PDEs | Online services and business data systems that serve users with **high availability** |
| **When a node fails** | Large batch jobs **checkpoint** to disk. On failure: **stop the whole cluster**, repair the node, restart from the last checkpoint. | Stopping everything is unacceptable: services must keep serving users |
| **Communication and trust** | Shared memory and **RDMA**: high bandwidth, low latency, but assumes **high trust** between users | Shared by **mutually untrusting** organizations, so it needs isolation (VMs), encryption, and authentication |
| **Network** | Specialized topologies (**multidimensional meshes, toruses**) for known communication patterns | IP/Ethernet in **Clos topologies** for high **bisection bandwidth** (a common measure of overall network performance) |
| **Geography** | All nodes close together | Nodes can span **multiple regions** |

Large analytical systems share some HPC traits, but **this book focuses on continuously available services**.

## 13. Data systems, law, and society
Architecture is shaped by business needs, **and** by a responsibility to **society**.

**Regulation:**
- **GDPR** (2018, Europe) gives people control and legal rights over their personal data. Similar laws exist elsewhere, e.g. **CCPA** (California).
- **EU AI Act:** further limits on how personal data can be used in AI.
- **Beyond regulation:** social media shapes news consumption and elections. Automated systems decide **loans, insurance, job interviews, and criminal suspicion**.
- **Everyone** building these systems shares responsibility for their ethical impact and legal compliance. Basic awareness matters as much as knowing distributed systems basics.

**The law affects system design itself: the right to be forgotten**
- GDPR gives the right to have your data **erased on request**.
- **Conflict 1:** many systems rely on **immutable, append-only logs**. How do you delete something in the middle of an immutable file?
- **Conflict 2:** deleted data may already be in **derived datasets**, e.g. **ML training data**.
- There are **no clear guidelines** on which technologies are "GDPR compliant". The law deliberately sets high-level principles, not technologies.

**The true cost of storing data** goes beyond the S3 bill:
- liability and **reputational damage** if it leaks
- **legal costs and fines** if processing isn't compliant
- governments or police may **compel handover**, which is a real **safety risk** to users when data reveals criminalized behaviour (e.g. location data or IP logs revealing a visit to an abortion clinic)

**Data minimization** (*Datensparsamkeit*): some data simply **isn't worth storing**, so delete it.
- This runs counter to "big data" (store everything in case it's useful later).
- It matches GDPR: collect personal data only for a **specified, explicit purpose**, **don't reuse it for other purposes**, and **don't keep it longer than necessary**.

**Industry standards:**
- **PCI** (Payment Card Industry) standards: required by card companies for payment processors, with frequent independent audits
- **SOC 2 Type 2:** buyers increasingly require it of software vendors, verified by third-party audits

**Balance** the needs of the business against the people whose data you process. Ch14 goes deeper into ethics, bias, and discrimination.

## 14. Chapter summary
1. **Trade-offs:** most questions have several answers, each with pros and cons.
2. **OLTP vs OLAP:** different access patterns *and* different audiences. Warehouses and lakes are fed by ETL. Their internal layouts differ (Ch4).
3. **Cloud vs self-hosting:** which is cheaper depends on your situation, but cloud-native design is changing architecture, e.g. **separating storage and compute**.
4. **Distributed vs single machine:** cloud systems are inherently distributed. Sometimes it's unavoidable, but **don't rush into distributing if one machine will do** (Ch9).
5. **Law and society:** privacy regulation shapes architecture too, and engineers often ignore it. Turning legal requirements into technical designs isn't formalized yet.

## 15. Key terms
| Term | One-line meaning |
|---|---|
| Data-intensive | Managing data is the main challenge |
| Stateless service | Forgets each request; state lives in the data infrastructure |
| OLTP | Interactive point reads and writes of current state |
| OLAP | Aggregating scans over history, ad hoc |
| Point query | Fetch a few records by key |
| BI | Business intelligence: reports for decision-making |
| Data warehouse | Separate read-only analytics DB combining all OLTP data |
| ETL / ELT | Extract-transform-load / extract-load-transform |
| Data silo | Data trapped in separate systems that can't be queried together |
| HTAP | OLTP and analytics in one system |
| Data lake | Raw files of any format, cheap object storage |
| Sushi principle | Raw data is better |
| Reverse ETL | Analytics output pushed back into operational systems |
| System of record | Authoritative source of truth |
| Derived data | Re-creatable transformed copy (cache, index, view, model) |
| IaaS | Rented VMs you administer |
| SaaS | Software run by a vendor, used via UI or API |
| Cloud native | Designed to build on cloud services |
| Object storage | S3-style file store that hides the machines |
| Disaggregation | Storage and compute separated |
| Multitenancy | Many customers on shared hardware |
| Vendor lock-in | Switching is expensive because there are no standard APIs |
| SRE / DevOps | Development and operations combined, automation-first |
| Node | One process in a distributed system |
| Elasticity | Scaling resources up and down with demand |
| Data residency | Laws requiring data to stay in-country |
| Observability | Collecting execution data so both metrics and individual events can be queried |
| Distributed tracing | Recording which service called which, for what, and how long it took (OpenTelemetry, Zipkin, Jaeger) |
| Distributed transaction | A transaction spanning several databases or services (rare in microservices) |
| SOA | Service-oriented architecture: the client/server ancestor of microservices |
| Microservice | One purpose, one API, one team, its own database |
| Kubernetes | Orchestration framework for deploying and running services |
| OpenAPI / gRPC | Standards for describing service APIs |
| Serverless / FaaS | The provider runs your functions on demand, billed per execution time |
| Cold start | Slow first invocation of a serverless function |
| HPC | High-performance computing (supercomputers), checkpoint-and-restart |
| RDMA | Remote direct memory access: fast, but assumes high trust |
| Bisection bandwidth | A common measure of a network's overall capacity |
| GDPR / CCPA | European / Californian privacy laws |
| Right to be forgotten | The right to have your data erased on request |
| Data minimization | Don't store data whose risk outweighs its value (*Datensparsamkeit*) |
| PCI / SOC 2 | Audited compliance standards for payment processors / software vendors |

## 16. How this connects to later weeks
- OLTP vs OLAP storage: Week 7 (column stores)
- Normalization and star schemas: Week 3
- Caches and indexes as derived data: Weeks 5–6
- Fault tolerance and replication: Weeks 1, 9–10
- Timeouts and unsafe retries: Week 14
- Pipelines, streams, and reverse ETL: Weeks 17–19
- Single-node engines (DuckDB, SQLite): Week 7
- REST/RPC, OpenAPI/gRPC, API evolution: Week 8
- Distributed transactions: Week 13
- Deleting from append-only logs (compaction, tombstones): Week 5
- Ethics, bias, and compliance: Week 20

---

## My additions
(Your own thoughts, examples from work, and links to videos you watched.)
-

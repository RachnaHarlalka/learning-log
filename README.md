# 15-Day Python + Database Interview Prep (Nov 16 – Nov 30, 2026)

Branch `python` of my learning log. I'm preparing for **client interviews for full-stack projects** at my association.
I study **1 hour per day**: **30 min Python + 30 min Database (PostgreSQL / SQL)**.
Everything is **interview-oriented**: concepts I can explain clearly, code I can write live, and answers to the questions clients actually ask.

> The earlier 42-day Python-only plan is paused. It lives in [archive/42-day-plan/](archive/42-day-plan/README.md) (see the bottom of this page).

---

## How each day works

```
days/day-NN/
├── python/
│   ├── theory.md        # concepts + interview Q&A
│   ├── practice.py      # exercises with TODOs + function stubs
│   └── test_practice.py # pytest tests so I can self-check
├── database/
│   ├── theory.md        # concepts + interview Q&A
│   ├── setup.sql        # tables + sample data (only if new tables are needed)
│   └── practice.sql     # numbered query exercises
└── solutions/           # created ONLY on "show solutions day N"
project/                 # the Task Manager, one small feature added per day
```

**The 1-hour routine**

| Time | What |
|---|---|
| 12 min | Read `python/theory.md` |
| 18 min | Do `python/practice.py` until `pytest days/day-NN/python` is green, then the day's `project/` feature |
| 12 min | Read `database/theory.md` |
| 18 min | Run `database/practice.sql` in `psql` and write each query |

Rule: try first, peek later. Solutions only after my own attempt.

### Setup (once)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pytest
brew install postgresql@17 && brew services start postgresql@17   # see Day 1 database/theory.md
createdb interview_prep
```

Run one day's Python tests with `pytest days/day-NN/python`. Run the project tests with `pytest project`. (Run one day at a time: every day has a `test_practice.py`.)

---

## Commands I use with Claude Code

| Command | What it does |
|---|---|
| `Day N` / `start Day N` / `generate today` | Generate that day's folder following the rules in the next section |
| `quiz day N` | 10 rapid-fire interview questions on that day's topics, one at a time; waits for my answer and grades it |
| `show solutions day N` | Write solutions with explanations into `days/day-NN/solutions/` |
| `revise days A-B` | One-page revision sheet of those days |
| `mock interview` | Claude acts as a client interviewer (Day 15) |

After each day, update the **Progress Tracker** below.

## Daily generation rules (for Claude Code)

**theory.md format (Python and DB)**
1. **Why this matters in interviews**: 2–3 lines.
2. **Core concepts**: short explanations, each with a small code/SQL example.
3. **Common pitfalls / gotchas**: the traps interviewers like to test.
4. **Top interview questions**: 8–10 questions with crisp model answers (under 60 seconds out loud).
5. **One-line cheat sheet**: a recap I can revise in 2 minutes before an interview.

Each theory file is readable in about 12 minutes, so the remaining ~18 minutes go to practice.

**practice files format**
- 5–7 exercises, ordered easy → medium → interview-level. At least one is a real interview-style question.
- Python: function stubs + docstrings + pytest tests.
- SQL: each exercise has a comment with the question and the expected output shape (columns).
- No solutions in the practice files.

**Running projects (consistent across all days)**
- **Python mini-project:** a "Task Manager" that grows daily (functions → classes → file storage → database → REST API on Day 13). Each day adds one small feature in `project/`.
- **Database:** one shared **e-commerce + company schema** in PostgreSQL, created on Day 1 and extended later: `departments, employees, customers, products, categories, orders, order_items, payments`. Reused every day.

---

## Roadmap

### Week 1: Foundations

**Day 1 · Mon Nov 16: Setup & Basics** ([open](days/day-01/))
- **Python:** installing Python, venv, running scripts; variables, data types (int, float, str, bool, None); dynamic typing; mutable vs immutable; `type()`, `id()`, `is` vs `==`; input/output; f-strings.
- **Database:** what a database is, DBMS vs RDBMS, SQL vs NoSQL overview; install PostgreSQL; tables, rows, columns, data types (INT, VARCHAR, TEXT, NUMERIC, DATE, TIMESTAMP, BOOLEAN); `CREATE TABLE`, `INSERT`, basic `SELECT`. Create the shared schema.
- **Interview focus:** "Is Python compiled or interpreted?", "Mutable vs immutable?", "What is an RDBMS?"

**Day 2 · Tue Nov 17: Strings, Lists, Tuples | Filtering Data**
- **Python:** string methods, slicing, list operations & methods, tuples, packing/unpacking, list comprehensions (intro).
- **Database:** `WHERE`, comparison/logical operators, `IN`, `BETWEEN`, `LIKE`/`ILIKE`, `IS NULL`, `ORDER BY`, `LIMIT/OFFSET`, `DISTINCT`, aliases.
- **Interview focus:** list vs tuple, reversing a string, NULL behavior in comparisons.

**Day 3 · Wed Nov 18: Dicts & Sets | Aggregation**
- **Python:** dictionaries, sets, dict/set comprehensions, iteration patterns, shallow vs deep copy, hashability.
- **Database:** `COUNT, SUM, AVG, MIN, MAX`, `GROUP BY`, `HAVING`, `WHERE` vs `HAVING`, logical order of SQL execution (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT).
- **Interview focus:** "Why can't a list be a dict key?", count word frequency, `COUNT(*)` vs `COUNT(col)`.

**Day 4 · Thu Nov 19: Functions | Constraints & Relationships**
- **Python:** control flow, functions, `*args/**kwargs`, default arguments, mutable default pitfall, LEGB scope, `global/nonlocal`, lambda, `map/filter/sorted` with keys.
- **Database:** PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, CHECK, DEFAULT; 1:1, 1:N, M:N relationships (junction tables); `UPDATE`, `DELETE`, `ON DELETE CASCADE`; `DELETE` vs `TRUNCATE` vs `DROP`.
- **Interview focus:** mutable default argument bug, primary vs unique key, designing M:N.

**Day 5 · Fri Nov 20: Errors & Files | JOINs**
- **Python:** `try/except/else/finally`, raising and custom exceptions, file handling, `with` / context managers, JSON and CSV read/write. Project: save tasks to a JSON file.
- **Database:** INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF JOIN; join conditions vs filters; finding unmatched rows with LEFT JOIN + NULL.
- **Interview focus:** "What does `finally` guarantee?", "Customers who never ordered", employee–manager self join.

**Day 6 · Sat Nov 21: OOP Part 1 | Subqueries & Set Operations**
- **Python:** classes & objects, `__init__`, `self`, instance vs class attributes, `@classmethod`, `@staticmethod`, `@property`, encapsulation. Project: convert Task Manager to classes.
- **Database:** subqueries (scalar, in `FROM`, in `WHERE`), correlated subqueries, `EXISTS` vs `IN`, `UNION` vs `UNION ALL`, `INTERSECT`, `EXCEPT`.
- **Interview focus:** classmethod vs staticmethod, second-highest salary, UNION vs UNION ALL.

**Day 7 · Sun Nov 22: OOP Part 2 | Normalization & Schema Design**
- **Python:** inheritance, `super()`, MRO, polymorphism, abstraction (`abc`), dunder methods (`__str__`, `__repr__`, `__eq__`, `__len__`), `dataclasses`.
- **Database:** normalization 1NF → 2NF → 3NF → BCNF, anomalies, when to denormalize, ER diagrams; design a schema from a client requirement.
- **Interview focus:** 4 pillars of OOP, `__str__` vs `__repr__`, "Normalize this table", "Design the DB for a booking app".
- **+ Weekly revision:** `revise days 1-7` and `quiz` on weak areas.

### Week 2: Intermediate & Interview-Level

**Day 8 · Mon Nov 23: Iterators, Generators, Decorators | Indexes**
- **Python:** iterables vs iterators, `iter/next`, generators & `yield`, generator expressions, closures, decorators (with arguments, `functools.wraps`). Write a timing/logging decorator.
- **Database:** how indexes work (B-tree), single vs composite indexes, column order, unique and partial indexes, when indexes hurt, `EXPLAIN` / `EXPLAIN ANALYZE`, clustered vs non-clustered (concept).
- **Interview focus:** generator vs list memory, "Write a decorator", "Why is my query slow?"

**Day 9 · Tue Nov 24: Modules & Typing | Window Functions & CTEs**
- **Python:** modules, packages, `__name__ == "__main__"`, imports, pip & `requirements.txt`, type hints, PEP 8, project structure.
- **Database:** CTEs (`WITH`), recursive CTEs (org chart), window functions: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG/LEAD`, running totals, `PARTITION BY`.
- **Interview focus:** RANK vs DENSE_RANK, top-N per group, month-over-month growth.

**Day 10 · Wed Nov 25: Problem Solving | Transactions**
- **Python:** Big-O basics; `collections` (`Counter`, `defaultdict`, `deque`, `namedtuple`), `heapq`; patterns: hash map, two pointers, sliding window. Classic problems: two-sum, anagrams, duplicates, valid parentheses.
- **Database:** transactions, `BEGIN/COMMIT/ROLLBACK`, savepoints, ACID, isolation levels, dirty/non-repeatable/phantom reads, locking, deadlocks.
- **Interview focus:** live coding of 2–3 easy/medium problems, "Explain ACID with a bank transfer".

**Day 11 · Thu Nov 26: Python Internals & Concurrency | Advanced DB Objects & Security**
- **Python:** memory management, reference counting & garbage collection, the GIL, threading vs multiprocessing vs asyncio (when to use which), `async/await` basics.
- **Database:** views & materialized views, functions/stored procedures, triggers, roles & permissions, SQL injection and parameterized queries.
- **Interview focus:** "What is the GIL?", "Is Python good for concurrency?", "How do you prevent SQL injection?"

**Day 12 · Fri Nov 27: Python ↔ Database | NoSQL & Caching**
- **Python:** `psycopg` (PostgreSQL driver), connections & cursors, parameterized queries, transactions from code; SQLAlchemy ORM basics (models, session, CRUD). Project: move Task Manager storage to PostgreSQL.
- **Database:** MongoDB basics (documents, collections), SQL vs NoSQL trade-offs, CAP theorem, Redis as a cache, when to choose what.
- **Interview focus:** ORM vs raw SQL, "SQL or NoSQL for this project?", connection pooling.

**Day 13 · Sat Nov 28: REST API (Full-Stack Bridge) | Production DB Concerns**
- **Python:** FastAPI CRUD API for the Task Manager: routes, path/query params, Pydantic models, HTTP methods & status codes, REST principles, CORS (for a frontend). How a frontend talks to this API.
- **Database:** migrations (Alembic), N+1 query problem, pagination strategies, connection pooling, backups.
- **Interview focus:** "Walk me through a request from the browser to the DB", PUT vs PATCH, 401 vs 403, N+1.

**Day 14 · Sun Nov 29: Testing & Best Practices | SQL Interview Problem Set & Scaling**
- **Python:** `pytest` (fixtures, parametrize), mocking basics, logging, env variables & config, clean code, Git workflow basics.
- **Database:** classic SQL interview problems (Nth highest salary, duplicates, consecutive records, top-N per group, pivoting with `CASE`, employees earning more than managers); scaling: replication, partitioning, sharding, read replicas.
- **Interview focus:** timed problem solving, "How would you scale this DB to 10x users?"

**Day 15 · Mon Nov 30: Full Mock Interview**
- **Python (30 min):** Claude acts as a client interviewer: 10 concept questions + 2 live coding problems + 1 "explain your project" question. Grade each answer and suggest a better answer.
- **Database (30 min):** 5 SQL queries on the shared schema + 1 schema design from a client brief + 5 concept questions.
- **Also prepare:** a 2-minute self-introduction, a 3-minute walkthrough of the Task Manager project (architecture: FastAPI + PostgreSQL), and answers to "Why should we pick you for this project?"
- **Output:** a final report with strengths, weak topics, and a 7-day follow-up plan (next: frontend: HTML/CSS/JS/React).

---

## Interview priority map (if time is short, never skip these)

| Python | Database |
|---|---|
| Mutable vs immutable, list/dict/set | JOINs (all types) |
| Functions, `*args/**kwargs`, scope | GROUP BY / HAVING |
| OOP (4 pillars, dunder methods) | Keys & constraints, normalization |
| Exceptions & context managers | Indexes & query performance |
| Generators & decorators | Window functions & CTEs |
| GIL & concurrency basics | Transactions & ACID |
| FastAPI + REST basics | SQL vs NoSQL, SQL injection |

---

## Progress tracker

| Day | Date | Python done | DB done | Confidence (1–5) | Weak topics |
|---|---|---|---|---|---|
| 1 | Nov 16 | [ ] | [ ] | | |
| 2 | Nov 17 | [ ] | [ ] | | |
| 3 | Nov 18 | [ ] | [ ] | | |
| 4 | Nov 19 | [ ] | [ ] | | |
| 5 | Nov 20 | [ ] | [ ] | | |
| 6 | Nov 21 | [ ] | [ ] | | |
| 7 | Nov 22 | [ ] | [ ] | | |
| 8 | Nov 23 | [ ] | [ ] | | |
| 9 | Nov 24 | [ ] | [ ] | | |
| 10 | Nov 25 | [ ] | [ ] | | |
| 11 | Nov 26 | [ ] | [ ] | | |
| 12 | Nov 27 | [ ] | [ ] | | |
| 13 | Nov 28 | [ ] | [ ] | | |
| 14 | Nov 29 | [ ] | [ ] | | |
| 15 | Nov 30 | [ ] | [ ] | | |

---

## Archived: the 42-day Python plan (paused)

The original 1-hour-a-day, Python-only plan (JS-to-Python, 7 phases, notebooks) is paused until the sprint ends. Day 1 is done and kept with the full roadmap in [archive/42-day-plan/](archive/42-day-plan/README.md). After Nov 30, resume from its Day 2, or fold its remaining topics (iteration protocols, `itertools`, typing, asyncio, DSA) into the 7-day follow-up plan from Day 15.

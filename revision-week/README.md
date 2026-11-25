# Python revision (Python only)

A 10-day, hands-on Python revision for client interviews on backend / full-stack roles like the Apple Finance JD (Python + FastAPI services, APIs, data processing, clean tested code). It follows the topic order of **Python for Everybody** (University of Michigan, Dr. Charles Severance) and then goes well past it (Days 6-10) to the depth expected from someone with ~4 years of experience.

- Free book: [py4e.com](https://www.py4e.com/) · Course: [Coursera specialization](https://www.coursera.org/specializations/python) (5 courses)
- **Python only.** No SQL study, React or DevOps here. SQLite appears only as Python's `sqlite3` module (Day 7).

## How it works

Each day is a folder with two notebooks:

| File | What it is |
|---|---|
| `exercises.ipynb` | Your workspace. Each exercise has a prompt, a code cell with a stub, and a **check cell** that prints ✅ or ❌ with a hint. Ends with a score and "Say it out loud" interview questions. |
| `solutions.ipynb` | Reference solutions (every check passes) and model answers to the interview questions. Open it **after** you try. |

**The loop for each exercise:** read the prompt → write code in the code cell → run it → run the check cell → fix until ✅. Stuck for 10 minutes? Open the collapsed **Hint**, not the solution.

### Setup (once)
```bash
source .venv/bin/activate
pip install ipykernel          # lets VS Code / Jupyter run notebooks in this venv
```
Open an `exercises.ipynb` in VS Code, pick the `.venv` kernel, and run the first cell. Days 7 and 10 install `fastapi` and `httpx` in their own first cell.

## The 10 days

Plan on roughly **75-110 minutes** per day (about 7-8 exercises plus the spoken questions).

> **Experienced? Move fast through Days 1-3.** They are fundamentals you should already know. Aim for about 45 minutes each (do the `medium` and `interview` exercises and the spoken questions) and spend the saved time on Days 8-10, which is where interviews at the 4-year level actually go.

| Day | Topic | Python for Everybody | Why the JD cares | Exercises |
|---|---|---|---|---|
| 1 | [Core Python](day-1-core-python/): types, decisions, loops, functions, mutable defaults | Course 1, ch. 1-5 | clean, correct basics | 7 |
| 2 | [Strings and files](day-2-strings-and-files/) | Course 2, ch. 6-7 | parsing text and logs | 7 |
| 3 | [Lists, dicts, tuples, sets](day-3-lists-dicts-sets/) | Course 2, ch. 8-10 | reshaping data, hash maps | 8 |
| 4 | [Regex, JSON, CSV, API data](day-4-regex-json-apis/) | Course 3, ch. 11-13 | integration components, API error handling | 8 |
| 5 | [OOP and exceptions](day-5-oop-and-exceptions/) | Course 4, ch. 14 | owning components, clean design | 7 |
| 6 | [Intermediate Python](day-6-intermediate-python/): comprehensions, generators, decorators | beyond the course | reusable, scalable code | 8 |
| 7 | [Backend Python](day-7-backend-python/): dataclasses, `sqlite3`, SQL injection, mocking, FastAPI | Course 4 ch. 15 + beyond | the actual job: APIs, data, tests | 7 |
| 8 | [Python internals](day-8-python-internals/): copies, iterators, dunders and hashing, MRO, `__slots__`, `contextlib`, `lru_cache`, LRU cache | beyond the course | "why does Python do that?" questions | 8 |
| 9 | [Concurrency and async](day-9-concurrency-and-async/): `gather`, Semaphore, timeouts, threads vs processes, retries, locks | beyond the course | FastAPI is async; the GIL; integration jobs | 7 |
| 10 | [Production FastAPI](day-10-production-fastapi/): `Depends` and overrides, 401 vs 403, pagination, error handlers, middleware, pytest, logging, config, idempotency | beyond the course | running a real service, not just a route | 7 |

Day 6, the FastAPI/typing/mocking parts of Day 7, and all of Days 8-10 go beyond *Python for Everybody* on purpose, because the course stops before them but the JD (and a 4-year interview) does not.

## How the JD maps to this week

| JD line | Where you practise it |
|---|---|
| "Build backend services and APIs using Python and FastAPI" | Day 7, exercise 6 (routes, Pydantic, 201/404/422); Day 10 (dependencies, auth, pagination, errors, middleware) |
| "Design APIs that expose data securely and efficiently" | Day 4 (status handling), Day 7 (validation, SQL injection), Day 10 (401 vs 403, pagination, idempotent payments) |
| "Data processing and integration components" | Days 2-4 (files, regex, JSON, CSV, flatten, group) |
| "Write clean, modular, reusable, well-tested code" | Days 1, 5, 6 and the test-writing exercise on Day 7 |
| "Develop automated unit/API tests" | Day 7: `TestClient`, `Mock`, writing test cases; Day 10: fixtures, `parametrize`, `monkeypatch`, dependency overrides |
| "Diagnose production issues, root causes" | Day 5 exceptions, Day 4 retryable vs non-retryable errors, Day 8 memory and references, Day 10 logging and slow-endpoint debugging |
| "Large datasets" | Day 6 generators and batching (memory-friendly processing), Day 9 concurrent batch processing |
| "Scalable, high-performance services" | Day 9: asyncio vs threads vs processes, the GIL, blocking calls in `async def` |
| React, Node.js, SQL platforms, CI/CD | Not covered here (Python only) |

## The last hour: rehearse out loud

Once Day 10 is done, answer these without notes, in under 60 seconds each (every one is a "Say it out loud" question in the notebooks):

1. Compiled or interpreted? · 2. Mutable vs immutable · 3. `is` vs `==` · 4. The mutable default argument bug
5. List vs tuple, and why a list can't be a dict key · 6. Shallow vs deep copy · 7. `with` and context managers
8. Generator vs list · 9. What is a decorator? · 10. `*args` / `**kwargs` · 11. The four pillars of OOP
12. `__str__` vs `__repr__` · 13. Which API errors do you retry? · 14. How do you stop SQL injection?
15. Why mock dependencies in tests? · 16. What does FastAPI give you over plain code?
17. Why don't threads speed up CPU-bound Python (the GIL)? · 18. How does Python free memory, and what leaks?
19. `__eq__` without `__hash__` · 20. MRO and what `super()` really calls · 21. Iterable vs iterator
22. asyncio vs threads vs processes for 500 API calls · 23. Blocking code inside `async def` · 24. `def` vs `async def` routes
25. Processing a 1M-row CSV with an API call per row · 26. Structuring a 20-endpoint FastAPI service
27. Debugging a slow endpoint after a release · 28. Making a breaking API change · 29. Unit vs integration tests
30. Where secrets live and how the app loads them

Then explain your **Task Manager** project (`project/`) in 3 minutes: what it does, how it is structured, and one trade-off you chose.

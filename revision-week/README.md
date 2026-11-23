# Python revision week (Python only)

A 7-day, hands-on Python revision for client interviews on backend / full-stack roles like the Apple Finance JD (Python + FastAPI services, APIs, data processing, clean tested code). It follows the topic order of **Python for Everybody** (University of Michigan, Dr. Charles Severance) and then goes a bit past it where the JD asks for more.

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
Open an `exercises.ipynb` in VS Code, pick the `.venv` kernel, and run the first cell. Day 7 installs `fastapi` and `httpx` in its own first cell.

## The 7 days

Plan on roughly **75-100 minutes** per day (about 7-8 exercises plus the spoken questions).

| Day | Topic | Python for Everybody | Why the JD cares | Exercises |
|---|---|---|---|---|
| 1 | [Core Python](day-1-core-python/): types, decisions, loops, functions, mutable defaults | Course 1, ch. 1-5 | clean, correct basics | 7 |
| 2 | [Strings and files](day-2-strings-and-files/) | Course 2, ch. 6-7 | parsing text and logs | 7 |
| 3 | [Lists, dicts, tuples, sets](day-3-lists-dicts-sets/) | Course 2, ch. 8-10 | reshaping data, hash maps | 8 |
| 4 | [Regex, JSON, CSV, API data](day-4-regex-json-apis/) | Course 3, ch. 11-13 | integration components, API error handling | 8 |
| 5 | [OOP and exceptions](day-5-oop-and-exceptions/) | Course 4, ch. 14 | owning components, clean design | 7 |
| 6 | [Intermediate Python](day-6-intermediate-python/): comprehensions, generators, decorators | beyond the course | reusable, scalable code | 8 |
| 7 | [Backend Python](day-7-backend-python/): dataclasses, `sqlite3`, SQL injection, mocking, FastAPI | Course 4 ch. 15 + beyond | the actual job: APIs, data, tests | 7 |

Day 6 and the FastAPI/typing/mocking parts of Day 7 go beyond *Python for Everybody* on purpose, because the course stops before them but the JD does not.

## How the JD maps to this week

| JD line | Where you practise it |
|---|---|
| "Build backend services and APIs using Python and FastAPI" | Day 7, exercise 6 (routes, Pydantic, 201/404/422) |
| "Design APIs that expose data securely and efficiently" | Day 4 (status handling), Day 7 (validation, SQL injection) |
| "Data processing and integration components" | Days 2-4 (files, regex, JSON, CSV, flatten, group) |
| "Write clean, modular, reusable, well-tested code" | Days 1, 5, 6 and the test-writing exercise on Day 7 |
| "Develop automated unit/API tests" | Day 7: `TestClient`, `Mock`, writing test cases |
| "Diagnose production issues, root causes" | Day 5 exceptions, Day 4 retryable vs non-retryable errors |
| "Large datasets" | Day 6 generators and batching (memory-friendly processing) |
| React, Node.js, SQL platforms, CI/CD | Not covered here (Python only) |

## The last hour: rehearse out loud

Once Day 7 is done, answer these without notes, in under 60 seconds each (every one is a "Say it out loud" question in the notebooks):

1. Compiled or interpreted? · 2. Mutable vs immutable · 3. `is` vs `==` · 4. The mutable default argument bug
5. List vs tuple, and why a list can't be a dict key · 6. Shallow vs deep copy · 7. `with` and context managers
8. Generator vs list · 9. What is a decorator? · 10. `*args` / `**kwargs` · 11. The four pillars of OOP
12. `__str__` vs `__repr__` · 13. Which API errors do you retry? · 14. How do you stop SQL injection?
15. Why mock dependencies in tests? · 16. What does FastAPI give you over plain code?

Then explain your **Task Manager** project (`project/`) in 3 minutes: what it does, how it is structured, and one trade-off you chose.

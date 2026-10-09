# learning-log — Python 🐍

A personal learning log tracking my growth as a fullstack developer — covering AI/LLM concepts, frontend, backend, and everything in between. One branch per skill.

This branch (`python`) is a **42-day, 1-hour-a-day** hands-on Python plan. It skips "what is a variable" because I already know JavaScript, and goes for **confidence writing idiomatic Python**: Python's own data model, the idioms, OOP, generators, decorators, typing, testing, async, and DSA in Python.

---

## How each day works

```
days/
└── day-01-python-through-js-eyes/
    ├── notes.md           # brief notes: key concepts, JS ↔ Python comparison, links
    ├── questions.md       # the day's problems (warm-up → core → challenge)
    ├── practice.ipynb     # MY workspace: one cell per question, solve here
    └── solutions.ipynb    # reference solutions + why they're the "Pythonic" way
```

**The 1-hour routine**

| Time | What |
|------|------|
| 10 min | Read the day's `notes.md` and skim the linked resource |
| 40 min | Solve `questions.md` in `practice.ipynb`, **without** opening solutions |
| 10 min | Compare with `solutions.ipynb`, note what I'd change, tick the day off below |

Rules for myself: try first, peek later. If I'm stuck for more than 10 minutes on one question, read only the hint, not the full solution.

### Setup (once)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install jupyterlab pytest mypy
jupyter lab            # or open the .ipynb files in VS Code with the Jupyter extension
```

Use Python **3.12+** (`python3 --version`).

---

## Roadmap

### Phase 1: Python through JavaScript eyes (Days 1–5)
Get the syntax and the core built-in types right, and unlearn JS habits.

| Day | Topic | Key points |
|-----|-------|------------|
| 1 | Syntax and mental model | REPL, indentation, truthiness, `None` vs `null`/`undefined`, `is` vs `==`, f-strings, everything is an object |
| 2 | Numbers and strings | big ints, `//` `%` `**`, string methods, slicing `s[::-1]`, immutability |
| 3 | Lists and tuples | mutability, slicing, unpacking `a, *rest = ...`, copy vs reference, shallow vs deep copy |
| 4 | Dicts and sets | `get`/`setdefault`, iterating items, set algebra, hashability (why lists can't be keys) |
| 5 | Control flow | `for`/`else`, `range`, `enumerate`, `zip`, `while`, walrus `:=`, `match` (structural pattern matching) |

### Phase 2: Pythonic idioms (Days 6–11)
Write Python that looks like Python, not translated JS.

| Day | Topic | Key points |
|-----|-------|------------|
| 6 | Comprehensions | list/dict/set comprehensions, nested, conditional, when *not* to use them |
| 7 | Functions in depth | defaults (mutable default trap), `*args`/`**kwargs`, keyword-only and positional-only params |
| 8 | Scope and closures | LEGB, `nonlocal`, `global`, late-binding closures in loops |
| 9 | Functional tools | `lambda`, `sorted(key=...)`, `min`/`max` with key, `map`/`filter` vs comprehensions, `functools.partial`/`reduce` |
| 10 | `collections` module | `Counter`, `defaultdict`, `deque`, `namedtuple`, `ChainMap` |
| 11 | **Kata day** | mixed problems from Days 1–10, timed |

### Phase 3: Errors, files and modules (Days 12–16)

| Day | Topic | Key points |
|-----|-------|------------|
| 12 | Exceptions | `try`/`except`/`else`/`finally`, raising, custom exception classes, chaining, EAFP vs LBYL |
| 13 | Files and paths | `pathlib`, `with open(...)`, text vs bytes, `json`, `csv` |
| 14 | Modules and packages | imports, `__init__.py`, `if __name__ == "__main__"`, venv and pip, `pyproject.toml` basics |
| 15 | Standard library tour | `datetime`, `itertools` preview, `re` basics, `os`/`sys`, `argparse` |
| 16 | **Mini project** | CLI log analyzer: parse a log file, aggregate with `Counter`, output a report |

### Phase 4: Object-oriented Python (Days 17–23)

| Day | Topic | Key points |
|-----|-------|------------|
| 17 | Classes | `__init__`, `self`, instance vs class attributes, how this differs from JS classes and prototypes |
| 18 | Dunder methods (data model) | `__repr__`, `__str__`, `__eq__`, `__hash__`, `__len__`, `__getitem__`, `__lt__`, operator overloading |
| 19 | Inheritance | `super()`, MRO, multiple inheritance and mixins, composition over inheritance |
| 20 | Attributes and methods | `@property`, `@classmethod`, `@staticmethod`, "private" by convention `_x`/`__x`, `__slots__` |
| 21 | `dataclasses` and `enum` | `@dataclass` (frozen, ordering, defaults), `Enum`, `StrEnum` |
| 22 | Duck typing and interfaces | `abc.ABC`, `typing.Protocol`, when to use which |
| 23 | **Mini project** | library or bank system with classes, dataclasses and custom exceptions |

### Phase 5: Iteration, generators and decorators (Days 24–29)
The part that makes Python feel powerful.

| Day | Topic | Key points |
|-----|-------|------------|
| 24 | Iterator protocol | `__iter__`/`__next__`, `iter()`/`next()`, `StopIteration`, iterables vs iterators |
| 25 | Generators | `yield`, generator expressions, lazy pipelines, `yield from` (compare with JS `function*`) |
| 26 | `itertools` deep dive | `chain`, `groupby`, `islice`, `product`, `permutations`, `accumulate`, `pairwise`, `batched` |
| 27 | Decorators I | functions as objects, wrapping, `functools.wraps`, timing/logging decorators |
| 28 | Decorators II | decorators with arguments, class decorators, `functools.cache`/`lru_cache`, retry decorator |
| 29 | Context managers | `__enter__`/`__exit__`, `contextlib.contextmanager`, `suppress`, `ExitStack` |

### Phase 6: Modern, production-style Python (Days 30–35)

| Day | Topic | Key points |
|-----|-------|------------|
| 30 | Type hints | `list[int]`, `X \| None`, `TypedDict`, generics, `Callable`, running `mypy` (compare with TypeScript) |
| 31 | Testing with pytest | asserts, fixtures, `parametrize`, testing exceptions, `monkeypatch` |
| 32 | Concurrency I | threads vs processes, the GIL (and free-threaded builds), `concurrent.futures` |
| 33 | Concurrency II: `asyncio` | event loop, `async`/`await`, `gather`, `TaskGroup`, compare with JS Promises |
| 34 | HTTP and JSON | `httpx`/`requests`, calling a real API, handling errors and timeouts |
| 35 | Debugging and performance | `logging`, `breakpoint()`/pdb, `timeit`, `cProfile`, big-O of built-ins |

### Phase 7: DSA in Python and capstone (Days 36–42)

| Day | Topic | Key points |
|-----|-------|------------|
| 36 | Python for DSA | `heapq`, `bisect`, `deque`, sorting stability, built-in complexity cheat sheet |
| 37 | Arrays, strings and hashing | two pointers, sliding window, frequency maps (LeetCode-style) |
| 38 | Recursion and memoization | recursion limit, `@cache`, turning recursion into iteration |
| 39 | Graphs | adjacency lists with `defaultdict`, BFS with `deque`, DFS, topological sort |
| 40 | Capstone I | FastAPI basics: routes, Pydantic models, typed request/response |
| 41 | Capstone II | build a small REST service (e.g. a task tracker) with tests and type hints |
| 42 | Review and retrospective | re-solve the 5 hardest questions from earlier days, write what I learned |

---

## Progress tracker

| Phase | Days | Status |
|-------|------|--------|
| 1. Python through JS eyes | 1–5 | ⬜ |
| 2. Pythonic idioms | 6–11 | ⬜ |
| 3. Errors, files, modules | 12–16 | ⬜ |
| 4. OOP | 17–23 | ⬜ |
| 5. Iteration, generators, decorators | 24–29 | ⬜ |
| 6. Modern Python | 30–35 | ⬜ |
| 7. DSA and capstone | 36–42 | ⬜ |

---

## Resources

**Core reading**
- [The official Python Tutorial](https://docs.python.org/3/tutorial/): the canonical reference for syntax; skim the sections that match each day
- [Learn Python for JavaScript Developers (freeCodeCamp handbook)](https://www.freecodecamp.org/news/learn-python-for-javascript-developers-handbook/): side-by-side JS ↔ Python, good for Phase 1
- *Fluent Python* (2nd ed.), Luciano Ramalho: the best book for Phases 4–5 (data model, iterators, decorators)
- *Effective Python* (3rd ed.), Brett Slatkin: short, item-by-item best practices
- [Real Python](https://realpython.com/): in-depth tutorials for nearly every topic above

**Practice platforms (for extra reps)**
- [Exercism Python track](https://exercism.org/tracks/python): free, with volunteer mentoring
- [Python Morsels](https://www.pythonmorsels.com/exercises/): short idiomatic exercises with topic paths (decorators, iterators, classes)
- [Pybites](https://pybit.es/): bite-sized exercises from beginner to advanced
- [awesome-python-practice](https://github.com/reuven/awesome-python-practice): curated list of practice resources
- [LeetCode](https://leetcode.com/) / [NeetCode](https://neetcode.io/): for Phase 7

**Roadmaps and video**
- [roadmap.sh/python](https://roadmap.sh/python): community roadmap, used to check coverage of this plan
- Corey Schafer (YouTube): clear explanations of the standard library, OOP and decorators
- mCoding and ArjanCodes (YouTube): idiomatic and "clean code" Python

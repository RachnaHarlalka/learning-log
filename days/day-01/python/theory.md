# Day 1 · Python: Setup & Basics

## 1. Why this matters in interviews
Almost every Python screening starts with "mutable vs immutable", "`is` vs `==`" and "is Python compiled or interpreted?". They are cheap questions that quickly show whether you understand the language or only copy syntax. Get these precise and the rest of the interview starts well.

## 2. Core concepts

### Running Python, venv
```bash
python3 --version               # 3.12+
python3 -m venv .venv           # an isolated folder of packages for this project
source .venv/bin/activate       # Windows: .venv\Scripts\activate
pip install pytest
python3 script.py               # run a file
python3                         # REPL, for quick experiments
```
A **venv** keeps each project's dependencies separate, so two projects can use different versions of the same library.

### Variables are names, not boxes
```python
x = 10          # the name x points to an int object
y = x           # y points to the SAME object
x = 20          # x now points to a different object; y is still 10
```
There are no declarations. A variable is a label attached to an object, and the type belongs to the **object**, not the name.

### Built-in types
```python
age = 30            # int (arbitrary size: 2**200 works)
price = 9.99        # float (binary floating point: 0.1 + 0.2 != 0.3)
name = "Asha"       # str  (single or double quotes)
active = True       # bool (a subclass of int: True == 1)
nothing = None      # NoneType, the "no value" singleton
```

### Dynamic vs strong typing
```python
x = 5
x = "five"          # allowed: dynamic typing (the name can point to any type)
5 + "5"             # TypeError: strong typing (no silent conversion, unlike JS)
```
**Dynamic** = types are checked at run time and names can be rebound. **Strong** = Python will not silently coerce `int` + `str`.

### `type()`, `id()`, `is` vs `==`
```python
a = [1, 2]
b = [1, 2]
a == b      # True  : same VALUE
a is b      # False : different OBJECTS (compare `id(a) == id(b)`)
c = a
c is a      # True  : two names, one object
```
- `==` compares values (calls `__eq__`).
- `is` compares identity (same object in memory).
- Use `is` only for singletons: `if x is None:`.

### Mutable vs immutable
| Immutable (cannot change in place) | Mutable (can change in place) |
|---|---|
| `int`, `float`, `bool`, `str`, `tuple`, `frozenset`, `None` | `list`, `dict`, `set`, most custom objects |

```python
s = "hi"
s.upper()           # returns a NEW string; s is still "hi"

nums = [1, 2]
alias = nums
alias.append(3)     # changes the one shared list
print(nums)         # [1, 2, 3]
```
"Immutable" means the **object** cannot change. A name can still be re-pointed to another object.

### Input / output and f-strings
```python
name = input("Name: ")                  # always returns a str
age = int(input("Age: "))               # convert yourself
print(f"{name} is {age} years old")     # f-string
print(f"{3.14159:.2f}")                 # 3.14
print(f"{1234567:,}")                   # 1,234,567
print(f"{'left':<10}|{'right':>10}|")   # alignment
print(f"{age=}")                        # age=30  (handy for debugging)
```

### Compiled or interpreted?
CPython (the standard implementation) **compiles** your source to **bytecode** (`.pyc`), then its virtual machine **interprets** that bytecode. So the honest answer is "both": it is called interpreted because there is no separate compile step for the programmer and the VM runs the bytecode at run time.

## 3. Common pitfalls
- **Aliasing:** `b = a` for a list does not copy it. Use `a.copy()` or `a[:]`.
- **`[[0]*3]*3`:** creates 3 references to one row. Change one row and all change.
- **`is` with numbers or strings:** `a is b` can be True for small ints or interned strings by accident. Never rely on it. Use `==`.
- **Float equality:** `0.1 + 0.2 == 0.3` is False. Use `math.isclose` or `decimal.Decimal` for money.
- **`input()` returns text:** `"5" + "5"` is `"55"`. Convert first.
- **Truthiness:** `0`, `""`, `[]`, `{}`, `None` are falsy. `if not items:` is the idiomatic empty check.
- **Mutating a list while looping over it** skips elements (more on this on Day 2).

## 4. Top interview questions

1. **Is Python compiled or interpreted?**
   Both. CPython compiles source to bytecode, then the Python virtual machine interprets the bytecode. Other implementations (PyPy) add a JIT compiler.

2. **What is the difference between mutable and immutable types? Give examples.**
   A mutable object can be changed in place; an immutable one cannot, so any "change" creates a new object. Mutable: list, dict, set. Immutable: int, float, str, tuple, bool, `None`, frozenset.

3. **What is the difference between `is` and `==`?**
   `==` asks whether two objects have equal values. `is` asks whether they are the very same object (same `id`). Use `is` for `None`, `==` for everything else.

4. **Is Python statically or dynamically typed? Strongly or weakly?**
   Dynamically typed (types are checked at run time and a name can be rebound to any type) and strongly typed (`1 + "1"` raises `TypeError`). Type hints add optional static checking.

5. **What does "everything is an object" mean?**
   Even ints, functions and classes are objects with a type and an identity. A variable is only a name bound to an object.

6. **What happens when you do `b = a` where `a` is a list?**
   Nothing is copied. Both names point to the same list, so a change through one is visible through the other. Use `a.copy()` for a shallow copy.

7. **Why is a tuple faster and safer than a list in some cases?**
   It is immutable, so it can be a dict key, is safe to share, and uses a bit less memory. Use it for fixed records like `(lat, lng)`.

8. **How do you check the type of a value?**
   `type(x)` gives the exact type; `isinstance(x, int)` also accepts subclasses and is preferred in code. Example: `isinstance(True, int)` is True.

9. **Why does `0.1 + 0.2 != 0.3`, and how do you handle money?**
   Floats are binary and cannot represent 0.1 exactly. For money use `decimal.Decimal` or integers of the smallest unit (paise or cents).

10. **What is a virtual environment and why use one?**
    An isolated Python environment with its own packages. It prevents version clashes between projects and makes `requirements.txt` reproducible.

## 5. One-line cheat sheet
Variables are **names pointing to objects**; **mutable** = list/dict/set (changes in place, aliases see it), **immutable** = int/float/str/tuple/None; `==` is **value**, `is` is **identity** (use for `None`); Python is **dynamic + strong**, compiled to **bytecode** then interpreted; f-strings: `f"{x:.2f}"`; use a **venv** per project.

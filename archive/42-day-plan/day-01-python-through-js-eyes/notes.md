# Day 1 notes: Python through JavaScript eyes

**Goal:** get comfortable with Python's syntax and mental model, and spot where JS habits will trip me up.

## Today's plan (1 hour)

1. **10 min:** read this page, then skim [Python Tutorial §3 "An Informal Introduction"](https://docs.python.org/3/tutorial/introduction.html) and [§4.1–4.2 (`if`, `for`)](https://docs.python.org/3/tutorial/controlflow.html)
2. **40 min:** solve [questions.md](questions.md) in [practice.ipynb](practice.ipynb); every question has a test cell
3. **10 min:** compare with [solutions.ipynb](solutions.ipynb), fill in the reflection at the bottom of the practice notebook

## Key concepts

### Blocks are indentation, not braces
```python
if score > 90:
    print("great")      # 4 spaces = inside the block
elif score > 50:        # not "else if"
    print("ok")
else:
    pass                # an empty block needs `pass`
```

### Truthiness: empty things are falsy
Falsy: `False`, `None`, `0`, `0.0`, `""`, `[]`, `{}`, `set()`, `()`.
Everything else is truthy. **Unlike JS, `[]` and `{}` are falsy.**

### `None` is the only "nothing"
No `null` vs `undefined`. Missing dict keys raise `KeyError` instead of giving `undefined`; use `d.get("key")` to get `None` instead.

### `is` vs `==`
- `==` compares **values** (`[1, 2] == [1, 2]` → `True`). No `===` needed: Python doesn't coerce types (`1 == "1"` → `False`).
- `is` compares **identity** (same object in memory). Use it for `None`: `if x is None:`.

### `and` / `or` return one of the operands
Like JS `&&` / `||`: `name or "stranger"`. There's no `??`, so `0 or 5` gives `5`. When `0`/`""` are valid values, check `is None` explicitly.

### f-strings (template literals)
```python
name, price = "Coffee", 3.5
f"{name} costs ${price:.2f}"     # 'Coffee costs $3.50'
f"{1234567:,}"                   # '1,234,567'
f"{name:<10}|"                   # 'Coffee    |'   left-align in 10 chars
f"{0.256:.1%}"                   # '25.6%'
f"{price=}"                      # 'price=3.5'     handy for debugging
```

### Numbers
- `/` always gives a float (`7 / 2` → `3.5`); `//` is floor division (`7 // 2` → `3`, `-7 // 2` → `-4`).
- `%` takes the sign of the divisor (`-7 % 3` → `2`; JS gives `-1`).
- `int` has no size limit: `2 ** 100` just works, no `BigInt`.
- `divmod(17, 5)` → `(3, 2)`.

### Everything is an object
Functions, classes, modules and `None` are all objects. `type(x)` tells you what something is, and you can pass functions around like in JS.

## JS ↔ Python cheat sheet

| JavaScript | Python |
|------------|--------|
| `let x = 1` / `const x = 1` | `x = 1` (no keyword; constants are `UPPER_CASE` by convention) |
| `null`, `undefined` | `None` |
| `true`, `false` | `True`, `False` |
| `&&`, `\|\|`, `!` | `and`, `or`, `not` |
| `===` | `==` |
| `a ?? b` | `b if a is None else a` |
| `cond ? a : b` | `a if cond else b` |
| `` `Hi ${name}` `` | `f"Hi {name}"` |
| `arr.length` | `len(arr)` |
| `console.log(x)` | `print(x)` |
| `typeof x` | `type(x)` |
| `x > 0 && x < 10` | `0 < x < 10` (chained comparison) |
| `[a, b] = [b, a]` | `a, b = b, a` |
| `// comment` | `# comment` |
| `throw new Error("…")` | `raise ValueError("…")` |

## Gotchas for JS developers
- `"3" + 4` is a `TypeError`, not `"34"`. Convert explicitly: `"3" + str(4)` or `int("3") + 4`.
- No block scope: a variable created inside `if` or `for` is still visible after it.
- Assigning to a name anywhere inside a function makes it local to the **whole** function (`UnboundLocalError`).
- Indentation errors are syntax errors. Use 4 spaces and never mix tabs.

## Files
| File | What |
|------|------|
| [questions.md](questions.md) | 10 questions: warm-up (Q1–3), core (Q4–8), challenge (Q9–10) |
| [practice.ipynb](practice.ipynb) | my workspace, with a test cell after each question |
| [solutions.ipynb](solutions.ipynb) | reference solutions and why they're the Pythonic way |

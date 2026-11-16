# Day 1: Questions

Solve these in [practice.ipynb](practice.ipynb). Each one has a test cell there. Only open [solutions.ipynb](solutions.ipynb) after you've tried.

| # | Level | Topic |
|---|-------|-------|
| Q1 | Warm-up | Truthiness check |
| Q2 | Warm-up | `is` vs `==` |
| Q3 | Warm-up | Translate JS to Python |
| Q4 | Core | Receipt with f-string formatting |
| Q5 | Core | Numbers: division and splitting a bill |
| Q6 | Core | Everything is an object |
| Q7 | Core | Chained comparisons and `and`/`or` |
| Q8 | Core | Tuple assignment: Fibonacci |
| Q9 | Challenge | Scope gotchas |
| Q10 | Challenge | `safe_get`: optional chaining in Python |

---

## Q1. Truthiness check  ·  _Warm-up_

In JS, `[]` and `{}` are truthy. In Python they're not.

**Predict first:** which of these are truthy? Write your guesses in the markdown cell, then run the cell to check.

**Then write** `count_truthy(values)`, which returns how many items in `values` are truthy.

```python
values = [0, "", [], {}, None, "0", " ", [0], 0.0, -1, "False", set()]
for v in values:
    print(repr(v), "->", bool(v))
```

<details><summary>Expected behaviour (the test cell)</summary>

```python
assert count_truthy([0, "", [], {}, None, "0", " ", [0], 0.0, -1, "False", set()]) == 5
assert count_truthy([]) == 0
assert count_truthy([[], [[]]]) == 1
print("✅ Q1 passed")
```

</details>

---

## Q2. `is` vs `==`  ·  _Warm-up_

**Predict first:** what does each line print?

**Then write** `describe(x)`, which returns:
- `"missing"` if `x` is `None`
- `"empty"` if `x` is falsy but not `None` (`0`, `""`, `[]`, `False`, ...)
- `"value"` otherwise

```python
a = [1, 2]
b = [1, 2]
c = a
print(a == b)
print(a is b)
print(c is a)
c.append(3)
print(a)
print(1 == "1")
print(1 == 1.0)
```

<details><summary>Expected behaviour (the test cell)</summary>

```python
assert describe(None) == "missing"
assert describe(0) == "empty"
assert describe("") == "empty"
assert describe([]) == "empty"
assert describe(False) == "empty"
assert describe("hi") == "value"
assert describe([0]) == "value"
print("✅ Q2 passed")
```

</details>

---

## Q3. Translate JS to Python  ·  _Warm-up_

Translate this JS into Python. `user` is a dict like `{"name": "Asha", "is_admin": True, "messages": ["hi"]}`; `name` and `is_admin` may be missing.

```js
function greet(user) {
  const name = user.name || "stranger";
  const title = user.isAdmin ? "Admin" : "User";
  const count = user.messages.length;
  return `Hello ${name} (${title}), you have ${count} new message${count === 1 ? "" : "s"}`;
}
```

<details><summary>Expected behaviour (the test cell)</summary>

```python
assert greet({"name": "Asha", "is_admin": True, "messages": ["hi"]}) == "Hello Asha (Admin), you have 1 new message"
assert greet({"name": "", "messages": []}) == "Hello stranger (User), you have 0 new messages"
assert greet({"messages": ["a", "b"]}) == "Hello stranger (User), you have 2 new messages"
print("✅ Q3 passed")
```

</details>

---

## Q4. Receipt with f-string formatting  ·  _Core_

Write `format_receipt(items)` where `items` is a list of `(name, unit_price, qty)` tuples. Return one string (lines joined with `"\n"`) laid out like this:

```
Item          Qty      Amount
Coffee          2        7.00
Laptop          1    1,299.99
TOTAL                1,306.99
```

Column rules:
- name: left-aligned, 12 characters wide
- qty: right-aligned, 5 characters wide (blank on the TOTAL row)
- amount (`unit_price * qty`): right-aligned, 12 characters wide, comma thousands separator, 2 decimals

Tip: you can loop over tuples with unpacking: `for name, price, qty in items:`.

<details><summary>Expected behaviour (the test cell)</summary>

```python
receipt = format_receipt([("Coffee", 3.5, 2), ("Laptop", 1299.99, 1)])
lines = receipt.split("\n")
assert lines[0] == "Item          Qty      Amount", repr(lines[0])
assert lines[1] == "Coffee          2        7.00", repr(lines[1])
assert lines[2] == "Laptop          1    1,299.99", repr(lines[2])
assert lines[3] == "TOTAL                1,306.99", repr(lines[3])
assert format_receipt([]).split("\n")[-1] == "TOTAL                    0.00"
print(receipt)
print("✅ Q4 passed")
```

</details>

---

## Q5. Numbers: division and splitting a bill  ·  _Core_

**Predict first:** what does each line print? (One of them raises an error.)

**Then write** `split_bill(total_cents, people)`. It returns a list of `people` integer shares that **add up exactly** to `total_cents`. When it doesn't divide evenly, the first people each pay 1 extra cent. Raise `ValueError` if `people` is less than 1.

Example: `split_bill(1000, 3)` → `[334, 333, 333]`

```python
print(7 / 2)
print(7 // 2)
print(-7 // 2)
print(-7 % 3)
print(2 ** 100)
print(0.1 + 0.2 == 0.3)
print(int("42") + 1)
print(divmod(17, 5))
try:
    print("3" + 4)
except TypeError as e:
    print("TypeError:", e)
```

<details><summary>Expected behaviour (the test cell)</summary>

```python
assert split_bill(1000, 3) == [334, 333, 333]
assert split_bill(900, 3) == [300, 300, 300]
assert split_bill(2, 5) == [1, 1, 0, 0, 0]
assert sum(split_bill(12345, 7)) == 12345
try:
    split_bill(100, 0)
    assert False, "should have raised ValueError"
except ValueError:
    pass
print("✅ Q5 passed")
```

</details>

---

## Q6. Everything is an object  ·  _Core_

**Predict first:** what does each line print?

**Then write** `apply_all(funcs, value)`, which calls every function in `funcs` with `value` and returns a dict mapping each function's name to its result.

Hint: every function has a `__name__` attribute.

Example: `apply_all([len, str.upper], "hi")` → `{"len": 2, "upper": "HI"}`

```python
def shout(s):
    return s.upper() + "!"

print(type(42), type("hi"), type(None), type([]))
print(type(shout))
print(type(len))
print(shout.__name__)
yell = shout          # no call: just another name for the same function
print(yell("hey"))
print(yell is shout)
print(type(type))
```

<details><summary>Expected behaviour (the test cell)</summary>

```python
assert apply_all([len, str.upper, str.title], "hello world") == {
    "len": 11, "upper": "HELLO WORLD", "title": "Hello World"
}
assert apply_all([abs, str], -5) == {"abs": 5, "str": "-5"}
assert apply_all([], 1) == {}
print("✅ Q6 passed")
```

</details>

---

## Q7. Chained comparisons and `and`/`or`  ·  _Core_

**Predict first:** `and`/`or` return one of their operands, not necessarily `True`/`False`. What does each line print?

**Then write** `grade(score)`:
- raise `ValueError` if `score` is not between 0 and 100 inclusive
- `"A"` for 90+, `"B"` for 75–89, `"C"` for 50–74, `"F"` below 50

Use a chained comparison (`a <= x <= b`) for the range check.

```python
print(0 or "default")
print("a" and "b")
print("" and "b")
print(None or 0 or "")
print([] and 1 / 0)     # does this crash?
print(not [])
print(1 < 2 < 3, 3 > 2 > 1, 1 < 3 < 2)
```

<details><summary>Expected behaviour (the test cell)</summary>

```python
assert grade(100) == "A" and grade(90) == "A"
assert grade(89) == "B" and grade(75) == "B"
assert grade(74) == "C" and grade(50) == "C"
assert grade(49) == "F" and grade(0) == "F"
for bad in (-1, 101):
    try:
        grade(bad)
        assert False, f"grade({bad}) should raise"
    except ValueError:
        pass
print("✅ Q7 passed")
```

</details>

---

## Q8. Tuple assignment: Fibonacci  ·  _Core_

Python can assign several names at once: `a, b = b, a` swaps two values without a temp variable.

Write `fib(n)` returning the n-th Fibonacci number (`fib(0) = 0`, `fib(1) = 1`) **iteratively**, using tuple assignment. Aim for 4 lines in the body.

Then look at `fib(100)`. In JS you'd need `BigInt` for it.

<details><summary>Expected behaviour (the test cell)</summary>

```python
assert [fib(i) for i in range(10)] == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
assert fib(100) == 354224848179261915075
print(fib(100))
print("✅ Q8 passed")
```

</details>

---

## Q9. Scope gotchas  ·  _Challenge_

No code to write: **predict the output** of each snippet, then run it. In the markdown cell below, write one sentence per snippet explaining *why*. Then fix snippet C so it prints `10` and then `20`.

```python
# Snippet A
for i in range(3):
    pass
print("A:", i)

# Snippet B
if True:
    secret = "visible"
print("B:", secret)

# Snippet C
x = 10
def show():
    try:
        print("C:", x)
    except UnboundLocalError as e:
        print("C: UnboundLocalError ->", e)
    x = 20
show()
```

---

## Q10. `safe_get`: optional chaining in Python  ·  _Challenge_

Python has no `?.` or `??`. Write `safe_get(data, path, default=None)` that does what this JS does:

```js
data?.user?.tags?.[1] ?? defaultValue
```

- `path` is a dot-separated string, e.g. `"user.tags.1"`
- dict segments are keys; for lists, a segment of digits is an index
- if any step is missing, out of range, or not traversable (e.g. indexing into a string or `None`), return `default`
- like `??`, **only `None`** falls back to `default`. Falsy values like `0`, `False` and `""` are returned as they are

Hints: `isinstance(x, dict)`, `isinstance(x, list)`, `"12".isdigit()`, `key in some_dict`.

<details><summary>Expected behaviour (the test cell)</summary>

```python
data = {"user": {"name": "Asha", "age": 0, "active": False, "tags": ["admin", "beta"], "address": None}}
assert safe_get(data, "user.name") == "Asha"
assert safe_get(data, "user.age", 99) == 0              # falsy, but not None
assert safe_get(data, "user.active", True) is False
assert safe_get(data, "user.tags.1") == "beta"
assert safe_get(data, "user.tags.5", "none") == "none"   # out of range
assert safe_get(data, "user.tags.x", "none") == "none"   # not an index
assert safe_get(data, "user.address", "n/a") == "n/a"    # None -> default
assert safe_get(data, "user.address.city", "?") == "?"   # can't go into None
assert safe_get(data, "user.name.first", "?") == "?"     # can't go into a str
assert safe_get(data, "nope") is None
print("✅ Q10 passed")
```

</details>

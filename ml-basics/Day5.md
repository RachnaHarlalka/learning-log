# Day 5 — Python Crash Course for JavaScript Developers

> **Series:** ML Prerequisites for "Hands-On Large Language Models" + "Build a Large Language Model From Scratch"
> **Audience:** Fullstack JS/TS developer — you already know how to code
> **Goal:** Read ML Python code fluently without tripping on syntax. Not "learn Python deeply" — learn enough to not be lost in the books.

---

## The Right Mindset

You are **not learning Python from scratch**. You are learning:

1. What Python syntax _looks like_ so you can read it
2. Where it differs from JS so you don't misread it
3. The specific patterns both books use constantly

You will not be writing Python from scratch this week. You will be _reading_ it.
That's a much lower bar — and you can clear it today.

---

## Part 1 — The Most Important Difference: Indentation

Python uses **indentation** (whitespace) to define blocks — not `{}` curly braces.
This is the single biggest visual shock for JS developers.

```python
# Python
def greet(name):
    if name == "Alice":
        print("Hello, Alice!")
    else:
        print("Hello, stranger.")
```

```javascript
// JavaScript equivalent
function greet(name) {
  if (name === "Alice") {
    console.log("Hello, Alice!");
  } else {
    console.log("Hello, stranger.");
  }
}
```

**Rules:**

- Standard is 4 spaces per level (both books use this consistently)
- Mixing tabs and spaces will crash your code
- The `:` at the end of `def`, `if`, `for`, `class`, `with` lines is mandatory — it signals "block starts here"

---

## Part 2 — Variables and Types

No `let`, `const`, or `var`. Just assign.

```python
# Python
x = 42              # int
y = 3.14            # float
name = "Alice"      # str
flag = True         # bool  (capital T — not 'true')
nothing = None      # None  (not 'null' or 'undefined')
```

```javascript
// JavaScript equivalents
let x = 42;
let y = 3.14;
let name = "Alice";
let flag = true;
let nothing = null;
```

**Type checking:** Python is dynamically typed like JS, but stricter at runtime.

```python
type(x)       # <class 'int'>
type(name)    # <class 'str'>
isinstance(x, int)  # True
```

---

## Part 3 — Strings and f-strings

Python has **f-strings** — the equivalent of JS template literals.

```python
# Python f-string
epoch = 3
loss = 0.423
print(f"Epoch {epoch}: loss = {loss:.3f}")
# Output: Epoch 3: loss = 0.423
```

```javascript
// JavaScript template literal equivalent
console.log(`Epoch ${epoch}: loss = ${loss.toFixed(3)}`);
```

**The `:.3f` format spec** means "3 decimal places, float format." You'll see this constantly in training loops:

```python
# From "Build an LLM" — actual book code pattern:
print(f"Ep {epoch+1} (Step {global_step:06d}): "
      f"Train loss {train_loss:.3f}, "
      f"Val loss {val_loss:.3f}")
# Output: Ep 1 (Step 000000): Train loss 3.421, Val loss 3.589
```

`{global_step:06d}` = integer, padded with zeros to 6 digits.

---

## Part 4 — Lists

Lists in Python work like arrays in JS.

```python
tokens = ["Hello", ",", "world", "!"]
tokens[0]      # "Hello"
tokens[-1]     # "!"  ← negative index = from the end (no JS equivalent natively)
tokens[1:3]    # [",", "world"]  ← slicing: index 1 up to (not including) 3
tokens[:2]     # ["Hello", ","]  ← from start up to index 2
tokens[2:]     # ["world", "!"] ← from index 2 to end

len(tokens)    # 4

tokens.append("?")   # like .push()
tokens.pop()         # removes last item, like .pop()
```

```javascript
// JS equivalents
tokens[tokens.length - 1]; // last element
tokens.slice(1, 3); // slicing
tokens.push("?");
tokens.pop();
```

---

## Part 5 — Dictionaries

Python dicts are like JS objects / Maps.

```python
# Python
config = {
    "vocab_size": 50257,
    "emb_dim": 768,
    "n_heads": 12,
    "context_length": 1024,
}

config["vocab_size"]        # 50257   (bracket access)
config.get("n_layers", 12)  # 12      (with default, like JS obj?.prop ?? default)

# Iterate
for key, value in config.items():
    print(f"{key}: {value}")
```

```javascript
// JavaScript equivalents
const config = { vocab_size: 50257, emb_dim: 768 };
config.vocab_size;
config["vocab_size"];
Object.entries(config).forEach(([key, value]) =>
  console.log(`${key}: ${value}`),
);
```

> **Book pattern:** Both books pass `config` dictionaries into model classes constantly —
> you'll see `cfg["emb_dim"]` and `cfg["n_heads"]` everywhere.

---

## Part 6 — Tuples

Tuples are like read-only arrays. Used heavily for shapes.

```python
shape = (8, 4, 256)    # tuple: immutable, ordered
shape[0]               # 8
a, b, c = shape        # destructuring — exactly like JS: const [a, b, c] = shape

# You'll see this often with tensor shapes:
batch_size, seq_len, embed_dim = tensor.shape
```

---

## Part 7 — For Loops

```python
# Basic loop
for i in range(5):      # range(5) = 0, 1, 2, 3, 4
    print(i)

# Loop over list
tokens = ["Hello", "world"]
for token in tokens:
    print(token)

# With index — use enumerate() (not .forEach with index)
for i, token in enumerate(tokens):
    print(f"{i}: {token}")

# Loop over two lists together — zip()
keys = ["a", "b", "c"]
values = [1, 2, 3]
for k, v in zip(keys, values):
    print(f"{k} = {v}")
```

```javascript
// JS equivalents
for (let i = 0; i < 5; i++) { ... }
tokens.forEach(token => ...)
tokens.forEach((token, i) => ...)
keys.forEach((k, i) => console.log(`${k} = ${values[i]}`))
```

---

## Part 8 — List Comprehensions

This is Python's most powerful one-liner. JS developers often get tripped by it.

```python
# Pattern: [expression for item in iterable if condition]

# Basic: square each number
squares = [x**2 for x in range(5)]
# → [0, 1, 4, 9, 16]

# With filter: only even numbers
evens = [x for x in range(10) if x % 2 == 0]
# → [0, 2, 4, 6, 8]

# Real book example — from "Build an LLM":
# Collect token IDs from a vocabulary
token_ids = [vocab[token] for token in tokenized_text if token in vocab]
```

```javascript
// JS equivalents (map + filter)
const squares = Array.from({ length: 5 }, (_, x) => x ** 2);
const evens = Array.from({ length: 10 }, (_, x) => x).filter(
  (x) => x % 2 === 0,
);
// or:
const squares = [0, 1, 2, 3, 4].map((x) => x ** 2);
```

---

## Part 9 — Functions

```python
# Basic function
def add(a, b):
    return a + b

# Default arguments
def train(model, lr=0.001, epochs=3):
    # ...
    pass   # ← 'pass' = empty body placeholder (like {})

# Multiple return values (returns a tuple)
def get_stats():
    return 0.423, 0.891    # train_loss, val_loss

train_loss, val_loss = get_stats()   # destructure on the left
```

```javascript
// JS equivalents
function add(a, b) {
  return a + b;
}
function train(model, lr = 0.001, epochs = 3) {}
function getStats() {
  return [0.423, 0.891];
}
const [trainLoss, valLoss] = getStats();
```

> **Book pattern:** Functions in both books frequently return multiple values.
> You'll see: `return train_losses, val_losses, train_accs, val_accs`

---

## Part 10 — Classes

This is critical — both books implement everything as PyTorch classes.

```python
class Dog:
    def __init__(self, name, breed):   # constructor (like JS constructor())
        self.name = name               # instance variable (like this.name)
        self.breed = breed

    def speak(self):                   # method — note: 'self' is explicit everywhere
        return f"{self.name} says woof!"

# Usage
dog = Dog("Rex", "Labrador")          # no 'new' keyword in Python
print(dog.speak())                     # "Rex says woof!"
```

```javascript
// JS equivalent
class Dog {
  constructor(name, breed) {
    this.name = name;
    this.breed = breed;
  }
  speak() {
    return `${this.name} says woof!`;
  }
}
const dog = new Dog("Rex", "Labrador"); // JS needs 'new'
```

**Key differences:**

- Python uses `self` where JS uses `this`
- `self` must be the first parameter of every method — always explicitly written
- No `new` keyword when creating instances in Python

---

## Part 11 — The PyTorch Class Pattern (Most Important Pattern in Both Books)

Everything in PyTorch is a subclass of `nn.Module`. You will see this hundreds of times.

```python
import torch
import torch.nn as nn

class SelfAttention(nn.Module):           # inherits from nn.Module
    def __init__(self, d_in, d_out):
        super().__init__()                # always call parent constructor first
        self.W_query = nn.Linear(d_in, d_out, bias=False)
        self.W_key   = nn.Linear(d_in, d_out, bias=False)
        self.W_value = nn.Linear(d_in, d_out, bias=False)

    def forward(self, x):                 # forward() = how data flows through
        queries = self.W_query(x)
        keys    = self.W_key(x)
        values  = self.W_value(x)

        attn_scores = queries @ keys.T    # @ = matrix multiplication
        attn_weights = torch.softmax(attn_scores, dim=-1)
        return attn_weights @ values

# Usage:
model = SelfAttention(d_in=3, d_out=2)
output = model(inputs)   # calls forward() automatically
```

**What to notice:**

- `super().__init__()` — always the first line of `__init__`; like calling `super()` in JS
- `self.W_query = nn.Linear(...)` — define layers in `__init__`
- `def forward(self, x)` — define data flow in `forward()`
- `model(inputs)` — calling the model as a function triggers `forward()` automatically
- `@` operator — matrix multiplication (you learned this in Day 4)

---

## Part 12 — Imports

```python
# Import a module
import torch

# Import specific things from a module
import torch.nn as nn                    # alias: nn.Module, nn.Linear, etc.
import torch.nn.functional as F         # alias: F.softmax, F.cross_entropy, etc.
from torch import tensor                 # import just 'tensor' directly
from sentence_transformers import SentenceTransformer

# Standard library
import os
import json
import re
```

```javascript
// JS equivalents
import torch from "torch"; // (no direct JS equiv for most)
import { SentenceTransformer } from "sentence-transformers";
import * as nn from "torch/nn";
```

> **Pattern you'll see constantly:**
>
> ```python
> import torch
> import torch.nn as nn
> from chapter03 import MultiHeadAttention   # importing from another file in the project
> ```

---

## Part 13 — The `with` Statement

Python's `with` is a resource manager — like `using` in some languages or try/finally.
You'll see it for files and gradient contexts:

```python
# File reading (very common in the books)
with open("the-verdict.txt", "r", encoding="utf-8") as f:
    raw_text = f.read()
# File is automatically closed when the block ends

# Torch no_grad context (disables gradient tracking during inference)
with torch.no_grad():
    outputs = model(X_train)
# Gradient tracking resumes after this block
```

```javascript
// JS rough equivalent for file reading
const fs = require("fs");
const text = fs.readFileSync("file.txt", "utf-8");
// (no direct equivalent for torch.no_grad)
```

---

## Part 14 — Common Operators & Built-ins

```python
# Operators
x ** 2          # x squared (not x^2 — that's XOR in Python)
x // 2          # integer division (floor): 7 // 2 = 3
x % 2           # modulo: same as JS
a and b         # logical AND (not &&)
a or b          # logical OR (not ||)
not a           # logical NOT (not !)
a == b          # equality (same as JS ===, Python has no ===/!==)
a is None       # identity check (use this instead of == None)
a is not None   # not is None

# Useful built-in functions
len(mylist)          # length
range(start, stop)   # integer sequence
enumerate(mylist)    # (index, item) pairs
zip(list1, list2)    # pair elements from two lists
sorted(mylist)       # returns sorted copy
sum([1, 2, 3])       # 6
max([1, 5, 3])       # 5
min([1, 5, 3])       # 1
print(x)             # console.log
```

---

## Part 15 — The Training Loop Pattern

This is the most important code pattern in "Build an LLM." Learn to read it:

```python
import torch
import torch.nn as nn

# Setup
model = NeuralNetwork(num_inputs=2, num_outputs=2)
optimizer = torch.optim.SGD(model.parameters(), lr=0.5)
num_epochs = 3

# The training loop
for epoch in range(num_epochs):            # repeat for N epochs
    model.train()                          # set model to training mode

    for input_batch, target_batch in train_loader:  # iterate batches
        optimizer.zero_grad()              # ① reset gradients to 0

        outputs = model(input_batch)       # ② forward pass
        loss = criterion(outputs, target_batch)  # ③ compute loss

        loss.backward()                    # ④ backprop: compute gradients
        optimizer.step()                   # ⑤ update weights

    # Evaluation after each epoch
    model.eval()                           # set model to eval mode
    with torch.no_grad():                  # no gradient tracking during eval
        val_outputs = model(val_data)
        print(f"Epoch {epoch+1}, Loss: {loss.item():.3f}")
```

**The 5-step pattern repeats for every batch:**

1. `optimizer.zero_grad()` — clear old gradients (must do this or they accumulate)
2. `model(input)` — forward pass
3. `loss_fn(outputs, targets)` — compute how wrong we are
4. `loss.backward()` — compute gradients via backprop
5. `optimizer.step()` — nudge weights in the right direction

---

## Part 16 — Type Annotations (You'll See These)

Modern Python ML code often has type hints — they look like TypeScript but are optional:

```python
# Python type hints
def compute_loss(logits: torch.Tensor, targets: torch.Tensor) -> torch.Tensor:
    return torch.nn.functional.cross_entropy(logits, targets)

def load_data(file_path: str, batch_size: int = 32) -> list:
    ...
```

```typescript
// TypeScript equivalent
function computeLoss(logits: Tensor, targets: Tensor): Tensor { ... }
function loadData(filePath: string, batchSize: number = 32): any[] { ... }
```

These are **hints only** — Python doesn't enforce them at runtime.
You don't need to write them, just be able to read them.

---

## Side-by-Side Reference Card

| JavaScript          | Python                         | Notes                         |
| ------------------- | ------------------------------ | ----------------------------- |
| `let x = 5`         | `x = 5`                        | No declaration keyword        |
| `const x = 5`       | `x = 5`                        | Python has no const           |
| `null`              | `None`                         | Capital N                     |
| `undefined`         | _(doesn't exist)_              |                               |
| `true` / `false`    | `True` / `False`               | Capital                       |
| `console.log(x)`    | `print(x)`                     |                               |
| `arr.length`        | `len(arr)`                     |                               |
| `arr.push(x)`       | `arr.append(x)`                |                               |
| `arr.slice(1,3)`    | `arr[1:3]`                     | Upper bound exclusive in both |
| `arr[arr.length-1]` | `arr[-1]`                      | Negative indexing             |
| `arr.map(fn)`       | `[fn(x) for x in arr]`         | List comprehension            |
| `arr.filter(fn)`    | `[x for x in arr if fn(x)]`    |                               |
| `&&` / `\|\|` / `!` | `and` / `or` / `not`           |                               |
| `===`               | `==`                           | Python has no strict equality |
| `obj.prop`          | `obj.prop`                     | Same                          |
| `obj['key']`        | `obj['key']`                   | Same                          |
| `this`              | `self`                         | Always explicit in Python     |
| `new MyClass()`     | `MyClass()`                    | No `new` in Python            |
| `class X extends Y` | `class X(Y):`                  | Inheritance syntax            |
| `super()`           | `super().__init__()`           | Must call explicitly          |
| `x ** 2`            | `x ** 2`                       | Same                          |
| `Math.floor(x)`     | `x // 2` or `int(x)`           |                               |
| `` `${x}` ``        | `f"{x}"`                       | f-string                      |
| `// comment`        | `# comment`                    |                               |
| `{ }` blocks        | indentation                    | Most critical difference      |
| `import x from 'y'` | `import y` / `from y import x` |                               |

---

## Quick-Read Exercises

Read the following code snippets from the actual books and answer the questions below.
Do NOT run this code — just read it.

**Snippet A** (from "Build an LLM" Appendix A):

```python
class NeuralNetwork(nn.Module):
    def __init__(self, num_inputs, num_outputs):
        super().__init__()
        self.layers = nn.Sequential(
            nn.Linear(num_inputs, 30),
            nn.ReLU(),
            nn.Linear(30, 20),
            nn.ReLU(),
            nn.Linear(20, num_outputs)
        )

    def forward(self, x):
        logits = self.layers(x)
        return logits
```

Questions:

1. What class does `NeuralNetwork` inherit from?
2. What does `super().__init__()` do?
3. How many layers does this network have? (Hint: count the `nn.Linear` calls)
4. What happens when you call `model(some_tensor)`?

---

**Snippet B** (from "Build an LLM" Ch. 2):

```python
vocab = {"Hello": 0, "world": 1, "!": 2}
text = ["Hello", "world", "world", "!"]

token_ids = [vocab[token] for token in text]
print(token_ids)   # what does this print?
```

Questions: 5. What does `vocab[token]` do? 6. Rewrite the list comprehension as a JS `.map()` call.

---

**Snippet C** (from "Build an LLM" Ch. 6):

```python
for epoch in range(num_epochs):
    model.train()
    for input_batch, target_batch in train_loader:
        optimizer.zero_grad()
        loss = calc_loss_batch(input_batch, target_batch, model, device)
        loss.backward()
        optimizer.step()
    print(f"Ep {epoch+1}: loss {loss.item():.3f}")
```

Questions: 7. If `num_epochs = 3`, how many times does `optimizer.zero_grad()` run per epoch? Why? 8. What does `loss.backward()` do conceptually? 9. What does `:.3f` format in the f-string do? 10. What is `loss.item()`? Why not just `loss`?

---

## Answers

1. `nn.Module` — the PyTorch base class for all models
2. Calls the parent class constructor — initializes PyTorch's internal machinery. Always required.
3. Three linear layers (plus two ReLU activations between them)
4. Automatically calls `forward(some_tensor)` — Python's `__call__` mechanism triggers this
5. Looks up the token's integer ID in the vocabulary dictionary
6. `const tokenIds = text.map(token => vocab[token]);`
7. Once per batch — there can be many batches per epoch. Gradients must be reset after each weight update, not each epoch.
8. Computes gradients of the loss with respect to every learnable parameter via backpropagation
9. Format the float with exactly 3 decimal places
10. `.item()` extracts a plain Python number from a PyTorch scalar tensor — needed for printing/logging

---

## Vocabulary Cheatsheet

| Term                      | Meaning                                                              |
| ------------------------- | -------------------------------------------------------------------- |
| **indentation**           | Python uses spaces (not `{}`) to define code blocks                  |
| **f-string**              | `f"text {variable}"` — Python's template literal                     |
| **list comprehension**    | `[expr for x in iterable if cond]` — compact map+filter              |
| **None**                  | Python's null/undefined equivalent                                   |
| **self**                  | Python's `this` — always the first method parameter                  |
| **super().**init**()**    | Call parent class constructor — required in PyTorch subclasses       |
| **nn.Module**             | PyTorch base class for all neural network components                 |
| ****init****              | Constructor method — runs when object is created                     |
| **forward()**             | The method PyTorch calls when you run `model(x)`                     |
| **range(n)**              | Generates integers 0..n-1, like `Array.from({length:n},(_,i)=>i)`    |
| **enumerate()**           | Returns (index, item) pairs when iterating                           |
| **zip()**                 | Pairs elements from two iterables together                           |
| **pass**                  | Empty placeholder body — like `{}` in JS                             |
| **with**                  | Context manager — ensures cleanup (file closing, gradient disabling) |
| **torch.no_grad()**       | Context where gradients are not tracked — used during inference/eval |
| **model.train()**         | Puts model in training mode (enables dropout etc.)                   |
| **model.eval()**          | Puts model in evaluation mode (disables dropout etc.)                |
| **optimizer.zero_grad()** | Clears accumulated gradients before each batch                       |
| **loss.backward()**       | Computes gradients via backpropagation                               |
| **optimizer.step()**      | Updates model weights using computed gradients                       |
| **@**                     | Matrix multiplication operator in Python (same as `matmul`)          |
| **\*\***                  | Exponentiation operator (`x**2` = x squared)                         |
| **//**                    | Integer (floor) division: `7 // 2 = 3`                               |
| **is None**               | Identity check — use instead of `== None`                            |

---

## Curated Resources

### Essential (today)

1. **"Python for JavaScript Developers" — scrimba or any focused comparison tutorial**
   Search: "Python tutorial for JavaScript developers" — pick any video under 30 min

2. **"Python in 100 Seconds" — Fireship**
   https://www.youtube.com/watch?v=x7X9w_GIm1s
   _(3 min lightning overview — good calibration of how little Python syntax there really is)_

3. **"PyTorch in 5 Minutes"**
   https://www.youtube.com/watch?v=IC0_FRiX-sw
   _(Fastest possible look at actual PyTorch code patterns)_

### Supplementary

4. **Official Python Tutorial (just sections 3–5)**
   https://docs.python.org/3/tutorial/introduction.html
   _(Reliable reference if you want to look something up)_

5. **"Autograd" — PyTorch official 60-minute blitz**
   https://pytorch.org/tutorials/beginner/blitz/autograd_tutorial.html
   _(Covers `.backward()` and gradients — important for reading Ch. 4+ of Build an LLM)_

---

## Day 5 Summary (One Paragraph)

Python's core syntax is simpler than JavaScript's — no semicolons, no `var/let/const`,
no `{}` blocks, no `this` confusion. The critical differences to internalize: indentation
defines scope, `self` is JavaScript's `this` but always written explicitly, `None`/`True`/`False`
are capitalized, and list comprehensions replace `.map()` + `.filter()`. The one pattern
that unlocks both books is the PyTorch `nn.Module` subclass: define layers in `__init__`,
wire them together in `forward()`, and call the model as a function. The five-step training
loop (zero_grad → forward → loss → backward → step) repeats for every batch in every
epoch — once you can read that loop fluently, you can follow 80% of the code in both books.

---

\*Next: **Day 6 — Consolidation, full self-test, and a structured preview of the books.\***

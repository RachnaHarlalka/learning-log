# Day 7 — Reading Companion: Your First Day in the Books

> **Series:** ML Prerequisites for "Hands-On Large Language Models" + "Build a Large Language Model From Scratch"
> **This file:** An active reading guide — not a summary. Use it _alongside_ the books, not instead of them.
> **Goal:** Make everything you encounter today land correctly the first time.

---

## How This Day Works

Day 7 is not a passive reading day. Passive reading of technical books is mostly wasted time — you turn pages, feel like you understood, and retain almost nothing.

This guide turns you into an active reader. For each major section you'll hit today:

- You get a **Before You Read** briefing — what to watch for
- You get **Anchor Questions** — what you should be able to answer after
- You get **Code Decoding** — line-by-line walkthroughs of the critical snippets
- You get **Confusion Interceptions** — common wrong interpretations, flagged in advance

Work through this file in parallel with the books. When the book says something you don't fully follow, check this file first before rereading from the start.

---

## Recommended Reading Order for Day 7

There are two books. Here's the order that works best and why:

```
START HERE:
"Build an LLM From Scratch" (Raschka) — Appendix A (PyTorch intro)
      ↓
"Build an LLM From Scratch" — Chapter 1 (LLM concepts)
      ↓
"Hands-On LLMs" (Alammar) — Chapter 1 (LLM history and landscape)
      ↓
"Hands-On LLMs" — Chapter 2 (Tokens and Embeddings)
      ↓ (if time remains)
"Build an LLM From Scratch" — Chapter 2 (Working with text data)
```

**Why this order?**
Raschka's Appendix A is almost entirely covered by your Day 4–5 prep — it will feel easy and build confidence. His Chapter 1 gives you a clean architectural map. Alammar's Chapter 1 then fills in the history and intuition. Alammar's Chapter 2 gives you practical embedding code you can actually run. Raschka's Chapter 2 goes deeper on the same embedding concepts but in a from-scratch implementation style.

Don't feel obligated to finish all of this today. The goal is depth over speed.

---

## Section 1 — "Build an LLM" Appendix A: Introduction to PyTorch

**Estimated reading time:** 45–60 min

### Before You Read

This appendix is your PyTorch warm-up. You've already seen most of these concepts in Days 4–5. Your job here isn't to learn — it's to _verify_ that your mental model matches what the book says, and to see the concepts in runnable code for the first time.

Set up a Jupyter notebook or a Python file. Run every code listing as you encounter it. Do not skip this. The whole book is code-first — if you develop a habit of reading code without running it, you'll be lost by Chapter 3.

### Anchor Questions (answer after reading)

1. What does `torch.tensor([[1, 2], [3, 4]]).shape` return? What does each number mean?
2. Why does PyTorch use `float32` by default for decimals instead of `float64`?
3. What is the difference between `.reshape()` and `.view()`? When does it matter?
4. What is the `@` operator doing in `tensor2d @ tensor2d.T`?
5. What does `requires_grad=True` mean on a tensor? Why is it significant?

### Code Decoding — The `nn.Module` Pattern

When you reach the `NeuralNetwork` class in the appendix, it looks like this:

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

Line by line:

| Line                              | What it does                                                                                      |
| --------------------------------- | ------------------------------------------------------------------------------------------------- |
| `class NeuralNetwork(nn.Module):` | Inherits from PyTorch's base class — gives access to `.parameters()`, `.train()`, `.eval()`, etc. |
| `super().__init__()`              | Initializes PyTorch internals — required, always first                                            |
| `nn.Sequential(...)`              | A container that runs layers in order, like a pipeline                                            |
| `nn.Linear(30, 20)`               | A fully-connected layer: 30 inputs → 20 outputs. Has learnable weights (30×20 matrix) and biases  |
| `nn.ReLU()`                       | An activation function layer (no parameters, just applies ReLU element-wise)                      |
| `def forward(self, x):`           | Called automatically when you do `model(x)`                                                       |
| `logits = self.layers(x)`         | Passes input through the Sequential pipeline — all 5 layers in order                              |

**What `nn.Linear(30, 20)` actually does:**

- It holds a weight matrix of shape `[20, 30]` and a bias vector of shape `[20]`
- When you pass an input tensor of shape `[batch, 30]`, it computes `input @ weight.T + bias`
- Output shape: `[batch, 20]`
- These weights start random and are what training adjusts

### Code Decoding — The Training Loop

```python
for epoch in range(num_epochs):
    model.train()                          # ← mode switch
    for X_batch, y_batch in train_loader:
        optimizer.zero_grad()              # ① clear old gradients
        loss = F.cross_entropy(model(X_batch), y_batch)  # ② forward + loss
        loss.backward()                    # ③ backprop
        optimizer.step()                   # ④ update weights
```

**Why `optimizer.zero_grad()` must come before `loss.backward()`:**
PyTorch accumulates gradients by default — every call to `.backward()` _adds_ to existing
gradients rather than replacing them. If you don't clear them first, the gradient from
batch 2 includes leftover signal from batch 1, which corrupts the update. This is a real
bug source for beginners — the code runs without error but trains incorrectly.

**What `model.train()` actually does:**
It doesn't start training. It flips a flag inside the model that activates certain
layers (specifically dropout and batch normalization) that behave differently during
training vs. evaluation. The appendix uses a simple model without these, so it's
technically redundant here — but the book includes it because it's required best
practice for any real model.

### Confusion Interception

> "If `nn.Linear(30, 20)` has a weight matrix of shape `[20, 30]`, why is the input `[batch, 30]` and not `[batch, 20]`?"

The weight matrix is stored as `[output_size, input_size]` for computational reasons,
then transposed during the multiply. The _logical_ mapping is: 30 inputs → 20 outputs.
When you read `nn.Linear(a, b)`, always read it as "takes `a` features, produces `b` features."

---

## Section 2 — "Build an LLM" Chapter 1: Understanding Large Language Models

**Estimated reading time:** 30–40 min

### Before You Read

This chapter is mostly conceptual — very little code. Read it at a faster pace. Its job
is to orient you. The key things to lock in are:

- The distinction between **encoder-only** (BERT), **decoder-only** (GPT), and
  **encoder-decoder** (original Transformer) architectures
- Why GPT is called "autoregressive"
- The surprising fact that next-token prediction on raw text produces such capable models

### Anchor Questions

1. What does "autoregressive" mean? How does it relate to how GPT generates text?
2. GPT-3 has 96 transformer layers. The original 2017 Transformer had 6. What changed and why does it matter?
3. What is "emergent behavior" in LLMs? Give one example from the chapter.
4. Why is next-word prediction considered "self-supervised" rather than "unsupervised"?

### Critical Concept — Self-Supervised Learning

The book calls LLM pretraining "self-supervised." Here's the precise distinction:

- **Unsupervised:** No labels at all — model finds structure (e.g. clustering)
- **Supervised:** Human-provided labels (e.g. "this email is spam")
- **Self-supervised:** Labels generated automatically from the data itself

For LLMs: given the sentence "The cat sat on the", the next word "mat" is the
**automatic label**. No human labeled it. The structure of language creates the labels.
This is why you can train on all text ever written without any annotation — the labels
are already there in the text itself.

### The GPT Architecture — What the Chapter Establishes

```
Encoder (BERT-style) = reads entire input at once, bidirectional context
Decoder (GPT-style)  = reads left-to-right only, generates one token at a time
```

Why does GPT use decoder-only? Because it generates text. A decoder is designed to
produce output one token at a time, with each token conditioned on all previous tokens.
This is exactly what autoregressive generation requires.

The encoder is not needed for generation — it was designed for translation (encoding
a source language into a fixed representation). GPT discards it entirely.

### Confusion Interception

> "The book says GPT is trained on next-word prediction. But ChatGPT clearly does
> instruction-following and answering questions — those aren't in the training objective."

Correct — and this is one of the most important ideas in the field. The next-word
prediction task forces the model to develop an implicit world model: grammar,
facts, reasoning, causality — all emerge because predicting the next word in realistic
text requires understanding all of these. The instruction-following behavior is then
unlocked through fine-tuning (RLHF, instruction tuning) applied on top of the
pretrained base. The pretraining creates the capability; fine-tuning directs it.

---

## Section 3 — "Hands-On LLMs" Chapter 1: An Introduction to LLMs

**Estimated reading time:** 45–60 min

### Before You Read

Jay Alammar writes visually. **Do not skim the figures.** Each figure usually contains
more information than the paragraph around it. Budget 30–60 seconds per figure to
actually trace what's being shown.

This chapter covers the history of NLP from Word2Vec → RNNs → Transformers.
You've studied all the concepts. Here you'll see them in historical context, which
makes the "why" of every design decision click.

### Anchor Questions

1. What specific limitation of RNNs motivated the invention of the attention mechanism?
2. What is the key difference between Word2Vec and BERT's approach to word embeddings?
3. What does "autoregressive" mean, and why is it used to describe GPT but not BERT?
4. What is the difference between text generation models and text representation models? Give one example of each.

### Critical Concept — The RNN Bottleneck

Before transformers, RNNs translated text like this:

```
Input:  "I love dogs"
         ↓   ↓   ↓
RNN:   [h₁] [h₂] [h₃] → single fixed vector → decoder → output
```

The entire input sentence had to be compressed into **one hidden state vector**
before the decoder could start generating. For long sentences, early words were
mostly lost by the time the decoder ran. The encoder-decoder attention mechanism
fixed this by letting the decoder look at _all_ encoder hidden states at each step —
not just the final one.

Transformers took this further: they eliminated the RNN entirely and made attention
the entire computation.

### The Embedding Type Taxonomy (Important for Ch. 2)

Alammar introduces several types of embeddings in Chapter 1. Keep this map handy:

| Type                | Level              | Example model               | Context-sensitive?                    |
| ------------------- | ------------------ | --------------------------- | ------------------------------------- |
| Word embeddings     | Per word           | Word2Vec, GloVe             | No (static)                           |
| Token embeddings    | Per sub-word token | GPT-2 (inside model)        | No (lookup) → Yes (after transformer) |
| Sentence embeddings | Per sentence       | sentence-transformers/SBERT | Yes                                   |
| Document embeddings | Per document       | averaged token embeddings   | Depends                               |

### Confusion Interception

> "The chapter mentions BERT uses a [CLS] token. What is that?"

`[CLS]` (classification token) is a special token prepended to every input sequence
in BERT. Because BERT is bidirectional — it reads the entire sequence — the `[CLS]`
token's final embedding aggregates information from all other tokens. This makes it
a useful "summary embedding" for the whole input, used for tasks like classification.
GPT-style models don't need this because they use causal (left-to-right only) attention.
You'll encounter `[CLS]` again in Alammar's Chapter 4 (classification).

---

## Section 4 — "Hands-On LLMs" Chapter 2: Tokens and Embeddings

**Estimated reading time:** 60–90 min (this one has code to run)

### Before You Read

This is the first chapter with substantial code. Install the dependencies before reading:

```bash
pip install sentence-transformers gensim transformers torch
```

The chapter covers:

1. Tokenization (word → subword → BPE) — new concept
2. Token embeddings in practice
3. Text/sentence embeddings with `sentence-transformers`
4. Word2Vec with `gensim`

Run the code as you go. The chapter is much clearer when you can print outputs and
inspect shapes yourself.

### Anchor Questions

1. What is subword tokenization and why is it better than word-level tokenization?
2. What does BPE (Byte Pair Encoding) do at a high level?
3. The `all-mpnet-base-v2` model produces vectors of size 768 for a whole sentence. What does that mean and how is it computed?
4. After running `model.most_similar("king")`, what do the similarity scores represent?
5. What is the shape of the vector returned by `model.encode("Best movie ever!")`?

### Critical Concept — Tokenization vs. Words

This is new territory — your prereqs didn't cover this in detail.

**Why not tokenize by word?**

Consider the word "apologize." Word tokenization makes it one token. But the model
also needs to handle "apologetic," "apology," "apologetically" — these are closely related
but a word tokenizer treats them as completely different tokens with no shared embedding.

**BPE's solution:** Start from individual characters. Repeatedly merge the most
frequent character pair in the training corpus into a new token. After many merges,
common words become single tokens, rare words are split into common subword pieces.

```
"apologize"    → ["apolog", "ize"]   ← 2 tokens (prefix shared with others)
"apologetic"   → ["apolog", "etic"]  ← 2 tokens (same prefix)
"apologetically" → ["apolog", "etic", "ally"] ← 3 tokens (builds from pieces)
"Akwirw"       → ["Ak", "w", "ir", "w"]  ← unknown word → character pieces
```

The practical result: no `<UNK>` (unknown) token needed. Any word, including
ones that didn't exist when the model was trained, can be represented.

### Code Decoding — Sentence Embeddings

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
vector = model.encode("Best movie ever!")
print(vector.shape)  # (768,)
```

What's happening step by step:

1. `"Best movie ever!"` → tokenizer → token IDs (e.g. `[101, 2190, 3185, 2428, 102]`)
2. Token IDs → embedding layer → token vectors (shape: `[5, 768]` — one per token)
3. Transformer processes these, producing contextual embeddings (`[5, 768]`)
4. **Mean pooling:** average across all 5 token vectors → `[768]`
5. That `[768]`-dimensional vector is what `.encode()` returns

The model was specifically trained (with SBERT / contrastive learning) so that
semantically similar sentences end up with similar vectors after this pooling step.
Generic models like raw BERT produce poor sentence embeddings because they weren't
trained for this task.

### Code Decoding — Word2Vec Nearest Neighbors

```python
model.most_similar([model['king']], topn=11)
# Returns:
# [('king', 1.0), ('prince', 0.82), ('queen', 0.78), ('emperor', 0.77), ...]
```

The score next to each word is **cosine similarity** — you learned this in Day 4.
`('king', 1.0)` means the vector of "king" is perfectly similar to itself (expected).
`('queen', 0.78)` means the vectors for "king" and "queen" are pointing in nearly
the same direction in the 50-dimensional embedding space.

This lookup is just: compute cosine similarity between the query vector and all
vocabulary vectors, return the top-N highest. No magic — just vector geometry.

### Confusion Interception

> "The chapter shows `model['king'] - model['man'] + model['woman'] ≈ model['queen']`.
> How can vector arithmetic produce semantically meaningful results?"

This works because Word2Vec's training objective implicitly creates a geometry where
semantic relationships become linear directions in embedding space. If "king" and
"man" share a certain directional component (the "royal male" direction), then
subtracting "man" and adding "woman" removes the male component and adds a
female one — leaving you near "queen." This was discovered empirically, not designed.
It's one of the most striking demonstrations that neural networks can learn structured
representations of meaning.

---

## Section 5 — "Build an LLM" Chapter 2: Working with Text Data

**Estimated reading time:** 75–90 min (heaviest code chapter today)

### Before You Read

This is where Raschka implements everything from scratch that Alammar showed you
with libraries. If you're running low on time today, do Alammar's Chapter 2 first and
return to this one tomorrow. If you have energy, this chapter pays off enormously —
it demystifies what `SentenceTransformer.encode()` is actually doing.

Install before reading:

```bash
pip install tiktoken torch
```

### Anchor Questions

1. After tokenizing "the-verdict.txt" with BPE, how many tokens does the book get?
2. What is the `<|endoftext|>` special token for?
3. What is a "sliding window" approach to generating training data?
4. After calling `token_embedding_layer(inputs)` on a batch of shape `[8, 4]`, what shape is the output?
5. Why is positional encoding added _after_ the embedding lookup?

### Critical Concept — Sliding Window Training Data

This is how raw text becomes training examples:

```
Full tokenized text:   [1, 2, 3, 4, 5, 6, 7, 8, 9]
Context length = 4:

Window 1:  input=[1,2,3,4]  target=[2,3,4,5]  ← shift by 1
Window 2:  input=[2,3,4,5]  target=[3,4,5,6]  ← slide by stride
Window 3:  input=[3,4,5,6]  target=[4,5,6,7]
...
```

Each `(input, target)` pair teaches the model: "given this context, predict the next token."
The input and target are the same sequence, offset by one position.

**JS analogy:** Imagine a sliding window over an array:

```javascript
const tokens = [1, 2, 3, 4, 5, 6, 7, 8, 9];
const windowSize = 4;
for (let i = 0; i <= tokens.length - windowSize - 1; i++) {
  const input = tokens.slice(i, i + windowSize);
  const target = tokens.slice(i + 1, i + windowSize + 1);
}
```

### Code Decoding — The Embedding Layer Output Shape

```python
vocab_size = 50257
output_dim = 256
token_embedding_layer = torch.nn.Embedding(vocab_size, output_dim)

inputs = torch.tensor([[40, 367, 2885, 1464],   # batch item 1: 4 token IDs
                        [1807, 3619, 402, 271]])  # batch item 2: 4 token IDs

token_embeddings = token_embedding_layer(inputs)
print(token_embeddings.shape)   # torch.Size([2, 4, 256])
```

Decoding the shape `[2, 4, 256]`:

- `2` = batch size (2 sentences)
- `4` = sequence length (4 tokens each)
- `256` = embedding dimension (256 numbers per token)

For each of the 8 token IDs (2 × 4), the embedding layer looks up that ID's row in
the `[50257, 256]` weight matrix. The result is a 3D tensor.

### Code Decoding — Positional Embeddings

```python
context_length = 4
pos_embedding_layer = torch.nn.Embedding(context_length, output_dim)
pos_embeddings = pos_embedding_layer(torch.arange(context_length))
# torch.arange(4) = tensor([0, 1, 2, 3])
# pos_embeddings.shape = [4, 256]

# Final input to transformer:
input_embeddings = token_embeddings + pos_embeddings
# [2, 4, 256] + [4, 256] → [2, 4, 256]  (broadcast over batch)
```

`torch.arange(4)` generates `[0, 1, 2, 3]` — position indices. The positional embedding
layer maps each position index to a 256-dimensional vector. These are **also learnable
parameters** — the model figures out what position encodings work best during training.

The addition works via PyTorch broadcasting: `[4, 256]` is broadcast to match `[2, 4, 256]`
by repeating it for each item in the batch.

### Confusion Interception

> "Why is `<|endoftext|>` assigned token ID 50256 — the last ID in the vocabulary?"

It's a convention, not a requirement. The vocabulary is built bottom-up: first all the
subword merge rules are established (50,000 entries), then special tokens are appended
at the end. `<|endoftext|>` is GPT-2's only special token, so it gets ID 50256.
When batching texts of different lengths, this token is also used for padding — though
the attention mask ensures the model never actually "pays attention" to padding tokens.

---

## The Attention Interlude — A Sneak Preview of Chapter 3

You will hit Chapter 3 ("Coding Attention Mechanisms") either today or very soon.
It is the hardest chapter in "Build an LLM." Here's what you need to understand before
you open it — a conceptual bridge your prereqs didn't fully build.

### The Problem Attention Solves

In the embedding pipeline you've studied, token `"bank"` always gets the same embedding
vector regardless of whether it appears in "river bank" or "bank account."

The transformer's job is to take those static embeddings and _update_ them based on
context. After the attention mechanism processes them, the same token has a different
vector depending on what surrounds it. That updated vector is called a **context vector**.

Attention is the mechanism that computes context vectors.

### The Q/K/V Intuition

Self-attention creates three projections of each token's embedding:

- **Query (Q):** "What am I looking for?" — the current token's search query
- **Key (K):** "What do I contain?" — every token's "label" for what it offers
- **Value (V):** "What information do I contribute?" — the actual content to mix in

The mechanism:

1. Compute how relevant each token is to the current token: `score = Q · Kᵀ`
2. Normalize to probabilities: `weights = softmax(score / √d_k)`
3. Weighted sum of value vectors: `context = weights · V`

**Database analogy** (the books use this): Think of a key-value store, but instead
of exact key matching, you have a _fuzzy query_ that matches all keys to varying degrees.
The weights tell you how much of each value to retrieve.

### What the Code Will Look Like

```python
# inputs shape: [6, 3]  (6 tokens, 3-dim embeddings)
# W_query, W_key, W_value: trainable [3, 2] matrices

queries = inputs @ W_query   # [6, 3] @ [3, 2] → [6, 2]
keys    = inputs @ W_key     # [6, 2]
values  = inputs @ W_value   # [6, 2]

attn_scores  = queries @ keys.T             # [6, 2] @ [2, 6] → [6, 6]
attn_weights = softmax(attn_scores / √2)    # [6, 6], each row sums to 1
context_vecs = attn_weights @ values         # [6, 6] @ [6, 2] → [6, 2]
```

The `[6, 6]` attention score matrix is the most important tensor to understand.
Row `i`, column `j` contains "how much should token `i` attend to token `j`."
After softmax, each row is a probability distribution over all tokens.

The final context vectors have the same shape as the input embeddings — `[6, 2]` —
but now each token's vector is a **weighted blend of all tokens' value vectors**,
weighted by relevance. This is contextualisation.

---

## Active Reading Techniques

### The Three-Pass System

For code-heavy chapters (Ch. 2–3 of both books):

**Pass 1 — Read the code, predict the output.**
Before running a listing, look at it and write down what you expect the print to say.
Specifically: what shape do you expect the output tensor to be?

**Pass 2 — Run it and check.**
If your prediction was wrong, find exactly which step you misunderstood. Don't move on until you understand the discrepancy.

**Pass 3 — Modify it.**
Change one thing — the batch size, the embedding dimension, the number of tokens —
and predict the new output shape. Run to verify. This builds genuine intuition.

### When to Stop vs. When to Keep Reading

**Stop and reread when:**

- A shape doesn't make sense to you (usually means missing a matrix multiplication somewhere)
- A concept is used before it's been defined (make a note and look for the definition ahead)
- Code produces output you can't trace back to the input

**Keep reading when:**

- A concept is introduced but not yet fully explained (the books often explain shortly after)
- A library function's internals are unclear (trust the interface; internals can wait)
- You don't understand _why_ an architectural choice was made (often explained in the next section)

### The Shape-Tracking Method

For every operation on a tensor, write the shapes:

```
inputs:           [6, 3]
@ W_query [3,2]:  [6, 2]   ← (6×3) @ (3×2) = (6×2)  ✓
@ keys.T [2,6]:   [6, 6]   ← (6×2) @ (2×6) = (6×6)  ✓
softmax:          [6, 6]   ← same shape, normalizes rows
@ values [6,2]:   [6, 2]   ← (6×6) @ (6×2) = (6×2)  ✓
```

Matrix multiplication rule: `[a, b] @ [b, c] = [a, c]` — inner dimensions must match,
outer dimensions become the output shape. If the inner dimensions don't match,
you have a bug.

---

## Quick Reference Card for Today

Things you'll look up repeatedly — they're here so you don't break your flow.

### Common Tensor Operations

| Operation                  | What it does                 | Example                            |
| -------------------------- | ---------------------------- | ---------------------------------- |
| `tensor.shape`             | Dimensions as tuple          | `torch.Size([8, 4, 256])`          |
| `tensor.T`                 | Transpose (2D only)          | `[4, 6]` → `[6, 4]`                |
| `A @ B`                    | Matrix multiply              | `[6, 3] @ [3, 2]` → `[6, 2]`       |
| `tensor.unsqueeze(0)`      | Add dimension at axis 0      | `[4]` → `[1, 4]`                   |
| `tensor.squeeze(0)`        | Remove dimension at axis 0   | `[1, 4]` → `[4]`                   |
| `tensor.view(a, b)`        | Reshape (must be contiguous) | `[8]` → `[2, 4]`                   |
| `tensor.reshape(a, b)`     | Reshape (works always)       | Same output                        |
| `torch.cat([a, b], dim=1)` | Concatenate along axis       | `[3,2],[3,2]` → `[3,4]`            |
| `torch.softmax(x, dim=-1)` | Softmax along last axis      | Normalizes last dimension to sum=1 |
| `tensor.tolist()`          | Convert to Python list       | For printing/debugging             |
| `tensor.item()`            | Extract single scalar        | `tensor(0.42)` → `0.42`            |

### Matrix Multiply Shape Rule

```
[a, b] @ [b, c]  =  [a, c]
         ↑↑
    these must match
```

If they don't match, PyTorch raises `RuntimeError: mat1 and mat2 shapes cannot be multiplied`.
When you see this error, print both shapes and check the inner dimensions.

### Common PyTorch Errors and What They Mean

| Error                                                                                                          | Likely cause                                                                                       |
| -------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------- |
| `RuntimeError: mat1 and mat2 shapes cannot be multiplied`                                                      | Matrix multiply shape mismatch — print `.shape` on both tensors                                    |
| `RuntimeError: Expected all tensors to be on the same device`                                                  | Mixing CPU and GPU tensors — `tensor.to(device)`                                                   |
| `IndexError: index out of range`                                                                               | Token ID exceeds `vocab_size` in embedding layer                                                   |
| `RuntimeError: Expected input batch_size (N) to match target batch_size (M)`                                   | Input and target shapes don't align in loss computation                                            |
| `RuntimeError: one of the variables needed for gradient computation has been modified by an inplace operation` | Modified a tensor that's in the computation graph — avoid `tensor[i] = x`; use `torch.cat` instead |

---

## End-of-Day Check

Before you close the books, answer these without looking:

1. What is the shape of token embeddings after passing a batch of 8 sentences, each 4 tokens long, through an `nn.Embedding(50257, 256)` layer?

2. Why do we add positional embeddings to token embeddings?

3. In BPE tokenization, what happens to a word the tokenizer has never seen before?

4. What are the three weight matrices in self-attention called, and what does each produce?

5. Describe in one sentence what a context vector is and how it differs from the input embedding it replaces.

6. Why is the attention score divided by `√d_k` (square root of the key dimension) before softmax?

7. Run this mentally: input shape `[6, 3]`, `W_query` shape `[3, 2]`. What is `(inputs @ W_query).shape`?

### Answers

1. `[8, 4, 256]` — batch × sequence × embedding
2. The embedding layer is position-blind — token 3 gets the same vector regardless of whether it's first or last. Positional encodings inject order information.
3. BPE falls back to subword pieces and ultimately individual characters — no `<UNK>` token needed
4. Query (Q), Key (K), Value (V) — Q is what the current token searches for; K is what each token offers as a search target; V is the information retrieved
5. A context vector is an updated representation of a token that has been enriched with information from all other tokens in the sequence, weighted by their relevance
6. For high-dimensional embeddings, dot products grow large, pushing softmax into saturation (near 0/1 outputs) which produces tiny gradients and stalls training. Scaling by `√d_k` keeps the scores in a range where softmax gradients are healthy
7. `[6, 2]` — `[6, 3] @ [3, 2]` → inner dimension (3) matches, outer dimensions (6, 2) form the result

---

## A Honest Note on Pace

You may not finish all five sections today. That is completely normal.

Both books are dense by design — they're teaching you to build one of the most complex
systems in modern computing from first principles. If you reach the end of Alammar's
Chapter 2 and feel genuinely clear on tokenization and embeddings, that's a strong
Day 7. The books don't expire. The concepts compound — each chapter you understand
deeply is worth three chapters skimmed.

The thing to avoid is the feeling of "I read the page." Reading is not understanding.
If you can't answer the Anchor Questions for a section, you need to go back —
not to the beginning of the book, but to the specific paragraph that contains the answer.
Use the questions as a compass, not a judgment.

---

_Day 7 complete. From here, you're reading with a foundation. The books will do the rest._

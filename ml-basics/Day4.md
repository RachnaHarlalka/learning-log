# Day 4 — Vectors, Matrices, Tensors & Embeddings

> **Series:** ML Prerequisites for "Hands-On Large Language Models" (Alammar & Grootendorst) + "Build a Large Language Model From Scratch" (Raschka)
> **Audience:** Fullstack JS/TS developer, zero prior ML background
> **Goal:** Understand the mathematical data structures that every LLM is built on

---

## Why This Day Matters

Everything in ML — every weight, every neuron output, every word, every sentence — is
ultimately a **number inside a data structure**. Vectors, matrices, and tensors are those
data structures. Embeddings are _how meaning gets converted into those numbers_.

You cannot read a single page of either book without hitting these terms. After today,
they will feel completely natural.

---

## Part 1 — The Shape Hierarchy: Scalar → Vector → Matrix → Tensor

Think of this as a nesting of dimensions, just like data structures you already know.

### 1.1 Scalar (0D)

A scalar is a single number. That's it.

```
42        3.14        -0.007
```

**JS analogy:** `const x = 42;`

In ML: a loss value, a single weight, a learning rate — all scalars.

---

### 1.2 Vector (1D)

A vector is an **ordered list of numbers**. It has one dimension — its length.

```
[1.2, -0.5, 0.8, 3.1]   ← a vector of length 4
```

**JS analogy:** `const v = [1.2, -0.5, 0.8, 3.1];`

In ML, a vector represents **one thing described by multiple numbers** — for example,
a word described by 768 numbers (its embedding). The length of the vector is called
its **dimensionality**.

> ⚠️ **Terminology trap:** A "3-dimensional vector" like `[x, y, z]` is still a **1D tensor**
> (rank 1). The three elements are the _values_, not the _axes_. This distinction matters —
> the books use "dimensions" to mean _size of the embedding_, not _tensor rank_.

---

### 1.3 Matrix (2D)

A matrix is a **grid of numbers** — rows and columns. Two dimensions.

```
[[1, 2, 3],
 [4, 5, 6],
 [7, 8, 9]]   ← a 3×3 matrix (3 rows, 3 columns)
```

**JS analogy:** `const m = [[1,2,3],[4,5,6],[7,8,9]];` — a 2D array.

In ML, matrices are everywhere:

- An **embedding lookup table** is a matrix: `vocab_size × embedding_dim`
  (e.g. 50,257 rows × 768 columns for GPT-2 small)
- A **weight matrix** in a neural network layer connects inputs to outputs
- A **batch of vectors** is a matrix: `batch_size × embedding_dim`

---

### 1.4 Tensor (ND)

A tensor is the **general term** for any of the above — and beyond 2D.

| Shape           | Name       | Rank          |
| --------------- | ---------- | ------------- |
| `42`            | Scalar     | 0 (0D tensor) |
| `[1, 2, 3]`     | Vector     | 1 (1D tensor) |
| `[[1,2],[3,4]]` | Matrix     | 2 (2D tensor) |
| `[[[...]]]`     | 3D Tensor  | 3             |
| and so on...    | N-D Tensor | N             |

**Why do LLMs need 3D tensors?**

When you feed a batch of sentences to an LLM, the shape is:

```
[batch_size, sequence_length, embedding_dim]
```

For example: 8 sentences × 4 tokens each × 256 embedding dimensions = a tensor of
shape `[8, 4, 256]`. You can't represent that in a scalar or vector — you need 3 axes.

**JS analogy:** A 3D tensor is like a 3D array — an array of arrays of arrays.

```javascript
// 3D array in JS (2×2×2)
const tensor3d = [
  [
    [1, 2],
    [3, 4],
  ],
  [
    [5, 6],
    [7, 8],
  ],
];
```

---

### 1.5 Tensor Libraries (PyTorch)

In Python, you work with tensors using **PyTorch** (the library both books use heavily).

```python
import torch

scalar  = torch.tensor(1)               # shape: []
vector  = torch.tensor([1, 2, 3])       # shape: [3]
matrix  = torch.tensor([[1, 2],         # shape: [2, 2]
                         [3, 4]])
tensor3d = torch.tensor([[[1, 2],       # shape: [2, 2, 2]
                           [3, 4]],
                          [[5, 6],
                           [7, 8]]])

# Check shape (like .length, but for every dimension)
print(matrix.shape)   # torch.Size([2, 2])
```

**JS analogy:** PyTorch is like lodash — but for multi-dimensional numerical arrays,
with GPU support and automatic differentiation built in.

> **Data types matter:** PyTorch defaults to `torch.int64` for integers and
> `torch.float32` for decimals. Most ML uses `float32` — it's a deliberate tradeoff:
> enough precision for training, less memory than `float64`, and GPUs are optimized
> for 32-bit math.

---

## Part 2 — Embeddings

This is the most important concept in both books. If tensors are _how_ data is stored,
embeddings are _what meaning looks like as numbers_.

### 2.1 The Core Problem

Neural networks only understand numbers. The word `"king"` means nothing to a model.
So we need a way to convert words (and tokens, sentences, images) into vectors of
numbers — and those numbers must carry **semantic meaning**.

That's what an **embedding** is: a dense vector of floating-point numbers that
represents something (a word, a token, a sentence) in a way that captures its meaning.

**JS analogy:** Imagine you had a function:

```javascript
embed("king"); // → [0.9, 0.1, 0.8, -0.3, ...] (768 numbers)
embed("queen"); // → [0.8, 0.9, 0.7, -0.2, ...] (768 numbers, similar pattern!)
embed("apple"); // → [-0.1, 0.0, 0.3, 0.9, ...]  (768 numbers, very different)
```

Words with similar meanings have **similar vectors**. This is not hardcoded —
the model _learns_ it from data.

---

### 2.2 Why "Dense"?

An older approach called **one-hot encoding** represents a word as a vector of all zeros
with a single `1` at the word's index:

```
Vocabulary: [cat, dog, king, queen]

"king" → [0, 0, 1, 0]   ← sparse: only one non-zero value
```

Problems:

- If your vocabulary is 50,000 words, every vector is 50,000 numbers long and nearly all zeros — enormous waste of memory.
- `"king"` and `"queen"` look completely unrelated because their `1`s are in different positions — no semantic information is captured.

**Embeddings fix this** — they're "dense" (most values are non-zero) and the pattern
of values encodes _relationships_:

```
"king"  → [0.9, 0.1, 0.8, ...]  ← 768 meaningful non-zero numbers
"queen" → [0.8, 0.9, 0.7, ...]  ← similar pattern = similar meaning
```

---

### 2.3 The Famous Word2Vec Insight

Word2Vec was an early breakthrough that showed how to _train_ embeddings to capture
meaning. The key idea:

> **Words that appear in similar contexts tend to have similar meanings.**

Training procedure (simplified):

1. Start every word with a **random** vector
2. Train a neural network on millions of word pairs from text:
   - Input: two words that appear near each other → model should output `1` (neighbors)
   - Input: two randomly chosen words → model should output `0` (not neighbors)
   - _(Adding random non-neighbor pairs is called "negative sampling")_
3. During training, vectors of neighboring words get pulled closer together; non-neighboring words get pushed apart
4. After training, the trained vectors _are_ the embeddings — throw away the network, keep the vectors

The result of this training: `king - man + woman ≈ queen`. Arithmetic works because
the embedding space encodes relationships geometrically.

> ⚠️ **Important limitation of Word2Vec:** The word `"bank"` gets _one_ embedding,
> forever — regardless of context (financial bank vs. river bank). This is called a
> **static embedding**. LLMs fix this with _contextual embeddings_ (see Part 3).

---

### 2.4 How Similarity Is Measured

If words are vectors, "similarity" means "closeness" in that high-dimensional space.
The most common measure is **cosine similarity** — it measures the angle between two
vectors, not their absolute distance:

- **Cosine similarity = 1** → vectors point in the same direction → very similar meaning
- **Cosine similarity = 0** → vectors are perpendicular → unrelated
- **Cosine similarity = -1** → vectors point in opposite directions → opposite meaning

**JS analogy:** Imagine two arrows drawn from the origin in 3D space. Cosine similarity
tells you how much they're pointing the same way, regardless of how long they are.

```python
# From "Hands-On LLMs": nearest neighbors of "king" in embedding space:
# model.most_similar("king") returns:
# [('prince', 0.82), ('queen', 0.78), ('emperor', 0.77), ...]
# These scores ARE cosine similarities.
```

---

### 2.5 Embedding Dimensions

The number of values in an embedding vector is its **dimensionality**. Bigger ≠ always better:

| Model                                     | Embedding Dimensions |
| ----------------------------------------- | -------------------- |
| GloVe (word2vec-style, Wikipedia)         | 50–300               |
| GPT-2 Small (117M params)                 | 768                  |
| GPT-2 Large                               | 1,280                |
| GPT-3 (175B params)                       | 12,288               |
| all-mpnet-base-v2 (sentence-transformers) | 768                  |

Higher dimensions can capture more nuance but cost more memory and compute.
This is a **deliberate design tradeoff** in every model architecture.

---

## Part 3 — Embeddings Inside an LLM

This is where it all connects to what you'll read in the books.

### 3.1 The Token → Embedding Pipeline

Before a transformer model processes text, that text must become numbers:

```
Raw text: "Hello world"
    ↓
Tokenizer → Token IDs: [15496, 995]
    ↓
Embedding Layer → Vectors: [[0.3, -0.1, ...], [-0.5, 0.8, ...]]
    (each token ID looks up a row in the embedding weight matrix)
    ↓
Positional Encoding added → final input vectors
    ↓
Transformer layers process these vectors
    ↓
Output: contextual embedding vectors for each token position
```

### 3.2 The Embedding Matrix (Lookup Table)

Inside an LLM, there's a large matrix called the **embedding layer**:

```
Shape: [vocab_size × embedding_dim]
e.g.:  [50,257   ×     768       ]  ← for GPT-2 small
```

When a token with ID `3` enters the model, the embedding layer simply **looks up row 3**
of this matrix. That row is the token's embedding vector.

**JS analogy:**

```javascript
const embeddingMatrix = [
  [0.1, -0.4, 0.9], // row 0: embedding for token ID 0
  [0.5, 0.2, -0.3], // row 1: embedding for token ID 1
  [-0.2, 0.8, 0.1], // row 2: embedding for token ID 2
  [-0.4, 0.9, -1.1], // row 3: embedding for token ID 3
  // ...50,257 rows total
];

function embed(tokenId) {
  return embeddingMatrix[tokenId]; // simple array index lookup
}
```

The crucial insight: **these values are not hardcoded — they are parameters that get
learned during training**, just like any other weight in the network. The embedding
matrix starts random and gets refined over millions of training steps.

---

### 3.3 Static vs. Contextual Embeddings

|                       | Static (Word2Vec, GloVe)        | Contextual (LLMs)                          |
| --------------------- | ------------------------------- | ------------------------------------------ |
| `"bank"` always means | the same thing                  | depends on surrounding words               |
| How produced          | fixed lookup table, pre-trained | computed dynamically by transformer layers |
| Output                | same vector every time          | different vector per context               |
| Example models        | Word2Vec, GloVe                 | BERT, GPT-2, GPT-3                         |

LLMs produce **contextual embeddings** — the output vector for a token is influenced
by every other token in the sentence. This is the core job of the transformer's
**attention mechanism**, which you'll study deeply in the books.

---

### 3.4 Text Embeddings (Sentence-Level)

For some tasks (semantic search, RAG, classification), you need **one vector for an
entire sentence or document** — not one per token.

Special models called **sentence transformers** handle this:

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
vector = model.encode("Best movie ever!")
print(vector.shape)  # (768,)  ← the whole sentence compressed into one vector
```

The whole sentence `"Best movie ever!"` → one vector with 768 numbers.
Similar sentences will have similar vectors. This is what powers semantic search and RAG
(Retrieval-Augmented Generation), which the books cover extensively.

---

### 3.5 The Batch Shape — Putting It All Together

Here's a real shape from the books — what an LLM actually sees during training:

```python
# 8 sentences, each 4 tokens long, 256-dimensional embeddings
token_embeddings.shape   # torch.Size([8, 4, 256])
```

| Axis   | Meaning                        | Size |
| ------ | ------------------------------ | ---- |
| Axis 0 | Batch (number of sentences)    | 8    |
| Axis 1 | Sequence (tokens per sentence) | 4    |
| Axis 2 | Embedding (numbers per token)  | 256  |

This 3D tensor is what flows into the transformer layers. Every matrix multiplication,
every attention score, and every output in the model operates on tensors of shapes like
this.

---

## Part 4 — Positional Encodings (Preview)

Embedding layers have a subtle problem: they give the same vector to `"cat"` whether
it appears first or last in a sentence. Word order is lost.

The fix: **positional encodings** — a second set of vectors (one per position) that
get added to the token embeddings before the transformer processes them:

```
Final input vector = Token Embedding + Positional Encoding
```

The model then knows both _what_ a token is and _where_ it sits in the sequence.
Both books cover this in detail — you now have enough context that it will click
immediately when you encounter it.

---

## Mental Model — Everything at Once

```
Raw text:     "The cat sat"
Token IDs:    [  464,  3797,  3332 ]             ← 3 integers from tokenizer
                    ↓
Embedding:    [ [v₁...], [v₂...], [v₃...] ]      ← shape [3, 768], each vᵢ is 768 floats
                    ↓
+ Position:   [ [v₁+p₁], [v₂+p₂], [v₃+p₃] ]    ← still shape [3, 768]
                    ↓
Batch of 8:   shape becomes [8, 3, 768]           ← 3D tensor enters transformer
                    ↓
Transformer:  [8, 3, 768] → [8, 3, 768]          ← contextual output embeddings
```

---

## Vocabulary Cheatsheet

| Term                          | Plain English                                                                                                   |
| ----------------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Scalar**                    | A single number. Rank-0 tensor.                                                                                 |
| **Vector**                    | An ordered list of numbers. Rank-1 tensor.                                                                      |
| **Matrix**                    | A 2D grid of numbers (rows × columns). Rank-2 tensor.                                                           |
| **Tensor**                    | General term for any N-dimensional array of numbers.                                                            |
| **Rank / Order**              | Number of axes a tensor has (0=scalar, 1=vector, 2=matrix...)                                                   |
| **Shape**                     | The size of each axis, e.g. `[8, 4, 256]`                                                                       |
| **Embedding**                 | A dense float vector representing something (word/token/sentence) such that similar things have similar vectors |
| **Embedding Dimension**       | How many numbers are in each embedding vector (e.g. 768)                                                        |
| **Embedding Layer**           | A learnable lookup table (matrix) mapping token IDs → embedding vectors                                         |
| **Static Embedding**          | Same vector regardless of context (Word2Vec, GloVe)                                                             |
| **Contextual Embedding**      | Vector changes based on surrounding tokens (BERT, GPT)                                                          |
| **Word2Vec**                  | Early embedding algorithm; trains by predicting neighboring words                                               |
| **Skip-gram**                 | Word2Vec variant: given a word, predict its neighbors                                                           |
| **Negative Sampling**         | Word2Vec trick: train on real pairs vs. random "fake" pairs                                                     |
| **Cosine Similarity**         | Measures angle between two vectors; 1=identical direction, 0=unrelated                                          |
| **One-Hot Encoding**          | Sparse vector: all zeros except one position; predecessor to dense embeddings                                   |
| **Token Embedding**           | Embedding for a single token (a sub-word unit, not necessarily a full word)                                     |
| **Sentence / Text Embedding** | One vector representing an entire sentence or document                                                          |
| **Positional Encoding**       | Extra vector added to token embeddings to preserve word-order information                                       |
| **Batch**                     | Group of inputs processed together; adds one axis to the tensor shape                                           |
| **float32**                   | 32-bit floating point — standard numeric type for ML weights and embeddings                                     |
| **PyTorch**                   | Python library for tensor computation with GPU support and autograd                                             |
| **`torch.tensor()`**          | Creates a PyTorch tensor from a Python list or number                                                           |
| **`.shape`**                  | Attribute showing a tensor's dimensions, e.g. `torch.Size([8, 4, 256])`                                         |
| **`.dtype`**                  | Attribute showing a tensor's data type, e.g. `torch.float32`                                                    |
| **vocab_size**                | Total number of unique tokens in the model's vocabulary (50,257 for GPT-2)                                      |
| **Dense vector**              | A vector where most values are non-zero (opposite of sparse/one-hot)                                            |
| **sentence-transformers**     | Python library for producing sentence-level embeddings using pretrained models                                  |

---

## Self-Check Questions

Answer without looking back. If you can't, re-read that section.

**Conceptual:**

1. What is the difference between a "3-dimensional vector" (e.g. `[x, y, z]`) and a "3D tensor"? Why does this distinction matter when reading the books?
2. Why can't you feed the string `"king"` directly into a neural network?
3. What is the core problem with one-hot encoding that dense embeddings solve? Name two problems.
4. What is Word2Vec's training objective? What linguistic assumption does it make?
5. What is the fundamental limitation of static embeddings? Provide a concrete example where they fail.
6. Why do LLMs add positional encodings on top of token embeddings? What problem does this solve?
7. What does it mean for two embedding vectors to have a cosine similarity of `0.82` vs `0.04`?

**Applied:** 8. A batch of 8 sentences, each 4 tokens long, embedded into 256 dimensions — what is the resulting tensor shape? Write it as `[a, b, c]` and name each axis. 9. GPT-2 small has a vocabulary of 50,257 tokens and embedding dimension 768. What is the shape of the embedding matrix? How many individual parameters is that? 10. GPT-3 uses 12,288 embedding dimensions vs GPT-2's 768. What are the tradeoffs of this choice? 11. A model gives you these similarity scores: `sim("dog", "cat") = 0.82`, `sim("dog", "automobile") = 0.12`. What does this tell you about what the model learned? 12. You want to build a semantic search engine over 10,000 documents. Do you use token embeddings or sentence embeddings? Why?

**Code reading:**

```python
import torch
token_embedding_layer = torch.nn.Embedding(50257, 256)
inputs = torch.tensor([[40, 367, 2885, 1464],
                        [1807, 3619, 402, 271]])
output = token_embedding_layer(inputs)
```

13. What is the shape of `output`? Explain each dimension.
14. What does `torch.nn.Embedding(50257, 256)` create? What are its learnable parameters?
15. If you printed `output[0][2]`, what would you get and what does it represent?

---

## Book Connection Map

| Concept from today                              | Where you'll see it                                                        |
| ----------------------------------------------- | -------------------------------------------------------------------------- |
| Embeddings as lookup tables                     | "Build an LLM" Ch. 2 (§2.3–2.8) — implemented from scratch in PyTorch      |
| Token embeddings + positional encoding          | "Build an LLM" Ch. 2 (§2.8) — exact pipeline you built mentally today      |
| Word2Vec training process                       | "Hands-On LLMs" Ch. 1 (history) + Ch. 2 (deep dive + code)                 |
| Text/sentence embeddings                        | "Hands-On LLMs" Ch. 2 — used throughout in RAG, search, classification     |
| `[batch, seq_len, embed_dim]` shape             | "Build an LLM" Ch. 2–3 — you'll see this tensor shape on nearly every page |
| Static vs. contextual embeddings                | Both books — this distinction is _why_ transformers exist                  |
| Cosine similarity                               | "Hands-On LLMs" Ch. 4–5 (classification, clustering, semantic search)      |
| sentence-transformers library                   | "Hands-On LLMs" Ch. 2 + Ch. 10 (SBERT, contrastive training)               |
| Multi-head attention on tensors                 | "Build an LLM" Ch. 3 — attention weight matrices, Q/K/V tensors            |
| Multimodal embeddings (image patches as tokens) | "Hands-On LLMs" Ch. 9 — images turned into embedding vectors same as text  |

---

## Curated Video Resources

Watch in this order — total runtime ~90–120 min:

### Essential (watch today)

1. **"Visualizing Neural Networks" — 3Blue1Brown Chapter 1**
   https://www.youtube.com/watch?v=aircAruvnKk
   _(Covers how tensors flow through a network; extremely visual. Watch the full 4-part series if time allows.)_

2. **"Word Embeddings, Bias in ML, Why You Think What You Think" — StatQuest**
   https://www.youtube.com/watch?v=viZrOnJclY0
   _(Best plain-English explanation of embeddings; ~20 min)_

3. **"The Illustrated Word2Vec" — Jay Alammar (co-author of your book)**
   https://jalammar.github.io/illustrated-word2vec/
   _(Blog post, not video — but Jay is the best visual ML explainer in the industry)_

### Supplementary (if you want more depth)

4. **"Sentence Transformers / SBERT" — StatQuest**
   https://www.youtube.com/watch?v=QWMUBqYCGF4
   _(Covers how sentence-level embeddings are trained; relevant to Ch. 10 of Hands-On LLMs)_

5. **"PyTorch Tensors Crash Course" — Aladdin Persson**
   https://www.youtube.com/watch?v=x9JiIFvlUwk
   _(Hands-on tensor operations — good preview before Day 5's Python session)_

---

## Day 4 Summary (One Paragraph)

Scalars, vectors, matrices, and tensors are just nested containers for numbers —
the data structures of ML. An embedding is a dense float vector representing something
(a word, token, sentence) such that semantic meaning is encoded as geometry: similar
things have similar vectors. Word2Vec proved this was learnable from raw text, but it
produced static embeddings — the same vector for `"bank"` regardless of context. LLMs
fix this with _contextual_ embeddings: the same token gets a different output vector
depending on all surrounding tokens, powered by the attention mechanism. Inside an
LLM, text becomes numbers as: string → token IDs → embedding matrix lookup → 3D
tensor `[batch, seq_len, embed_dim]` → transformer layers. Understanding shapes like
`[8, 4, 768]` is not optional — both books assume you can read them fluently from
the first chapter.

---

_Next: **Day 5 — Python syntax crash course for JavaScript developers** — reading ML code without being a Python expert._

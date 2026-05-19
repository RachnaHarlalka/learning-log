# Chapter 3 — Looking Inside Large Language Models

## Elaborate Study Notes

> **Book:** Hands-On Large Language Models — Jay Alammar & Maarten Grootendorst
> **Builds on:** Chapter 1 (Transformers), Chapter 2 (tokens, embeddings)
> **Time to read these notes:** ~45–60 minutes

---

## Table of Contents

1. [The Big Picture — What This Chapter Covers](#1-the-big-picture--what-this-chapter-covers)
2. [How a Transformer LLM Generates Text](#2-how-a-transformer-llm-generates-text)
3. [The 3 Major Components of a Transformer LLM](#3-the-3-major-components-of-a-transformer-llm)
4. [The Forward Pass — Step by Step](#4-the-forward-pass--step-by-step)
5. [The LM Head — Choosing the Next Token](#5-the-lm-head--choosing-the-next-token)
6. [Decoding Strategies](#6-decoding-strategies)
7. [Parallel Token Processing and Context Size](#7-parallel-token-processing-and-context-size)
8. [The KV Cache — Why Generation Is Fast](#8-the-kv-cache--why-generation-is-fast)
9. [Inside the Transformer Block](#9-inside-the-transformer-block)
10. [The Feedforward Network](#10-the-feedforward-network)
11. [Self-Attention — The Full Explanation](#11-self-attention--the-full-explanation)
12. [Multi-Head Attention](#12-multi-head-attention)
13. [Recent Improvements — Efficient Attention](#13-recent-improvements--efficient-attention)
14. [Positional Embeddings and RoPE](#14-positional-embeddings-and-rope)
15. [Residual Connections and Layer Normalization](#15-residual-connections-and-layer-normalization)
16. [Glossary](#16-glossary)
17. [Chapter Summary](#17-chapter-summary)

---

## 1. The Big Picture — What This Chapter Covers

In Chapter 2, you learned how text becomes tokens and tokens become vectors. Chapter 3 answers the next question: **what happens inside the model after those vectors go in?**

We open the black box. By the end of this chapter you'll understand:

- How LLMs generate text one token at a time (autoregressive generation)
- What the 3 major components of a Transformer LLM are
- What happens inside each Transformer block (attention + feedforward)
- How attention actually works mathematically (Query/Key/Value)
- Why the KV cache dramatically speeds up generation
- What modern improvements like RoPE and grouped-query attention do

> 💡 **Why this matters for you as a fullstack dev:**
> You don't need to implement a Transformer from scratch. But understanding the internals helps you:
>
> - Debug why generation is slow (KV cache, context length)
> - Understand what "temperature" and "top-p" actually do
> - Make informed decisions about model architecture when choosing models for your app
> - Understand error messages and performance bottlenecks

---

## 2. How a Transformer LLM Generates Text

### Token-by-Token Generation (Autoregressive)

LLMs do NOT generate an entire response in one shot. They generate **one token at a time**, in a loop:

```
Step 1: Input: "The capital of France is"
        → Model generates token: "Paris"

Step 2: Input: "The capital of France is Paris"
        → Model generates token: ","

Step 3: Input: "The capital of France is Paris,"
        → Model generates token: "which"

... continues until stop condition (max tokens, end-of-text token)
```

Each step is called a **forward pass** — one pass of data through the entire neural network.

This process has a specific name: **autoregressive generation**. The model consumes its own outputs as future inputs. Each generated token influences all subsequent tokens.

```python
# What the pipeline is doing under the hood:
prompt = "Write an email apologizing to Sarah..."
output = generator(prompt)

# Under the hood, this is a LOOP:
# generated_tokens = []
# while not done:
#     next_token = model.forward(prompt + generated_tokens)
#     generated_tokens.append(next_token)
```

> 💡 **This is why streaming exists.** Most LLM APIs offer streaming responses — they send you each token as it's generated rather than waiting for the full response. This is why you see ChatGPT type out text word by word. Under the hood, it's sending tokens one by one.

---

## 3. The 3 Major Components of a Transformer LLM

```
┌──────────────────────────────────────┐
│  INPUT TEXT                          │
└──────────────────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│  1. TOKENIZER                        │
│  Text → Token IDs                    │
│  (Chapter 2 — you know this!)        │
└──────────────────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│  2. STACK OF TRANSFORMER BLOCKS      │
│  [Block 1] → [Block 2] → ... → [Block 32]  │
│  Each block: Attention + Feedforward │
│  (The "brain" — does all processing) │
└──────────────────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│  3. LM HEAD (Language Modeling Head) │
│  Final vector → probability for      │
│  every token in vocabulary           │
│  → pick the next token               │
└──────────────────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│  OUTPUT TOKEN ID → TOKENIZER.DECODE  │
│  Token ID → Text                     │
└──────────────────────────────────────┘
```

### Inspecting a Real Model's Architecture

```python
# Print the full architecture of Phi-3
print(model)
```

Output (simplified):

```
Phi3ForCausalLM(
  (model): Phi3Model(
    (embed_tokens): Embedding(32064, 3072)  ← vocab: 32,064 tokens, each 3,072-dim
    (layers): ModuleList(
      (0-31): 32 x Phi3DecoderLayer(        ← 32 Transformer blocks
        (self_attn): Phi3Attention(...)      ← Attention layer in each block
        (mlp): Phi3MLP(...)                 ← Feedforward network in each block
        (input_layernorm): Phi3RMSNorm()    ← Normalization (before attention)
        (post_attention_layernorm): Phi3RMSNorm()  ← Normalization (before FFN)
      )
    )
    (norm): Phi3RMSNorm()
  )
  (lm_head): Linear(3072 → 32064)           ← LM Head: 3072 dims → 32,064 scores
)
```

**What this tells you:**

- `embed_tokens`: 32,064 tokens × 3,072 dimensions = the embedding matrix
- `32 x Phi3DecoderLayer`: 32 stacked Transformer blocks
- Each block has `self_attn` (attention) + `mlp` (feedforward)
- `lm_head`: maps the final 3,072-dim vector to 32,064 probability scores (one per token)

---

## 4. The Forward Pass — Step by Step

One **forward pass** = one token generation. Here's what happens:

```
1. Input prompt → tokenizer → token IDs

2. Token IDs → embedding matrix lookup → static token vectors
   Shape: [batch_size, num_tokens, embedding_dim]
   e.g.,  [1,          6,          3072]

3. Vectors flow through 32 Transformer blocks one by one
   Each block: attention → feedforward → output vectors
   Shape stays: [1, 6, 3072] throughout

4. Final vectors from Block 32 → LM Head
   LM Head maps [1, 6, 3072] → [1, 6, 32064]
   (probability score for every token for every position)

5. Take ONLY the last position's scores: [1, 32064]
   → find the token with highest score (or sample from distribution)
   → that's the next generated token

6. Decode token ID → text
   Append to prompt
   → Go back to Step 1 for next token
```

### In Code

```python
prompt = "The capital of France is"
input_ids = tokenizer(prompt, return_tensors="pt").input_ids.to("cuda")

# Step 3: run through all 32 Transformer blocks
model_output = model.model(input_ids)
print(model_output[0].shape)  # torch.Size([1, 6, 3072])

# Step 4: run through LM head
lm_head_output = model.lm_head(model_output[0])
print(lm_head_output.shape)  # torch.Size([1, 6, 32064])

# Step 5: get the last token's scores and find the highest
token_id = lm_head_output[0, -1].argmax(-1)
print(tokenizer.decode(token_id))  # "Paris"
```

> 💡 **Shape notation reminder:** `[1, 6, 3072]` means:
>
> - `1` = batch size (1 sentence)
> - `6` = number of tokens in the input
> - `3072` = embedding dimensions (Phi-3's model dimension)

---

## 5. The LM Head — Choosing the Next Token

The **LM Head** is a simple linear layer that takes the final vector from the last Transformer block and converts it into a score for every token in the vocabulary:

```
Input:  vector of size 3,072   (the model's "understanding" of what comes next)
Output: vector of size 32,064  (a score for each of the 32,064 possible tokens)
```

These scores are called **logits**. They are passed through a **softmax** function to convert them into probabilities that sum to 1.

```
Before softmax (logits):  [2.3, -0.5, 1.1, 4.7, ...]  (any values)
After softmax (probs):    [0.02, 0.001, 0.008, 0.40, ...]  (sum = 1.0)
```

Now we have a probability distribution over all 32,064 tokens. The question is: which token do we pick?

---

## 6. Decoding Strategies

How you choose a token from the probability distribution is called the **decoding strategy**. This is one of the most important things to understand for building LLM-powered apps.

### Greedy Decoding

Always pick the highest probability token.

```python
# Greedy decoding
next_token_id = probabilities.argmax()  # always pick the max
```

- Deterministic: same prompt always produces same output
- Not always the best output — can get stuck in repetitive loops
- Controlled by `do_sample=False` (or `temperature=0`)

### Sampling

Pick randomly based on probability distribution.

```python
# Sampling — picks "Paris" 40% of the time if its probability is 0.40
next_token_id = torch.multinomial(probabilities, num_samples=1)
```

- Non-deterministic: same prompt can produce different outputs
- More creative and varied
- Controlled by `do_sample=True`

### Temperature

**Temperature** controls how sharp or flat the probability distribution is before sampling.

```
Low temperature (0.1):  [0.001, 0.000, 0.998, ...]  ← very peaked, near-greedy
Mid temperature (1.0):  [0.10, 0.05, 0.40, ...]      ← normal distribution
High temperature (2.0): [0.30, 0.25, 0.35, ...]      ← flatter, more random
```

- **Low temperature (< 1.0)** → more focused, predictable, factual
- **Temperature = 0** → exactly greedy decoding
- **High temperature (> 1.0)** → more creative, surprising, potentially incoherent

> 💡 **Practical guide for your apps:**
>
> - Factual Q&A, coding: temperature 0–0.3
> - Balanced chat assistant: temperature 0.7
> - Creative writing, brainstorming: temperature 1.0–1.5
> - Pure chaos (testing/fun): temperature > 2.0

### Top-p (Nucleus Sampling)

Only sample from the smallest set of tokens whose cumulative probability exceeds p.

```
All tokens sorted by probability:
Token A: 0.40 (cumulative: 0.40)
Token B: 0.25 (cumulative: 0.65)
Token C: 0.20 (cumulative: 0.85)  ← top-p=0.85 stops here
Token D: 0.10  ← excluded
Token E: 0.05  ← excluded
```

With `top_p=0.85`, only Tokens A, B, C are candidates. This prevents very unlikely tokens from ever being chosen while still allowing variety.

These decoding parameters are covered in detail in Chapter 6.

---

## 7. Parallel Token Processing and Context Size

One of the Transformer's key strengths is **parallel processing**. All input tokens are processed simultaneously in separate streams.

```
Input: "The capital of France is"
       [The]  [capital]  [of]  [France]  [is]
         ↓        ↓       ↓       ↓       ↓
       [stream1][stream2][stream3][stream4][stream5]
         ↓        ↓       ↓       ↓       ↓
       (through 32 Transformer blocks, in parallel)
         ↓        ↓       ↓       ↓       ↓
       [out1]   [out2]  [out3]  [out4]  [out5]
                                          ↓
                                    LM Head uses only
                                    this last output
                                    to predict next token
```

The **context length** (or context size) is the maximum number of these parallel streams. Phi-3-mini's 4K context means it can process up to 4,096 streams simultaneously.

**Why process all tokens if only the last output is used?**

The attention mechanism in each Transformer block requires all previous token vectors to compute attention scores. Even though only the last position's final vector goes to the LM Head, the intermediate vectors from all positions are used during attention computation in every block.

---

## 8. The KV Cache — Why Generation Is Fast

### The Problem Without Cache

When generating token #2, the model needs to re-process the entire input PLUS token #1:

```
Generation step 1: process ["The", "capital", "of", "France", "is"]
                   → generates "Paris"

Generation step 2: process ["The", "capital", "of", "France", "is", "Paris"]
                   → generates ","
                   ↑ ALL of this was already computed in step 1!
                   ↑ Re-doing this is wasteful
```

Without caching: each generation step repeats all previous computations. For a 100-token response, you'd compute the first token's representation 100 times.

### The KV Cache Solution

During attention, the key (K) and value (V) matrices from previous tokens don't change between generation steps. We can cache them:

```
Step 1: Compute K,V for all input tokens → CACHE them
        Use only token position 5 (last) for LM Head

Step 2: New token arrives ("Paris")
        → Compute K,V for "Paris" only → ADD to cache
        → Use cached K,V for all previous tokens
        → Only one new computation needed!
```

### The Performance Difference

```python
# With cache (default)
%%timeit -n 1
model.generate(input_ids, max_new_tokens=100, use_cache=True)
# Result: ~4.5 seconds on T4 GPU

# Without cache
%%timeit -n 1
model.generate(input_ids, max_new_tokens=100, use_cache=False)
# Result: ~21.8 seconds on T4 GPU
```

**4.8x speedup** just from caching. In production, this is critical.

> 💡 **The KV cache is why longer context = more memory.** Every token in your context window requires storing K and V matrices in GPU memory. This is why large context windows (200K tokens) require much more VRAM than small ones (4K tokens). When you get OOM (out of memory) errors, the KV cache is often the culprit.

---

## 9. Inside the Transformer Block

Each of the 32 Transformer blocks in Phi-3 has the same structure:

```
Input vectors (from previous block or embedding layer)
    ↓
[Layer Normalization]  ← normalize before attention
    ↓
[Self-Attention Layer] ← incorporate context from other tokens
    ↓
[Residual Connection]  ← add input to output (skip connection)
    ↓
[Layer Normalization]  ← normalize before feedforward
    ↓
[Feedforward Network]  ← store knowledge, do computation
    ↓
[Residual Connection]  ← add input to output again
    ↓
Output vectors (passed to next block)
```

Two major components:

1. **Self-Attention** — looks at other tokens for context
2. **Feedforward Network** — stores knowledge, processes information

We'll cover each in detail.

---

## 10. The Feedforward Network

### What It Does

The feedforward neural network (FFN, also called MLP — Multi-Layer Perceptron) in each Transformer block is where most of the model's **stored knowledge** lives.

> 💡 **Think of it this way:** If you type "The Shawshank" the model outputs "Redemption". The FFN is what stores the fact that these two words go together — it memorized this from training data.

The FFN:

- **Memorizes facts and patterns** from training data
- **Interpolates** between patterns it has seen — this is how it handles inputs it's never seen before
- Processes each token's vector independently (unlike attention which looks at all tokens)

### Structure

```python
# Phi-3 FFN dimensions
# Input:   3,072 dims
# Hidden:  16,384 dims (expands)
# Output:  3,072 dims (contracts back)

(gate_up_proj): Linear(3072 → 16384)
(down_proj):    Linear(8192 → 3072)
(activation_fn): SiLU()
```

The FFN expands the vector to a much higher dimension (16,384) to do rich computation, then contracts it back to the model dimension (3,072). This expansion-contraction pattern is where the model has capacity to store complex patterns.

### Memorization vs Generalization

The FFN doesn't just memorize — it generalizes. This is the key difference between an LLM and a lookup table:

```
Lookup table:  "The Shawshank" → "Redemption"  (exact match only)
LLM FFN:       Can handle "Shawshank film from 1994" → "Redemption"
               (interpolates between patterns it learned)
```

---

## 11. Self-Attention — The Full Explanation

This is the most important mechanism in the entire Transformer. Read this carefully.

### The Problem Attention Solves

Consider: "The dog chased the squirrel because **it** was hungry."

What does "it" refer to — the dog or the squirrel? A human knows from context it's the dog. But a model processing each word independently would have no way to know.

**Attention solves this** by allowing the "it" token to look at all other tokens and pull in relevant information.

### The Two Steps of Attention

**Step 1: Relevance Scoring** — How relevant is each previous token to the current token?

**Step 2: Combining Information** — Weighted mix of previous token information based on relevance scores.

### Query, Key, Value — The Core Mechanism

Attention uses three matrices learned during training:

- **Query (Q)**: "What am I looking for?" — represents the current token's information need
- **Key (K)**: "What do I contain?" — represents what each token offers
- **Value (V)**: "What information do I carry?" — the actual content to mix in

> 💡 **Developer analogy:** Think of attention like a database query.
>
> - **Query** = your SELECT statement ("what I'm looking for")
> - **Key** = the index of each row ("what this row is about")
> - **Value** = the actual data in the row ("what this row contains")
> - **Attention score** = how well the query matches each key
> - **Output** = a weighted mix of values based on match quality

### Step-by-Step Calculation

```
Starting position: processing token "it" in "Sarah fed the cat because it"

Inputs:
  - Current token vector: v_it (the vector for "it")
  - All previous token vectors: v_Sarah, v_fed, v_the, v_cat, v_because

Learned projection matrices (from training):
  - W_Q (query projection matrix)
  - W_K (key projection matrix)
  - W_V (value projection matrix)

Step A: Project inputs to Q, K, V spaces
  Q = v_it × W_Q               ← Query for current token
  K = [v_Sarah, v_fed, v_the, v_cat, v_because, v_it] × W_K  ← Keys for all tokens
  V = [v_Sarah, v_fed, v_the, v_cat, v_because, v_it] × W_V  ← Values for all tokens

Step B: Relevance scoring
  scores = Q × K^T              ← dot product: how much does Q match each K?
  scores = scores / sqrt(dim)   ← scale (prevents scores from getting too large)
  scores = softmax(scores)      ← normalize to sum to 1

  Result (example):
    "Sarah": 0.05
    "fed":   0.02
    "the":   0.01
    "cat":   0.70   ← HIGH — "it" is most related to "cat"
    "because": 0.15
    "it":    0.07

Step C: Combine information
  output = scores × V
         = 0.05×v_Sarah + 0.02×v_fed + 0.01×v_the + 0.70×v_cat + 0.15×v_because + 0.07×v_it

  Result: a new vector for "it" that contains 70% cat information
          → "it" now carries "cat" context → model understands "it" = cat
```

### Masked Attention in Decoders

Generative LLMs (decoder-only) use **masked self-attention**: when processing position N, it can only attend to positions 1 through N. It cannot look into the future.

```
Processing position 3 ("of") in "The capital of France is":
  Can attend to: "The" (pos 1), "capital" (pos 2), "of" (pos 3)
  Cannot attend to: "France" (pos 4), "is" (pos 5) ← masked (zeroed out)
```

This masking is what makes the model autoregressive — it can only use information that has already been "seen."

---

## 12. Multi-Head Attention

### Why Multiple Heads?

A single attention operation can only focus on one type of relationship at a time. Language has many simultaneous relationships:

- Grammatical (subject-verb agreement)
- Semantic (pronoun references)
- Positional (nearby words)
- Syntactic (dependency parsing)

**Multi-head attention** runs several attention operations in parallel, each potentially learning different relationship types.

```
Input vectors
    ↓
Split into H heads (H = 32 in Phi-3)
    ↓
[Head 1]  [Head 2]  ...  [Head 32]   ← each head has its own Q,K,V matrices
    ↓         ↓               ↓
[out_1]   [out_2]  ...  [out_32]
    ↓
Concatenate all head outputs
    ↓
Linear projection
    ↓
Final output
```

Each head can specialize: Head 1 might focus on pronoun resolution, Head 2 on syntactic structure, etc. (this specialization emerges from training, not from explicit design).

### Multi-Query and Grouped-Query Attention

**Multi-Head Attention (original):** Each of the H heads has its own Q, K, V matrices.

```
Head 1: Q₁, K₁, V₁
Head 2: Q₂, K₂, V₂
...
Head 32: Q₃₂, K₃₂, V₃₂
```

Problem: The K and V matrices are large and must all be stored in the KV cache. For large models, this is expensive.

**Multi-Query Attention:** All heads share ONE set of K, V matrices. Each head only has its own Q matrix.

```
Head 1: Q₁, K_shared, V_shared
Head 2: Q₂, K_shared, V_shared
...
Head 32: Q₃₂, K_shared, V_shared
```

Benefit: much smaller KV cache → faster inference, less memory.
Downside: some quality loss (all heads see the same K, V).

**Grouped-Query Attention (GQA):** A middle ground — divide heads into groups, each group shares K, V.

```
Group 1 (Heads 1-8):  Q₁-Q₈, K₁_shared, V₁_shared
Group 2 (Heads 9-16): Q₉-Q₁₆, K₂_shared, V₂_shared
...
```

GQA is used by Llama 2, Llama 3, Mistral, and many modern models. It provides most of the efficiency gain of multi-query attention while maintaining more of the quality of full multi-head attention.

---

## 13. Recent Improvements — Efficient Attention

### Local/Sparse Attention

Full attention: every token attends to every previous token. For a 4K context, that's 4,000 × 4,000 comparisons per layer.

**Sparse attention** limits each token to only attend to nearby tokens (a sliding window). This reduces computation from O(n²) to O(n × window_size).

GPT-3 alternates between full attention blocks and sparse attention blocks to balance quality and efficiency.

### Flash Attention

The attention calculation involves multiple large matrix operations. A naive implementation moves data back and forth between GPU high bandwidth memory (HBM) and fast on-chip memory (SRAM) many times.

**Flash Attention** reorders the computation to minimize this data movement — it fuses multiple operations to keep data in SRAM as long as possible. The result:

- 2–4x faster attention computation
- Less GPU memory required
- Supports longer sequences

Flash Attention v2 and v3 provide further improvements. It's now used by virtually every serious LLM implementation. Enabled by default in Hugging Face Transformers.

---

## 14. Positional Embeddings and RoPE

### Why Position Matters

Unlike RNNs which process tokens sequentially (so position is implicit), Transformers process all tokens in parallel. This means the model has no inherent sense of which token comes first.

**Positional embeddings** add position information to each token's vector:

```
Without position info:
  "Dog bites man" and "Man bites dog" → same token vectors in same attention

With position info:
  Token at position 1 gets a different encoding than token at position 3
  → Order is preserved
```

### Absolute Positional Embeddings (Original)

The original 2017 Transformer added a position-specific vector to each token embedding at the start:

```
token_vector[pos 1] = embedding("Dog") + position_encoding(1)
token_vector[pos 2] = embedding("bites") + position_encoding(2)
```

Problem: these are fixed to specific positions. When documents are packed together during training (multiple short docs in one context), the position numbers are misleading.

### RoPE — Rotary Position Embeddings

**RoPE** (used by Llama, Phi-3, Mistral, and most modern models) encodes position differently:

- Instead of adding a position vector at the start, it **rotates** the Q and K vectors in the attention step by an angle proportional to their position
- Captures both **absolute** position (where in the sequence) and **relative** position (how far apart two tokens are)
- Applied during attention, not at the beginning of the forward pass

```
Traditional: token_vector += position_vector  (at start, once)
RoPE:        Q = rotate(Q, position_angle)    (during attention)
             K = rotate(K, position_angle)
```

> 💡 **Why this matters for you:** RoPE is one reason modern models can generalize to sequences longer than they were trained on (with some techniques). When you see models extend their context window (e.g. from 4K to 128K), RoPE-based positional encoding makes this much easier than absolute embeddings.

---

## 15. Residual Connections and Layer Normalization

### Residual Connections (Skip Connections)

In each Transformer block, the input is added back to the output of each sublayer:

```
output = sublayer(input) + input
         ↑                 ↑
    (processed)       (original)
```

**Why:** Prevents vanishing gradients during training. With 32+ blocks, gradients need to flow from the last block all the way back to the first. Without residuals, gradients get multiplied by small numbers repeatedly and vanish. Residuals provide a direct path.

**Intuition:** Think of it as the model saying "here's my refined version, but keep the original information too." Information can't get lost — it flows straight through.

### Layer Normalization

Between sublayers, the vectors are normalized to have zero mean and unit variance:

```
Before norm: [234.5, -0.003, 8765, ...]   ← wildly different scales
After norm:  [0.23, -0.001, 0.87, ...]    ← consistent scale
```

**Why:** Keeps the magnitude of vectors consistent throughout 32 blocks. Without this, vectors would grow or shrink uncontrollably.

**Modern variant: RMSNorm** (Root Mean Square Normalization) — simpler and faster than the original LayerNorm. Used by Llama, Phi-3, Mistral. Applied BEFORE each sublayer (Pre-Norm) rather than after (Post-Norm as in the original Transformer).

---

## 16. Glossary

| Term                              | Definition                                                                                         |
| --------------------------------- | -------------------------------------------------------------------------------------------------- |
| **Forward Pass**                  | One complete flow of data through the entire neural network → produces next token prediction       |
| **Autoregressive**                | Generating one token at a time, feeding each output back as input for the next step                |
| **LM Head**                       | Final linear layer that maps model output → probability score for each token                       |
| **Logits**                        | Raw unnormalized scores output by LM Head before softmax                                           |
| **Softmax**                       | Function that converts logits into probabilities summing to 1.0                                    |
| **Decoding Strategy**             | Method for choosing the next token from the probability distribution                               |
| **Greedy Decoding**               | Always pick the highest probability token (deterministic)                                          |
| **Sampling**                      | Pick token randomly based on probability distribution (non-deterministic)                          |
| **Temperature**                   | Controls sharpness of probability distribution — lower = more focused, higher = more random        |
| **Top-p (Nucleus Sampling)**      | Sample only from tokens whose cumulative probability ≤ p                                           |
| **Context Length**                | Maximum number of tokens a model can process in one forward pass                                   |
| **KV Cache**                      | Caching Key and Value matrices from previous tokens to avoid recomputing them                      |
| **Transformer Block**             | One unit of the Transformer stack — contains self-attention + feedforward network                  |
| **Self-Attention**                | Attention mechanism where each token attends to all other tokens in the same sequence              |
| **Query (Q)**                     | Projection of current token — "what am I looking for?"                                             |
| **Key (K)**                       | Projection of all tokens — "what do I contain?"                                                    |
| **Value (V)**                     | Projection of all tokens — "what information do I carry?"                                          |
| **Attention Score**               | Relevance score: how much should the current token attend to each previous token                   |
| **Masked Attention**              | Decoder attention where future tokens are masked — can only attend to past positions               |
| **Multi-Head Attention**          | Running multiple attention operations in parallel, each with its own Q,K,V matrices                |
| **Multi-Query Attention**         | All attention heads share one set of K,V matrices — efficient but lower quality                    |
| **Grouped-Query Attention (GQA)** | Groups of heads share K,V matrices — balance between quality and efficiency                        |
| **Flash Attention**               | Hardware-optimized attention implementation — faster and less memory by reducing GPU data movement |
| **Feedforward Network (FFN/MLP)** | The part of each Transformer block that stores knowledge and does computation                      |
| **Positional Embedding**          | Information added to token vectors to encode their position in the sequence                        |
| **Absolute Positional Embedding** | Fixed position vectors added at the start of the forward pass                                      |
| **RoPE**                          | Rotary Position Embedding — encodes position by rotating Q and K vectors during attention          |
| **Residual Connection**           | Adding the input of a sublayer directly to its output — prevents gradient vanishing                |
| **Layer Normalization**           | Normalizes vector values to consistent scale — applied between sublayers                           |
| **RMSNorm**                       | Simpler and faster variant of Layer Normalization used by modern LLMs                              |
| **Streaming**                     | Sending tokens to the client as they're generated rather than waiting for full response            |

---

## 17. Chapter Summary

### The Full Forward Pass — One Token Generation

```
Input text: "The capital of France is"

1. TOKENIZER
   → [1, 450, 7483, 310, 3444, 338]   (6 token IDs)

2. EMBEDDING LOOKUP
   → 6 vectors of size 3072

3. 32 TRANSFORMER BLOCKS (in sequence)
   Each block:
     a. RMSNorm
     b. Self-Attention (Q×K relevance scoring → weighted sum of V)
     c. + Residual connection
     d. RMSNorm
     e. Feedforward Network (expand to 16384, contract to 3072)
     f. + Residual connection
   Output: still 6 vectors of size 3072 (but now context-aware)

4. FINAL RMNORM

5. LM HEAD
   Last vector [3072] → [32064] probability scores

6. DECODING
   argmax → token ID for "Paris"

7. TOKENIZER DECODE
   → "Paris"

8. APPEND TO INPUT AND REPEAT FROM STEP 1
```

### Key Design Decisions in Modern Transformer LLMs

| Component                | Original (2017)          | Modern (2024)                |
| ------------------------ | ------------------------ | ---------------------------- |
| Attention                | Multi-Head               | Grouped-Query (Llama, Phi-3) |
| Position encoding        | Absolute (fixed/learned) | RoPE (rotary)                |
| Normalization            | Post-LayerNorm           | Pre-RMSNorm                  |
| Activation function      | ReLU                     | SiLU / SwiGLU                |
| Attention implementation | Naive                    | Flash Attention              |

### Three Things That Matter for Your Apps

```
1. TEMPERATURE controls creativity:
   0 = deterministic  |  0.7 = balanced  |  >1.5 = creative/chaotic

2. CONTEXT LENGTH determines memory:
   Everything in the context window costs VRAM (via KV cache)
   Longer context = more memory = slower generation

3. KV CACHE must be enabled (it is by default):
   Without it: 5x slower generation
   With it: only new tokens need computing — previous ones are cached
```

### What's Coming in Chapter 4

We are done with the internals. From Chapter 4 onwards, the book focuses on **applications** — using pre-trained LLMs to solve real-world problems. Chapter 4 starts with **text classification**: given a piece of text, assign it a label (positive/negative, spam/not spam, topic). Both encoder-only (BERT) and decoder-only (GPT) approaches are covered.

---

_Next: [`summary.md`](./summary.md) — the 1-page revision card_
_Practice: [`practice/ch03_practice.ipynb`](./practice/ch03_practice.ipynb) — inspect model internals, measure KV cache_

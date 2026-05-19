# Chapter 3 — Revision Card

> **Use this when:** You come back after days, weeks, or months and need a quick refresh.
> **Reading time:** ~10 minutes

---

## The Story in One Paragraph

LLMs generate text one token at a time in a loop — this is called autoregressive generation. Each iteration is one forward pass through the model's 3 components: tokenizer → stack of Transformer blocks → LM Head. The LM Head converts the final vector into probability scores for every token in the vocabulary, and a decoding strategy picks the next token. Inside each Transformer block, two sublayers work together: the feedforward network stores knowledge and the self-attention layer incorporates context from other tokens using Query/Key/Value matrices. Multiple attention operations run in parallel (multi-head attention), and modern models share K/V matrices across heads (grouped-query attention) for efficiency. The KV cache stores previous tokens' K/V matrices to avoid redundant computation — providing ~5x generation speedup. Modern LLMs also use RoPE for position encoding and RMSNorm instead of LayerNorm.

---

## The Full Forward Pass

```
"The capital of France is"
     ↓ tokenizer.encode()
[token IDs: 1, 450, 7483, ...]
     ↓ embedding matrix lookup
[6 vectors × 3072 dims]
     ↓ × 32 Transformer blocks
     │   each block:
     │   ├── RMSNorm
     │   ├── Self-Attention (Q×K scores → weighted sum of V)
     │   ├── + Residual connection
     │   ├── RMSNorm
     │   ├── Feedforward Network
     │   └── + Residual connection
     ↓
[6 vectors × 3072 dims] (context-aware now)
     ↓ LM Head: Linear(3072 → 32064)
[32,064 probability scores]
     ↓ argmax (greedy) or sample
token_id = "Paris"
     ↓ tokenizer.decode()
"Paris" → appended to input → repeat
```

---

## The 3 Components of a Transformer LLM

```
1. TOKENIZER          text → token IDs
2. TRANSFORMER BLOCKS token vectors → context-aware vectors
3. LM HEAD            final vector → probability over all tokens
```

---

## Self-Attention — Q/K/V in Plain English

```
Q (Query)  = "What am I looking for?"    — current token
K (Key)    = "What do I contain?"        — all previous tokens
V (Value)  = "What info do I carry?"     — all previous tokens

Step 1 — Relevance scoring:
  scores = softmax(Q × Kᵀ / √dim)
  → a score for each previous token: how much should I attend to it?

Step 2 — Combine:
  output = scores × V
  → weighted mix of all previous tokens' information

Result: current token vector now contains context from relevant previous tokens
```

> Example: "it" in "Sarah fed the cat because **it** was hungry"
> → attention to "cat" scores HIGH → "it" vector now contains "cat" information

---

## Decoding Strategies

| Strategy           | How                                 | Result                                 |
| ------------------ | ----------------------------------- | -------------------------------------- |
| Greedy (temp=0)    | Always pick highest prob token      | Deterministic, safe, can be repetitive |
| Sampling           | Random pick based on probs          | Varied, creative                       |
| Low temp (0.1–0.3) | Sharpen distribution → near-greedy  | Focused, factual                       |
| Mid temp (0.7)     | Balanced                            | Good for chat                          |
| High temp (1.5+)   | Flatten distribution → random       | Creative, unpredictable                |
| Top-p              | Sample from top cumulative-p tokens | Prevents very unlikely tokens          |

---

## Multi-Head vs Multi-Query vs Grouped-Query

```
Multi-Head (original):
  Each head → own Q, K, V        → best quality, most memory

Multi-Query:
  All heads → shared K, V        → fastest inference, some quality loss

Grouped-Query (GQA) ⭐ — used by Llama, Mistral, Phi-3:
  Head groups → shared K, V      → balance quality + efficiency
```

---

## KV Cache — Why It Matters

```
Without cache:
  Token 1: compute all 6 input token vectors
  Token 2: recompute all 6 + new token = 7 tokens
  Token 100: recompute 105 tokens every time!
  Result: ~21 seconds for 100 tokens

With cache (default):
  Token 1: compute all 6, SAVE K,V
  Token 2: compute only 1 new token, USE cached K,V
  Token 100: compute only 1 new token, USE cached K,V
  Result: ~4.5 seconds for 100 tokens (5x faster!)

Cost: each token in context = K,V matrices stored in VRAM
→ longer context = more VRAM needed
```

---

## Modern vs Original Transformer

| Feature              | Original (2017) | Modern (2024)         |
| -------------------- | --------------- | --------------------- |
| Attention type       | Multi-Head      | Grouped-Query         |
| Position encoding    | Absolute        | RoPE (rotary)         |
| Normalization timing | Post            | Pre (before sublayer) |
| Norm type            | LayerNorm       | RMSNorm               |
| Activation           | ReLU            | SiLU / SwiGLU         |
| Attention impl       | Naive           | Flash Attention       |

---

## Critical Numbers for Phi-3-mini

```
Vocabulary:         32,064 tokens
Embedding dim:      3,072
Transformer blocks: 32
LM Head output:     32,064 (one score per vocab token)
Context length:     4,096 tokens
```

---

## Practical Settings for Your Apps

```python
generator = pipeline(
    "text-generation",
    model=model,
    tokenizer=tokenizer,
    do_sample=False,        # True = sampling, False = greedy
    temperature=0.7,        # only used if do_sample=True
    top_p=0.9,              # only used if do_sample=True
    max_new_tokens=500,     # response length limit
    use_cache=True,         # ALWAYS keep True for performance
)
```

---

## Self-Check — Answer From Memory

1. What is autoregressive generation? Why does it mean one token at a time?
2. What does the LM Head do? What shape is its input and output for Phi-3?
3. Explain the two steps of self-attention in plain English.
4. What is the KV cache and why does it provide such a large speedup?
5. What is grouped-query attention and which models use it?
6. Why do modern LLMs use RoPE instead of absolute positional embeddings?
7. Your app needs a creative writing assistant. What temperature would you use? What about a factual Q&A bot?

---

_For deep revision → [`notes.md`](./notes.md)_
_For hands-on practice → [`practice/ch03_practice.ipynb`](./practice/ch03_practice.ipynb)_

# Chapter 2 — Revision Card

> **Use this when:** You come back after days, weeks, or months and need a quick refresh.
> **Reading time:** ~10 minutes

---

## The Story in One Paragraph

Before text reaches an LLM, it goes through two conversions: text → token IDs (via tokenizer) → vectors (via embedding matrix). Tokens are not always words — modern LLMs use subword tokenization (BPE or WordPiece) which breaks rare words into known pieces. Each model has its own tokenizer with its own vocabulary, and they can't be swapped. Inside the model, static token embeddings are transformed into contextualized embeddings by Transformer layers — the same word gets different vectors in different contexts. For whole-sentence tasks like semantic search, we use sentence embedding models that pool all token embeddings into one single vector. The word2vec algorithm (skip-gram + negative sampling) showed that embeddings can represent anything that appears in sequences — not just words, but songs, products, and more.

---

## The Pipeline

```
Raw Text
  ↓ tokenizer.encode()
Token IDs: [1, 14350, 385, ...]
  ↓ embedding matrix lookup
Static token vectors: [[0.23, -0.11,...], ...]
  ↓ Transformer layers (self-attention)
Contextualized vectors: [[0.81, 0.34,...], ...]
  ↓ output head → new token ID
  ↓ tokenizer.decode()
Output Text
```

---

## 4 Types of Tokenization

| Type           | Example: "apologizing"  | Handles new words? |
| -------------- | ----------------------- | ------------------ |
| **Word**       | `["apologizing"]`       | ❌ → `[UNK]`       |
| **Subword** ⭐ | `["apolog", "izing"]`   | ✅                 |
| **Character**  | `["a","p","o","l",...]` | ✅                 |
| **Byte**       | raw bytes               | ✅                 |

Subword is dominant. BPE = GPT family. WordPiece = BERT family.

---

## 3 Types of Embeddings

| Type                     | Context-aware? | Shape                   | Use                              |
| ------------------------ | -------------- | ----------------------- | -------------------------------- |
| **Static token**         | ❌             | `[vocab_size, dims]`    | Internal model input             |
| **Contextualized token** | ✅             | `[batch, tokens, dims]` | NER, classification per token    |
| **Sentence/text**        | ✅             | `[dims]` per sentence   | Semantic search, clustering, RAG |

---

## Tokenizer Design Decisions

```
1. Method: BPE vs WordPiece vs SentencePiece
2. Vocabulary size: 30K (BERT) → 100K+ (GPT-4)
3. Special tokens: [CLS], [SEP], [UNK], [MASK], <|user|>, etc.
4. Capitalization: lowercase all (BERT uncased) or preserve (GPT)
5. Training dataset: English text vs code vs multilingual
```

---

## word2vec — The Recipe

```
1. Sliding window over text → generate (center, neighbor) pairs → label: 1
2. Add random non-neighbor pairs → label: 0  (negative sampling)
3. Train model: predict if two words are neighbors
4. Result: similar words → similar vectors

Skip-gram = the sliding window approach
Negative sampling = adding the random negative pairs
```

This same recipe works for songs (playlists), products (carts), movies (sessions).

---

## Key Code Patterns

```python
# Tokenize text → token IDs
from transformers import AutoTokenizer
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
ids = tokenizer("Hello world", return_tensors="pt").input_ids

# Decode a token ID
tokenizer.decode(14350)   # → "Write"

# Contextualized token embeddings
from transformers import AutoModel
model = AutoModel.from_pretrained("microsoft/deberta-v3-xsmall")
output = model(**tokenizer("Hello world", return_tensors="pt"))[0]
# shape: [batch, num_tokens, embedding_dims]

# Sentence embeddings
from sentence_transformers import SentenceTransformer
embed_model = SentenceTransformer("all-MiniLM-L6-v2")
vector = embed_model.encode("Hello world")
# shape: (384,)  ← one vector for the whole sentence

# Word2vec embeddings
import gensim.downloader as api
model = api.load("glove-wiki-gigaword-50")
model.most_similar(["king"], topn=5)
```

---

## Token Pricing Intuition

```
~1 word ≈ 1.3 tokens
~750 words ≈ 1,000 tokens
GPT-4 input: ~$0.03 per 1,000 tokens

Your 500-word prompt ≈ 650 tokens ≈ $0.02 per call
10,000 calls/day ≈ $200/day in input tokens alone
```

Choosing an efficient tokenizer (larger vocab) = fewer tokens per text = lower cost.

---

## Tokenizer Comparison — Quick Cheat Sheet

| Model        | Method    | Vocab | Handles emojis?    | Digit-per-token? |
| ------------ | --------- | ----- | ------------------ | ---------------- |
| BERT uncased | WordPiece | 30K   | ❌ → [UNK]         | No               |
| GPT-2        | BPE       | 50K   | ✅ (byte fallback) | No               |
| GPT-4        | BPE       | 100K+ | ✅                 | No               |
| StarCoder2   | BPE       | 49K   | ✅                 | ✅               |
| Phi-3/Llama  | BPE       | 32K   | ✅                 | ✅               |

---

## Self-Check — Answer From Memory

1. Why can't you swap tokenizers between models?
2. What are the two tokenization methods used by BERT and GPT respectively?
3. What is the difference between a static embedding and a contextualized embedding?
4. You want to build semantic search for your app. Do you need token embeddings or sentence embeddings? Which library do you use?
5. Explain skip-gram and negative sampling in one sentence each.
6. Why does StarCoder2 tokenize each digit separately?

---

_For deep revision → [`notes.md`](./notes.md)_
_For hands-on practice → [`practice/ch02_practice.ipynb`](./practice/ch02_practice.ipynb)_

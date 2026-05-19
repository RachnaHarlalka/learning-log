# Chapter 2 — Tokens and Embeddings

## Elaborate Study Notes

> **Book:** Hands-On Large Language Models — Jay Alammar & Maarten Grootendorst
> **Builds on:** Chapter 1 (Transformers, BERT, GPT, representation vs generative models)
> **Time to read these notes:** ~45–60 minutes

---

## Table of Contents

1. [Why Tokens and Embeddings Matter](#1-why-tokens-and-embeddings-matter)
2. [What Is a Token?](#2-what-is-a-token)
3. [How a Tokenizer Works — Step by Step](#3-how-a-tokenizer-works--step-by-step)
4. [The 4 Types of Tokenization](#4-the-4-types-of-tokenization)
5. [Comparing Real Tokenizers](#5-comparing-real-tokenizers)
6. [Tokenizer Design Choices](#6-tokenizer-design-choices)
7. [Token Embeddings — The Model's Vocabulary Table](#7-token-embeddings--the-models-vocabulary-table)
8. [Contextualized Word Embeddings](#8-contextualized-word-embeddings)
9. [Text Embeddings — Sentences and Documents](#9-text-embeddings--sentences-and-documents)
10. [word2vec — How It Actually Works](#10-word2vec--how-it-actually-works)
11. [Embeddings for Recommendation Systems](#11-embeddings-for-recommendation-systems)
12. [Glossary](#12-glossary)
13. [Chapter Summary](#13-chapter-summary)

---

## 1. Why Tokens and Embeddings Matter

In Chapter 1 we learned that LLMs take text as input and produce text as output. But that description skips over something critical: **computers don't understand text**. They only understand numbers.

So before any text reaches an LLM, it must go through two transformations:

```
Raw Text
    ↓  (Step 1: Tokenizer)
Token IDs  [1, 14350, 385, 4876, ...]
    ↓  (Step 2: Embedding Layer inside model)
Vectors    [[0.23, -0.11, ...], [0.54, 0.72, ...], ...]
    ↓
LLM processes vectors → generates new token IDs → Tokenizer decodes → Output Text
```

**Tokens** are the chunks of text the model reads. **Embeddings** are the numerical vectors that represent those chunks. These two concepts appear in almost every chapter of this book — understanding them deeply now pays off for everything that comes later.

> 💡 **As a fullstack dev:** Every API call you make to OpenAI, Anthropic, or Hugging Face goes through this exact pipeline internally. Tokens are also how **pricing works** — you pay per token, not per character or word. Understanding what counts as a token helps you manage costs.

---

## 2. What Is a Token?

A **token** is the basic unit of text that a language model processes. It is NOT always a word. It can be:

- A complete word: `"Write"` → 1 token
- Part of a word: `"apologizing"` → `"apolog"` + `"izing"` → 2 tokens
- A punctuation mark: `"."` → 1 token
- A special marker: `"<|assistant|>"` → 1 special token
- A whitespace sequence: `"    "` (4 spaces) → 1 token (in GPT-4)

### The Rough Rule of Thumb

| Unit                        | Approximate Token Count |
| --------------------------- | ----------------------- |
| 1 word (English)            | ~1.3 tokens on average  |
| 100 words                   | ~130 tokens             |
| 1 page of text (~500 words) | ~650 tokens             |
| 1 token                     | ~4 characters           |

> 💡 **Pricing example:** GPT-4 charges ~$0.03 per 1,000 input tokens. A 500-word prompt ≈ 650 tokens ≈ $0.02 per call. If your app makes 10,000 calls/day, that's $200/day just in input tokens. This is why understanding tokens matters for cost estimation.

### Why Not Just Use Words?

You might wonder: why not just split on spaces and call each word a token?

Three problems:

**Problem 1: Out-of-vocabulary words**
If a new word appears that wasn't in training (new slang, a new product name, a typo), a word-level tokenizer has no way to handle it. It would just output `[UNK]` (unknown).

**Problem 2: Redundant vocabulary**
Words like `apology`, `apologize`, `apologetic`, `apologist` are all separate entries in a word vocabulary, even though they share the root `apolog`. Subword tokenization handles all variants with just `apolog` + suffix tokens.

**Problem 3: Different languages and scripts**
Some languages (Mandarin, Japanese) don't use spaces. Word-level tokenization completely fails for them.

**The solution: Subword tokenization** — the dominant approach used by virtually all modern LLMs.

---

## 3. How a Tokenizer Works — Step by Step

Let's trace exactly what happens when you send a prompt to a model:

### Step 1: Text → Token IDs (Encoding)

```python
from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")

prompt = "Write an email apologizing to Sarah for the tragic gardening mishap."
input_ids = tokenizer(prompt, return_tensors="pt").input_ids

print(input_ids)
# tensor([[ 1, 14350, 385, 4876, 27746, 5281, 304, 19235, ...]])
```

The tokenizer converts each piece of text to an integer — its **token ID**. This ID is an index into a lookup table (the vocabulary) stored inside the tokenizer.

### Step 2: See What the Tokens Actually Are

```python
for id in input_ids[0]:
    print(tokenizer.decode(id))
```

Output:

```
<s>         ← special "beginning of text" token
Write       ← complete word
an          ← complete word
email       ← complete word
apolog      ← PARTIAL WORD
izing       ← suffix (connected to previous)
to
Sarah
for
the
trag        ← PARTIAL WORD
ic          ← suffix
garden      ← PARTIAL WORD
ing         ← suffix
mishap
.
```

Notice:

- `<s>` is a **special token** marking the start of text
- `apologizing` becomes `apolog` + `izing` (2 tokens)
- `tragic` becomes `trag` + `ic` (2 tokens)
- `gardening` becomes `garden` + `ing` (2 tokens)
- Punctuation is its own token

### Step 3: Model Generates → Token IDs → Decode Back to Text

```python
generation_output = model.generate(input_ids=input_ids, max_new_tokens=20)

# Decode the output token IDs back to text
print(tokenizer.decode(generation_output[0]))
```

The model outputs a tensor of integer token IDs. The tokenizer's `decode()` method converts them back to human-readable text.

**The full pipeline:**

```
"Write an email..."
    → tokenizer.encode() → [1, 14350, 385, 4876, ...]
    → model.generate()   → [1, 14350, ..., 3323, 622, 29901, ...]
    → tokenizer.decode() → "Subject: My Sincere Apologies..."
```

### The Space Convention

One thing that confuses beginners: where do spaces go?

In most modern tokenizers, **spaces are attached to the token that follows them**, not their own separate token. Tokens that DON'T have a space marker are assumed to be connected to the previous token (like suffixes).

```
"apologizing" → ["apolog", "▁izing"]
                            ↑
                    hidden space marker means
                    "I am connected to previous token"
```

---

## 4. The 4 Types of Tokenization

| Type          | How it splits        | Example: "playing"              | Handles new words?       | Used by              |
| ------------- | -------------------- | ------------------------------- | ------------------------ | -------------------- |
| **Word**      | Split on spaces      | `["playing"]`                   | ❌ (unknown word)        | word2vec             |
| **Subword**   | Common subword units | `["play", "ing"]`               | ✅ (falls back to parts) | GPT, BERT, most LLMs |
| **Character** | One char per token   | `["p","l","a","y","i","n","g"]` | ✅ (always works)        | Some older models    |
| **Byte**      | One byte per token   | Raw bytes                       | ✅ (always works)        | ByT5, CANINE         |

### Subword Tokenization — The Sweet Spot

Subword tokenization is the dominant approach because it hits the sweet spot:

- Smaller vocabulary than word-level (no need for every inflection)
- More efficient than character-level (fewer tokens per sentence)
- Handles unknown words by breaking them into known parts
- Works across languages

**Two main algorithms:**

**BPE (Byte Pair Encoding)** — used by GPT-2, GPT-4, Phi-3, Llama:

- Start with individual characters
- Repeatedly merge the most frequent adjacent pair into a new token
- Repeat until vocabulary size is reached

**WordPiece** — used by BERT:

- Similar to BPE but merges based on what maximizes language model likelihood
- Unknown subwords are marked with `##` prefix

> 💡 **For context window efficiency:** Subword tokenization fits roughly 3x more text in the same context window compared to character-level tokenization. A 4,096 token window with subwords ≈ 12,000+ characters ≈ ~2,000+ words.

---

## 5. Comparing Real Tokenizers

The book compares how different tokenizers handle the same test string. Here are the key takeaways:

### Test string:

```
English and CAPITALIZATION
🎵鸟
show_tokens False None elif == >= else: two tabs:"  " Three tabs: "   "
12.0*50=600
```

### Key observations across tokenizers:

**BERT (uncased, 2018) — WordPiece, vocab: 30,522**

- Converts everything to lowercase
- Emojis and Chinese characters → `[UNK]` (completely lost!)
- `capitalization` → `capital` + `##ization`
- No newline tokens — model is blind to line breaks

**BERT (cased, 2018) — WordPiece, vocab: 28,996**

- Preserves capitalization
- `CAPITALIZATION` → 8 tokens (`CA ##PI ##TA ##L ##I ##Z ##AT ##ION`) — very inefficient!
- Emojis and Chinese still → `[UNK]`

**GPT-2 (2019) — BPE, vocab: 50,257**

- Preserves capitalization and newlines
- `CAPITALIZATION` → 4 tokens (more efficient)
- Emojis handled via byte fallback — reconstructable
- Spaces handled token by token

**GPT-4 (2023) — BPE, vocab: 100,000+**

- Much more efficient: `CAPITALIZATION` → 2 tokens
- 4 consecutive spaces → 1 single token (important for Python code indentation!)
- `elif` gets its own dedicated token (code-aware)
- Most efficient at fitting text into context

**StarCoder2 (2024) — BPE, code-focused**

- Each digit gets its own token: `600` → `6`, `0`, `0`
- Hypothesis: better at arithmetic and number reasoning
- Code indentation handled efficiently

**Phi-3 (reuses Llama 2 tokenizer) — BPE, vocab: 32,000**

- Has chat special tokens: `<|user|>`, `<|assistant|>`, `<|system|>`
- Each digit tokenized separately (like StarCoder)

### What This Tells You

Different models have different tokenizers tuned for different purposes. When choosing a model for your app, consider:

- **Multilingual content?** → Use a model with multilingual tokenizer (not old BERT uncased)
- **Code generation?** → Use a code-focused model (GPT-4, StarCoder) with efficient whitespace handling
- **Cost optimization?** → Larger vocabulary = fewer tokens per text = cheaper API calls
- **Emoji/special characters?** → Check if the tokenizer handles them or drops them as `[UNK]`

---

## 6. Tokenizer Design Choices

Three major factors determine how a tokenizer behaves:

### 1. Tokenization Method

The algorithm used: BPE, WordPiece, SentencePiece, Unigram. Each produces different token boundaries for the same text.

### 2. Tokenizer Parameters

**Vocabulary size:** How many unique tokens the tokenizer knows.

- Too small → many rare words get split into many pieces, wasting context
- Too large → rare tokens get little training data, poor quality
- Typical: 30K–100K

**Special tokens:** Tokens with roles beyond representing text:

| Token             | Purpose                     | Example                                             |
| ----------------- | --------------------------- | --------------------------------------------------- |
| `<s>` / `[CLS]`   | Beginning of sequence       | Marks start of input                                |
| `</s>` / `[SEP]`  | End of sequence / separator | Marks end or separates two sequences                |
| `[PAD]`           | Padding                     | Fills unused positions to reach fixed length        |
| `[UNK]`           | Unknown                     | Represents characters the tokenizer can't handle    |
| `[MASK]`          | Masking                     | Used during BERT training (predict the masked word) |
| `<\|endoftext\|>` | End of generation           | GPT models use this to signal they're done          |
| `<\|user\|>` etc. | Chat roles                  | Separate conversation turns                         |

**Capitalization:** Lowercase all text (BERT uncased) or preserve case (GPT, BERT cased)?

### 3. Training Dataset

Even with the same method and parameters, a tokenizer trained on English Wikipedia behaves differently from one trained on code or multilingual text. The algorithm optimizes the vocabulary for whatever dataset it's trained on.

---

## 7. Token Embeddings — The Model's Vocabulary Table

Now we understand how text becomes token IDs. But the model still can't work with integers — it needs vectors. This is where **token embeddings** come in.

### The Embedding Matrix

Every language model contains an **embedding matrix** — a giant lookup table:

```
Embedding Matrix shape: [vocabulary_size × embedding_dimensions]

Example (GPT-2 style):
  - vocabulary_size: 50,257 tokens
  - embedding_dimensions: 768

So the matrix is 50,257 rows × 768 columns
Each row = the embedding vector for one token
```

When a token ID comes in, the model just looks up that row in the matrix to get the token's vector:

```
Token ID: 14350
    ↓ lookup row 14350 in embedding matrix
Token embedding: [0.23, -0.11, 0.88, 0.45, ..., -0.33]  ← 768 numbers
```

### Initialization and Training

Before training, the embedding matrix is initialized with **random values**. During training, these values are updated via backpropagation alongside all other model weights. By the end of training, the embedding values encode the semantic meaning of each token.

When you download a pretrained model, you're downloading this embedding matrix (plus all the other model weights). The embeddings are "baked in" — they represent what the model learned about language during training.

> 💡 **This is why you can't swap tokenizers.** The model's internal embedding matrix has one vector per token in ITS tokenizer's vocabulary. If you use a different tokenizer, the token IDs would map to wrong vectors.

---

## 8. Contextualized Word Embeddings

Here's the limitation of the token embedding matrix above: every token always gets the **same vector**, regardless of context.

```
"I went to the bank to deposit money"  →  "bank" gets embedding[bank_id]
"I sat on the bank of the river"       →  "bank" gets embedding[bank_id]  ← SAME!
```

This is the **static embedding** problem we discussed with word2vec in Chapter 1. The embedding matrix alone doesn't solve it.

**The Transformer layers solve it.** After looking up the static token embedding, the model passes the vectors through multiple layers of self-attention and feedforward networks. This process produces **contextualized embeddings** — representations that change based on surrounding tokens.

```
Input:  "bank" in "river bank context"
    ↓ static embedding lookup
[0.23, -0.11, 0.88, ...]   ← same starting vector for "bank"
    ↓ through Transformer layers (self-attention adjusts based on "river")
[0.54, 0.31, -0.22, ...]   ← DIFFERENT output — now means "riverbank"

Input:  "bank" in "financial bank context"
    ↓ static embedding lookup
[0.23, -0.11, 0.88, ...]   ← same starting vector
    ↓ through Transformer layers (self-attention adjusts based on "money", "deposit")
[-0.11, 0.76, 0.43, ...]   ← DIFFERENT output — now means "financial institution"
```

### Producing Contextualized Embeddings in Code

```python
from transformers import AutoModel, AutoTokenizer

# DeBERTa v3 — excellent at producing contextual token embeddings
tokenizer = AutoTokenizer.from_pretrained("microsoft/deberta-base")
model = AutoModel.from_pretrained("microsoft/deberta-v3-xsmall")

# Tokenize
tokens = tokenizer('Hello world', return_tensors='pt')

# Run through the model — output is contextualized embeddings
output = model(**tokens)[0]

print(output.shape)
# torch.Size([1, 4, 384])
# ↑              ↑   ↑
# batch size   tokens  embedding dimensions
# (1 sentence) (CLS + Hello + world + SEP = 4)
```

The output shape `[1, 4, 384]` means:

- 1 sentence in the batch
- 4 tokens (`[CLS]`, `Hello`, `world`, `[SEP]`)
- Each token represented as a vector of 384 numbers

These 384-dimensional vectors are what the model "thinks" about each token in context. Downstream tasks (classification, NER, etc.) use these vectors as input.

### What Are These Contextualized Embeddings Used For?

| Task                     | What it uses                                                         |
| ------------------------ | -------------------------------------------------------------------- |
| Text classification      | `[CLS]` token embedding → classification head                        |
| Named Entity Recognition | Each token's embedding → label each as PERSON, ORG, etc.             |
| Extractive summarization | Token embeddings → identify most important sentences                 |
| AI image generation      | Text embeddings guide the image generator (DALL-E, Stable Diffusion) |

---

## 9. Text Embeddings — Sentences and Documents

Token embeddings are great for token-level tasks. But many real-world applications need a single vector representing an **entire sentence or document**:

- Semantic search: compare query to thousands of documents
- Clustering: group 10,000 customer reviews by topic
- Classification: classify entire documents

For these, we need **text embeddings** (also called sentence embeddings).

### How Text Embeddings Are Produced

The most common approach: run text through an encoder model, then **pool** the token embeddings into a single vector.

**Mean pooling** — average all token embeddings:

```
tokens:   [CLS]    Hello     World    [SEP]
vectors:  [v1]     [v2]      [v3]     [v4]
                      ↓ average
single vector:    [(v1+v2+v3+v4) / 4]
```

**[CLS] pooling** — just use the [CLS] token's embedding (BERT-style).

### Sentence-Transformers — The Go-To Library

The `sentence-transformers` library wraps embedding models into a clean API:

```python
from sentence_transformers import SentenceTransformer

# Load a high-quality embedding model
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# Encode text → single vector
vector = model.encode("Best movie ever!")

print(vector.shape)
# (768,)  ← one vector of 768 numbers for the entire sentence
```

That's it. One sentence → one vector of 768 numbers. You can then:

- Store this vector in a vector database
- Compare it to other vectors using cosine similarity
- Cluster vectors to find topics
- Use it as a feature for classification

### Choosing an Embedding Model

Different embedding models have different strengths. Common choices:

| Model                             | Dimensions | Good for                            |
| --------------------------------- | ---------- | ----------------------------------- |
| `all-MiniLM-L6-v2`                | 384        | Fast, general purpose, low memory   |
| `all-mpnet-base-v2`               | 768        | Higher quality general purpose      |
| `text-embedding-3-small` (OpenAI) | 1536       | High quality via API, no GPU needed |
| `text-embedding-3-large` (OpenAI) | 3072       | Highest quality via API             |

Chapter 4 covers how to choose an embedding model for your specific task.

---

## 10. word2vec — How It Actually Works

Chapter 1 introduced word2vec at a high level. Chapter 2 goes deeper — and it's worth understanding because the same ideas appear in Chapter 10 (contrastive training) and Chapter 9 (multimodal models).

### The Core Idea

word2vec learns embeddings by training a model to answer one question:

> **"Do these two words tend to appear near each other in text?"**

Output: `1` if yes, `0` if no.

### The Training Process

**Step 1: Sliding window to generate training examples**

Take a sentence: `"Thou shalt not make a machine in the likeness of a human mind"`

Use a window size of 2 (look 2 words left and 2 words right of each center word):

```
Center: "not"
Neighbors: "Thou", "shalt", "make", "a"

Training examples (positive):
  ("not", "Thou")   → label: 1
  ("not", "shalt")  → label: 1
  ("not", "make")   → label: 1
  ("not", "a")      → label: 1
```

**Step 2: Add negative examples (random non-neighbors)**

If you only train on positive pairs, the model will cheat by predicting `1` for everything. You need negative examples too:

```
Negative examples (random words that are NOT neighbors):
  ("not", "pizza")    → label: 0
  ("not", "elephant") → label: 0
  ("not", "running")  → label: 0
```

This technique is called **negative sampling**.

**Step 3: Train the neural network**

The model takes two word embeddings and predicts 0 or 1. Through training:

- Words that frequently co-occur → their vectors are pushed **closer**
- Words that rarely co-occur → their vectors are pushed **farther apart**

After millions of examples, the embeddings capture semantic meaning.

### Two Key Concepts

| Concept               | What it is                                                                                         |
| --------------------- | -------------------------------------------------------------------------------------------------- |
| **Skip-gram**         | The method of selecting center word + context window neighbors to generate positive training pairs |
| **Negative sampling** | Adding random non-neighboring pairs with label 0 to prevent the model from cheating                |

### Why This Matters Beyond word2vec

This "train a model to predict if two things are related" pattern is extremely powerful and appears everywhere:

- **word2vec** → words that appear near each other in text
- **Recommendation systems** (next section) → songs that appear together in playlists
- **Multimodal models (Chapter 9)** → image + caption that belong together
- **Contrastive training (Chapter 10)** → sentences with similar meaning

---

## 11. Embeddings for Recommendation Systems

One of the most practical (and surprising) applications of embeddings. The same word2vec algorithm that learns word meaning can learn the "meaning" of songs, products, movies — anything that appears in sequences.

### The Key Insight

If words in the same sentence = semantically related, then:

- Songs in the same playlist = musically related
- Products in the same shopping cart = frequently bought together
- Movies watched in the same session = similar taste

**Treat songs as words, playlists as sentences** → train word2vec → get song embeddings → find similar songs.

### Building a Song Recommender

```python
from gensim.models import Word2Vec

# playlists is a list of lists — each inner list is a playlist of song IDs
# Think of it as sentences where each "word" is a song ID
# [["song1", "song3", "song7"], ["song2", "song3", "song9"], ...]

model = Word2Vec(
    playlists,
    vector_size=32,   # embedding dimensions for each song
    window=20,        # look 20 songs left/right in playlist
    negative=50,      # 50 negative examples per positive
    min_count=1,      # include songs that appear at least once
    workers=4         # parallel training
)

# Find songs similar to "Billie Jean" by Michael Jackson (ID: 3822)
model.wv.most_similar(positive="3822", topn=5)
# Returns: Prince, Madonna, other Michael Jackson songs
```

The model learned that songs frequently appearing in the same playlists are musically similar — without any musical features, just co-occurrence patterns.

### Why This Is Relevant to You as a Dev

Recommendation systems are one of the most valuable features in any product:

- "Users who bought this also bought..."
- "You might also like..."
- "Similar articles..."

Many companies build these using this exact technique — embedding items (products, articles, songs) based on co-occurrence in user sessions and finding nearest neighbors.

---

## 12. Glossary

| Term                         | Definition                                                                                 |
| ---------------------------- | ------------------------------------------------------------------------------------------ |
| **Token**                    | The basic unit of text a model processes — a word, subword, character, or special marker   |
| **Token ID**                 | An integer that maps to a specific token in the tokenizer's vocabulary                     |
| **Tokenizer**                | Converts text → token IDs (encoding) and token IDs → text (decoding)                       |
| **Vocabulary**               | The complete set of tokens a tokenizer knows — typically 30K–100K tokens                   |
| **Subword Tokenization**     | Splitting text into frequent word pieces — the dominant LLM approach                       |
| **BPE (Byte Pair Encoding)** | Tokenization algorithm that merges most frequent character pairs iteratively               |
| **WordPiece**                | BERT's tokenization algorithm — similar to BPE but merges to maximize likelihood           |
| **SentencePiece**            | Tokenization library that supports BPE and Unigram, language-agnostic                      |
| **Special Tokens**           | Tokens with functional roles: `[CLS]`, `[SEP]`, `[UNK]`, `<s>`, `</s>`, `[MASK]`           |
| **[CLS] Token**              | Beginning-of-sequence token in BERT — its embedding represents the whole input             |
| **[SEP] Token**              | Separator token — separates two text sequences in BERT                                     |
| **[UNK] Token**              | Unknown token — replaces characters/words the tokenizer can't handle                       |
| **[MASK] Token**             | Used during BERT training to mask tokens for the model to predict                          |
| **Embedding Matrix**         | The lookup table inside a model — one vector per vocabulary token                          |
| **Static Embedding**         | A fixed vector per word regardless of context (word2vec)                                   |
| **Contextualized Embedding** | A dynamic vector that changes based on surrounding tokens (BERT, GPT)                      |
| **Text Embedding**           | A single vector representing an entire sentence or document                                |
| **Sentence Embedding**       | A text embedding for a sentence — enables semantic search                                  |
| **Mean Pooling**             | Averaging all token embeddings to produce a single text embedding                          |
| **word2vec**                 | 2013 algorithm that learns semantic word embeddings from co-occurrence                     |
| **Skip-gram**                | word2vec method: use center word to predict context window neighbors                       |
| **Negative Sampling**        | Adding random non-neighbor pairs as negative training examples                             |
| **Contrastive Training**     | Training by comparing positive pairs vs negative pairs — used in word2vec and beyond       |
| **sentence-transformers**    | Python library for producing high-quality text/sentence embeddings                         |
| **Gensim**                   | Python library for word2vec and other word embedding models                                |
| **Cosine Similarity**        | Distance metric for comparing embeddings — 1.0 = identical, 0.0 = unrelated                |
| **Vector Database**          | Database optimized for storing and querying embeddings (e.g. Pinecone, Weaviate, pgvector) |

---

## 13. Chapter Summary

### The Full Pipeline — Text to Model Input

```
"Write an email apologizing..."
         ↓
    TOKENIZER (encode)
         ↓
[1, 14350, 385, 4876, 27746, ...]    ← Token IDs (integers)
         ↓
    EMBEDDING MATRIX LOOKUP
         ↓
[[0.23, -0.11, ...],                 ← Static token embeddings
 [0.54, 0.72, ...],                     (one vector per token)
 ...]
         ↓
    TRANSFORMER LAYERS (self-attention + feedforward)
         ↓
[[0.81, 0.34, ...],                  ← Contextualized embeddings
 [-0.12, 0.91, ...],                    (now context-aware)
 ...]
         ↓
    OUTPUT HEAD (generates next token ID)
         ↓
    TOKENIZER (decode)
         ↓
"Subject: My Sincere Apologies..."
```

### The Three Types of Embeddings — Quick Reference

```
STATIC TOKEN EMBEDDINGS
  Source:   Embedding matrix (lookup table inside model)
  Context:  ❌ No — same vector for "bank" regardless of context
  Use:      Internal model representation (first step inside model)

CONTEXTUALIZED TOKEN EMBEDDINGS
  Source:   Output of Transformer layers
  Context:  ✅ Yes — "bank" means different things in different sentences
  Use:      NER, extractive summarization, classification at token level

TEXT/SENTENCE EMBEDDINGS
  Source:   Embedding models (BERT + pooling, sentence-transformers)
  Context:  ✅ Yes — entire sentence is one vector
  Use:      Semantic search, clustering, classification at sentence/doc level
```

### The word2vec Recipe (Applies to Much More Than Words)

```
1. Treat items as "words" (songs, products, articles)
2. Treat co-occurrence sequences as "sentences" (playlists, carts, sessions)
3. Generate positive pairs (items that co-occur) + negative pairs (random)
4. Train model to predict: are these two items related? (0 or 1)
5. The learned embeddings capture semantic/behavioral similarity
6. Find similar items using cosine similarity on their embeddings
```

### What You Should Now Understand

After studying this chapter, you should be able to explain:

- [ ] Why tokens are not always words, and what subword tokenization solves
- [ ] The difference between BPE and WordPiece
- [ ] What token IDs are and how to encode/decode them in code
- [ ] Why different models have different tokenizers and why they can't be swapped
- [ ] The difference between static, contextualized, and sentence embeddings
- [ ] How word2vec training works (skip-gram + negative sampling)
- [ ] How the same embedding idea applies to recommendation systems

### What's Coming in Chapter 3

Chapter 3 goes inside the Transformer model itself:

- What happens inside each Transformer layer?
- How does multi-head attention work in detail?
- What are positional embeddings and why do Transformers need them?
- How does the model actually generate the next token?

---

_Next: [`summary.md`](./summary.md) — the 1-page revision card_
_Practice: [`practice/ch02_practice.ipynb`](./practice/ch02_practice.ipynb) — hands-on exercises_

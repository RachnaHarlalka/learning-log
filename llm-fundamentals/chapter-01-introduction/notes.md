# Chapter 1 — An Introduction to Large Language Models

## Elaborate Study Notes

> **Book:** Hands-On Large Language Models — Jay Alammar & Maarten Grootendorst
> **Branch:** `llm-fundamentals`
> **Prerequisite:** None — this is the starting point
> **Time to read these notes:** ~45–60 minutes

---

## Table of Contents

1. [What Is Language AI?](#1-what-is-language-ai)
2. [Representing Language as Bag-of-Words](#2-representing-language-as-bag-of-words)
3. [Better Representations — Dense Vector Embeddings](#3-better-representations--dense-vector-embeddings)
4. [Types of Embeddings](#4-types-of-embeddings)
5. [Encoding Context with RNNs and Attention](#5-encoding-context-with-rnns-and-attention)
6. [The Transformer — Attention Is All You Need](#6-the-transformer--attention-is-all-you-need)
7. [Representation Models — BERT (Encoder-Only)](#7-representation-models--bert-encoder-only)
8. [Generative Models — GPT (Decoder-Only)](#8-generative-models--gpt-decoder-only)
9. [The Year of Generative AI](#9-the-year-of-generative-ai)
10. [The Moving Definition of LLM](#10-the-moving-definition-of-llm)
11. [How LLMs Are Trained](#11-how-llms-are-trained)
12. [What Can LLMs Do?](#12-what-can-llms-do)
13. [Responsible LLM Development](#13-responsible-llm-development)
14. [Hardware — GPUs and VRAM](#14-hardware--gpus-and-vram)
15. [Interfacing with LLMs](#15-interfacing-with-llms)
16. [Generating Your First Text — Code Walkthrough](#16-generating-your-first-text--code-walkthrough)
17. [Glossary](#17-glossary)
18. [Chapter Summary](#18-chapter-summary)

---

## 1. What Is Language AI?

### Artificial Intelligence — The Broad Term

**AI** is the science and engineering of making machines behave intelligently. The term is intentionally broad — it includes everything from simple if-else logic in NPC game characters all the way to ChatGPT. Not everything marketed as "AI" is genuinely intelligent.

### Language AI — The Subfield We Care About

**Language AI** (also called **NLP — Natural Language Processing**) is the subfield of AI specifically focused on:

- Understanding human language
- Processing human language
- Generating human language

Every time you use a chatbot, a grammar checker, a translation tool, or a search engine that understands _meaning_ — that's Language AI.

> 💡 **Why this matters for you as a fullstack dev:**
> When you call the OpenAI API, the Anthropic API, or use Hugging Face models in your app, you are building on top of Language AI. This entire book teaches you how that foundation works so you can use it more effectively and make smarter architectural decisions.

### Language AI vs NLP

The book uses "Language AI" rather than NLP deliberately — NLP traditionally referred to rule-based or statistical systems, while Language AI includes the newer deep learning approaches that have largely replaced them. For practical purposes, treat them as interchangeable.

---

## 2. Representing Language as Bag-of-Words

### The Core Problem

Computers only understand numbers. Text is unstructured — a string of characters with no inherent numerical meaning. The entire history of Language AI is essentially the history of finding better and better ways to convert text into numbers that preserve meaning.

**Bag-of-Words (BoW)** was one of the first serious attempts at this. It originated in the 1950s but became widely used in the 2000s.

### How It Works — Step by Step

**Step 1: Tokenization** — Split text into individual words (tokens)

```
"I love machine learning"  →  ["I", "love", "machine", "learning"]
"I love deep learning"     →  ["I", "love", "deep", "learning"]
```

**Step 2: Build a Vocabulary** — Collect all unique words across all sentences

```
Vocabulary: ["I", "love", "machine", "learning", "deep"]
              idx:  0      1         2             3         4
```

**Step 3: Count occurrences** — For each sentence, count how many times each vocab word appears

```
"I love machine learning" → [1, 1, 1, 1, 0]
"I love deep learning"    → [1, 1, 0, 1, 1]
```

These lists of numbers are called **vectors** or **vector representations**. The book calls models that produce these kinds of representations **Representation Models**.

### What BoW Gets Right

- Simple and fast to compute
- Gives you a numerical representation of any text
- Still useful today (Chapter 5 uses it for topic modeling)

### What BoW Gets Wrong — Critical Limitations

**Problem 1: Ignores word order and meaning**

```
"The dog bit the man"  → [1, 1, 1, 1, 1]
"The man bit the dog"  → [1, 1, 1, 1, 1]  ← IDENTICAL vectors!
```

These mean completely opposite things but produce the same vector. BoW is literally a _bag_ — order is thrown out, just counting.

**Problem 2: Ignores semantic meaning**

```
"car" and "automobile" → very different vectors (different words)
```

Even though they mean the same thing, BoW treats them as completely unrelated because they are different strings.

**Problem 3: Sparse and high-dimensional**

With a vocabulary of 50,000 words, every sentence becomes a vector of 50,000 numbers — almost all zeros. This is wasteful and hard to work with.

> 💡 **Developer analogy:** BoW is like searching a database with `WHERE content LIKE '%keyword%'` — fast, but it misses synonyms, context, and meaning entirely. What we eventually want is semantic search — searching by _meaning_, not exact words.

---

## 3. Better Representations — Dense Vector Embeddings

### The Motivation

BoW ignores meaning. We need representations where:

- "car" and "automobile" are close to each other
- "king" and "queen" are related
- "bank" means something different in "river bank" vs "investment bank"

This is exactly what **word2vec** (2013, Google) achieved.

### What Are Embeddings?

An **embedding** is a vector representation of data that attempts to capture its _meaning_ — not just its surface form.

Instead of a sparse 50,000-number vector (mostly zeros), embeddings are:

- **Dense** — every dimension has a meaningful value
- **Fixed size** — typically 50 to 768 numbers per word
- **Semantically meaningful** — similar meanings = similar vectors

```
# Conceptual example (oversimplified)
"apple"  → [0.23, -0.11, 0.88, 0.45, ...]  # 300 numbers
"banana" → [0.21, -0.09, 0.85, 0.41, ...]  # very similar to apple!
"car"    → [-0.54, 0.72, -0.33, 0.12, ...]  # very different
```

### How word2vec Learns Embeddings

word2vec uses a **neural network** trained with a clever trick: predict whether two words are likely to appear near each other in a sentence.

**Training process:**

1. Start every word in the vocabulary with a random vector (say, 300 random numbers)
2. Go through massive amounts of text (e.g. all of Wikipedia)
3. For each pair of words that appear near each other: nudge their vectors slightly closer
4. For each pair that don't appear near each other: nudge their vectors slightly apart
5. After millions of iterations: words with similar meanings end up with similar vectors

**Why does this work?**

Words that appear in similar contexts tend to mean similar things. "Doctor" and "physician" both tend to appear near words like "hospital", "patient", "medicine". Over training, their vectors become similar.

### Neural Networks — A Quick Primer

word2vec uses a **neural network** — a system of interconnected layers of nodes where each connection has a numerical **weight** (also called a **parameter**).

```
Input layer → Hidden layer(s) → Output layer
```

- The network processes an input (e.g. a word) and produces an output (e.g. a probability)
- During training, the weights are adjusted to minimize the error between predicted and actual output
- All those weights together are what we call the **parameters** of the model

> 💡 When you hear "GPT-3 has 175 billion parameters" — that means 175 billion numerical weights inside its neural network. More parameters = more capacity to learn patterns from data.

### The Famous word2vec Math

```
king - man + woman ≈ queen
```

This works because the embedding captures relational meaning. The vector difference between "king" and "man" represents "royalty offset from maleness." Add that to "woman" and you get close to "queen." This is not magic — it's a natural result of how the embeddings are trained on context.

### Critical Limitation of word2vec

word2vec creates **static** embeddings — each word always gets the same vector regardless of context.

```
"I went to the bank to deposit money"  →  "bank" gets vector_bank
"I sat on the bank of the river"       →  "bank" gets vector_bank  ← SAME!
```

The word "bank" has the same embedding in both sentences even though it means completely different things. This was the next problem to solve.

---

## 4. Types of Embeddings

Embeddings exist at different levels of granularity:

| Type                    | What it represents | Example models                      |
| ----------------------- | ------------------ | ----------------------------------- |
| **Word embeddings**     | A single word      | word2vec, GloVe                     |
| **Token embeddings**    | A subword token    | Used internally by all transformers |
| **Sentence embeddings** | An entire sentence | Sentence-BERT, all-MiniLM           |
| **Document embeddings** | An entire document | Bag-of-words (crudely), Doc2Vec     |

Throughout this book, embeddings are central — they appear in:

- **Chapter 4** — Classification (embed text, classify by embedding)
- **Chapter 5** — Clustering (group embeddings by similarity)
- **Chapter 6** — Semantic search (find similar embeddings)
- **Chapter 8** — RAG (retrieve relevant document embeddings at query time)

> 💡 **Practical insight:** When you build a semantic search feature or a "find similar items" feature in your app, you're working with embeddings under the hood. Understanding what an embedding IS helps you debug and improve those features intelligently.

---

## 5. Encoding Context with RNNs and Attention

### The Problem word2vec Couldn't Solve

We need context-aware representations. "Bank" should mean different things in different sentences. To achieve this, we need a model that reads the _entire sentence_ before deciding what each word means.

### Recurrent Neural Networks (RNNs)

**RNNs** are neural networks designed to process _sequences_ — they read text word by word and maintain a "memory" of what they've read so far.

RNNs were used for **encoder-decoder** tasks like translation:

```
Encoder RNN: reads "I love llamas" word by word → produces a context embedding
Decoder RNN: takes the context embedding → generates "Ik hou van lama's" word by word
```

This process is **autoregressive** — each generated word depends on all previously generated words.

### The Bottleneck Problem

The encoder compresses the entire input sentence into a single fixed-size context embedding. For short sentences this works. For long sentences, you're trying to squeeze everything into one vector — information is lost.

Imagine reading a 10-page document and then having to summarize the _entire thing_ in a single sentence before you're allowed to answer any questions. You'd lose crucial details.

### The Attention Mechanism (2014)

**Attention** was introduced to solve the bottleneck problem. Instead of compressing everything into one vector, attention lets the decoder _look back_ at all of the encoder's intermediate states and decide which parts of the input are most relevant at each generation step.

**Conceptual example — translating "I love llamas" to Dutch:**

When generating the Dutch word "lama's" (= llamas):

- Attention to "llamas" → HIGH (directly related)
- Attention to "love" → MEDIUM (somewhat related)
- Attention to "I" → LOW (not very relevant here)

The model dynamically focuses on the most relevant words at each generation step.

> 💡 **Developer analogy:** Attention is like a dynamic weighted query. Instead of pre-computing static relationships, at each step the model asks "which parts of the input are most relevant to what I'm generating right now?" and weights them accordingly.

### Why RNNs + Attention Still Had a Problem

Even with attention, RNNs processed tokens **sequentially** — one at a time. This meant:

- Training couldn't be parallelized across a GPU
- Long sequences were slow to train
- Learning signals degraded over long distances

This brought us to the biggest breakthrough in Language AI history.

---

## 6. The Transformer — Attention Is All You Need

### The Breakthrough Paper (2017)

A Google Brain paper titled _"Attention Is All You Need"_ proposed removing the RNN entirely and building a model using **only attention mechanisms**.

This was revolutionary for two reasons:

1. **Parallelization** — without sequential RNN dependencies, the entire sequence can be processed at once on a GPU → dramatically faster training
2. **Better long-range understanding** — attention directly connects any two tokens regardless of distance

The architecture they proposed is called the **Transformer** and it is the foundation of virtually every modern LLM.

### Transformer Architecture Overview

The Transformer has two main components:

```
Input Text
    ↓
[Encoder Stack]   ← multiple encoder blocks stacked on top of each other
    ↓
[Decoder Stack]   ← multiple decoder blocks stacked on top of each other
    ↓
Output Text
```

**Encoder Block** (understanding side):

- **Self-Attention layer** — each token looks at all other tokens in the input and updates its representation based on what's relevant
- **Feedforward Neural Network** — processes each token's updated representation

**Decoder Block** (generation side):

- **Masked Self-Attention** — like encoder self-attention, but each token can only attend to tokens that came BEFORE it (can't look into the future — that would be cheating during training)
- **Cross-Attention** — attends to the encoder's output to find relevant parts of the input
- **Feedforward Neural Network**

### Self-Attention — The Core Innovation

**Self-attention** allows each token to look at ALL other tokens in the same sequence simultaneously — not one at a time like RNNs.

```
Sentence: "The bank by the river was steep"

When processing "bank":
  - attends to "river"  → HIGH (changes meaning of bank)
  - attends to "steep"  → MEDIUM
  - attends to "The"    → LOW
  Result: "bank" now has a context-aware representation meaning RIVERBANK
```

This is how the Transformer solves the word2vec static embedding problem — the same word gets different representations depending on surrounding context.

### Masked Self-Attention in the Decoder

The decoder generates text one token at a time. When generating token N, it must NOT be allowed to "see" tokens N+1, N+2, etc. (that would be cheating — the answer would already be there). So the decoder uses **masking** — it zeroes out attention scores for future positions.

```
Generating: "Ik hou van lama's"
When generating "van" (position 3):
  - Can attend to: "Ik" (pos 1), "hou" (pos 2)
  - Cannot attend to: "lama's" (pos 4) ← masked out
```

### What Changed After Transformers

After the 2017 paper, the entire field pivoted. Two powerful specializations emerged:

- **Encoder-only Transformers** → BERT (2018) — optimized for understanding text
- **Decoder-only Transformers** → GPT (2018) — optimized for generating text

---

## 7. Representation Models — BERT (Encoder-Only)

### What Is BERT?

**BERT** = Bidirectional Encoder Representations from Transformers (Google, 2018)

BERT takes the encoder part of the Transformer and removes the decoder entirely. It stacks multiple encoder blocks and trains the whole thing to deeply understand language.

"**Bidirectional**" is key — unlike RNNs which read left-to-right, BERT's self-attention looks at the entire sequence in both directions simultaneously. This gives it much richer contextual understanding.

### How BERT Is Trained — Masked Language Modeling

BERT uses a clever self-supervised training trick called **Masked Language Modeling (MLM)**:

1. Take a sentence: `"The cat sat on the mat"`
2. Randomly mask some tokens: `"The cat [MASK] on the [MASK]"`
3. Train BERT to predict the masked words
4. The model must use surrounding context from both directions to predict correctly

This forces BERT to deeply understand the relationships between all words in a sentence.

### The [CLS] Token

BERT adds a special `[CLS]` (classification) token at the beginning of every input. After processing, this token's embedding represents the _entire sentence_. This is commonly used as input to a classification layer on top of BERT.

```
Input:  [CLS] The movie was great [SEP]
Output: A rich vector for [CLS] that represents the whole sentence
        → use this vector to classify as positive/negative
```

### Transfer Learning with BERT

BERT introduced **transfer learning** to NLP:

```
Step 1: Pre-train BERT on massive data (Wikipedia, BookCorpus)
              ↓ BERT learns general language understanding
Step 2: Fine-tune on your specific task (e.g. sentiment classification)
              ↓ BERT adapts to your domain with much less data
```

This is powerful because Step 1 is done once (by Google, expensively). You take the pre-trained weights and adapt them for your specific task with much less compute and data.

### When to Use BERT-style Models

Use representation models when you need to **understand** text:

- Text classification (sentiment, spam, topic detection)
- Named entity recognition (find person names, locations in text)
- Semantic search (find documents similar in meaning)
- Text clustering (group similar documents)
- Feature extraction (convert text into vectors for downstream tasks)

---

## 8. Generative Models — GPT (Decoder-Only)

### What Is GPT?

**GPT** = Generative Pre-trained Transformer (OpenAI, 2018)

GPT takes the decoder part of the Transformer and removes the encoder entirely. It stacks multiple decoder blocks and trains the whole thing to predict the next word.

### How GPT Is Trained — Next Token Prediction

GPT's training objective is simple: given all previous words, predict the next one.

```
Input:  "The quick brown fox"
Target: "jumps"

Input:  "The quick brown fox jumps"
Target: "over"
```

This seems almost too simple, but training on trillions of words forces the model to learn grammar, facts, reasoning, coding patterns, and much more — all from predicting the next token.

### Base Models vs Instruct/Chat Models

A base GPT model is a **completion machine** — give it text, it completes it. Useful but not intuitive for most people.

To make models like ChatGPT, the base model is further fine-tuned using techniques like **RLHF (Reinforcement Learning from Human Feedback)** to create **instruct models** that follow instructions and answer questions coherently.

```
Base model:     "The weather today is" → "sunny with a high of 72 degrees..."
Instruct model: "What is the weather?" → "I don't have access to real-time data, but..."
```

### Context Window — A Critical Concept

The **context window** (or context length) is the maximum number of tokens a model can process in a single request. Everything you send — system prompt, conversation history, user message — must fit within this window.

```
Context window = 4,096 tokens (~3,000 words)

Your full request: [system prompt] + [history] + [user message] + [model response]
                   ALL of this must fit within 4,096 tokens
```

Modern models have much larger windows:

- GPT-4: up to 128K tokens
- Claude 3.5: up to 200K tokens
- Gemini 1.5 Pro: up to 1M tokens

> 💡 **This matters when you build apps.** If you're building a chatbot, you can't just keep appending messages forever — you'll hit the context window limit. You need a strategy: summarize old messages, use RAG instead of stuffing documents, or selectively prune history.

### The Scale Race — Parameters Matter

More parameters = more capacity to learn patterns (up to a point):

| Model      | Parameters              | Year |
| ---------- | ----------------------- | ---- |
| GPT-1      | 117 million             | 2018 |
| GPT-2      | 1.5 billion             | 2019 |
| GPT-3      | 175 billion             | 2020 |
| GPT-4      | ~1 trillion (estimated) | 2023 |
| Phi-3-mini | 3.8 billion             | 2024 |

Note: Phi-3-mini has only 3.8B parameters but performs surprisingly well — proving that training data quality and techniques matter as much as raw parameter count.

### When to Use GPT-style Models

Use generative models when you need to **generate** text:

- Chatbots and conversational AI
- Text summarization
- Code generation
- Document drafting
- Question answering
- Creative writing

---

## 9. The Year of Generative AI

### ChatGPT's Impact

ChatGPT launched in November 2022 and hit:

- 1 million users in 5 days
- 100 million users in 2 months (fastest product to 100M users ever, at the time)

It didn't introduce fundamentally new technology — GPT-3 had been available via API since 2020. The difference was the **chat interface** and **instruction fine-tuning** that made the underlying power accessible to everyone, not just developers.

### The Model Explosion (2023)

2023 saw a flood of competing models released at unprecedented pace:

| Company    | Model(s)                 |
| ---------- | ------------------------ |
| OpenAI     | GPT-4, GPT-4 Turbo       |
| Meta       | Llama 2 (open weights)   |
| Mistral AI | Mistral 7B, Mixtral 8x7B |
| Google     | PaLM 2, Gemini           |
| Anthropic  | Claude 2                 |
| Microsoft  | Phi-1, Phi-2             |
| Cohere     | Command R                |

Alongside Transformers, new architectures emerged (Mamba, RWKV) that attempt to achieve similar performance with better efficiency — but Transformers remain dominant.

---

## 10. The Moving Definition of LLM

The term "Large Language Model" is fuzzy and evolving. The book deliberately broadens it:

> **For this book, LLMs include BOTH generative AND representation models — regardless of size — that understand or generate human language.**

Why? Because a highly capable 1B parameter model shouldn't be excluded just because it isn't "large" by today's standards. What matters is capability, not size label.

| What people usually mean by LLM       | What the book means by LLM            |
| ------------------------------------- | ------------------------------------- |
| Big generative models (GPT-4, Claude) | All capable language models           |
| Decoder-only (text generation)        | Both encoder-only AND decoder-only    |
| Billions of parameters                | Any size — capability is what matters |

---

## 11. How LLMs Are Trained

### Traditional ML vs LLM Training

**Traditional ML** (one step):

```
Labeled data → Train model for specific task → Done
Example: 10,000 labeled images → train image classifier → ship it
```

**LLM Training** (two steps):

```
Step 1: PRE-TRAINING
  - Input: massive unlabeled text data (trillions of tokens from the internet)
  - Task: predict next token (GPT) or predict masked tokens (BERT)
  - Duration: weeks to months on thousands of GPUs
  - Cost: millions of dollars (Llama 2 cost ~$5 million)
  - Result: Foundation Model / Base Model
            (deep language understanding, but doesn't follow instructions yet)

Step 2: FINE-TUNING
  - Input: smaller, curated, task-specific dataset
  - Task: adapt the model to specific behavior or domain
  - Duration: hours to days
  - Cost: much cheaper than pre-training
  - Result: Task-specific model (follows instructions, classifies, etc.)
```

### What This Means For You As a Developer

You will almost never do Step 1. As a fullstack dev you will:

- Use pre-trained models directly via API (OpenAI, Anthropic, Cohere, etc.)
- Use pre-trained open models from Hugging Face
- Occasionally fine-tune a pre-trained model for your specific use case (Chapters 11 & 12)

The expensive pre-training work is done for you. Your job is to leverage these models effectively in your applications.

### Foundation Models

A **foundation model** (also called base model) is the result of pre-training. It's a general-purpose model that has not been specialized yet. Think of it as an incredibly well-read person who knows a vast amount about language and the world, but hasn't been trained for any specific job yet.

Fine-tuning is like giving that person on-the-job training for a specific role.

---

## 12. What Can LLMs Do?

Here are the key use cases with practical context added for fullstack developers:

### Text Classification

Assign a category label to a piece of text.

- Is this review positive or negative? (sentiment analysis)
- Is this email spam?
- What category does this support ticket belong to?

**Both encoder-only and decoder-only models** can do this. Covered in Chapter 4.

**Your app:** Add sentiment tagging to user reviews. Auto-route support tickets. Flag potentially harmful content before it's posted.

---

### Text Clustering and Topic Modeling

Group similar texts together without predefined labels — fully unsupervised.

- Discover common themes across 10,000 customer feedback responses
- Find what topics a large document collection covers
- Group similar user queries to build a smarter FAQ

**Encoder-only models** produce embeddings → clustering algorithms group them. Covered in Chapter 5.

**Your app:** Analyze user feedback at scale without manually reading everything. Surface patterns in logs or support tickets automatically.

---

### Semantic Search and RAG

Find documents by meaning (not just keyword matching). RAG lets LLMs answer questions grounded in your own documents.

- "Show me articles about account recovery" finds docs titled "password reset guide"
- An AI assistant that answers questions about your product docs
- Legal document retrieval by concept, not exact phrasing

Covered in Chapters 6 and 8. **This is arguably the highest-value LLM skill for a fullstack dev.**

**Your app:** Replace your `LIKE '%keyword%'` search with semantic search. Build a docs-aware chatbot. Create a knowledge base assistant.

---

### LLM Chatbots with Tools and Documents

Combine prompt engineering + RAG + tool use to build a capable AI assistant.

- Customer support bot that knows your product
- Code assistant that understands your codebase
- Research assistant that reads and reasons about PDFs

Covered across Chapters 6, 7, 8, and 12.

---

### Multimodal Tasks

LLMs that process images alongside text.

- "What's in this image?"
- Extract structured data from screenshots or invoices
- Generate alt text for images automatically
- Describe product photos for e-commerce

Covered in Chapter 9.

**Your app:** Image-to-text pipelines, accessibility tooling, document processing automation.

---

## 13. Responsible LLM Development

These are not just ethical talking points — they are real engineering concerns you will face building production applications:

### Bias and Fairness

LLMs are trained on internet data which contains societal biases. Models can reproduce and amplify these biases in their outputs.

**As a builder:** Test your application with diverse inputs before shipping. Don't assume the model is neutral. Add content moderation layers for sensitive use cases. Be especially careful with hiring, lending, or medical applications.

### Hallucination

LLMs confidently generate incorrect information. This is called **hallucination**. The model doesn't know what it doesn't know — it will fabricate facts rather than admit uncertainty.

**As a builder:** Never use an LLM as the sole source of truth for critical information. Always add verification layers. RAG helps (you ground the model in real documents) but doesn't eliminate hallucination entirely. For high-stakes outputs, always have human review.

### Transparency and Accountability

Users may not know they are interacting with AI. Regulations in some regions require disclosure. AI outputs in high-stakes domains (medical, legal, financial) may carry liability.

**As a builder:** Be transparent about AI involvement. Build human oversight into high-stakes decision flows. Keep audit logs of AI decisions.

### Intellectual Property

If an LLM's output closely resembles its training data, copyright issues may arise. The law here is actively evolving and varies by jurisdiction.

**As a builder:** Understand the license of the models you use. Be cautious about using AI-generated content commercially in creative domains without legal review.

### Regulation — EU AI Act

The EU AI Act (2024) classifies AI systems by risk level and imposes obligations. Foundation models are regulated as "General Purpose AI." High-risk use cases (medical, legal, hiring, credit scoring) face strict requirements.

**As a builder:** If your product is used in the EU, understand how the Act applies to your specific use case. Plan for compliance from the beginning — retrofitting is painful.

---

## 14. Hardware — GPUs and VRAM

### Why GPUs Matter

LLMs require massive parallel computation — exactly what GPUs are designed for. The key hardware constraint when running LLMs locally is **VRAM** (the memory on your GPU).

You need enough VRAM to load the entire model into GPU memory at once. If a model doesn't fit, it can't run at full speed (or at all).

### Rough VRAM Guidelines

| Model Size        | Approx. VRAM needed (fp16) | Approx. VRAM (quantized 4-bit) |
| ----------------- | -------------------------- | ------------------------------ |
| 3.8B (Phi-3-mini) | ~8 GB                      | ~2-3 GB                        |
| 7B                | ~14 GB                     | ~4-5 GB                        |
| 13B               | ~26 GB                     | ~7-8 GB                        |
| 70B               | ~140 GB                    | ~35-40 GB                      |

**Quantization** = compressing model weights to lower precision (e.g. 16-bit → 4-bit) to reduce VRAM requirements with a small performance tradeoff. Covered in Chapters 7 & 12.

### The GPU-Poor Reality

Pre-training Llama 2 cost Meta roughly $5 million in GPU compute. You won't be doing that.

For this book, everything runs on:

- **Google Colab free tier** (T4 GPU, 16 GB VRAM) ← recommended for all hands-on work
- Any consumer GPU with ≥ 8 GB VRAM

> 💡 As a fullstack dev, you'll mostly use cloud APIs (zero GPU overhead) or small open models on Colab/hosted inference. You do NOT need a powerful GPU to build excellent AI-powered apps.

---

## 15. Interfacing with LLMs

### Option A: Proprietary APIs (Closed Source)

Models where weights and architecture are kept secret, accessed only via API.

**Examples:** OpenAI GPT-4, Anthropic Claude, Google Gemini, Cohere Command R

```python
# Standard OpenAI API pattern
from openai import OpenAI

client = OpenAI(api_key="your-key-here")

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain what RAG is in 2 sentences."}
    ]
)
print(response.choices[0].message.content)
```

| ✅ Pros                     | ❌ Cons                            |
| --------------------------- | ---------------------------------- |
| No GPU needed               | Costs money per token              |
| Easiest to get started      | Your data is sent to their servers |
| Highest performance today   | Can't fine-tune yourself           |
| Provider handles scaling    | Vendor lock-in risk                |
| No infrastructure to manage | Rate limits                        |

---

### Option B: Open Models via Hugging Face

Models where weights are publicly downloadable and can be run locally.

**Examples:** Llama 3, Mistral, Phi-3, Command R, Falcon, Qwen

**Hugging Face** is the central hub — think of it as GitHub for AI models (800,000+ models). Every model has a model card with documentation, benchmarks, license, and usage examples.

```python
# Standard Hugging Face pattern
from transformers import pipeline

generator = pipeline(
    "text-generation",
    model="microsoft/Phi-3-mini-4k-instruct",
    device_map="auto"
)
output = generator([{"role": "user", "content": "Explain RAG in 2 sentences."}])
print(output[0]["generated_text"])
```

| ✅ Pros                         | ❌ Cons                                |
| ------------------------------- | -------------------------------------- |
| Free to run                     | Needs GPU for good performance         |
| Data stays on your servers      | More setup required                    |
| Can fine-tune for your use case | You manage infrastructure              |
| No vendor lock-in               | Performance can lag proprietary models |
| Full model transparency         |                                        |

---

### Open Source Frameworks Used in This Book

| Framework                     | What it does                                       |
| ----------------------------- | -------------------------------------------------- |
| **Hugging Face Transformers** | Core library — load, run, fine-tune any open model |
| **Sentence Transformers**     | Specialized for creating embeddings                |
| **LangChain**                 | Build chains, agents, RAG pipelines                |
| **llama.cpp**                 | Run LLMs efficiently even on CPU                   |
| **BERTopic**                  | Topic modeling with LLMs                           |

---

## 16. Generating Your First Text — Code Walkthrough

Let's break down every line of the book's first code example in detail:

### Loading the Model and Tokenizer

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
```

- `AutoModelForCausalLM` — loads a **causal** (decoder-only, generative) language model. "Causal" means it only attends to previous tokens — the masked self-attention we discussed.
- `AutoTokenizer` — loads the tokenizer that was trained alongside the model. Different models use different tokenizers — you must use the matching one.
- `pipeline` — a high-level wrapper that bundles model + tokenizer + inference into one convenient function.

```python
model = AutoModelForCausalLM.from_pretrained(
    "microsoft/Phi-3-mini-4k-instruct",
    # ↑ Model ID on Hugging Face Hub: {organization}/{model-name}
    # "4k" = 4,096 token context window
    # "instruct" = fine-tuned to follow instructions (not just complete text)

    device_map="auto",
    # ↑ Automatically places model on GPU if available, falls back to CPU
    # Use "cuda" to force GPU, "cpu" to force CPU

    torch_dtype="auto",
    # ↑ Uses the model's recommended numerical precision (usually float16)
    # float16 uses half the memory of float32 with minimal quality loss

    trust_remote_code=True,
    # ↑ Phi-3 includes custom Python code in its repo that must run locally
    # Only set True for models from trusted organizations
)

tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct")
```

### Creating the Pipeline

```python
generator = pipeline(
    "text-generation",      # Task type — tells pipeline what kind of model to expect
    model=model,            # The loaded model
    tokenizer=tokenizer,    # The matching tokenizer
    return_full_text=False, # Return only the generated response, not the prompt too
    max_new_tokens=500,     # Maximum tokens to generate — prevents runaway responses
    do_sample=False,        # False = always pick the most probable next token (deterministic)
                            # True = introduce randomness (creative but less predictable)
                            # Temperature parameter controls HOW random — covered in Ch. 6
)
```

### Sending a Message

```python
messages = [
    {"role": "user", "content": "Create a funny joke about chickens."}
]
output = generator(messages)
print(output[0]["generated_text"])
```

The `messages` format is the **chat template** — a standardized list of dictionaries with `role` and `content`. This same format is used across OpenAI, Anthropic, and Hugging Face, making it easy to swap models.

**Available roles:**

- `"user"` — what the human types
- `"assistant"` — what the model previously responded (for multi-turn conversations)
- `"system"` — instructions that shape the model's behavior throughout the conversation

**Multi-turn conversation example:**

```python
messages = [
    {"role": "system", "content": "You are a concise coding assistant."},
    {"role": "user", "content": "What is a REST API?"},
    {"role": "assistant", "content": "A REST API is an interface..."},
    {"role": "user", "content": "How do I call one in Python?"},
    # ↑ The model sees the full conversation history and responds in context
]
```

---

## 17. Glossary

| Term                              | Definition                                                                          |
| --------------------------------- | ----------------------------------------------------------------------------------- |
| **Language AI / NLP**             | Subfield of AI focused on understanding and generating human language               |
| **Token**                         | The basic unit of text a model processes — roughly a word or subword                |
| **Tokenization**                  | Splitting text into tokens before feeding to the model                              |
| **Vector**                        | A list of numbers representing data mathematically                                  |
| **Embedding**                     | A dense vector that captures the semantic meaning of text                           |
| **Bag-of-Words**                  | Simple word-counting representation — fast but ignores meaning and order            |
| **word2vec**                      | 2013 model that learned semantic word embeddings from context                       |
| **Parameters**                    | The numerical weights inside a neural network — learned during training             |
| **RNN**                           | Recurrent Neural Network — processes sequences one token at a time                  |
| **Attention**                     | Mechanism that lets a model dynamically focus on relevant parts of input            |
| **Self-Attention**                | Attention within a single sequence — each token attends to all others               |
| **Transformer**                   | Neural network architecture (2017) using only attention — foundation of modern LLMs |
| **Encoder**                       | Transformer component that reads and understands the full input                     |
| **Decoder**                       | Transformer component that generates output one token at a time                     |
| **BERT**                          | Encoder-only Transformer for understanding text (Google, 2018)                      |
| **GPT**                           | Decoder-only Transformer for generating text (OpenAI, 2018)                         |
| **Representation Model**          | Encoder-only model — produces embeddings, doesn't generate text                     |
| **Generative Model**              | Decoder-only model — generates text token by token                                  |
| **Masked Language Modeling**      | BERT's training trick — predict randomly masked words                               |
| **Next Token Prediction**         | GPT's training trick — predict the next word given all previous words               |
| **Pre-training**                  | Expensive first training step on massive data — produces foundation model           |
| **Fine-tuning**                   | Cheaper second step — adapt pre-trained model to specific task or behavior          |
| **Foundation Model / Base Model** | Result of pre-training — general purpose, not yet task-specific                     |
| **Instruct Model**                | Base model fine-tuned to follow instructions (e.g. ChatGPT)                         |
| **Context Window**                | Maximum tokens a model can process in one request                                   |
| **Autoregressive**                | Generating one token at a time, each depending on all previous tokens               |
| **Transfer Learning**             | Starting from a pre-trained model and adapting it for a new task                    |
| **Hallucination**                 | When an LLM confidently generates factually incorrect information                   |
| **RAG**                           | Retrieval-Augmented Generation — grounding LLM responses in real external documents |
| **VRAM**                          | GPU memory — the primary hardware constraint when running LLMs locally              |
| **Quantization**                  | Compressing model weight precision to reduce VRAM requirements                      |
| **Hugging Face**                  | Central platform for open-source AI models, datasets, and tools                     |
| **[CLS] Token**                   | Special BERT token whose embedding represents the full input sentence               |
| **RLHF**                          | Reinforcement Learning from Human Feedback — used to create instruct models         |

---

## 18. Chapter Summary

### The Evolution of Language AI — One Diagram

```
1950s–2000s   Bag-of-Words
              Count words → sparse vectors
              ❌ Ignores meaning, order, context
                    ↓
2013          word2vec
              Neural network → dense semantic embeddings
              ❌ Static (same word = same vector always, ignores context)
                    ↓
2014          RNN + Attention
              Sequential processing + dynamic focus on relevant words
              ❌ Can't parallelize training, slow on long sequences
                    ↓
2017 ⭐        Transformer — "Attention Is All You Need"
              Attention only, all tokens processed in parallel
              ✅ Fast training, scalable, deeply context-aware
                    ↓
         ┌────────────────────────────────┐
         ↓                                ↓
2018  BERT (Encoder-only)          GPT (Decoder-only)
      Bidirectional understanding   Generative text completion
      → classification, search      → chat, summarization, code
         ↓                                ↓
2022–now  ChatGPT launch → mass adoption → model explosion
          Instruction fine-tuning made power accessible to everyone
```

### The Two Model Types — Your Core Mental Model

```
REPRESENTATION MODELS  🔵
  Architecture : Encoder-only Transformer
  Training     : Masked Language Modeling (predict masked tokens)
  Output       : Embeddings (vectors)
  Use for      : Classification, semantic search, clustering
  Examples     : BERT, RoBERTa, all-MiniLM, Sentence-BERT
  Think of as  : "Understanding machine" — reads, comprehends, indexes

GENERATIVE MODELS  🔴
  Architecture : Decoder-only Transformer
  Training     : Next Token Prediction (predict the next word)
  Output       : Text
  Use for      : Chat, summarization, code generation, writing
  Examples     : GPT-4, Llama 3, Mistral, Phi-3, Claude
  Think of as  : "Writing machine" — reads, then generates
```

### What You Should Now Understand

After studying this chapter you should be able to clearly explain:

- [ ] Why text needs to be converted to numbers and how that approach evolved from BoW → embeddings → transformers
- [ ] What the Transformer architecture is and the core problem it solved
- [ ] The difference between encoder-only models (BERT) and decoder-only models (GPT)
- [ ] How LLMs are trained in two steps and which step you'll actually work with as a dev
- [ ] What a context window is and why it matters in production apps
- [ ] When to choose a proprietary API vs a local open model
- [ ] The key responsible AI concerns you must consider as a builder

### Coming Up in Chapter 2

Chapter 2 dives into **Tokens and Embeddings** — two concepts introduced here but not yet fully explained:

- How exactly does a tokenizer split text? (Hint: it's not just spaces)
- What are **subword tokens** and why do they matter?
- How do modern models create **context-aware embeddings** (solving the word2vec static problem)?
- How can you use embeddings for real tasks in your apps?

---

_Next: [`summary.md`](./summary.md) — the 1-page revision card_
_Practice: [`practice/ch01_practice.ipynb`](./practice/ch01_practice.ipynb) — hands-on exercises_

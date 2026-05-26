# Day 6 — Consolidation, Full Self-Test & Book Preview

> **Series:** ML Prerequisites for "Hands-On Large Language Models" + "Build a Large Language Model From Scratch"
> **Audience:** Fullstack JS/TS developer — completing the prerequisite week
> **Goal:** Verify that all five days of concepts are solid, find gaps, and walk into Day 7 (the actual books) with a clear mental map of what you'll encounter

---

## How to Use This Day

Day 6 has three phases:

**Phase 1 — Concept Web (30 min):** Read through the full concept map. This is your
mental "index" for everything studied. Identify any term that still feels fuzzy.

**Phase 2 — Full Self-Test (60–90 min):** Answer every question cold, on paper or in a
note. Do not look at earlier notes first. After finishing, grade yourself and revisit
only the sections where you scored poorly.

**Phase 3 — Book Preview (30 min):** Read the annotated walkthrough of what the
first chapters of both books contain. You're not reading the books yet — you're
building a map so nothing surprises you on Day 7.

---

## Phase 1 — The Full Concept Web

Everything from Days 1–5, connected.

### The Big Picture Chain

```
Human language
    ↓
Tokenizer → Token IDs (integers)
    ↓
Embedding Layer (lookup table matrix) → Token Vectors
    ↓
+ Positional Encoding
    ↓
Transformer Blocks (attention + feedforward) [repeated N times]
    ↓
Language Model Head → Logits (one score per vocab token)
    ↓
Softmax → Probabilities
    ↓
Sampling/Argmax → Next Token ID
    ↓  (append to input, repeat)
Generated Text
```

Every concept you studied lives somewhere in this chain.

---

### Concept Map by Day

**Day 1 — The Landscape**

- AI ⊃ ML ⊃ Deep Learning ⊃ LLMs
- Model = function with parameters that maps input → output
- Training = adjusting parameters to minimize error on data
- Inference = using a trained model to make predictions
- Parameters = the numbers inside the model (GPT-3 has 175B of them)
- Pretraining vs. fine-tuning

**Day 2 — Neural Networks**

- Neuron = weighted sum of inputs → activation function → output
- Layer = many neurons processing the same input in parallel
- Network = layers stacked in sequence
- Activation functions: ReLU (clamp negatives to 0), Softmax (probabilities that sum to 1)
- Supervised learning: labeled input→output pairs
- Unsupervised learning: no labels, find structure

**Day 3 — Training Mechanics**

- Loss function: measures how wrong the model is (Cross-Entropy for classification/text generation, MSE for regression)
- Gradient descent: take small steps downhill on the loss landscape
- Learning rate: size of each step (too big = overshoot, too small = too slow)
- Backpropagation: efficiently compute which direction each parameter should move
- Epoch: one full pass over the training data
- Batch: subset of data processed at once
- Overfitting: model memorizes training data, fails on new data
- Dropout, regularization: techniques to prevent overfitting

**Day 4 — Data Structures & Embeddings**

- Scalar → Vector → Matrix → Tensor (rank 0, 1, 2, N)
- Shape: size of each axis, e.g. `[8, 4, 768]` = batch × sequence × embedding
- Dense vector = most values non-zero (opposite: sparse/one-hot)
- Embedding = learned dense vector representing meaning
- Word2Vec: train by predicting neighboring words (skip-gram + negative sampling)
- Static embeddings: one vector per word, context-blind
- Contextual embeddings: vector changes per context — what LLMs produce
- Embedding layer: a learned matrix, shape `[vocab_size, embed_dim]`; lookup by index
- Cosine similarity: measures angle between vectors; used to compare semantic similarity
- Sentence embeddings: one vector per sentence; used in RAG, semantic search
- Positional encoding: added to token embeddings to preserve word order

**Day 5 — Python Patterns**

- Indentation defines blocks (no `{}`)
- `self` = `this`, always explicit
- No `new` keyword for instantiation
- f-strings: `f"text {var:.3f}"`
- List comprehensions: `[expr for x in iterable if cond]`
- `nn.Module` subclass pattern: define layers in `__init__`, wire in `forward()`
- The 5-step training loop: zero_grad → forward → loss → backward → step
- `with torch.no_grad()` for inference
- `model.train()` / `model.eval()` mode switching

---

## Phase 2 — Full Self-Test

Answer these cold. No notes. Be honest with yourself.
Grade: ✅ confident / 🟡 shaky / ❌ blank → revisit that day's notes.

---

### Section A — Landscape & Concepts (Day 1)

1. What is the relationship between AI, ML, and deep learning? Which contains which?

2. In one sentence, what is a model in ML?

3. What is the difference between training and inference? Give a concrete example of each in the context of GPT.

4. What does "175 billion parameters" mean for GPT-3? Are these numbers stored before or after training?

5. What is fine-tuning, and why would you do it instead of pretraining from scratch?

6. You are building a sentiment classifier on top of GPT-2. Is this more likely to involve pretraining or fine-tuning? Why?

---

### Section B — Neural Networks (Day 2)

7. Describe what a single neuron computes. What are the inputs, what is the operation, and what is the output?

8. What does the ReLU activation function do? Why is it used instead of no activation at all?

9. What does Softmax do? When specifically is it used in an LLM?

10. What is the difference between supervised and unsupervised learning? Give one example of each.

11. An LLM is trained to predict the next word in a sequence. Is this supervised or unsupervised learning? Justify your answer — this is a trick question.

12. Why do neural networks need activation functions between layers? What happens if you remove them?

---

### Section C — Training Mechanics (Day 3)

13. What does a loss function measure? Name two loss functions and describe when each is appropriate.

14. Explain gradient descent in plain English, without equations. What is the "gradient" and what do we do with it?

15. What is the learning rate? What goes wrong if it's too high? Too low?

16. What is backpropagation? What problem does it solve, and at a high level, how does it work?

17. What is an epoch? What is a batch? How are they related?

18. You train a model that achieves 99% accuracy on training data but 60% on test data. What is happening and what are two techniques to fix it?

19. Your training loss keeps decreasing, but your validation loss starts increasing after epoch 5. Draw or describe what this means. What should you do?

---

### Section D — Tensors & Embeddings (Day 4)

20. What is the rank of each: a scalar, a vector, a 4-column by 6-row table of numbers, a batch of 8 sequences each with 4 tokens each embedded at 256 dimensions?

21. A batch tensor has shape `[16, 128, 768]`. What does each dimension represent in an LLM context?

22. What is the problem with one-hot encoding that word embeddings solve? Name two problems.

23. What does Word2Vec's training objective teach the model? What assumption does it make about language?

24. What is the critical limitation of Word2Vec embeddings compared to what LLMs produce?

25. An embedding layer in GPT-2 small covers a vocabulary of 50,257 tokens with embedding dimension 768. What is the shape of this matrix? How many scalar parameters is that?

26. If `cosine_similarity(embed("surgeon"), embed("doctor")) = 0.91` and `cosine_similarity(embed("surgeon"), embed("skateboard")) = 0.03`, what does this tell you about what the embedding model has learned?

27. Why do LLMs add positional encodings to token embeddings before the transformer processes them?

28. What is a sentence embedding? How does it differ from a token embedding, and when would you use it?

---

### Section E — Python Reading (Day 5)

Read each snippet and answer the question. No running allowed.

**Snippet 1:**

```python
results = [x**2 for x in range(6) if x % 2 == 0]
```

29. What is the value of `results`?

**Snippet 2:**

```python
class TransformerBlock(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.att = MultiHeadAttention(d_in=cfg["emb_dim"], d_out=cfg["emb_dim"])
        self.ff  = FeedForward(cfg)
        self.norm = nn.LayerNorm(cfg["emb_dim"])

    def forward(self, x):
        shortcut = x
        x = self.norm(x)
        x = self.att(x)
        x = x + shortcut
        return x
```

30. What class does `TransformerBlock` inherit from?
31. What is `super().__init__()` doing here?
32. What is `shortcut = x` doing, and why is `x = x + shortcut` important conceptually?
33. In what order are `self.norm`, `self.att`, and the shortcut addition applied?

**Snippet 3:**

```python
for epoch in range(3):
    model.train()
    for batch in train_loader:
        optimizer.zero_grad()
        loss = compute_loss(model, batch)
        loss.backward()
        optimizer.step()
    print(f"Epoch {epoch+1}/3 done")
```

34. If `train_loader` has 100 batches, how many times does `optimizer.step()` execute across all 3 epochs?
35. Why must `optimizer.zero_grad()` come before `loss.backward()`, not after?
36. What is `f"Epoch {epoch+1}/3 done"` for epoch=0?

**Snippet 4:**

```python
with open("data.txt", "r", encoding="utf-8") as f:
    text = f.read()

with torch.no_grad():
    embeddings = model.encode(text[:100])
```

37. What does the `with` block guarantee about the file handle?
38. Why is `torch.no_grad()` used here instead of just calling `model.encode()` directly?

---

### Section F — Integration (Hardest)

These require connecting concepts across days.

39. A language model generates text one token at a time. Trace the complete journey of a single forward pass: starting with a string of text, ending with a predicted next token. Include: tokenization, embedding, positional encoding, transformer output, and sampling.

40. You want to build a semantic search engine over a company knowledge base (10,000 documents). Describe the full pipeline: what type of embeddings you'd use, why, how you'd store them, and how you'd query them at runtime.

41. A colleague says: "We don't need positional encodings — the embedding layer already encodes meaning, so the model can figure out order from context." Is this correct? Explain precisely why or why not.

42. Word2Vec embeddings for "bank" in the sentence "I went to the bank to deposit money" and "She sat on the bank of the river" are **identical**. GPT-2 embeddings for the same word in the same two sentences are **different**. Explain mechanically why — what does GPT-2 do that Word2Vec cannot?

43. You're reading the books and encounter this tensor shape: `[1, 1024, 768]`. Based on what you've learned, what does each dimension likely represent? What model does this suggest you're reading about?

---

### Scoring Guide

Count your ✅:

- **38–43:** You're ready to open the book. Day 7 will feel natural.
- **28–37:** Solid foundation. Revisit 1–2 sections of weaker days.
- **18–27:** Core concepts are there but some gaps. Re-read the shaky days fully.
- **Below 18:** Don't panic — take a partial Day 6.5. Focus on Days 3 and 4.

---

## Phase 3 — Book Preview

What you will actually encounter on Day 7.

---

### "Hands-On Large Language Models" — Alammar & Grootendorst

**Chapter 1: An Introduction to Large Language Models**

What's in it:

- History: from Word2Vec → RNNs → Transformers
- How GPT-style models generate text (autoregressive: predict one token, append, repeat)
- Types of embeddings and why they matter
- The "Year of Generative AI"

What will feel familiar from your prep:

- The Word2Vec discussion directly uses Day 4 concepts (skip-gram, negative sampling, static embeddings)
- The RNN limitation section is exactly why contextual embeddings (Day 4) were invented
- The LLM overview references training and inference (Day 1)

What will be new (that's fine — it's the book's job):

- Specific model timelines (BERT, GPT-1/2/3, ChatGPT)
- Specifics of the Transformer architecture — you'll understand the vocabulary but not all details yet

**Chapter 2: Tokens and Embeddings**

What's in it:

- Tokenization in detail: word → subword → BPE
- Token embeddings in code (with `sentence-transformers`)
- Word2Vec in code (with `gensim`)
- Text/sentence embeddings and their applications

What will feel familiar:

- Everything from Day 4 (Embeddings section)
- The `SentenceTransformer.encode()` call — you already saw this in your notes
- The discussion of embedding dimensions and cosine similarity

What might trip you up:

- BPE (Byte Pair Encoding) tokenization — a new concept not in your prereqs. It's covered thoroughly; just read it fresh.
- `gensim` library — you haven't seen it, but it's just another Python library

**Chapter 3: Looking Inside Large Language Models**

What's in it:

- The Transformer architecture in depth (encoder, decoder, attention)
- Self-attention mechanism: Q/K/V vectors, relevance scoring, combining information
- Multi-head attention
- The full forward pass of an LLM

What will feel familiar:

- The concept of layers, forward pass, activations (Day 2)
- The tensor shapes throughout — `[batch, seq, embed]` (Day 4)
- Python class patterns for model components (Day 5)

What will be genuinely new:

- The mathematical details of attention (how Q, K, V matrices work)
- This is the book's main teaching — go slowly here

> **Reading tip for Alammar's book:** Jay Alammar is famous for diagrams. Do not skim
> the figures. The figures often carry more information than the text. Spend time with each one.

---

### "Build a Large Language Model From Scratch" — Raschka

**Appendix A: Introduction to PyTorch**

Highly recommended to read before Chapter 1 proper.

What's in it:

- Tensor creation and operations (exactly what you covered in Days 4–5)
- Autograd and `.backward()`
- The training loop (exactly what you studied in Day 5)
- `nn.Module` subclassing

What will feel familiar:

- Almost everything — this appendix covers what Days 4–5 targeted
- The `NeuralNetwork` class you saw in Day 5 is literally from this appendix

Read this first even if it's listed as an appendix. It's the practical foundation for
every code listing in the book.

**Chapter 1: Understanding Large Language Models**

What's in it:

- What LLMs are, why they work
- Pretraining vs fine-tuning (exactly Day 1)
- The transformer architecture conceptually
- GPT vs BERT architecture differences

What will feel familiar:

- All of it conceptually — this chapter reinforces Days 1–2
- Use it as validation that your mental model is correct

**Chapter 2: Working with Text Data**

What's in it:

- Tokenization in Python: splitting text, building vocabulary, BPE via `tiktoken`
- Creating token IDs
- Embedding layers in PyTorch: `nn.Embedding`
- Positional embeddings
- Data loaders for LLM training

What will feel familiar:

- Day 4 (embeddings, embedding matrix, `[batch, seq, embed]` shapes)
- Day 5 (PyTorch code patterns, `nn.Module`)

What will be new:

- `tiktoken` library — GPT-2/3's actual tokenizer
- Sliding window / stride for creating training examples
- You will write real PyTorch code for the first time in this chapter

**Chapter 3: Coding Attention Mechanisms**

What's in it:

- Self-attention from scratch
- Scaled dot-product attention (Q/K/V matrices)
- Causal masking (why GPT can only look backward)
- Multi-head attention
- Dropout on attention weights

This is the hardest chapter in the book. **Budget extra time here.**

> **Reading tip for Raschka's book:** Every code listing is meant to be run. Set up a
> Jupyter notebook or Python environment and execute the code as you read. The book
> is structured as a step-by-step implementation — skipping code will leave you lost.

---

### What to Watch Out For in Week 1 of Reading

**Things the books assume you already know (that you now do):**

- What loss functions are and why they matter
- What gradient descent does
- What a tensor is and how to read shapes like `[8, 4, 768]`
- What embeddings are and how the embedding matrix works
- Basic PyTorch class patterns

**Things you'll encounter fresh (not covered in prereqs — that's fine):**

- BPE tokenization mechanics
- Specific attention math (Q/K/V in detail)
- `tiktoken`, `gensim`, `sentence-transformers` library APIs
- Causal masking
- Layer normalization
- Residual/skip connections (you saw a preview in Day 5 Snippet 2)

**Common early confusion points:**

- "Dimensions" means embedding size (768), not tensor rank. The books switch between these informally.
- `nn.Linear` performs matrix multiplication — not just "a line." When the books say "linear layer," they mean `output = input @ weight.T + bias`.
- `model(x)` calls `model.forward(x)` — you don't call `forward()` directly.
- `loss.item()` vs `loss` — always use `.item()` when logging a scalar loss.

---

## Day 6 Vocabulary Master List

All key terms from all five days, in one place.

| Term                      | Definition                                                                            |
| ------------------------- | ------------------------------------------------------------------------------------- |
| **AI**                    | Broad field of machines performing tasks requiring human intelligence                 |
| **ML**                    | AI where systems learn from data rather than explicit rules                           |
| **Deep Learning**         | ML using neural networks with many layers                                             |
| **LLM**                   | Neural network trained on massive text data to understand and generate language       |
| **Model**                 | A function with learnable parameters that maps inputs to outputs                      |
| **Parameter**             | A single learnable number inside a model (weights and biases)                         |
| **Training**              | Process of adjusting parameters to minimize error on data                             |
| **Inference**             | Using a trained model to make predictions on new input                                |
| **Pretraining**           | Training on large unlabeled data (e.g. next-token prediction)                         |
| **Fine-tuning**           | Further training a pretrained model on smaller, specific labeled data                 |
| **Neuron**                | Computes weighted sum of inputs → activation function → single output                 |
| **Layer**                 | Many neurons processing the same input in parallel                                    |
| **Activation function**   | Non-linear function applied to neuron output (ReLU, Softmax, etc.)                    |
| **ReLU**                  | Activation: max(0, x) — passes positives, zeros negatives                             |
| **Softmax**               | Activation: converts logits to probabilities that sum to 1                            |
| **Forward pass**          | Computing output from input through all layers                                        |
| **Supervised learning**   | Training with labeled input→output pairs                                              |
| **Unsupervised learning** | Training without labels; model finds structure in data                                |
| **Loss function**         | Measures how wrong the model's prediction is                                          |
| **Cross-entropy loss**    | Loss for classification/text generation; penalizes confident wrong predictions        |
| **MSE**                   | Mean Squared Error — loss for regression (continuous outputs)                         |
| **Gradient**              | Vector of partial derivatives; points uphill on loss surface                          |
| **Gradient descent**      | Iteratively move parameters in the opposite direction of the gradient                 |
| **Learning rate**         | Step size in gradient descent (hyperparameter)                                        |
| **Backpropagation**       | Efficient algorithm to compute gradients for all parameters                           |
| **Epoch**                 | One complete pass over the entire training dataset                                    |
| **Batch**                 | Subset of training data processed together in one gradient update                     |
| **Overfitting**           | Model memorizes training data; fails to generalize                                    |
| **Dropout**               | Randomly zero out neurons during training to prevent overfitting                      |
| **Scalar**                | A single number; rank-0 tensor                                                        |
| **Vector**                | Ordered list of numbers; rank-1 tensor                                                |
| **Matrix**                | 2D grid of numbers; rank-2 tensor                                                     |
| **Tensor**                | N-dimensional array of numbers; generalization of all above                           |
| **Shape**                 | Size of each dimension; e.g. `[8, 4, 256]`                                            |
| **Embedding**             | Dense float vector representing something with semantic meaning encoded geometrically |
| **Embedding dimension**   | Number of values in an embedding vector (e.g. 768)                                    |
| **Embedding layer**       | Learnable lookup table: token ID → embedding vector                                   |
| **Word2Vec**              | Early embedding algorithm using skip-gram + negative sampling                         |
| **Static embedding**      | Same vector regardless of context                                                     |
| **Contextual embedding**  | Vector changes based on surrounding tokens (LLMs)                                     |
| **One-hot encoding**      | Sparse vector: all zeros except one position                                          |
| **Cosine similarity**     | Measures angle between vectors; 1=same direction, 0=perpendicular                     |
| **Positional encoding**   | Vector added to token embeddings to preserve word-order                               |
| **Token embedding**       | Embedding for a single token                                                          |
| **Sentence embedding**    | Single vector representing an entire sentence or document                             |
| **Tokenizer**             | Converts raw text into token IDs                                                      |
| **BPE**                   | Byte Pair Encoding — tokenization algorithm used by GPT-2/3                           |
| **vocab_size**            | Total unique tokens in model's vocabulary (50,257 for GPT-2)                          |
| **Attention mechanism**   | Lets each token "look at" all other tokens when computing its representation          |
| **Self-attention**        | Attention where a sequence attends to itself                                          |
| **Q/K/V**                 | Query, Key, Value matrices — the three projections in attention                       |
| **Multi-head attention**  | Running attention multiple times in parallel with different learned projections       |
| **Transformer**           | Architecture built entirely on attention mechanisms; backbone of all modern LLMs      |
| **nn.Module**             | PyTorch base class for all neural network components                                  |
| **forward()**             | Method defining data flow through a PyTorch model                                     |
| **optimizer.zero_grad()** | Clears accumulated gradients before each batch                                        |
| **loss.backward()**       | Computes gradients via backpropagation                                                |
| **optimizer.step()**      | Updates weights using computed gradients                                              |
| **torch.no_grad()**       | Context disabling gradient tracking; used during inference                            |
| **model.train()**         | Sets model to training mode                                                           |
| **model.eval()**          | Sets model to evaluation mode                                                         |

---

## Final Checklist Before Day 7

Check each item. If you can't check it confidently, spend 15 minutes on that day's notes.

**Day 1:**

- [ ] I can explain the difference between AI, ML, deep learning, and LLMs without confusion
- [ ] I understand what a model's parameters are and that they're learned during training
- [ ] I can distinguish training vs. inference and pretraining vs. fine-tuning

**Day 2:**

- [ ] I understand what a neuron computes (weighted sum → activation)
- [ ] I understand why activation functions are necessary (non-linearity)
- [ ] I know what ReLU and Softmax do and when Softmax is used in LLMs

**Day 3:**

- [ ] I can explain what gradient descent does in plain English
- [ ] I understand the 5-step training loop and what each step does
- [ ] I can describe overfitting and name two techniques to combat it

**Day 4:**

- [ ] I can explain the scalar → vector → matrix → tensor hierarchy
- [ ] I can read a tensor shape like `[8, 4, 768]` and name what each axis represents
- [ ] I understand what an embedding is and why it's better than one-hot encoding
- [ ] I understand the difference between static and contextual embeddings
- [ ] I know what the embedding matrix looks like and how it maps token ID → vector
- [ ] I can explain cosine similarity intuitively

**Day 5:**

- [ ] I can read Python code without getting confused by indentation
- [ ] I understand the `nn.Module` subclass pattern (`__init__` + `forward`)
- [ ] I can read the training loop without confusion
- [ ] I know the JS equivalent of the most common Python constructs

---

## A Note on What You've Actually Accomplished

You started this week with zero ML background. In 5 days you've built:

- A conceptual model of how LLMs work end-to-end
- An understanding of why every architectural decision exists (embeddings → attention → transformers)
- The mathematical vocabulary to read technical writing without panic
- The ability to read PyTorch code without confusion

That is a genuine foundation. Most people who try to read these books without this
background either give up in Chapter 2 or develop wrong mental models they spend
weeks unlearning.

You're not going to understand everything on Day 7. That's expected and fine.
When something is unclear, ask: "Is this unclear because I'm missing a prerequisite, or because the book hasn't explained it yet?" If it's the latter — keep reading. The books are cumulative; the explanation often comes two pages later.

---

_Day 7: Open the books. Start with Appendix A of "Build an LLM From Scratch" or Chapter 1 of "Hands-On LLMs" — whichever spine you grab first._

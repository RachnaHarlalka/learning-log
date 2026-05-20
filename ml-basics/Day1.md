# Day 1 — ML Study Notes

## Topics: What ML Is · What a Model Is · Training · Parameters

> **Goal for today:** Understand the landscape of AI/ML, what a model is,
> what training means, and what parameters are — all from a developer's perspective.

---

## 1. The Map of the Territory

Before anything else, you need to know how these terms nest inside each other.
The book uses all of them and treats them as distinct.

```
Artificial Intelligence (AI)
└── Machine Learning (ML)
    └── Deep Learning (DL)
        └── Large Language Models (LLMs)
            └── Generative AI (GenAI)  ← ChatGPT, Claude, Gemini
```

These are NOT synonyms. Each one is a subset of the one above it.

---

### 1.1 Artificial Intelligence (AI)

The broadest term. Formal definition (John McCarthy, one of the founders):

> "The science and engineering of making intelligent machines,
> especially intelligent computer programs."

In practice the word is heavily overloaded — NPCs in video games driven by
`if/else` trees have been called "AI" for decades. A chess engine doing brute-force
move evaluation is "AI." In modern usage, when people say AI they almost always
mean ML — but the term technically covers far more.

**The key property AI systems are supposed to have:**
The ability to perform tasks that normally require human-like intelligence —
recognising patterns, understanding language, making decisions from incomplete data.

---

### 1.2 Machine Learning (ML)

A **specific subset of AI**, defined by one central idea:

> Instead of programming the rules manually, you give the system data
> and let it find the rules itself.

This is the central philosophical shift. Everything in ML flows from it.

```
Traditional programming:   Rules + Data  →  Answers
Machine learning:          Data + Answers  →  Rules  (learned automatically)
```

The book's own definition:

> "Machine learning involves the development of algorithms that can learn
> from and make predictions or decisions based on data
> without being explicitly programmed."

**What does "without being explicitly programmed" actually mean?**

It means: no developer sat down and wrote:

```js
if (email.subject.includes("FREE MONEY")) return "SPAM";
```

Instead, a developer said:
"Here are 100,000 emails. Here is whether each one is spam or not.
Figure out what makes spam, spam."

The algorithm analysed the data and derived its own internal rules.

---

### 1.3 Deep Learning (DL)

A **specific subset of ML** that uses a particular type of algorithm:
**neural networks with many layers.**

The "deep" literally refers to the depth (number of layers) of the network.

**Key distinction from traditional ML:**

|                    | Traditional ML                                  | Deep Learning                               |
| ------------------ | ----------------------------------------------- | ------------------------------------------- |
| Feature extraction | Manual — a human expert decides what to measure | Automatic — the network learns what matters |
| Data needed        | Can work with less                              | Needs large amounts                         |
| Compute needed     | Low–medium                                      | High                                        |
| Good for           | Structured tabular data                         | Raw text, images, audio                     |

Deep learning became dominant because you no longer need experts to
hand-craft features for every new domain. Feed it raw data; it figures out
what's relevant.

---

### 1.4 Large Language Models (LLMs)

A **specific type of deep neural network** trained on human language.

- Built on an architecture called the **Transformer** (invented 2017)
- "Large" refers to the number of internal parameters — billions to trillions
- The book is entirely about this layer of the stack

You don't need to understand the Transformer architecture today.
Just know the name exists.

---

### 1.5 Generative AI (GenAI)

A **subset of LLMs** (and some other model types) that _generate_ new content
— text, images, audio — rather than just classifying or analysing existing content.

- ChatGPT, Claude, Gemini → GenAI ✅
- A spam classifier → NOT GenAI (it only classifies, doesn't create)
- An image classifier → NOT GenAI

---

## 2. What is Machine Learning, Really?

### 2.1 The problem ML solves

Some problems are easy to solve with explicit rules:

- Sorting a list → write the algorithm
- Validating an email format → write a regex
- Calculating tax → write the formula

But some problems resist explicit rules completely:

- **Recognising a dog in a photo.**
  You could try: "check for four legs, fur, a tail…"
  But you'd need thousands of rules and they'd still fail constantly.
  How do you even detect "fur" in raw pixel values?

- **Translating English to French.**
  Language has exceptions to every rule.
  Grammar rules alone don't capture meaning.

- **Detecting credit card fraud.**
  Patterns are too subtle, too varied, and constantly evolving.

These problems share something:
**Humans can solve them intuitively, but cannot articulate the rules explicitly.**
We can't write down what makes a dog a dog in a way a compiler can execute.

**ML's answer:** Instead of writing the rules, show the system thousands of examples
of solved problems and let it induce the rules itself.

---

### 2.2 The 6-step loop that describes ALL of ML

```
1. Collect training data
   → A large set of inputs paired with correct outputs
   → e.g. 10,000 emails, each labelled "spam" or "not spam"

2. Define a model
   → A mathematical function with many internal adjustable numbers

3. Run training data through the model
   → Measure how wrong the outputs are

4. Automatically adjust the internal numbers
   → Make the model slightly less wrong

5. Repeat steps 3–4 thousands or millions of times
   → The numbers converge toward values that produce correct outputs

6. Stop adjusting — the model is now "trained"
   → Run it on new, previously unseen inputs
```

Everything in the book — transformers, attention mechanisms, fine-tuning,
embeddings — is just a specific, sophisticated answer to one of the questions
embedded in those 6 steps.

---

## 3. What is a Model?

The word you will see more than any other in the book. Nail this precisely.

### 3.1 Formal definition

> A model is a mathematical function that maps inputs to outputs.

```
model(input) → output
```

For a spam classifier:

```
model(email_text) → 0.97   // probability of spam, between 0 and 1
```

For an LLM:

```
model("What is the capital of France?") → "The capital of France is Paris."
```

Nothing more mysterious than that. It is a function.

---

### 3.2 What is inside the function?

The function is not a fixed formula you write by hand.
It is a **parameterised function** — a function whose behaviour is entirely controlled
by thousands (or billions) of internal numbers called **parameters** or **weights**.

Simple analogy from maths:

```
y = mx + b
```

- `x` is the input
- `y` is the output
- `m` (slope) and `b` (intercept) are the **parameters**

Different values of `m` and `b` → completely different lines → completely different behaviour.

A neural network is this idea scaled to billions of parameters instead of two,
with a much more complex mathematical structure.

**The key insight:**

> The parameters define how the function behaves.
> Change the parameters → change the behaviour entirely.

---

### 3.3 The developer analogy

Think of a model as a class with billions of `float32` properties:

```js
class SpamDetector {
  constructor() {
    // Conceptually, imagine billions of these
    this.w1 = 0.0023;
    this.w2 = -0.7341;
    this.w3 = 0.1892;
    this.w4 = 0.5501;
    // ... billions more
  }

  predict(emailText) {
    // Mathematical operations using all those weights
    // Returns a probability between 0 and 1
  }
}
```

**Before training:** those weight values are random — the model outputs garbage.  
**After training:** those values have been carefully tuned — the model outputs useful predictions.

The model file you download (e.g. `llama-3-8b.gguf`) **is literally just those
billions of numbers stored on disk**, plus the architectural blueprint of the function
that uses them. That is the entire file.

---

### 3.4 Training vs. Inference — a critical distinction

These two words are used constantly. They are completely different operations.

|              | Training                                      | Inference                                        |
| ------------ | --------------------------------------------- | ------------------------------------------------ |
| What happens | Parameters are being adjusted                 | Parameters are frozen, just running the function |
| When         | Done once (or a few times), very expensive    | Done every time you use the model                |
| Who does it  | Anthropic, OpenAI, Meta, etc. on GPU clusters | You, when you call an API                        |
| Analogy      | Compiling + building the app                  | Running the compiled app                         |

**When you call the OpenAI or Anthropic API, you are doing inference —
running a frozen, pre-trained model. You are NOT training anything.**

This is why API calls are cheap and fast compared to the training runs that
cost tens of millions of dollars and take months.

---

## 4. What Are Parameters (Weights)?

Parameters are the internal numbers of the model that get adjusted during training.
They are literally what the model "knows."

### 4.1 Scale

| Model                                     | Year  | Parameters                                 |
| ----------------------------------------- | ----- | ------------------------------------------ |
| Simple spam classifier (traditional ML)   | —     | ~hundreds                                  |
| Small neural net for image classification | ~2012 | ~millions                                  |
| BERT (one of the first big LLMs)          | 2018  | 110 million                                |
| GPT-2                                     | 2019  | 1.5 billion                                |
| GPT-3                                     | 2020  | 175 billion                                |
| Llama 2                                   | 2023  | 7B – 70B                                   |
| Modern frontier models                    | 2024+ | Hundreds of billions – estimated trillions |

The "large" in Large Language Models refers directly to this number.
The book will use terms like "8B model" or "70B model" — those are parameter counts.

---

### 4.2 Parameters vs. Hyperparameters

You will encounter both terms. They are fundamentally different things.

**Parameters (weights):**

- Internal numbers the model _learns_ during training
- Change automatically via the training algorithm
- You never set them manually
- Example: every single weight value in the network

**Hyperparameters:**

- Settings YOU choose _before_ training begins
- Control how training runs, not what the model learns
- You set them manually based on experimentation
- Example: how many layers the network has, how fast it learns, how long to train

```
Hyperparameters control the training process.
Parameters are what the training process produces.
```

**Analogy:**

```
Hyperparameters  →  your webpack/tsconfig settings
Parameters       →  the compiled output those settings produce
```

---

### 4.3 What does a parameter actually represent?

After training, each parameter has learned to encode some aspect of the
pattern the model discovered. But — and this is important to internalise early —
**individual parameters are not interpretable.** You cannot point to parameter
#4,823,910 and say "this one stores the concept of cats."

The knowledge is **distributed** across ALL parameters collectively.
No single weight means anything in isolation. The meaning emerges from the
combination of billions of them working together.

This is very different from traditional code, where each variable has a clear,
human-assigned meaning. In neural networks, the representation is holistic and
emergent. This is why ML models are often called "black boxes" — not because
they're doing something unknowable, but because the internal representation
is not human-readable.

---

## 5. What is Training?

Training is the automated process of finding the right values for all the parameters.

### 5.1 Conceptual description

```
1. Take a batch of training examples (e.g. 32 emails)
2. Pass them through the model → get predictions
3. Compare predictions to correct answers → calculate the "error" (called loss)
4. Figure out which parameters caused the error (called backpropagation)
5. Nudge each parameter slightly in a direction that reduces the error
6. Repeat for the next batch
7. Repeat for millions of batches
8. Eventually the loss stops decreasing significantly → training is done
```

The word **epoch** means one full pass through the entire training dataset.
Training typically runs for multiple epochs.

### 5.2 The compiler analogy

```
Source code  (your .ts files)       →  Training data   (labelled examples)
Compiler     (tsc)                  →  Training algorithm (gradient descent)
Binary       (compiled output)      →  Model weights   (the .bin / .gguf file)
Runtime      (node, browser)        →  Inference       (running the model)
```

You ship the compiled binary, not the source code.
Similarly, you ship (or download) the trained weights, not the training data.

---

### 5.3 Pre-training vs. Fine-tuning

The book draws a critical distinction between these two phases:

**Pre-training:**

- Training from scratch on an enormous corpus of data (the entire internet, books, code)
- Goal: learn language itself — grammar, facts, reasoning patterns, world knowledge
- Extremely expensive — takes months, costs tens of millions of dollars
- Done by large organisations (Anthropic, OpenAI, Meta, Google)
- The result is called a **foundation model** or **base model**
- Llama 2 was pre-trained on 2 trillion tokens of text

**Fine-tuning:**

- Taking a pre-trained foundation model and training it further on a much
  smaller, task-specific dataset
- Goal: adapt the model to a specific task or behaviour
  (e.g. follow instructions, classify medical records, generate SQL)
- Far cheaper — hours to days, accessible to most developers
- The model already "knows" language; you're just steering it

```
Pre-training  →  Teaching someone English and general knowledge (years)
Fine-tuning   →  Training that English-speaker for a specific job (weeks)
```

Most of the book is about fine-tuning and using pre-trained models.
You will almost never pre-train from scratch.

---

## 6. The AI/ML Hierarchy — Summary Diagram

```
┌─────────────────────────────────────────────────┐
│                ARTIFICIAL INTELLIGENCE           │
│  Any system performing human-like tasks         │
│                                                  │
│  ┌───────────────────────────────────────────┐  │
│  │            MACHINE LEARNING               │  │
│  │  Algorithms that learn rules from data    │  │
│  │                                           │  │
│  │  ┌─────────────────────────────────────┐  │  │
│  │  │          DEEP LEARNING              │  │  │
│  │  │  ML using multi-layer neural nets   │  │  │
│  │  │                                     │  │  │
│  │  │  ┌───────────────────────────────┐  │  │  │
│  │  │  │   LARGE LANGUAGE MODELS       │  │  │  │
│  │  │  │   Deep nets for language      │  │  │  │
│  │  │  │                               │  │  │  │
│  │  │  │  ┌─────────────────────────┐  │  │  │  │
│  │  │  │  │     GENERATIVE AI       │  │  │  │  │
│  │  │  │  │  LLMs that generate     │  │  │  │  │
│  │  │  │  │  new content            │  │  │  │  │
│  │  │  │  └─────────────────────────┘  │  │  │  │
│  │  │  └───────────────────────────────┘  │  │  │
│  │  └─────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────┘  │
└─────────────────────────────────────────────────┘
```

---

## 7. Key Vocabulary — Day 1 Cheatsheet

| Term                              | Plain English Definition                                                    |
| --------------------------------- | --------------------------------------------------------------------------- |
| **Model**                         | A mathematical function (input → output) with tunable internal numbers      |
| **Parameters / Weights**          | The billions of internal numbers that define the model's behaviour          |
| **Training**                      | The automated process of finding the right values for all parameters        |
| **Inference**                     | Running a trained (frozen) model on new inputs to get predictions           |
| **Loss**                          | A number measuring how wrong the model's predictions are (lower = better)   |
| **Epoch**                         | One full pass through the entire training dataset                           |
| **Pre-training**                  | Training from scratch on massive data — produces a foundation model         |
| **Fine-tuning**                   | Further training a pre-trained model on a smaller, task-specific dataset    |
| **Foundation model / Base model** | A model produced by pre-training, before task-specific fine-tuning          |
| **Hyperparameter**                | A setting you choose before training (e.g. learning rate, number of layers) |
| **Deep learning**                 | ML using neural networks with many layers                                   |
| **Transformer**                   | The specific neural network architecture that all modern LLMs use           |
| **Generative AI**                 | Models that produce new content (text, images) rather than just classifying |

---

## 8. Common Misconceptions — Cleared Up Now

**"The model is learning while I chat with ChatGPT."**
No. When you chat, you are doing inference on a frozen model.
Training happened months ago on Anthropic's/OpenAI's servers.
Your conversation does not change the model's weights.

**"More parameters always means a better model."**
Not necessarily. A smaller model trained on better data with better techniques
can outperform a larger one. Parameter count is one factor, not the only one.

**"Downloading a model file is downloading an AI."**
Partially. You're downloading the trained weights — the numbers.
You also need the inference engine (the software that runs the mathematical
function using those numbers). Tools like Ollama bundle both.

**"AI understands language the way humans do."**
No. LLMs manipulate statistical patterns in numerical representations of text.
They don't "understand" in any philosophical sense — they produce outputs that
are statistically consistent with their training data. The book will be very
precise about this distinction.

---

## 9. Today's Recommended Resources

Work through these after reading these notes.

### Must-watch (in order):

1. **[3Blue1Brown — But what is a neural network? (18 min)](https://www.youtube.com/watch?v=aircAruvnKk)**
   Watch the full video. It gives a visual foundation for everything in these notes.
   Pay attention to how he describes neurons, layers, and the idea of a network
   "learning" — you will be building on this tomorrow.

2. **[Jay Alammar — A Visual Introduction to Machine Learning](http://www.r2d3.us/visual-intro-to-machine-learning-part-1/)**
   An interactive scroll-based visual explainer. Takes ~15 minutes.
   Focus on how a model "draws a boundary" between classes — the intuition
   for what a trained model actually does geometrically.

### Optional if you have time:

3. **[StatQuest — Machine Learning Fundamentals (12 min)](https://www.youtube.com/watch?v=Gv9_4yMHFhI)**
   Josh Starmer's channel is the clearest in the field for conceptual ML.
   Good reinforcement for the model/training concepts in these notes.

---

## 10. Self-Check — Answer These Before Day 2

Write your answers in plain English. If you can't, re-read the relevant section.

1. What is the difference between AI, ML, deep learning, and LLMs?
   Are they synonyms? How do they relate?

2. What is the core philosophical difference between traditional programming
   and machine learning?

3. A model is described as a "parameterised function." What does parameterised
   mean? What changes when you change the parameters?

4. When you call `fetch("https://api.openai.com/v1/chat/completions", ...)`,
   are you training a model or doing inference? What is the difference?

5. What is the difference between pre-training and fine-tuning?
   Why does fine-tuning exist as a separate step?

6. What is a hyperparameter? How is it different from a parameter?

7. Does chatting with ChatGPT update or change its weights? Why or why not?

---

## 11. What's Coming Tomorrow

**Day 2** covers:

- What a neural network actually is structurally (layers, neurons, activations)
- Supervised vs. unsupervised learning
- The 3Blue1Brown neural network series (videos 1 and 2 — ~38 min)

The concepts from today are the prerequisite for tomorrow.
Make sure you can answer the self-check questions above before moving on.

---

_Notes for "Hands-On Large Language Models" — Jay Alammar & Maarten Grootendorst_  
_Prerequisite study plan — Day 1 of 7_

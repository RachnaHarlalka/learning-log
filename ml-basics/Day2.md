# Day 2 — ML Study Notes

## Topics: Neural Networks · Supervised vs. Unsupervised Learning

> **Goal for today:** Build a solid structural mental model of what a neural network
> is — layers, neurons, activations, forward pass — and understand what supervised
> vs. unsupervised learning means in the context of LLMs specifically.

> **Prerequisite check:** Before continuing, you should be comfortable with Day 1.
> Can you explain the difference between training and inference? Between parameters
> and hyperparameters? If not, review Day 1 before continuing.

---

## 1. Why Neural Networks?

From Day 1, you know that ML is about letting an algorithm find patterns in data
instead of hand-coding rules. But _which_ algorithm do you use?

For decades, many different ML algorithms existed:

- Decision trees
- Support vector machines
- Linear regression
- K-nearest neighbours
- Random forests

All of these work well for _structured_ data — spreadsheet-like data where you define
clear input features (age, income, credit score → approve/deny loan).

But they all fail on **unstructured data:**

- Raw pixel values in an image
- Raw characters in a text document
- Raw audio samples

The reason: these algorithms need you to hand-engineer the features.
For a photo, you'd have to manually define what "edge", "fur", "shape" means in
pixel terms — an impossible task.

**Neural networks solve this because they learn their own features.**
You give them raw data and they figure out, layer by layer, what features matter.
This is the core reason deep learning took over the field after ~2012 when GPUs
became powerful enough to train large networks.

---

## 2. What is a Neuron?

The word "neuron" is a loose biological analogy. Don't over-index on it.
A neuron in a neural network is just a **single mathematical operation.**

Here is what one neuron does, precisely:

```
1. Takes several numbers as input          [0.5, 0.2, -0.8, 0.1]
2. Multiplies each input by a weight       [0.5*w1, 0.2*w2, -0.8*w3, 0.1*w4]
3. Adds them all together (+ a bias term)  sum = 0.5*w1 + 0.2*w2 + (-0.8)*w3 + 0.1*w4 + b
4. Passes the result through an
   activation function                     output = activation(sum)
5. Produces a single output number
```

That's it. One neuron = a weighted sum + an activation function → one number out.

The **weights** (`w1`, `w2`, `w3`, `w4`) and the **bias** (`b`) are the parameters
of that neuron. They get adjusted during training.

### Developer analogy

Think of a neuron as a reducer function:

```js
function neuron(inputs, weights, bias, activationFn) {
  const weightedSum = inputs.reduce((acc, x, i) => acc + x * weights[i], bias);
  return activationFn(weightedSum);
}
```

A neural network is just millions of these tiny reducer functions,
chained together in layers.

---

## 3. What is a Layer?

A **layer** is a collection of neurons that all:

- Receive the same input (the output of the previous layer)
- Process it in parallel and independently
- Each produce one output number
- Their outputs are collected into a vector and passed to the next layer

```
Previous layer output:  [0.5, 0.2, -0.8, 0.1]   ← 4 numbers
                           ↓    ↓    ↓    ↓
                        [ N1   N2   N3   N4   N5 ]  ← 5 neurons in this layer
                           ↓    ↓    ↓    ↓    ↓
This layer output:      [0.8, 0.1,  0.4, -0.2, 0.9]  ← 5 numbers
```

Each neuron in the layer uses the _entire_ previous layer's output as its input,
but has its own independent set of weights.

The number of neurons in a layer = the number of outputs that layer produces.
This is called the layer's **dimensionality** or **width**.

### The Linear Layer (most important layer type)

The book uses the term **Linear layer** (also called a Dense or Fully Connected layer)
constantly. It is exactly what was described above: every input connected to every
neuron, each with its own weight. The operation is mathematically a matrix multiply:

```
output = activation(W · input + b)

Where:
  W     = weight matrix  (rows = num neurons, cols = num inputs)
  input = input vector
  b     = bias vector
  ·     = matrix multiplication
```

You do not need to know how to do matrix multiplication by hand.
You just need to know this is what "Linear layer" means in code and in the book.

---

## 4. What is an Activation Function?

This is a critical concept that is often glossed over in beginner explanations.

### The problem without activation functions

If every layer just did a weighted sum (no activation function), then stacking 100
layers would be mathematically equivalent to having a single layer. All the
intermediate layers would collapse into one linear operation. No matter how many
layers you add, the whole network would only be able to learn linear relationships.

Real-world data is almost never linear. The relationship between pixels and
"this is a dog" is not a straight line.

### What activation functions do

An activation function introduces **non-linearity** — it takes the neuron's
weighted sum and applies a non-linear transformation to it.

This is what allows deep networks to model complex, curved, non-linear relationships
in data. Without activation functions, the "deep" in deep learning would be useless.

### The three activation functions you'll encounter in the book

**ReLU (Rectified Linear Unit)**

The simplest and historically most common activation function:

```
ReLU(x) = max(0, x)
```

In plain English: if the input is negative, output 0. If positive, output it unchanged.

```
ReLU(-5.2) = 0
ReLU(0)    = 0
ReLU(3.7)  = 3.7
```

Analogy: a one-way gate. Signal only flows forward if it's positive.

**GELU (Gaussian Error Linear Unit)**

A smoother version of ReLU used in modern LLMs including GPT.
Instead of a hard cut-off at 0, it has a smooth curve.

The key difference: even slightly negative inputs produce a small (not zero) output.
This means neurons with negative inputs can still contribute _something_ to learning.

```
GELU(-0.1) ≈ -0.046   (small but non-zero)
GELU(0)    = 0
GELU(1.0)  ≈ 0.841
```

The book uses GELU extensively in its GPT implementation.
You don't need to know the math — just know it's a smoother ReLU used in GPT.

**Softmax (output layer only)**

Used in the final layer of classification models. It takes a vector of raw scores
(called **logits**) and converts them into probabilities that sum to 1.

```
Input (logits):  [2.1,  0.5,  -1.3]   ← raw scores for 3 classes
Output (probs):  [0.76, 0.17,  0.07]  ← probabilities summing to 1.0
```

For LLMs generating text, the output layer produces a score for every word
in the vocabulary (~50,000 words). Softmax converts those scores into a
probability distribution over all possible next words. The model then either
picks the highest probability word or samples from the distribution.

```
Input:  scores for 50,257 tokens
Output: probability for each token being the next word
```

---

## 5. The Full Neural Network Structure

Now you can understand the full structure:

```
INPUT LAYER
  ↓
  Receives raw data (e.g. numbers representing tokens)
  No weights here — just the raw input values

HIDDEN LAYERS (1 to hundreds of them)
  ↓
  Each is a Linear layer + activation function
  Each transforms the representation from the previous layer
  Early layers: learn simple, low-level patterns
  Later layers: learn complex, high-level patterns

OUTPUT LAYER
  ↓
  Produces the final prediction
  For classification: one score per class → softmax → probabilities
  For LLMs: one score per vocabulary token → softmax → next word probability
```

### The "deep" in deep learning

"Deep" just means many hidden layers. There is no exact threshold but:

- 1-2 hidden layers: shallow network
- 3+ hidden layers: starting to be "deep"
- Modern LLMs (GPT-3, GPT-4, Llama): 96 to 120+ layers

The book's 124-million-parameter GPT-2 implementation has 12 transformer layers.
Each transformer layer is itself made of several sub-layers (attention + feedforward).

### Structural diagram

```
                   ┌─────────────────────────────────────────┐
  input data       │          NEURAL NETWORK                  │
  [0.2, 0.8,  ──▶  │  Layer1 ──▶ Layer2 ──▶ ... ──▶ LayerN  │  ──▶  output
   0.1, 0.5]       │  (Linear    (Linear               (Linear│       [probs]
                   │  + ReLU)    + ReLU)               +Softmax)
                   └─────────────────────────────────────────┘
  raw input                 hidden layers                  predictions
```

---

## 6. The Forward Pass

The **forward pass** is the name for running data through the network
from input to output to get a prediction.

The book uses this term constantly. It is simply: feed data in → get output out.

```
forward pass = model(input) → output
```

No learning happens during the forward pass. The weights are frozen.
You're just running the mathematical function.

```js
// Pseudocode — the forward pass is just calling the function
const output = model.forward(inputData);
// or in most frameworks, just:
const output = model(inputData);
```

**During training:**

1. Forward pass → get prediction
2. Calculate loss (how wrong was the prediction?)
3. Backward pass (backpropagation) → calculate gradients
4. Update weights

**During inference:**

1. Forward pass → get prediction
2. Done. No backward pass, no weight updates.

### The term "logits"

You will see the word **logits** in the book repeatedly.
Logits are the raw, unnormalised scores that come out of the final linear layer
_before_ the softmax is applied.

```
Layer output (logits):    [-1.2,  0.32, -0.71, ..., -1.55]   ← raw scores
After softmax (probs):    [0.001, 0.04,  0.002, ..., 0.0003]  ← probabilities
```

Logits can be any number (positive, negative, any magnitude).
After softmax, they become probabilities between 0 and 1.

---

## 7. What is the "Representation" a Network Learns?

This is the conceptually most important thing to understand about why neural
networks work — and it directly connects to how LLMs work.

As data passes through the layers of a network, each layer transforms it into a
**new representation** — a different set of numbers that encodes the same information
but in a way that is increasingly useful for the final task.

### The classic image processing example

For an image classifier:

```
Raw pixels
  [154, 209, 87, 201, ...]
           ↓  Layer 1
Edge representations
  [0.8 (horizontal edge here), 0.2 (no edge here), ...]
           ↓  Layer 2
Shape representations
  [0.9 (curved shape), 0.1 (sharp corner), ...]
           ↓  Layer 3
Object part representations
  [0.95 (eye-like), 0.85 (ear-like), ...]
           ↓  Layer 4
Object representations
  [0.97 (dog), 0.01 (cat), 0.02 (bird)]
```

Nobody told the network "look for edges in layer 1, shapes in layer 2."
The network learned this hierarchy of representations automatically from data.

### What this means for LLMs

For a language model, the same thing happens with text:

```
Token IDs (raw integers representing words)
  [3626, 6100, 345, ...]
           ↓  Early layers
Syntactic representations
  (grammar structure, parts of speech)
           ↓  Middle layers
Semantic representations
  (meaning, relationships between words)
           ↓  Deep layers
Contextual representations
  (this word in this specific context means X)
```

These final representations are called **context vectors** or **embeddings**.
The book spends a lot of time on this concept, especially in Chapters 2 and 3.

---

## 8. Supervised vs. Unsupervised Learning

Now that you understand neural network structure, supervised vs. unsupervised
becomes much clearer.

---

### 8.1 Supervised Learning

**Definition:** Training where every input has a corresponding label (correct answer).
The model learns to map inputs to those correct labels.

```
Training data format:
  input        →  label
  "great film" →  positive
  "awful film" →  negative
  "loved it"   →  positive
  "terrible"   →  negative
```

The word "supervised" refers to the fact that a human (or automated process)
has **supervised** the creation of the dataset by labelling every example.

**The training signal:** The model makes a prediction, we compare it to the label,
calculate the error (loss), and adjust weights. The label is what the model is
being "taught" to predict.

**Common supervised tasks:**

| Task                     | Input              | Output / Label                    |
| ------------------------ | ------------------ | --------------------------------- |
| Classification           | email text         | spam / not spam                   |
| Sentiment analysis       | review text        | positive / negative / neutral     |
| Named-entity recognition | sentence           | which words are names/places/etc. |
| Translation              | English sentence   | French sentence                   |
| Question answering       | question + context | answer span                       |

**In the book:** Fine-tuning for specific tasks (classification, instruction following)
is supervised learning. You provide labelled examples of the desired behaviour and
train the model to replicate them.

---

### 8.2 Unsupervised Learning

**Definition:** Training where there are NO labels. The model discovers structure
in raw, unlabelled data on its own.

```
Training data format:
  input
  "great film"
  "awful film"
  "loved it"
  "terrible"
  (no labels — just raw text)
```

The model isn't told what to predict. It must find its own signal.

**Common unsupervised tasks:**

- **Clustering:** Group similar items together (no predefined groups)
- **Dimensionality reduction:** Compress data while preserving structure
- **Anomaly detection:** Find items that don't fit the normal pattern
- **Topic modelling:** Discover themes in a large collection of documents

**In the book:** Chapter 5 covers text clustering entirely using unsupervised methods.
A large batch of documents → embeddings → clustering → groups emerge without labels.

---

### 8.3 Self-Supervised Learning ← The critical one for LLMs

This is the category that doesn't appear in most beginner ML curricula but is
**the most important one for understanding how LLMs are trained.**

**Definition:** A form of unsupervised learning where the model generates its OWN
labels from the raw data. No human labelling required.

**How LLMs use it — next-word prediction:**

```
Raw text (no human labels needed):
  "The cat sat on the mat"

The model's task is created automatically:
  Input:  "The cat sat on the"
  Label:  "mat"   ← generated from the text itself

  Input:  "The cat sat on"
  Label:  "the"

  Input:  "The cat sat"
  Label:  "on"
```

The labels are generated automatically by just taking the next word in the text.
No human needed. This is why LLMs can be trained on the entire internet —
all that raw text becomes training data with automatic labels.

**BERT uses a different self-supervised approach — masked language modelling:**

```
Original: "The cat sat on the mat"
Masked:   "The cat [MASK] on the mat"
Label:    "sat"   ← generated from the original text
```

The model learns to predict the masked word from context.
Again — labels come from the data itself, no human required.

**The key insight:**

```
Supervised learning:    needs human-labelled data      → expensive, limited scale
Unsupervised learning:  no labels, discovers structure → limited task performance
Self-supervised:        labels from data itself        → unlimited scale + high performance
```

Self-supervised pre-training is WHY LLMs are so capable.
Trillions of tokens of training data, all auto-labelled.

---

### 8.4 The Book's Specific Framing: Representation vs. Generative Models

The book makes a distinction you will see in almost every chapter.
It is worth understanding clearly now:

**Representation models (encoder-only, e.g. BERT):**

- Trained with masked language modelling (self-supervised)
- Goal: produce excellent numerical representations of text (embeddings)
- Do NOT generate text — they encode text into vectors
- Used for: classification, clustering, semantic search, similarity
- Colour coding in the book: **teal** with a vector icon

**Generative models (decoder-only, e.g. GPT):**

- Trained with next-word prediction (self-supervised)
- Goal: generate coherent text token by token
- Used for: chatbots, text completion, code generation
- Colour coding in the book: **pink** with a chat icon

```
Same input text → very different outputs:

Representation model:  "The cat sat" → [0.2, -0.7, 0.9, ...]   (a vector)
Generative model:      "The cat sat" → "on the mat"             (more text)
```

Both are neural networks. Both use transformer architecture.
The difference is their training objective and how their output is used.

---

## 9. How These Concepts Connect to the Book's Structure

The book is divided into three parts that map directly onto what you've learned today:

**Part 1 — Using LLMs (Chapters 1-3):**
Using pre-trained models for inference.
You'll see: tokenization, embeddings, forward pass, representations.

**Part 2 — Working with LLMs (Chapters 4-9):**
Classification (supervised), clustering (unsupervised), text generation, search.
You'll see: supervised fine-tuning, representation models, generative models.

**Part 3 — Training and Fine-tuning (Chapters 10-12):**
Actually training and fine-tuning models.
You'll see: loss functions, training loops, supervised and unsupervised techniques.

---

## 10. Important Terms Introduced Today

| Term                          | Meaning                                                                |
| ----------------------------- | ---------------------------------------------------------------------- |
| **Neuron**                    | A single weighted sum + activation function → one output number        |
| **Layer**                     | A collection of neurons processing the same input in parallel          |
| **Linear layer**              | A layer where every input connects to every neuron (fully connected)   |
| **Activation function**       | Non-linear transform applied after weighted sum (ReLU, GELU, Softmax)  |
| **ReLU**                      | Simple activation: `max(0, x)` — zeroes out negatives                  |
| **GELU**                      | Smooth activation used in GPT — small negative outputs allowed         |
| **Softmax**                   | Converts logits to probabilities (used in output layer)                |
| **Logits**                    | Raw unnormalised scores from the final layer, before softmax           |
| **Forward pass**              | Running data through the network input-to-output to get a prediction   |
| **Representation**            | The transformed version of data at any point inside the network        |
| **Supervised learning**       | Training with labelled input/output pairs                              |
| **Unsupervised learning**     | Training with no labels — model finds structure itself                 |
| **Self-supervised learning**  | Generates its own labels from raw data (next-word prediction, masking) |
| **Representation model**      | Encoder-only model (e.g. BERT) — encodes text into vectors             |
| **Generative model**          | Decoder-only model (e.g. GPT) — generates text token by token          |
| **Masked language modelling** | BERT's training objective — predict masked words                       |
| **Next-word prediction**      | GPT's training objective — predict the next token                      |

---

## 11. A Concrete Walk-Through: What Happens When You Type a Message to GPT

This ties everything from Days 1 and 2 together:

```
Step 1 — TOKENISATION
  "Hello, how are you?"
   ↓
  [15496, 11, 703, 389, 345, 30]   ← token IDs (integers)

Step 2 — EMBEDDING LOOKUP
  Each token ID is looked up in a learned table → a vector of 768 numbers
  [15496] → [0.23, -0.41, 0.09, ..., 0.87]   (768 numbers)
  [11]    → [0.01,  0.88, -0.3, ..., 0.12]
  ...

Step 3 — FORWARD PASS THROUGH ~96 TRANSFORMER LAYERS
  Each layer:
    - Attention: tokens look at each other and update their representations
    - Feed Forward: Linear → GELU → Linear
    - Layer Norm: normalise the values for training stability
  After 96 layers: each token now has a rich contextual representation

Step 4 — OUTPUT LAYER
  The final representation of the last token
    → Linear layer → logits (one score per vocabulary token, ~50,000 scores)
    → Softmax → probability for each possible next word

Step 5 — SAMPLING
  Pick the next token based on the probability distribution
  (or pick the highest probability — called "greedy decoding")
  "Hello, how are you?" → " I"

Step 6 — REPEAT
  Feed the new token back in, predict the next one
  "Hello, how are you? I" → " am"
  "Hello, how are you? I am" → " doing"
  ... until a stop token or max length
```

This is the entire forward pass of an LLM at inference time.
Training is the same steps 1-4, followed by measuring the loss and
adjusting all the weights via backpropagation.

---

## 12. What You Do NOT Need to Know Yet

Do not go down these rabbit holes before continuing with the book:

- How matrix multiplication works mathematically
- How backpropagation actually computes gradients
- What vanishing gradients are (mentioned briefly in the book — don't worry)
- The mathematical details of GELU vs. ReLU
- How softmax is computed numerically
- The difference between batch normalisation and layer normalisation

The book mentions all of these but provides intuition, not derivations.
Your job is to recognise the terms and not be confused — not implement them.

---

## 13. Today's Recommended Resources

### Must-watch (in order):

1. **[3Blue1Brown — But what is a neural network? (18 min)](https://www.youtube.com/watch?v=aircAruvnKk)**
   If you watched this on Day 1, re-watch the section from 8:00-18:00.
   Today you should understand exactly what he means by "layers", "activations",
   and "the network learning a representation." It will hit differently now.

2. **[3Blue1Brown — Gradient descent, how neural networks learn (21 min)](https://www.youtube.com/watch?v=IHZwWFHWa-w)**
   This is video 2 in the series. Focuses on what training actually does.
   Watch after reading these notes. (This also covers Day 3 material — great preview.)

### Highly recommended:

3. **[Jay Alammar — The Illustrated BERT, ELMo, and co.](https://jalammar.github.io/illustrated-bert/)**
   Visual explanation of BERT (representation model) and how masked language
   modelling works. You don't need to understand everything — just the visuals.
   This is the author of your book — his visual style IS the book's visual style.

4. **[Jay Alammar — The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/)**
   Visual walkthrough of the GPT architecture.
   Browse it and look at the diagrams. You'll see these exact diagrams in the book.

---

## 14. Self-Check — Answer These Before Day 3

1. What does a single neuron actually compute? Describe it step by step.

2. Why are activation functions necessary? What goes wrong without them?

3. What is the difference between ReLU and GELU?
   Which one does the book's GPT implementation use?

4. What is the forward pass? What is NOT happening during the forward pass?

5. What are logits? How are they different from probabilities?

6. What is the key difference between supervised and unsupervised learning?

7. What is self-supervised learning, and why does it matter specifically for LLMs?

8. What is the difference between a representation model (BERT) and a
   generative model (GPT) at a conceptual level?

9. In next-word prediction, where do the labels come from?
   Does a human need to create them?

10. Walk through (in plain English) what happens when you type a message to an LLM.
    Cover: tokenisation, embedding, forward pass, output, sampling.

---

## 15. What's Coming Tomorrow

**Day 3** covers:

- Loss functions (what they measure and why they matter)
- Gradient descent (the intuition for how training converges)
- Overfitting (what it is and why it matters for fine-tuning)

Day 3 is where the training process you've been building toward becomes fully clear.
The 3Blue1Brown video #2 you watch today is the perfect preview for it.

---

_Notes for "Hands-On Large Language Models" — Jay Alammar & Maarten Grootendorst_  
_Prerequisite study plan — Day 2 of 7_

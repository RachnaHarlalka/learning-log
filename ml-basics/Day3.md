# Day 3 — ML Study Notes

## Topics: Loss Functions · Gradient Descent · Backpropagation · Overfitting

> **Goal for today:** Understand how a neural network actually _learns_ — what
> it means to measure error, what gradient descent does intuitively, and what
> overfitting looks like and why it matters for fine-tuning LLMs specifically.

> **Prerequisite check:** You should know what a forward pass is, what logits are,
> and what parameters/weights are from Days 1 and 2. If not, review before continuing.

---

## 1. The Training Loop — Full Picture First

Before diving into individual concepts, here is the complete training loop at a glance.
Every concept in today's notes is one piece of this loop.

```
┌─────────────────────────────────────────────────────────────────────┐
│                     THE TRAINING LOOP                               │
│                                                                     │
│  1. FORWARD PASS                                                    │
│     Feed a batch of training examples through the network           │
│     Get predictions (logits)                                        │
│                                                                     │
│  2. COMPUTE LOSS          ← Topic 2 today                          │
│     Compare predictions to correct labels                           │
│     Calculate a single number: "how wrong is the model right now?"  │
│                                                                     │
│  3. BACKWARD PASS (Backpropagation)  ← Topic 3 today               │
│     Work backwards through the network                              │
│     Calculate how much each parameter contributed to the error       │
│                                                                     │
│  4. UPDATE WEIGHTS (Gradient Descent)  ← Topic 4 today             │
│     Nudge each parameter slightly in a direction that reduces loss   │
│                                                                     │
│  Repeat steps 1-4 for every batch, for multiple epochs             │
│  Monitor training loss AND validation loss  ← Topic 5 today        │
│  Stop when validation loss stops improving                          │
└─────────────────────────────────────────────────────────────────────┘
```

The book uses this exact loop — you'll see it in Chapter 5 (pretraining) and
Chapter 6 (fine-tuning for classification). Knowing it now means you'll never
be lost when the book walks through training code.

---

## 2. Loss Functions

### 2.1 What is a loss function?

A loss function is a function that takes:

- The model's prediction
- The correct answer (the label)

And returns a **single number** representing how wrong the prediction was.
Lower loss = better prediction. The goal of training is to minimise this number.

```
loss_function(prediction, correct_answer) → a number (lower is better)
```

The loss function is the "judge" of the training process. Without it, there is no
signal — the model has no way of knowing whether it is improving or not.

### 2.2 Developer analogy

Think of the loss function as your CI/CD pipeline's test failure score.

```js
// Conceptually:
function lossFunction(modelPrediction, correctAnswer) {
  // Measures how far off the prediction is from the correct answer
  // Returns 0 if perfect, higher numbers for worse predictions
  return someErrorMeasure(modelPrediction, correctAnswer);
}
```

Training is the automated process of adjusting the model until this score is minimised.

### 2.3 The three loss functions you'll see in the book

---

#### Cross-Entropy Loss (most important — used everywhere)

Used for **classification tasks** and **language modelling** (next-word prediction).

**Intuition:** Cross-entropy measures the difference between:

- The probability distribution the model predicted
- The true distribution (which is 1.0 for the correct class and 0 for all others)

In plain English: "How confident was the model in the correct answer?
Penalise it more if it was confident in the WRONG answer."

```
Example — spam classifier:
  Correct answer: spam (class 1)

  Model A prediction: [0.05 (not spam), 0.95 (spam)]  → low loss
  Model B prediction: [0.90 (not spam), 0.10 (spam)]  → high loss
  Model C prediction: [0.50 (not spam), 0.50 (spam)]  → medium loss
```

The model is heavily penalised not just for being wrong,
but for being **confidently** wrong. This is a key property of cross-entropy.

**For LLMs (next-word prediction):**

```
Input:  "The cat sat on the"
Correct next token:  "mat"  (token ID: 1234)

Model's output probabilities over all 50,257 vocabulary tokens:
  token 1234 ("mat"):   0.72  → model is fairly confident, low loss
  token 891  ("floor"): 0.15
  token 5532 ("couch"): 0.08
  ... 50,254 more tokens

Cross-entropy loss = -log(0.72) ≈ 0.33  ← low, model is learning well
```

If the model assigned "mat" a probability of 0.01 (very wrong):

```
Cross-entropy loss = -log(0.01) ≈ 4.60  ← high, model is not learning yet
```

This is exactly what you see in the book's GPT pretraining:

```
Ep 1 (Step 000000): Train loss 9.781   ← very high, model knows nothing
Ep 1 (Step 000005): Train loss 8.111   ← decreasing, model is learning
...
Ep 10 (Step 000085): Train loss 0.391  ← low, model has learned well
```

The loss decreasing from 9.781 → 0.391 over training is cross-entropy loss
decreasing as the model gets better at predicting the correct next token.

---

#### Binary Cross-Entropy Loss

A simplified version of cross-entropy for **two-class (binary) problems**.

```
Used when output is:  spam / not-spam,  positive / negative,  yes / no

Model outputs a single probability:
  0.97 → almost certainly spam
  0.03 → almost certainly not spam

Binary CE loss:
  Correct = spam, predicted = 0.97  → low loss
  Correct = spam, predicted = 0.03  → high loss
```

The book uses this when implementing the logistic regression example in the appendix.

---

#### MSE — Mean Squared Error

Used for **regression tasks** (predicting a continuous number, not a class).

```
Predicting house price:
  Correct: $500,000
  Predicted: $480,000
  MSE contribution: (500,000 - 480,000)² = 400,000,000

Squaring does two things:
  1. Makes all errors positive (no cancellation)
  2. Penalises large errors more than small ones
```

You won't see this much in the LLM book since LLMs mostly do classification or
text generation — but you'll see it mentioned in the appendix.

---

### 2.4 Why not just use accuracy as the loss?

This is a question almost every developer asks. The answer is important.

**Accuracy** = percentage of correct predictions. Simple and intuitive.
Why not just minimise `1 - accuracy`?

**Because accuracy is not differentiable.**

To run gradient descent (step 4 in the training loop), you need to calculate
the gradient of the loss with respect to each weight — how much did each weight
contribute to the error? This requires the loss function to be **smooth and
continuous**, so that tiny changes to weights produce smooth, predictable changes
in loss.

Accuracy is a step function — it jumps from 0 to 1 with no smooth in-between.
You can't compute a meaningful gradient on it.

Cross-entropy is smooth and differentiable — tiny changes to weights produce
smooth changes in loss. This is why it's used even when the actual metric
you care about is accuracy.

```
The goal:         maximise accuracy
The proxy:        minimise cross-entropy loss

These are aligned — minimising CE loss reliably increases accuracy.
But only CE is mathematically suitable for gradient descent.
```

The book makes this point explicitly when fine-tuning for spam classification:

> "Because classification accuracy is not a differentiable function,
> we use cross-entropy loss as a proxy to maximise accuracy."

---

## 3. Backpropagation (Intuition Only)

Before gradient descent can update the weights, it needs to know **which direction
to nudge each weight.** That information comes from backpropagation.

### 3.1 The problem backpropagation solves

After the forward pass, you have a loss value — say, 2.45. But a model with billions
of parameters has billions of weights. The question is:

> For each individual weight, if I increase it slightly, does the loss go up or down?
> And by how much?

Answering this for billions of weights simultaneously, efficiently, is the job of
backpropagation.

### 3.2 The intuition

Backpropagation uses the **chain rule** from calculus to propagate the error
signal backwards through the network, layer by layer, from the output back to
the input.

**You do not need to understand the chain rule mathematically.**
What you need to understand conceptually:

```
Forward pass:    input → Layer1 → Layer2 → ... → LayerN → prediction → loss
Backward pass:   loss → LayerN → ... → Layer2 → Layer1 → (gradient for every weight)
```

The backward pass travels in the opposite direction, assigning **blame** —
figuring out how much each weight contributed to the final error.

The result is a **gradient** for every single weight in the network.
The gradient is a number that says:

- If positive: increasing this weight increases the loss (bad)
- If negative: increasing this weight decreases the loss (good)
- If close to zero: this weight had little effect on the loss

### 3.3 What you need to remember about it

- Backpropagation happens automatically. In PyTorch, it's one line: `loss.backward()`
- You never implement it manually. The framework handles it.
- The output of backpropagation is a gradient for every parameter.
- Those gradients are then used by gradient descent to update the weights.

```python
# The full training step in PyTorch — you'll see this exact pattern in the book:
logits = model(input_batch)           # 1. Forward pass
loss = cross_entropy(logits, labels)  # 2. Compute loss
optimizer.zero_grad()                 # 3. Clear old gradients
loss.backward()                       # 4. Backprop — compute gradients
optimizer.step()                      # 5. Gradient descent — update weights
```

That 5-line pattern is the heart of every training loop in the book.
You don't need to understand the internals of `loss.backward()` —
just know what it produces (gradients for every weight).

---

## 4. Gradient Descent

Gradient descent is the algorithm that uses the gradients computed by backpropagation
to actually update the weights and reduce the loss.

### 4.1 The landscape analogy (the most important intuition in all of ML)

Imagine a vast hilly landscape. Every point on the landscape represents a particular
configuration of all the model's weights. The **height** at each point represents
the **loss** — the error.

```
High altitude = high loss (model is wrong)
Low altitude  = low loss  (model is correct)
Your goal: find the lowest valley (minimum loss)
```

You are blindfolded. You can feel the slope under your feet but you can't see.

**Gradient descent says:** always step in the downhill direction.

1. Feel the slope under your feet (calculate the gradient — which direction is downhill?)
2. Take one step in that direction (update all weights slightly)
3. You are now at a new position on the landscape (lower loss, hopefully)
4. Feel the slope again
5. Repeat thousands of times
6. Eventually you reach a valley (low loss — model has converged)

The gradient (from backpropagation) IS the slope. It tells you, for each weight,
which direction moves you downhill.

### 4.2 The weight update formula

The actual update is simple:

```
new_weight = old_weight - (learning_rate × gradient)
```

- If gradient is positive (going uphill this direction) → subtract → move left
- If gradient is negative (going downhill this direction) → subtract negative → move right

The gradient always points uphill. Subtracting it moves you downhill.

### 4.3 The learning rate — the most important hyperparameter

The learning rate controls **how big a step to take** each time.

```
learning_rate too HIGH:
  - You overshoot the valley
  - Jump to the other side of the hill
  - Loss bounces around, never converges
  - Or diverges completely (loss goes to infinity)

learning_rate too LOW:
  - Tiny baby steps
  - Takes forever to converge
  - May get stuck in small local valleys

learning_rate just right:
  - Smooth, steady decrease in loss
  - Converges to a good solution in reasonable time
```

Visually:

```
Loss
│
│\
│ \        Too high LR: bounces
│  \  /\/\/
│   \/      Just right: smooth descent
│    \___
│         Too low LR: very slow, similar shape but stretched over many more steps
└────────────────────── Training steps
```

The book's GPT pretraining uses `lr=0.0004` (0.04% step size per update).
Fine-tuning typically uses an even smaller learning rate because you don't want to
aggressively overwrite what the model already knows.

### 4.4 Variants of gradient descent you'll see in the book

**SGD — Stochastic Gradient Descent**

Instead of computing the gradient on the entire training dataset at once
(which would be impossibly expensive), you compute it on a small random subset
called a **batch** (typically 16–512 examples).

This is stochastic (random) because you're using a random sample, not the full data.
The gradient estimate is noisy but that's actually fine — and the compute savings
are enormous.

**Mini-batch gradient descent** is what's almost always used in practice.
"SGD" in modern frameworks often means this — gradient descent on batches.

**Adam / AdamW (what the book uses)**

A more sophisticated version of SGD that:

- Maintains a running average of past gradients (momentum)
- Adapts the learning rate separately for each parameter
- Converges faster and more reliably than vanilla SGD for most problems

**AdamW** is Adam with an additional technique called weight decay (a form of
regularisation to prevent overfitting — more on this below).

The book's GPT training uses AdamW:

```python
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=0.0004,        # learning rate
    weight_decay=0.1  # regularisation strength
)
```

You don't need to know how Adam works internally. Just know:

- It's a smarter, more reliable gradient descent variant
- It's the standard choice for training LLMs
- AdamW adds weight decay to help prevent overfitting

### 4.5 What "convergence" means

A model has **converged** when the loss stops meaningfully decreasing with more
training. The landscape analogy: you've reached a valley and further steps just
bounce you around the bottom without going lower.

```
Epoch 1: loss = 9.78
Epoch 2: loss = 7.05
Epoch 3: loss = 5.20
Epoch 4: loss = 3.81
Epoch 5: loss = 2.44
...
Epoch 18: loss = 0.41
Epoch 19: loss = 0.40
Epoch 20: loss = 0.40   ← converged, stop training
```

---

## 5. Overfitting — The Most Important Practical Concept

### 5.1 What is it?

Overfitting is when a model learns the **training data too well** — including
its noise, quirks, and random accidents — instead of learning the underlying
general pattern.

The result: the model performs excellently on training data it has seen,
but poorly on new, unseen data. It has memorised instead of generalised.

### 5.2 The developer analogy

Imagine writing a function that must pass an existing test suite AND work on
future inputs. Overfitting is like this:

```js
// OVERFITTED function — passes all existing tests but is useless for new inputs
function predictLabel(input) {
  // Hardcoded lookup table of every training example seen
  const memorised = {
    "great film": "positive",
    "awful film": "negative",
    "loved it": "positive",
    // ... 10,000 more memorised examples
  };
  return memorised[input] ?? "unknown"; // fails on any new input
}

// GENERALISED function — learned the actual pattern
function predictLabel(input) {
  // Applies a learned rule: positive words → positive, negative words → negative
  return learnedRule(input);
}
```

The overfitted model aces the training set but cannot handle anything new.
The generalised model performs slightly less perfectly on training data but
works well on inputs it has never seen.

### 5.3 How you detect overfitting — the train/val/test split

This is why the dataset is always split into three parts:

```
Full dataset (e.g. 100,000 examples)
  │
  ├── Training set (~70-80%)  ← model sees this during training
  │     Used to compute loss and update weights
  │
  ├── Validation set (~10-15%)  ← model NEVER trains on this
  │     Used to measure generalisation during training
  │     Checked after each epoch to monitor overfitting
  │
  └── Test set (~10-15%)  ← used exactly ONCE at the very end
        Final honest evaluation of real-world performance
        Never used to make any training decisions
```

**Why separate validation and test sets?**

If you keep tuning your model based on validation performance, you inadvertently
start optimising for the validation set too. The test set is kept completely untouched
until the very final evaluation — it represents a true, unbiased measure of real-world
performance.

### 5.4 The overfitting signal: training loss vs. validation loss

This is the key diagnostic. The book shows this exact chart when training GPT.

```
Epoch 1:  Train loss 9.78  | Val loss 9.93   ← both high, model knows nothing
Epoch 2:  Train loss 6.66  | Val loss 7.05   ← both decreasing, learning well ✓
Epoch 3:  Train loss 5.00  | Val loss 6.20   ← both still decreasing ✓
...
Epoch 8:  Train loss 1.20  | Val loss 6.39   ← GAP EMERGING — overfitting! ⚠
Epoch 9:  Train loss 0.54  | Val loss 6.39   ← train still drops, val stagnates ⚠
Epoch 10: Train loss 0.39  | Val loss 6.45   ← val is INCREASING — clear overfit ✗
```

The **gap between training loss and validation loss** is the overfitting signal.

```
Good training:
  Train loss: ↓↓↓
  Val loss:   ↓↓↓  (similar trajectory, small gap)

Overfitting:
  Train loss: ↓↓↓↓↓↓↓  (keeps going down)
  Val loss:   ↓↓ → flat → ↑  (stops improving or gets worse)
```

The book confirms this directly:

> "The losses start to diverge past the second epoch. This divergence and the fact
> that the validation loss is much larger than the training loss indicate that the
> model is overfitting to the training data."

### 5.5 Underfitting — the opposite problem

**Underfitting** is when the model is too simple to learn the pattern at all.
Both training AND validation loss remain high. The model hasn't learned anything useful.

```
Underfitting:
  Train loss: stays high (e.g. 8.5 after many epochs)
  Val loss:   stays high (e.g. 8.7 after many epochs)
  → Model hasn't learned the pattern

Overfitting:
  Train loss: low  (e.g. 0.3)
  Val loss:   high (e.g. 6.5)
  → Model memorised training data, doesn't generalise

Just right (good generalisation):
  Train loss: low  (e.g. 0.4)
  Val loss:   low  (e.g. 0.5)
  → Model learned the underlying pattern
```

The goal is always: train loss low AND val loss also low, with a small gap.

---

## 6. Techniques to Prevent Overfitting

The book uses all three of these. Know them at a conceptual level.

### 6.1 Dropout

**What it is:** During training, randomly "turn off" a percentage of neurons —
set their output to zero — for each forward pass. A different random set of neurons
is dropped each time.

**Why it works:** The network can no longer rely on any single neuron.
It's forced to learn **redundant representations** — multiple paths to the same
answer. This prevents over-specialisation.

**Key behaviour:**

- Only active during **training** — disabled at inference time
- You set a **dropout rate** (e.g. 0.1 means 10% of neurons dropped)
- Common rates: 0.1–0.2 for LLMs, 0.5 for smaller models

The book applies dropout in the attention mechanism of GPT:

> "Dropout in deep learning is a technique where randomly selected hidden layer
> units are ignored during training, effectively 'dropping' them out.
> It's important to emphasise that dropout is only used during training and is
> disabled afterward."

**Analogy:** Imagine studying for an exam while randomly covering 20% of your
notes each time you review. You're forced to understand the material deeply enough
that no single note is a single point of failure.

### 6.2 Weight Decay (Regularisation)

**What it is:** A penalty added to the loss function that discourages weights
from becoming very large.

**Why it works:** Models with very large weights tend to overfit — they've learned
to be extremely sensitive to specific patterns in training data. Keeping weights small
forces the model to find simpler, more generalisable patterns.

**In practice:** The AdamW optimiser's `weight_decay` parameter does this automatically.

The book's training uses `weight_decay=0.1`:

```python
optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=0.0004,
    weight_decay=0.1   # ← this is regularisation preventing overfitting
)
```

**Analogy:** A rule during training that says "use the simplest explanation that
fits the data." Occam's Razor baked into the learning algorithm.

### 6.3 Early Stopping

**What it is:** Monitor validation loss during training. Stop training when
validation loss starts to increase, even if training loss is still decreasing.

**Why it works:** The point where validation loss stops improving is the point
where the model has learned the general pattern but hasn't yet memorised the
training noise.

```
Epoch 1:  val_loss = 9.93
Epoch 2:  val_loss = 7.05  ↓ keep training
Epoch 3:  val_loss = 6.20  ↓ keep training
Epoch 4:  val_loss = 6.39  ↑ STOP — validation loss went up
```

**The practical advice from the book:**

> "If the model overfits after the first few epochs as a loss plot shows, you may
> need to reduce the number of epochs. Conversely, if the trendline suggests that
> the validation loss could improve with further training, you should increase the
> number of epochs."

---

## 7. Why Overfitting Matters Specifically for Fine-tuning LLMs

This is where everything connects to what you'll actually be doing with the book.

When you fine-tune an LLM on a small task-specific dataset, overfitting is
the main practical problem you'll face.

**The scenario:**

- Pre-trained model: trained on trillions of tokens — generalises well
- Fine-tuning dataset: 1,000 labelled spam emails — tiny

```
Training the model too long on 1,000 examples:
  → Model memorises those specific 1,000 emails
  → Stops generalising to real spam patterns
  → Test accuracy drops even as training accuracy approaches 100%
```

**The signs of good fine-tuning:**

> "The close proximity of the two lines [training accuracy and validation accuracy]
> throughout the epochs suggests that the model does not overfit the training data
> very much." — the book, Chapter 6

**Techniques used in practice:**

- Freeze most of the pre-trained model's layers, only fine-tune the last few
- Use a very small learning rate (don't aggressively overwrite pre-trained knowledge)
- Use dropout during fine-tuning
- Stop early based on validation loss
- Use the smallest fine-tuning dataset that achieves your required performance

---

## 8. The Vanishing Gradient Problem (One Mention Now, Saves Confusion Later)

The book mentions this in Chapter 4. You don't need deep knowledge — just
understand what it is.

In a very deep network, the gradient calculated by backpropagation gets smaller
and smaller as it travels backwards through many layers. By the time it reaches
the early layers, the gradient is nearly zero — those weights barely update at all.
The early layers can't learn. This is the **vanishing gradient problem.**

```
From the book (Chapter 4):
  Layer 5 gradient: 1.32   ← near output, large gradient, updates well
  Layer 4 gradient: 0.26
  Layer 3 gradient: 0.32
  Layer 2 gradient: 0.20
  Layer 1 gradient: 0.22   ← far from output, small gradient, barely updates

  (Without shortcut connections, layer 1 gradient drops to 0.0002 — effectively zero)
```

**The solution used in modern LLMs:** Shortcut connections (also called skip or
residual connections) — a direct path that lets the gradient "skip" layers and
flow back to early layers without vanishing. This is a core part of the GPT and
Transformer architecture. The book implements this in Chapter 4.

You do NOT need to understand the math. Just remember:

- Very deep networks have a gradient flow problem
- Shortcut connections solve it
- Every modern LLM uses them
- The book implements and visualises them

---

## 9. Full Vocabulary — Day 3 Cheatsheet

| Term                     | Plain English                                                        |
| ------------------------ | -------------------------------------------------------------------- |
| **Loss function**        | Measures how wrong the model's predictions are (lower = better)      |
| **Cross-entropy loss**   | Loss function for classification and next-word prediction            |
| **Binary cross-entropy** | Cross-entropy for two-class problems                                 |
| **MSE**                  | Mean Squared Error — loss for continuous output (regression)         |
| **Gradient**             | A number per weight that says which direction increases the loss     |
| **Backpropagation**      | Algorithm to compute gradients for all weights simultaneously        |
| **Gradient descent**     | Algorithm that updates weights using gradients to reduce loss        |
| **Learning rate**        | How big a step to take each weight update (hyperparameter)           |
| **SGD**                  | Stochastic Gradient Descent — gradient descent on mini-batches       |
| **Adam / AdamW**         | Smarter gradient descent variant used for LLMs (AdamW = standard)    |
| **Convergence**          | When loss stops meaningfully decreasing — training is done           |
| **Epoch**                | One full pass through the entire training dataset                    |
| **Batch**                | A small random subset of training data used for one weight update    |
| **Overfitting**          | Model memorises training data, fails on new data                     |
| **Underfitting**         | Model too simple, fails even on training data                        |
| **Training loss**        | Loss measured on data the model was trained on                       |
| **Validation loss**      | Loss measured on held-out data the model never trained on            |
| **Test set**             | Data held out for final evaluation only — never used during training |
| **Dropout**              | Randomly disabling neurons during training to prevent overfitting    |
| **Weight decay**         | Penalty on large weights — forces simpler, more general patterns     |
| **Early stopping**       | Stop training when validation loss stops improving                   |
| **Vanishing gradient**   | Gradients become near-zero in early layers of deep networks          |
| **Shortcut connections** | Skip connections that allow gradients to flow through deep networks  |

---

## 10. Connecting Today to the Book's Code

You will see this training loop pattern in Chapters 5 and 6.
Read it now, understand every line:

```python
for epoch in range(num_epochs):             # repeat for each epoch
    for batch in train_loader:              # for each mini-batch
        input_batch, labels = batch

        # 1. Forward pass
        logits = model(input_batch)

        # 2. Compute loss
        loss = F.cross_entropy(logits, labels)

        # 3. Clear old gradients (MUST do this — otherwise they accumulate)
        optimizer.zero_grad()

        # 4. Backpropagation — computes gradients for all weights
        loss.backward()

        # 5. Gradient descent — updates all weights
        optimizer.step()

    # After each epoch — evaluate on validation set
    val_loss = evaluate(model, val_loader)
    print(f"Epoch {epoch}: train_loss={loss:.2f}, val_loss={val_loss:.2f}")
    # Watch for val_loss increasing — that's the overfitting signal
```

You don't need to be able to write this from scratch — you just need to read it
and know exactly what each line does. You can do that now.

---

## 11. Today's Recommended Resources

### Must-watch:

1. **[3Blue1Brown — Gradient Descent, How Neural Networks Learn (21 min)](https://www.youtube.com/watch?v=IHZwWFHWa-w)**
   If you watched this at the end of Day 2, re-watch from 8:00 onwards.
   Focus on the landscape analogy and the learning rate section.
   His visualisation of the loss landscape is the best available anywhere.

2. **[StatQuest — Overfitting (8 min)](https://www.youtube.com/watch?v=EuBBz3bI-aA)**
   Josh Starmer explains overfitting with simple visuals.
   Pay attention to the train vs. validation curve — the exact shape you'll see in the book.

### Highly recommended:

3. **[StatQuest — Cross Entropy (10 min)](https://www.youtube.com/watch?v=6ArSys5qHAU)**
   The clearest explanation of why cross-entropy is used for classification.
   Directly relevant — the book's loss function throughout.

---

## 12. Self-Check — Answer These Before Day 4

1. Describe the 5-step training loop from memory (forward pass → loss → ... → update).

2. What does a loss function measure? What does it mean when the loss is 0?

3. Why can't you use accuracy directly as the loss function?

4. What does backpropagation compute? What does it take as input? What does it output?

5. Describe the "hilly landscape" analogy for gradient descent in your own words.

6. What happens if the learning rate is too high? What happens if it's too low?

7. What is overfitting? Write the developer analogy (unit test cheating) in your own words.

8. You're training a model and you see this:

   ```
   Epoch 5:  train_loss = 0.4,  val_loss = 0.5  → ?
   Epoch 6:  train_loss = 0.3,  val_loss = 0.6  → ?
   Epoch 7:  train_loss = 0.2,  val_loss = 0.7  → ?
   ```

   What is happening? What should you do?

9. What does dropout do and when is it active (training vs. inference)?

10. What is weight decay and why does AdamW use it?

11. What is the vanishing gradient problem and what solves it in modern LLMs?

---

## 13. What's Coming Tomorrow

**Day 4** covers:

- Vectors and matrices (what they are, why ML uses them)
- Embeddings (the single most important concept for understanding LLMs)
- Tensors (what PyTorch calls its multi-dimensional arrays)
- Why "similar words have similar vectors" and how that emerges from training

Day 4 is where the mathematical vocabulary of the book gets established.
After Day 4, you'll understand what "a 768-dimensional embedding vector" means
and why it matters.

---

_Notes for "Hands-On Large Language Models" — Jay Alammar & Maarten Grootendorst_
_Prerequisite study plan — Day 3 of 7_

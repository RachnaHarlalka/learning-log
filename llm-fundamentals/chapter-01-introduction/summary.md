# Chapter 1 — Revision Card

> **Use this when:** You come back after days, weeks, or months and need a quick refresh.
> **Reading time:** ~10 minutes

---

## The Story in One Paragraph

Language AI is the field of making computers understand and generate human language. The challenge was always converting unstructured text into numbers that preserve meaning. We went from simple word-counting (Bag-of-Words, 1950s) → learned word meaning vectors (word2vec, 2013) → sequential context-aware processing (RNNs + Attention, 2014) → fully parallel attention-only models (Transformer, 2017). The Transformer gave birth to two model families: BERT (encoder-only, understands text) and GPT (decoder-only, generates text). GPT scaled up into ChatGPT in 2022, causing a mass adoption explosion and kicking off the modern LLM era.

---

## The 7-Step Evolution

```
1. Bag-of-Words    (1950s–2000s)  Count words → sparse vectors. Ignores meaning & order.
2. word2vec        (2013)         Neural net → dense semantic embeddings. Static per word.
3. RNN             (pre-2017)     Sequential processing. Context-aware but slow to train.
4. Attention       (2014)         Dynamic focus on relevant words. Added on top of RNNs.
5. Transformer     (2017) ⭐       Attention only. Fully parallel. Fast. Scalable.
6. BERT            (2018)         Encoder-only. Bidirectional understanding. Embeddings.
7. GPT             (2018→now)     Decoder-only. Generates text. Scaled to ChatGPT.
```

---

## Two Model Types — Know This Cold

|                  | 🔵 Representation Models           | 🔴 Generative Models         |
| ---------------- | ---------------------------------- | ---------------------------- |
| **Architecture** | Encoder-only                       | Decoder-only                 |
| **Training**     | Masked Language Modeling           | Next Token Prediction        |
| **Output**       | Embeddings (vectors)               | Text                         |
| **Examples**     | BERT, RoBERTa, all-MiniLM          | GPT-4, Llama, Mistral, Phi-3 |
| **Use for**      | Classification, search, clustering | Chat, summarization, code    |

---

## LLM Training — 2 Steps

```
STEP 1: PRE-TRAINING  (done by big labs — costs millions)
  → Train on trillions of tokens from the internet
  → Result: Foundation Model (understands language, doesn't follow instructions)

STEP 2: FINE-TUNING  (you can do this)
  → Train further on smaller, task-specific data
  → Result: Task-specific model (follows instructions, classifies, etc.)

As a dev: you skip Step 1 entirely. You use pre-trained models and optionally fine-tune.
```

---

## Accessing LLMs

|                   | Proprietary API        | Open Model             |
| ----------------- | ---------------------- | ---------------------- |
| **Examples**      | OpenAI, Claude, Gemini | Llama, Mistral, Phi-3  |
| **GPU needed?**   | ❌ No                  | ✅ Yes (or use Colab)  |
| **Cost**          | 💰 Pay per token       | 🆓 Free                |
| **Data privacy**  | Sent to provider       | Stays local            |
| **Fine-tunable?** | ❌ No                  | ✅ Yes                 |
| **Best for**      | Quick start, best perf | Privacy, control, cost |

---

## Critical Terms — One-Liners

| Term                 | One-liner                                                           |
| -------------------- | ------------------------------------------------------------------- |
| **Token**            | A chunk of text the model reads — roughly a word or part of a word  |
| **Embedding**        | A list of numbers representing the _meaning_ of text                |
| **Attention**        | Mechanism to dynamically focus on the most relevant words           |
| **Self-Attention**   | Each token in a sequence attends to all other tokens simultaneously |
| **Context Window**   | Max tokens the model can process in one request                     |
| **Parameters**       | The numbers inside the model that encode its knowledge              |
| **Hallucination**    | LLM confidently generating false information                        |
| **RAG**              | Grounding LLM responses in real external documents                  |
| **Hugging Face**     | GitHub for AI models — where open models live                       |
| **Foundation Model** | Pre-trained base model before task-specific fine-tuning             |

---

## The First Code Pattern — Memorize This Shape

```python
from transformers import pipeline

# Load model
generator = pipeline("text-generation", model="microsoft/Phi-3-mini-4k-instruct", ...)

# Send message — same format across ALL LLM APIs
messages = [
    {"role": "system",    "content": "You are a helpful assistant."},
    {"role": "user",      "content": "Your question here"},
    {"role": "assistant", "content": "Previous response (for multi-turn)"},
    {"role": "user",      "content": "Follow-up question"},
]

output = generator(messages)
print(output[0]["generated_text"])
```

---

## Responsible AI — 5 Things to Remember as a Builder

1. **Hallucination** — LLMs make things up confidently. Never trust without verification.
2. **Bias** — Models inherit biases from training data. Test with diverse inputs.
3. **Privacy** — Proprietary APIs receive your data. Use open models for sensitive data.
4. **Transparency** — Disclose AI involvement to users, especially in high-stakes contexts.
5. **Regulation** — EU AI Act applies if your product is used in Europe. Plan for compliance.

---

## Self-Check — Answer From Memory

1. What's the difference between BERT and GPT?
2. What specific problem did the Transformer solve that RNNs couldn't?
3. What are the 2 steps of LLM training, and which one will you do as a dev?
4. Your app has sensitive medical data. OpenAI API or open model — which do you choose and why?
5. What is a context window and why does it matter when building a chatbot?
6. A user searches "how do I reset my account?" and you want to find relevant help docs even if they don't use those exact words. What type of model do you use?

---

_For deep revision → [`notes.md`](./notes.md)_
_For hands-on practice → [`practice/ch01_practice.ipynb`](./practice/ch01_practice.ipynb)_

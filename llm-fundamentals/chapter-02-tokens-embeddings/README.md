# Chapter 2 — Tokens and Embeddings

> **Difficulty:** 🟡 Beginner-Intermediate — builds directly on Chapter 1
> **Estimated Time:** 3 days × 1 hour
> **Hands-on:** Yes — you will tokenize text, explore embeddings, and build a song recommender

---

## 🎯 What You Will Learn

By the end of this chapter you will be able to:

- [ ] Explain what a token is and how a tokenizer converts text into token IDs
- [ ] Describe the 4 types of tokenization: word, subword, character, byte
- [ ] Explain what BPE (Byte Pair Encoding) and WordPiece are
- [ ] Read and decode token IDs using the Hugging Face tokenizer
- [ ] Explain the difference between static and contextualized embeddings
- [ ] Produce sentence embeddings using `sentence-transformers`
- [ ] Explain how word2vec is trained (skip-gram + negative sampling)
- [ ] Build a simple recommendation system using word2vec embeddings

---

## 📅 3-Day Study Plan

| Day       | Activity                                                       | Time    |
| --------- | -------------------------------------------------------------- | ------- |
| **Day 1** | Read book Chapter 2, first half (pages 37–56) — tokenization   | ~60 min |
| **Day 2** | Read book Chapter 2, second half (pages 57–71) — embeddings    | ~60 min |
| **Day 3** | Read `notes.md` → open `practice/ch02_practice.ipynb` on Colab | ~60 min |

After Day 3, read `summary.md` once to lock it in.

---

## 📂 Files in This Chapter

| File                           | When to Use                                                   |
| ------------------------------ | ------------------------------------------------------------- |
| `notes.md`                     | After reading the book — reinforcement and deeper explanation |
| `summary.md`                   | After completing the chapter — and every time you revisit     |
| `practice/ch02_practice.ipynb` | Day 3 — hands-on coding exercises                             |

---

## 🔑 Key Concepts Introduced

`Token` · `Token ID` · `Tokenizer` · `Vocabulary` · `Subword Tokenization` · `BPE` · `WordPiece` · `SentencePiece` · `Special Tokens` · `[CLS]` · `[SEP]` · `[UNK]` · `<|endoftext|>` · `Token Embedding` · `Static Embedding` · `Contextualized Embedding` · `Text Embedding` · `Sentence Embedding` · `word2vec` · `Skip-gram` · `Negative Sampling` · `Contrastive Training` · `Embedding Matrix` · `sentence-transformers` · `Gensim`

---

## ➡️ What Comes Next

**Chapter 3 — Looking Inside Large Language Models**

Chapter 2 covered how text becomes tokens and tokens become numbers. Chapter 3 goes inside the model itself — how does an LLM actually process those numbers and generate text? You'll see attention heads, feedforward layers, and the full forward pass of a Transformer.

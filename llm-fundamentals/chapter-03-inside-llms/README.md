# Chapter 3 — Looking Inside Large Language Models

> **Difficulty:** 🟡 Intermediate — builds directly on Chapters 1 & 2
> **Estimated Time:** 3 days × 1 hour
> **Hands-on:** Yes — you will inspect model internals, measure KV cache speedup, and trace a full forward pass

---

## 🎯 What You Will Learn

By the end of this chapter you will be able to:

- [ ] Explain what a forward pass is and what happens during each step
- [ ] Describe the 3 major components of a Transformer LLM
- [ ] Explain what the LM Head does and how the next token is selected
- [ ] Explain what autoregressive generation means
- [ ] Describe what happens inside a Transformer block (attention + feedforward)
- [ ] Explain self-attention in 2 steps: relevance scoring and combining information
- [ ] Explain what Query, Key, and Value matrices are
- [ ] Describe multi-head, multi-query, and grouped-query attention
- [ ] Explain what the KV cache is and why it dramatically speeds up generation
- [ ] Explain what positional embeddings are and why RoPE is better than absolute

---

## 📅 3-Day Study Plan

| Day       | Activity                                                                                        | Time    |
| --------- | ----------------------------------------------------------------------------------------------- | ------- |
| **Day 1** | Read book Chapter 3, first half (pages 73–91) — forward pass, autoregression, Transformer block | ~60 min |
| **Day 2** | Read book Chapter 3, second half (pages 91–107) — attention deep dive, recent improvements      | ~60 min |
| **Day 3** | Read `notes.md` → open `practice/ch03_practice.ipynb` on Colab                                  | ~60 min |

After Day 3, read `summary.md` once to lock everything in.

---

## 📂 Files in This Chapter

| File                           | When to Use                                                            |
| ------------------------------ | ---------------------------------------------------------------------- |
| `notes.md`                     | After reading the book — deep explanations with dev-friendly analogies |
| `summary.md`                   | After completing the chapter — and every time you revisit              |
| `practice/ch03_practice.ipynb` | Day 3 — hands-on: inspect model internals, measure KV cache            |

---

## 🔑 Key Concepts Introduced

`Forward Pass` · `Autoregressive Generation` · `LM Head` · `Decoding Strategy` · `Greedy Decoding` · `Temperature` · `Transformer Block` · `Attention Layer` · `Feedforward Network` · `Self-Attention` · `Query` · `Key` · `Value` · `Multi-Head Attention` · `Multi-Query Attention` · `Grouped-Query Attention` · `KV Cache` · `Positional Embeddings` · `RoPE` · `Flash Attention` · `Residual Connection` · `Layer Normalization` · `RMSNorm` · `Softmax` · `Context Length`

---

## ➡️ What Comes Next

**Chapter 4 — Text Classification**

Chapter 3 opened the black box of the LLM. Chapter 4 is where Part II begins — applying LLMs to real tasks. Text classification (sentiment analysis, spam detection, topic labeling) is the first practical application, using both generative and representation models.

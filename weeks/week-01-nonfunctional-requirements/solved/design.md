# Week 1 Design: Twitter/X home timeline

> 30 minutes on your own first. Then watch at most one video and add anything you missed, marked **(after video)**.

## 1. Requirements
**Functional:**

**Nonfunctional, as SLOs:**
| Requirement | Target | Why |
|---|---|---|
| Timeline load | | |
| Post delivery | | |
| Availability | | |
| Durability | | |

## 2. Estimates
- Posts/s (average and peak):
- Timeline reads/s:
- Fan-out writes/s (average and peak):
- Timeline cache memory:

## 3. Data model: system of record vs derived

## 4. Write path
```
client -> ...
```

## 5. Read path

## 6. Fault tolerance
**Fan-out worker crash (no missing, no duplicates):**

**Cache node lost:**

**Availability zone lost:**

## 7. Overload protection

## 8. Observability

## 9. Evolution at 10x

## 10. Maintainability
**Operability:**

**Simplicity:**

**Evolvability (switching to ranked timelines safely):**

## Interviewer follow-ups
**F1. Deleting a post:**

**F2. Ranking:**

**F3. Cold cache restart:**

**F4. Compute everything on read?**

## Chapter concepts used
-

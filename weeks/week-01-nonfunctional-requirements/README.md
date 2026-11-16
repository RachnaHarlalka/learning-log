# Week 1: Defining Nonfunctional Requirements

**Read:** DDIA Ch2
**Notes:** [notes.md](notes.md) is a summary of the full chapter text you shared (20 sections).
**Videos:** [videos.md](videos.md) lists real links, matched to each section of the notes.

## Folder layout
| Path | What it's for | Who writes it |
|---|---|---|
| [notes.md](notes.md) | Summarized chapter notes, plus a **My additions** section | Summary given, additions yours |
| [videos.md](videos.md) | Video for each topic, from your 3 channels, or others where they don't cover it | Given |
| [questions/mcqs.md](questions/mcqs.md) | 40 scenario-based MCQs. **Answer directly under each question.** | Given, answers yours |
| [questions/questions.md](questions/questions.md) | Part A: 14 interview scenarios · Part B: Python builds · Part C: a full design round | Given |
| [solved/](solved/) | **Your attempts**: written answers, design, code | You |
| [solutions/](solutions/) | MCQ key, model answers, design, and code | Given |

> **Rule:** finish your attempt *before* opening `solutions/`.

## Order of work (5–6 days)
1. Read the chapter alongside [notes.md](notes.md). Watch videos from [videos.md](videos.md) at the points it suggests.
2. **MCQs:** type your letter on the **Your answer:** line under each question in [questions/mcqs.md](questions/mcqs.md), then check your score from the repo root:
   `python3 tools/check_mcqs.py weeks/week-01-nonfunctional-requirements`
3. **Part A:** answer the interview scenarios in [solved/answers.md](solved/answers.md). Answer them out loud first if you can.
4. **Part B:** builds in [solved/code/](solved/code/). Run the tests until they pass.
5. **Part C:** the design round in [solved/design.md](solved/design.md).
6. Compare with [solutions/](solutions/), fill in the Review table, and watch the chapter recap video.

## Running the tests
The tests use no extra libraries. Run them from this week's folder:
```bash
python3 solved/code/test_week01.py                        # tests YOUR code
WEEK_IMPL=solutions python3 solved/code/test_week01.py    # tests the reference code
```

## Checklist
- [ ] Notes read and **My additions** written
- [ ] Videos: the suggested minimum list in [videos.md](videos.md)
- [ ] MCQs: score ≥ 32/40 (attempts: __ / __)
- [ ] Part A: scenarios S1–S14 answered (about 15 minutes each)
- [ ] B1 fan-out (pull, push, hybrid): tests pass
- [ ] B2 percentiles and histograms: tests pass
- [ ] B3 queueing and retry storm: tests pass
- [ ] B4 reliability maths: tests pass
- [ ] B5 capacity planning: tests pass
- [ ] B6 fault injection (stretch)
- [ ] B7 reversible migration: tests pass
- [ ] Part C design round attempted
- [ ] Compared with solutions and filled in the Review table

# Week 0: Trade-offs in Data Systems Architecture

**Read:** DDIA Ch1
**Notes:** [notes.md](notes.md) is a summary of the full chapter text you shared (16 sections).
**Videos:** [videos.md](videos.md) lists real links, matched to each section of the notes.

## Folder layout
| Path | What it's for | Who writes it |
|---|---|---|
| [notes.md](notes.md) | Summarized chapter notes, plus a **My additions** section | Summary given, additions yours |
| [videos.md](videos.md) | Video for each topic, from your 3 channels, or others where they don't cover it | Given |
| [questions/mcqs.md](questions/mcqs.md) | 32 scenario-based MCQs that test whether you can apply the concepts | Given |
| [questions/questions.md](questions/questions.md) | Part A: 12 interview scenarios · Part B: Python builds · Part C: a full design round with follow-ups | Given |
| [solved/](solved/) | **Your attempts**: MCQ answers, written answers, design, code | You |
| [solutions/](solutions/) | MCQ key, reference answers, design, and code | Given |

> **Rule:** finish your attempt in `solved/` *before* opening `solutions/`.

## Order of work (4–5 days)
1. Read the chapter alongside [notes.md](notes.md). Watch videos from [videos.md](videos.md) at the points it suggests.
2. **MCQs:** answer them in [solved/mcq-answers.md](solved/mcq-answers.md), then check your score: `python3 tools/check_mcqs.py weeks/week-00-tradeoffs` (from the repo root). Re-read the topics you got wrong.
3. Part A: answer the interview scenarios in [solved/answers.md](solved/answers.md). Answer them out loud first if you can, as in a real interview.
4. Part B builds in [solved/code/](solved/code/). Run the tests until they pass.
5. Part C design in [solved/design.md](solved/design.md)
6. Compare with [solutions/](solutions/), fill in the Review table, and watch the chapter recap video

## Running the tests
The tests use no extra libraries. Run them from this week's folder:
```bash
python3 solved/code/test_week00.py                        # tests YOUR code
WEEK_IMPL=solutions python3 solved/code/test_week00.py    # tests the reference code
```

## Checklist
- [ ] Notes read and **My additions** written
- [ ] Videos: the suggested minimum list in [videos.md](videos.md)
- [ ] MCQs: score ≥ 26/32 (attempts: __ / __)
- [ ] Part A: scenarios S1–S12 answered (about 15 minutes each)
- [ ] B1 OLTP vs OLAP: tests pass
- [ ] B2 ETL pipeline: tests pass
- [ ] B3 derived data: tests pass
- [ ] B4 cloud cost model: tests pass
- [ ] B5 network vs function call (stretch)
- [ ] B6 right to be forgotten: tests pass
- [ ] B7 mini distributed tracing (stretch)
- [ ] Part C design attempted
- [ ] Compared with solutions and filled in the Review table

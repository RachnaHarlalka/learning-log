"""Score a week's MCQs without revealing the right answers.

Answers are read from the "Your answer:" line under each question in
<week>/questions/mcqs.md, and compared with <week>/solutions/mcq-answers.md.

Usage (from the repo root):
    python3 tools/check_mcqs.py weeks/week-00-tradeoffs
"""

import re
import sys
from pathlib import Path

KEY_ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([A-Da-d]?)\s*\|")
QUESTION = re.compile(r"^\*\*(\d+)\.\*\*")
MY_ANSWER = re.compile(r"\*\*Your answer:\*\*\s*([A-Da-d])?\b")


def read_key(path):
    """{question_number: letter} from the answer-key table."""
    key = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = KEY_ROW.match(line)
        if match:
            key[int(match.group(1))] = match.group(2).upper()
    return key


def read_my_answers(path):
    """{question_number: letter} from the 'Your answer:' line under each question."""
    answers, current = {}, None
    for line in path.read_text(encoding="utf-8").splitlines():
        question = QUESTION.match(line)
        if question:
            current = int(question.group(1))
            continue
        mine = MY_ANSWER.search(line)
        if mine and current is not None:
            answers[current] = (mine.group(1) or "").upper()
    return answers


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    week = Path(sys.argv[1])
    key = read_key(week / "solutions" / "mcq-answers.md")
    mine = read_my_answers(week / "questions" / "mcqs.md")

    wrong = [q for q in sorted(key) if mine.get(q) and mine[q] != key[q]]
    blank = [q for q in sorted(key) if not mine.get(q)]
    correct = len(key) - len(wrong) - len(blank)

    print(f"Score: {correct} / {len(key)}")
    if wrong:
        print(f"Wrong:      {', '.join(map(str, wrong))}")
    if blank:
        print(f"Unanswered: {', '.join(map(str, blank))}")
    if not wrong and not blank:
        print("All correct!")
    elif wrong:
        print("Re-read those topics and try again before opening the answer key.")


if __name__ == "__main__":
    main()

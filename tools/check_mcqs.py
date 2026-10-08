"""Score a week's MCQs without revealing the right answers.

Usage (from the repo root):
    python3 tools/check_mcqs.py weeks/week-00-tradeoffs
"""

import re
import sys
from pathlib import Path

ROW = re.compile(r"^\|\s*(\d+)\s*\|\s*([A-Da-d]?)\s*\|")


def read_answers(path):
    """{question_number: letter} from a markdown table whose first two columns are Q and Answer."""
    answers = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if match:
            answers[int(match.group(1))] = match.group(2).upper()
    return answers


def main():
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    week = Path(sys.argv[1])
    key = read_answers(week / "solutions" / "mcq-answers.md")
    mine = read_answers(week / "solved" / "mcq-answers.md")

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

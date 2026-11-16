"""Run from the repo root: pytest project"""

from task_manager import format_task


def test_open_task():
    assert format_task(1, "Buy milk") == "[ ] 1: Buy milk"


def test_done_task():
    assert format_task(2, "Call client", True) == "[x] 2: Call client"


def test_done_defaults_to_false():
    assert format_task(3, "Write tests", done=False).startswith("[ ]")

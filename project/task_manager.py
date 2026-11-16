"""Task Manager: the mini-project that grows a little every day.

Roadmap:  functions -> classes -> file storage -> database -> REST API (Day 13)

Day 1 feature: show a task as a line of text with an f-string.
"""


def format_task(task_id, title, done=False):
    """Return one line describing a task.

    format_task(1, "Buy milk")             -> "[ ] 1: Buy milk"
    format_task(2, "Call client", True)    -> "[x] 2: Call client"

    A finished task shows "[x]", an open one shows "[ ]" (a space inside).
    """
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    sample = [(1, "Buy milk", False), (2, "Call client", True), (3, "Write tests", False)]
    for task_id, title, done in sample:
        print(format_task(task_id, title, done))

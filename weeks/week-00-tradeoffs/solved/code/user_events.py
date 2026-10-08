"""B6. Right to be forgotten in an append-only log. See ../../questions/questions.md for the full spec."""

import json
import os
import tempfile
from pathlib import Path


def append_event(log_path, event):
    """Append one JSON line. Never modify existing lines."""
    # TODO
    raise NotImplementedError


def read_events(log_path):
    """All events as a list of dicts ([] if the file doesn't exist)."""
    # TODO
    raise NotImplementedError


def build_event_counts(log_path):
    """Derived data: {user_id: number_of_events}."""
    # TODO
    raise NotImplementedError


def forget_user(log_path, user_id):
    """Erase every event of user_id by rewriting the file. Return how many were removed.
    Hint: write to tempfile.mkstemp(dir=same folder), then os.replace(tmp, log_path)."""
    # TODO
    raise NotImplementedError


def forget_everywhere(log_path, derived_counts, user_id):
    """Erase from the log AND from the derived_counts dict. Return how many log events were removed."""
    # TODO
    raise NotImplementedError


def purge_older_than(log_path, cutoff):
    """Data minimization: delete events with ts < cutoff ('YYYY-MM-DD'). Return how many were removed."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: append a few events, forget a user everywhere, purge old events, print the results
    pass

# Rewriting the whole file to delete one user: why is that a problem at 10 TB? Better ideas?
# Answer:

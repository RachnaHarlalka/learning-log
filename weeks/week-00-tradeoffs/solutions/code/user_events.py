"""B6. Right to be forgotten in an append-only log: reference solution."""

import json
import os
import tempfile
from pathlib import Path


def append_event(log_path, event):
    """Append one JSON line. Existing lines are never modified."""
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")


def read_events(log_path):
    path = Path(log_path)
    if not path.exists():
        return []
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def build_event_counts(log_path):
    """Derived data: number of events per user, re-creatable from the log."""
    counts = {}
    for event in read_events(log_path):
        counts[event["user_id"]] = counts.get(event["user_id"], 0) + 1
    return counts


def _rewrite_keeping(log_path, keep):
    """Rewrite the log with only the events where keep(event) is True. Returns number removed.

    Writes to a temp file in the same directory, then os.replace() swaps it in
    atomically: a crash leaves either the old log or the new one, never half of each.
    """
    events = read_events(log_path)
    kept = [e for e in events if keep(e)]
    directory = os.path.dirname(os.path.abspath(log_path))
    fd, tmp_path = tempfile.mkstemp(dir=directory, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        for event in kept:
            f.write(json.dumps(event) + "\n")
    os.replace(tmp_path, log_path)
    return len(events) - len(kept)


def forget_user(log_path, user_id):
    """GDPR erasure from the system of record."""
    return _rewrite_keeping(log_path, lambda e: e["user_id"] != user_id)


def forget_everywhere(log_path, derived_counts, user_id):
    """Erase from the source AND the derived data; forgetting only the source isn't enough."""
    removed = forget_user(log_path, user_id)
    derived_counts.pop(user_id, None)
    return removed


def purge_older_than(log_path, cutoff):
    """Data minimization: don't keep data longer than needed. ISO dates compare as text."""
    return _rewrite_keeping(log_path, lambda e: e["ts"] >= cutoff)


if __name__ == "__main__":
    with tempfile.TemporaryDirectory() as d:
        log = os.path.join(d, "events.jsonl")
        for user_id, ts in [(2, "2025-06-01"), (1, "2026-01-10"), (1, "2026-03-01"), (3, "2026-03-02"), (2, "2026-03-05")]:
            append_event(log, {"user_id": user_id, "type": "view", "ts": ts, "data": {}})

        counts = build_event_counts(log)
        print("before:          ", counts)
        print("forgot user 1:   ", forget_everywhere(log, counts, 1), "events removed")
        print("derived counts:  ", counts, " rebuilt:", build_event_counts(log))
        print("purged pre-2026: ", purge_older_than(log, "2026-01-01"), "events removed")
        print("left in log:     ", read_events(log))

# Why is rewriting the whole file a problem with 10 TB of logs?
# Deleting one user's few events means reading and rewriting ALL 10 TB: hours of
# I/O per request, and GDPR requests arrive constantly. Better approaches:
# - Split the log into segments and only rewrite segments containing that user,
#   or record a "tombstone" (a delete marker) and drop the data later during
#   background compaction (Week 5: log-structured storage does exactly this).
# - Crypto-shredding: encrypt each user's data with their own key; to "forget"
#   them, delete the key, and the data left in immutable logs becomes unreadable.
# - Don't forget derived data: caches, search indexes, warehouse copies, backups,
#   and ML models trained on the data (which may need retraining).

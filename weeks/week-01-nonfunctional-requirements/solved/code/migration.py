"""B7. A reversible migration from an old store to a new one. See ../../questions/questions.md.

Phases, in order:
    old_only     -> reads old, writes old
    dual_write   -> reads old, writes both            (backfill copies existing data)
    shadow_read  -> reads old, also reads new and appends the key to self.mismatches if they differ
    new_primary  -> reads new, still writes both      (old stays current: rollback possible)
    new_only     -> reads new, writes new             (old is stale: irreversible)
"""

PHASES = ["old_only", "dual_write", "shadow_read", "new_primary", "new_only"]


class IrreversibleError(Exception):
    pass


class MigratingStore:
    def __init__(self, old, new):
        self.old = old
        self.new = new
        self.phase = "old_only"
        self.mismatches = []

    def put(self, key, value):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def get(self, key):
        raise NotImplementedError

    def backfill(self):
        """Copy keys missing from new. Return how many were copied. Must be safe to run twice."""
        raise NotImplementedError

    def advance(self):
        """One phase forward; return the new phase. ValueError if already new_only.
        RuntimeError if leaving shadow_read while there are mismatches."""
        raise NotImplementedError

    def rollback(self):
        """One phase back; return the new phase. IrreversibleError from new_only.
        ValueError from old_only."""
        raise NotImplementedError


if __name__ == "__main__":
    # TODO: walk through every phase, find a "problem" in new_primary and roll back,
    # then show that rollback from new_only is impossible.
    pass

# Why does dual-writing keep the migration reversible? Which step is irreversible?
# Answer:

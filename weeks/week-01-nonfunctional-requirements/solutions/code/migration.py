"""B7. A reversible migration from an old store to a new one. Reference solution.

Phases, in order. Each step forward keeps the previous one reversible until the
very last step, which is the only irreversible one.

    old_only     -> reads old, writes old
    dual_write   -> reads old, writes both            (backfill copies existing data)
    shadow_read  -> reads old, also reads new and records mismatches
    new_primary  -> reads new, still writes both      (old stays current: rollback possible)
    new_only     -> reads new, writes new             (old is stale: irreversible)
"""

PHASES = ["old_only", "dual_write", "shadow_read", "new_primary", "new_only"]


class IrreversibleError(Exception):
    pass


class MigratingStore:
    def __init__(self, old, new):
        self.old = old      # dicts stand in for the two databases
        self.new = new
        self.phase = "old_only"
        self.mismatches = []

    def _writes_old(self):
        return self.phase != "new_only"

    def _writes_new(self):
        return self.phase != "old_only"

    def put(self, key, value):
        if self._writes_old():
            self.old[key] = value
        if self._writes_new():
            self.new[key] = value

    def delete(self, key):
        if self._writes_old():
            self.old.pop(key, None)
        if self._writes_new():
            self.new.pop(key, None)

    def get(self, key):
        if self.phase in ("new_primary", "new_only"):
            return self.new.get(key)
        value = self.old.get(key)
        if self.phase == "shadow_read" and self.new.get(key) != value:
            self.mismatches.append(key)
        return value

    def backfill(self):
        """Copy keys the new store doesn't have yet. Safe to run more than once."""
        copied = 0
        for key, value in self.old.items():
            if key not in self.new:
                self.new[key] = value
                copied += 1
        return copied

    def advance(self):
        """Move one phase forward. Refuse to cut over reads while shadow reads disagree."""
        index = PHASES.index(self.phase)
        if index == len(PHASES) - 1:
            raise ValueError("already fully migrated")
        if self.phase == "shadow_read" and self.mismatches:
            raise RuntimeError(f"{len(self.mismatches)} shadow-read mismatches: fix before cutting over")
        self.phase = PHASES[index + 1]
        return self.phase

    def rollback(self):
        """Move one phase back. Impossible once the old store stopped receiving writes."""
        if self.phase == "new_only":
            raise IrreversibleError("old store is stale since writes stopped; rollback impossible")
        index = PHASES.index(self.phase)
        if index == 0:
            raise ValueError("nothing to roll back")
        self.phase = PHASES[index - 1]
        return self.phase


if __name__ == "__main__":
    old, new = {"u1": "Asha", "u2": "Ravi"}, {}
    store = MigratingStore(old, new)

    store.advance()                       # dual_write
    store.put("u3", "Meera")              # goes to both
    print("backfilled:", store.backfill())
    store.advance()                       # shadow_read
    for key in ("u1", "u2", "u3"):
        store.get(key)
    print("shadow mismatches:", store.mismatches)

    store.advance()                       # new_primary: reads from new
    store.put("u4", "Kabir")
    print("problem found in new store! rolling back to:", store.rollback())
    print("old store is still complete:", sorted(old) == ["u1", "u2", "u3", "u4"])

    store.advance()
    store.advance()                       # new_only
    try:
        store.rollback()
    except IrreversibleError as e:
        print("final step:", e)

# Why dual-write before cutting over reads? Because it keeps the OLD store current.
# As long as old receives every write, switching back is just flipping a flag:
# the migration stays reversible. The only irreversible step (stop writing old) is
# taken last, after shadow reads and a period on new_primary proved the new store
# correct. Real migrations add: comparing data in bulk, handling writes that land
# in one store but fail in the other, and backfilling while writes continue.

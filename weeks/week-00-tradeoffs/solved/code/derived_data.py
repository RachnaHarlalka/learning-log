"""B3. System of record vs derived data. See ../../questions/questions.md for the full spec."""


class ProfileStore:
    """System of record: the authoritative copy, each fact stored once. Given."""

    def __init__(self):
        self._rows = {}

    def put(self, user_id, profile):
        self._rows[user_id] = dict(profile)

    def get(self, user_id):
        profile = self._rows.get(user_id)
        return dict(profile) if profile is not None else None

    def items(self):
        return ((user_id, dict(p)) for user_id, p in self._rows.items())


def build_city_index(store):
    """Derived: {city: set(user_ids)} built from the store."""
    # TODO
    raise NotImplementedError


class ProfileCache:
    """Derived: cache-aside copy of profiles."""

    def __init__(self, store):
        self.store = store
        self.hits = 0
        self.misses = 0
        # TODO: somewhere to keep cached profiles

    def get(self, user_id):
        # TODO: hit -> return cached; miss -> read store, remember, return
        raise NotImplementedError

    def invalidate(self, user_id):
        # TODO
        raise NotImplementedError


def update_profile(store, cache, city_index, user_id, profile):
    """Write to the system of record FIRST, then update the cache and the index."""
    # TODO: remember to remove a city key once it has no users left
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: demo (a) stale cache without propagation, (b) update_profile fixes it,
    #       (c) delete the index, rebuild it, and show it matches
    pass

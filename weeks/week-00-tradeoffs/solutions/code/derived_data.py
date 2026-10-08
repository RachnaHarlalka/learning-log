"""B3. System of record vs derived data: reference solution."""


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
    """Derived: re-creatable at any time from the system of record."""
    index = {}
    for user_id, profile in store.items():
        index.setdefault(profile["city"], set()).add(user_id)
    return index


class ProfileCache:
    """Derived: cache-aside copy of profiles to speed up reads."""

    def __init__(self, store):
        self.store = store
        self._data = {}
        self.hits = 0
        self.misses = 0

    def get(self, user_id):
        if user_id in self._data:
            self.hits += 1
            return self._data[user_id]
        self.misses += 1
        profile = self.store.get(user_id)
        if profile is not None:
            self._data[user_id] = profile
        return profile

    def invalidate(self, user_id):
        self._data.pop(user_id, None)


def update_profile(store, cache, city_index, user_id, profile):
    """Write to the system of record first, then propagate to every derived system."""
    old = store.get(user_id)
    store.put(user_id, profile)

    cache.invalidate(user_id)

    if old is not None and old["city"] in city_index:
        city_index[old["city"]].discard(user_id)
        if not city_index[old["city"]]:
            del city_index[old["city"]]
    city_index.setdefault(profile["city"], set()).add(user_id)


if __name__ == "__main__":
    store = ProfileStore()
    store.put(1, {"name": "Asha", "city": "Pune"})
    store.put(2, {"name": "Ravi", "city": "Delhi"})
    store.put(3, {"name": "Meera", "city": "Pune"})
    cache = ProfileCache(store)
    index = build_city_index(store)

    cache.get(1)
    print("(a) Update the store WITHOUT propagating")
    store.put(1, {"name": "Asha", "city": "Mumbai"})
    print(f"    store says: {store.get(1)['city']}, cache says: {cache.get(1)['city']}  <- stale")
    print(f"    index still has Asha in Pune: {1 in index['Pune']}  <- stale")

    print("(b) Update via update_profile (propagates to derived data)")
    store.put(1, {"name": "Asha", "city": "Pune"})  # reset
    index = build_city_index(store)
    cache.get(1)
    update_profile(store, cache, index, 1, {"name": "Asha", "city": "Mumbai"})
    print(f"    store: {store.get(1)['city']}, cache: {cache.get(1)['city']}, index: {dict(index)}")

    print("(c) Lose the derived index, rebuild from the system of record")
    maintained = {city: set(ids) for city, ids in index.items()}
    del index
    rebuilt = build_city_index(store)
    print(f"    rebuilt == maintained: {rebuilt == maintained}")
    print(f"\ncache hits={cache.hits}, misses={cache.misses}")

"""B1. Home timelines: pull vs push (fan-out on write) vs hybrid. Reference solution."""

import random


def followers_of(follows):
    """Invert {user: set(followees)} into {user: set(followers)}."""
    followers = {user: set() for user in follows}
    for user, followees in follows.items():
        for followee in followees:
            followers.setdefault(followee, set()).add(user)
    return followers


class PullTimeline:
    """Fan-out on read: store each post once; build the timeline when it's read."""

    def __init__(self, follows):
        self.follows = follows
        self.posts_by_user = {}
        self.writes = 0  # post-list / timeline insertions
        self.reads = 0   # post-list lookups while serving timelines

    def post(self, user, post_id, ts):
        self.posts_by_user.setdefault(user, []).append((ts, post_id))
        self.writes += 1

    def home_timeline(self, user, limit=20):
        merged = []
        for followee in self.follows.get(user, ()):
            self.reads += 1
            merged.extend(self.posts_by_user.get(followee, []))
        merged.sort(reverse=True)
        return [post_id for _, post_id in merged[:limit]]


class PushTimeline:
    """Fan-out on write: deliver each post into every follower's precomputed timeline."""

    def __init__(self, follows):
        self.followers = followers_of(follows)
        self.timelines = {}
        self.writes = 0
        self.reads = 0

    def post(self, user, post_id, ts):
        for follower in self.followers.get(user, ()):
            self.timelines.setdefault(follower, []).append((ts, post_id))
            self.writes += 1

    def home_timeline(self, user, limit=20):
        self.reads += 1
        timeline = sorted(self.timelines.get(user, []), reverse=True)
        return [post_id for _, post_id in timeline[:limit]]


class HybridTimeline:
    """Push for normal users; celebrity posts are stored once and merged in at read time."""

    def __init__(self, follows, celebrity_threshold):
        self.follows = follows
        self.followers = followers_of(follows)
        self.celebrities = {u for u, f in self.followers.items() if len(f) >= celebrity_threshold}
        self.timelines = {}
        self.celebrity_posts = {}
        self.writes = 0
        self.reads = 0

    def post(self, user, post_id, ts):
        if user in self.celebrities:
            self.celebrity_posts.setdefault(user, []).append((ts, post_id))
            self.writes += 1
            return
        for follower in self.followers.get(user, ()):
            self.timelines.setdefault(follower, []).append((ts, post_id))
            self.writes += 1

    def home_timeline(self, user, limit=20):
        self.reads += 1
        merged = list(self.timelines.get(user, []))
        for followee in self.follows.get(user, ()):
            if followee in self.celebrities:
                self.reads += 1
                merged.extend(self.celebrity_posts.get(followee, []))
        merged.sort(reverse=True)
        return [post_id for _, post_id in merged[:limit]]


def build_follow_graph(n_users=10_000, avg_follows=50, n_celebrities=5, celebrity_follow_prob=0.6, seed=0):
    """Users 0..n_celebrities-1 are celebrities that most people follow."""
    rng = random.Random(seed)
    follows = {}
    for user in range(n_users):
        followees = set(rng.sample(range(n_users), avg_follows)) - {user}
        followees |= {c for c in range(n_celebrities) if c != user and rng.random() < celebrity_follow_prob}
        follows[user] = followees
    return follows


def run_workload(timeline, n_users, n_posts, n_reads, celebrity_ids, celebrity_post_share=0.05, seed=1):
    """Replay the same posts and timeline reads against any strategy."""
    rng = random.Random(seed)
    for i in range(n_posts):
        author = rng.choice(celebrity_ids) if rng.random() < celebrity_post_share else rng.randrange(n_users)
        timeline.post(author, post_id=i, ts=i)
    for _ in range(n_reads):
        timeline.home_timeline(rng.randrange(n_users))
    return timeline.writes, timeline.reads


if __name__ == "__main__":
    print("Book's back-of-envelope numbers")
    polls = 10_000_000 / 5
    print(f"  pull + polling: {polls:,.0f} queries/s x 200 followees = {polls * 200:,.0f} lookups/s")
    print(f"  push:           5,800 posts/s x 200 followers = {5_800 * 200:,} timeline writes/s\n")

    n_users, n_celebs = 10_000, 5
    follows = build_follow_graph(n_users=n_users, n_celebrities=n_celebs)
    celebs = list(range(n_celebs))
    print(f"Simulation: {n_users:,} users, celebrities have ~{len(followers_of(follows)[0]):,} followers")
    print(f"{'strategy':<10} {'writes':>12} {'reads':>12} {'total work':>12}")
    for name, timeline in [
        ("pull", PullTimeline(follows)),
        ("push", PushTimeline(follows)),
        ("hybrid", HybridTimeline(follows, celebrity_threshold=1_000)),
    ]:
        writes, reads = run_workload(timeline, n_users, n_posts=5_000, n_reads=50_000, celebrity_ids=celebs)
        print(f"{name:<10} {writes:>12,} {reads:>12,} {writes + reads:>12,}")

# Observations (10:1 reads to posts here; real social networks are far more read-heavy):
# - Pull does little work on writes but ~50+ lookups per timeline read.
# - Push makes reads O(1) but every celebrity post costs ~6,000 writes.
# - Hybrid keeps push's cheap reads and avoids the celebrity write explosion,
#   at the cost of a few extra lookups per read (one per followed celebrity).
# Which wins depends on the read/write ratio and the follower distribution:
# that's why "understanding load" comes before choosing an architecture.

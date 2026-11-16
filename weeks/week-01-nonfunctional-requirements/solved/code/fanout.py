"""B1. Home timelines: pull vs push (fan-out on write) vs hybrid. See ../../questions/questions.md."""

import random


def followers_of(follows):
    """Invert {user: set(followees)} into {user: set(followers)}. Every user appears as a key."""
    # TODO
    raise NotImplementedError


class PullTimeline:
    """Fan-out on read. post(): store once (writes += 1). home_timeline(): merge followees' posts
    (reads += 1 per followee looked up). Return post_ids newest first, at most `limit`."""

    def __init__(self, follows):
        self.follows = follows
        self.writes = 0
        self.reads = 0
        # TODO

    def post(self, user, post_id, ts):
        raise NotImplementedError

    def home_timeline(self, user, limit=20):
        raise NotImplementedError


class PushTimeline:
    """Fan-out on write. post(): insert into every follower's timeline (writes += 1 per follower).
    home_timeline(): read your own precomputed timeline (reads += 1)."""

    def __init__(self, follows):
        self.writes = 0
        self.reads = 0
        # TODO

    def post(self, user, post_id, ts):
        raise NotImplementedError

    def home_timeline(self, user, limit=20):
        raise NotImplementedError


class HybridTimeline:
    """Users with >= celebrity_threshold followers are celebrities (self.celebrities = set of ids).
    Celebrity posts are stored once (writes += 1); others fan out like PushTimeline.
    home_timeline(): own timeline (reads += 1) + each followed celebrity's posts (reads += 1 each)."""

    def __init__(self, follows, celebrity_threshold):
        self.writes = 0
        self.reads = 0
        self.celebrities = set()
        # TODO

    def post(self, user, post_id, ts):
        raise NotImplementedError

    def home_timeline(self, user, limit=20):
        raise NotImplementedError


def build_follow_graph(n_users=10_000, avg_follows=50, n_celebrities=5, celebrity_follow_prob=0.6, seed=0):
    """Given (no changes needed): users 0..n_celebrities-1 are celebrities that most people follow."""
    rng = random.Random(seed)
    follows = {}
    for user in range(n_users):
        followees = set(rng.sample(range(n_users), avg_follows)) - {user}
        followees |= {c for c in range(n_celebrities) if c != user and rng.random() < celebrity_follow_prob}
        follows[user] = followees
    return follows


def run_workload(timeline, n_users, n_posts, n_reads, celebrity_ids, celebrity_post_share=0.05, seed=1):
    """Given (no changes needed): replay the same posts and reads against any strategy."""
    rng = random.Random(seed)
    for i in range(n_posts):
        author = rng.choice(celebrity_ids) if rng.random() < celebrity_post_share else rng.randrange(n_users)
        timeline.post(author, post_id=i, ts=i)
    for _ in range(n_reads):
        timeline.home_timeline(rng.randrange(n_users))
    return timeline.writes, timeline.reads


if __name__ == "__main__":
    # TODO: print the book's back-of-envelope numbers (polling vs push), then run all three
    # strategies on build_follow_graph() with run_workload(..., n_posts=5_000, n_reads=50_000)
    # and print writes / reads / total for each.
    pass

# Which strategy did the least total work, and why? When would the answer change?
# Answer:

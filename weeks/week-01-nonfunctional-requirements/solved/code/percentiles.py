"""B2. Percentiles, tail amplification, histograms. See ../../questions/questions.md."""

import math
import random
import statistics


def percentile(values, p):
    """Nearest-rank percentile: sorted(values)[ceil(p/100 * n) - 1].
    ValueError if empty or p not in (0, 100].
    Watch out: 99.9 / 100 * 1000 == 999.0000000000001 in floating point!"""
    # TODO
    raise NotImplementedError


def summarize(values):
    """Dict with keys: mean, p50, p95, p99, p999, max."""
    # TODO
    raise NotImplementedError


def tail_amplification(n_backends, p_slow):
    """Probability a user request is slow when it must wait for all n backends."""
    # TODO
    raise NotImplementedError


def average_of_percentiles(groups, p):
    """The WRONG way to combine servers: mean of each group's percentile. (Implement it anyway.)"""
    # TODO
    raise NotImplementedError


class Histogram:
    """Log-bucketed histogram. A value v goes into bucket ceil(log(v) / log(1 + precision)).
    percentile(p) returns the upper bound (1 + precision) ** index of the bucket holding rank
    ceil(p/100 * count). merge(other) returns a NEW histogram with bucket counts added."""

    def __init__(self, precision=0.01):
        self.precision = precision
        self.buckets = {}
        self.count = 0

    def record(self, value):
        raise NotImplementedError

    def merge(self, other):
        raise NotImplementedError

    def percentile(self, p):
        raise NotImplementedError


if __name__ == "__main__":
    # TODO: two servers (A healthy, B with 5% very slow requests). Compare: average of the two
    # p99s vs the true p99 of all requests vs the p99 of the merged histograms.
    pass

# Why is averaging percentiles wrong?
# Answer:

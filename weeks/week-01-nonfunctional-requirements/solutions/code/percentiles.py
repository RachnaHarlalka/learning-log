"""B2. Percentiles, tail amplification, and why you add histograms instead of averaging percentiles."""

import math
import random
import statistics


def percentile(values, p):
    """Nearest-rank percentile. ValueError if values is empty or p not in (0, 100]."""
    if not values:
        raise ValueError("values must not be empty")
    if not 0 < p <= 100:
        raise ValueError("p must be in (0, 100]")
    ordered = sorted(values)
    # round() guards against float error: 99.9 / 100 * 1000 == 999.0000000000001
    rank = math.ceil(round(p / 100 * len(ordered), 9))
    return ordered[rank - 1]


def summarize(values):
    return {
        "mean": statistics.fmean(values),
        "p50": percentile(values, 50),
        "p95": percentile(values, 95),
        "p99": percentile(values, 99),
        "p999": percentile(values, 99.9),
        "max": max(values),
    }


def tail_amplification(n_backends, p_slow):
    """Probability a user request is slow when it waits for all n backends."""
    return 1 - (1 - p_slow) ** n_backends


def average_of_percentiles(groups, p):
    """The WRONG way to combine: average each server's percentile."""
    return statistics.fmean(percentile(g, p) for g in groups)


class Histogram:
    """Log-bucketed histogram (the idea behind HdrHistogram / DDSketch).

    Each value lands in bucket ceil(log(v) / log(1 + precision)), so a reported
    percentile is within `precision` relative error of the true one, using
    memory proportional to the number of buckets, not the number of values.
    """

    def __init__(self, precision=0.01):
        self.precision = precision
        self._log_base = math.log(1 + precision)
        self.buckets = {}
        self.count = 0

    def record(self, value):
        if value <= 0:
            raise ValueError("values must be positive")
        index = math.ceil(math.log(value) / self._log_base)
        self.buckets[index] = self.buckets.get(index, 0) + 1
        self.count += 1

    def merge(self, other):
        """Combining histograms is just adding bucket counts."""
        if other.precision != self.precision:
            raise ValueError("can only merge histograms with the same precision")
        merged = Histogram(self.precision)
        for source in (self, other):
            for index, n in source.buckets.items():
                merged.buckets[index] = merged.buckets.get(index, 0) + n
            merged.count += source.count
        return merged

    def percentile(self, p):
        if self.count == 0:
            raise ValueError("histogram is empty")
        if not 0 < p <= 100:
            raise ValueError("p must be in (0, 100]")
        rank = math.ceil(round(p / 100 * self.count, 9))
        seen = 0
        for index in sorted(self.buckets):
            seen += self.buckets[index]
            if seen >= rank:
                return (1 + self.precision) ** index  # bucket upper bound
        raise AssertionError("unreachable")


if __name__ == "__main__":
    rng = random.Random(42)
    # Server A: healthy. Server B: a few very slow requests (e.g. GC pauses).
    server_a = [rng.uniform(20, 60) for _ in range(9_000)]
    server_b = [rng.uniform(20, 60) if rng.random() > 0.05 else rng.uniform(800, 1200) for _ in range(1_000)]
    everything = server_a + server_b

    print("Summary of all requests (ms):", {k: round(v, 1) for k, v in summarize(everything).items()})
    print(f"\np99 server A: {percentile(server_a, 99):7.1f}   p99 server B: {percentile(server_b, 99):7.1f}")
    print(f"Average of the two p99s (WRONG): {average_of_percentiles([server_a, server_b], 99):7.1f}")
    print(f"True p99 of all requests:        {percentile(everything, 99):7.1f}")

    hist_a, hist_b = Histogram(), Histogram()
    for v in server_a:
        hist_a.record(v)
    for v in server_b:
        hist_b.record(v)
    print(f"p99 from merged histograms:      {hist_a.merge(hist_b).percentile(99):7.1f}  (within 1%)")

    print("\nTail amplification with 1% slow backends:")
    for n in (1, 10, 50, 100):
        print(f"  {n:>3} backends -> {tail_amplification(n, 0.01):6.1%} of user requests slow")

# Why is averaging p99s wrong? Server B handles only 10% of traffic, and its slow
# requests are ~5% of B = only 0.5% of ALL requests. So the true combined p99 is
# ~60 ms (the slow tail shows up at p99.9 instead), yet averaging the two p99s says
# ~590 ms: a number no request experienced, 10x off. Percentiles ignore how many
# requests each group had; counts don't. So you merge histograms (add bucket counts)
# and read the percentile once from the combined distribution.

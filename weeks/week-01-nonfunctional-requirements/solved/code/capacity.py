"""B5. Understanding load and capacity planning. See ../../questions/questions.md."""

import math


def months_until_limit(current_load, capacity, monthly_growth):
    """Whole months until load EXCEEDS capacity at compound growth.
    0 if already over; math.inf if growth <= 0."""
    raise NotImplementedError


def nodes_needed(peak_load, per_node_capacity, target_utilization=0.7, spare=1):
    """ceil(peak / (per_node * target_utilization)) + spare."""
    raise NotImplementedError


def scaling_efficiency(measurements):
    """{nodes: throughput} -> {nodes: throughput / (nodes * throughput_at_1_node)}."""
    raise NotImplementedError


def classify_scaling(measurements, tolerance=0.1):
    """'linear' / 'sublinear' / 'superlinear' based on efficiency at the largest node count."""
    raise NotImplementedError


def data_rate_mb_per_s(requests_per_second, request_size_mb):
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: months until limit for 4,000 req/s vs 10,000 capacity at 8%/month; nodes for 50k peak;
    # efficiency of {1: 1000, 2: 1950, 4: 3700, 8: 6400, 16: 9600}; the two 100 MB/s systems
    pass

# Why plan for 70% utilization rather than 100%? Why does efficiency fall as nodes grow?
# Answer:

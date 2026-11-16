"""B5. Understanding load and capacity planning. Reference solution."""

import math


def months_until_limit(current_load, capacity, monthly_growth):
    """Whole months until load exceeds capacity at compound growth (0 if already over)."""
    if current_load > capacity:
        return 0
    if monthly_growth <= 0:
        return math.inf
    months = math.log(capacity / current_load) / math.log(1 + monthly_growth)
    return math.floor(months) + 1


def nodes_needed(peak_load, per_node_capacity, target_utilization=0.7, spare=1):
    """Nodes for the peak, run below full utilization (queueing!), plus spare(s) for failures."""
    return math.ceil(peak_load / (per_node_capacity * target_utilization)) + spare


def scaling_efficiency(measurements):
    """{nodes: throughput} -> {nodes: throughput / (nodes * single-node throughput)}."""
    base = measurements[1]
    return {n: thr / (n * base) for n, thr in sorted(measurements.items())}


def classify_scaling(measurements, tolerance=0.1):
    """'linear', 'sublinear' or 'superlinear', judged at the largest cluster size."""
    efficiency = scaling_efficiency(measurements)[max(measurements)]
    if efficiency > 1 + tolerance:
        return "superlinear"
    if efficiency < 1 - tolerance:
        return "sublinear"
    return "linear"


def data_rate_mb_per_s(requests_per_second, request_size_mb):
    return requests_per_second * request_size_mb


if __name__ == "__main__":
    print(f"Load 4,000 req/s, capacity 10,000, growing 8%/month -> "
          f"limit in {months_until_limit(4_000, 10_000, 0.08)} months")
    print(f"Peak 50,000 req/s, 2,000 per node, 70% target, N+1 -> {nodes_needed(50_000, 2_000)} nodes")

    measured = {1: 1_000, 2: 1_950, 4: 3_700, 8: 6_400, 16: 9_600}
    print("\nScaling efficiency:", {n: f"{e:.0%}" for n, e in scaling_efficiency(measured).items()},
          "->", classify_scaling(measured))

    print("\nSame bandwidth, very different systems (no magic scaling sauce):")
    print(f"  100,000 req/s x 1 kB  = {data_rate_mb_per_s(100_000, 0.001):.0f} MB/s  (tiny requests: CPU/connection bound)")
    print(f"  3 req/min x 2 GB      = {data_rate_mb_per_s(3 / 60, 2_000):.0f} MB/s  (huge transfers: bandwidth/streaming bound)")

# Why target 70% utilization instead of 100%? Queueing (see B3): response time
# explodes near full utilization, and you need headroom for spikes and for a node
# failing (N+1). Why does efficiency drop at 16 nodes? Coordination, shared
# bottlenecks (a single DB, a lock, a hot shard): cost grows faster than linearly.

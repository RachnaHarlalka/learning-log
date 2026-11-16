"""B3. Queueing delay and metastable failure (retry storms). Reference solution."""

import random
import statistics


def simulate_queue(utilization, n_requests=50_000, service_ms=10.0, seed=0):
    """Single-server FIFO queue with random (exponential) arrivals and service times.

    Returns each request's response time = queueing delay + service time.
    """
    if not 0 < utilization < 1:
        raise ValueError("utilization must be in (0, 1)")
    rng = random.Random(seed)
    arrival_rate = utilization / service_ms  # requests per ms
    clock = 0.0
    server_free_at = 0.0
    response_times = []
    for _ in range(n_requests):
        clock += rng.expovariate(arrival_rate)
        start = max(clock, server_free_at)  # wait if the server is busy
        server_free_at = start + rng.expovariate(1 / service_ms)
        response_times.append(server_free_at - clock)
    return response_times


def simulate_retry_storm(ticks=120, base_load=80, capacity=100, timeout=3,
                         spike=(10, 20, 150), max_retries=3, shed_expired=False):
    """Tick-based model of a server, its queue, and clients that time out and retry.

    Each tick: new requests arrive (base_load, or spike load during [start, end)),
    plus any scheduled retries. The server processes up to `capacity` requests
    from the front of the queue. A request whose age exceeds `timeout` has been
    abandoned by its client: processing it is wasted work. When a request reaches
    age == timeout while still queued, its client retries it (a NEW request next
    tick) unless it has used up max_retries. The abandoned original stays in the
    queue unless shed_expired=True, in which case the server drops abandoned
    requests instead of processing them (load shedding).

    Returns a list of per-tick stats dicts.
    """
    queue = []  # list of (created_tick, attempt), FIFO
    retries_next_tick = []
    stats = []
    spike_start, spike_end, spike_load = spike
    for t in range(ticks):
        arrivals = spike_load if spike_start <= t < spike_end else base_load
        new = [(t, 0)] * arrivals + [(t, attempt) for attempt in retries_next_tick]
        retries = len(retries_next_tick)
        queue.extend(new)
        retries_next_tick = []

        shed = 0
        if shed_expired:
            before = len(queue)
            queue = [(c, a) for c, a in queue if t - c <= timeout]
            shed = before - len(queue)

        processed, queue = queue[:capacity], queue[capacity:]
        goodput = sum(1 for c, _ in processed if t - c <= timeout)
        wasted = len(processed) - goodput

        for created, attempt in queue:
            if t - created == timeout and attempt < max_retries:
                retries_next_tick.append(attempt + 1)

        stats.append({"tick": t, "arrivals": arrivals, "retries": retries, "queue": len(queue),
                      "goodput": goodput, "wasted": wasted, "shed": shed})
    return stats


if __name__ == "__main__":
    print("Response time vs utilization (service time 10 ms)")
    print(f"{'util':>5} {'mean ms':>9} {'p99 ms':>9}")
    for u in (0.5, 0.7, 0.8, 0.9, 0.95):
        rt = sorted(simulate_queue(u))
        print(f"{u:>5.0%} {statistics.fmean(rt):>9.1f} {rt[int(len(rt) * 0.99)]:>9.1f}")

    for label, kwargs in [
        ("no mitigation (retries, FIFO)", {}),
        ("no retries at all", {"max_retries": 0}),
        ("load shedding of expired requests", {"shed_expired": True}),
    ]:
        stats = simulate_retry_storm(**kwargs)
        print(f"\n{label}")
        for s in stats[::10]:
            print(f"  tick {s['tick']:>3}: arrivals {s['arrivals']:>3} + retries {s['retries']:>3} | "
                  f"queue {s['queue']:>6} | goodput {s['goodput']:>3} | wasted {s['wasted']:>3} | shed {s['shed']:>4}")

# Takeaways:
# - Queueing makes response time explode as utilization nears 100%: mean at 95%
#   is ~10x the mean at 50% for the same hardware.
# - The spike lasts 10 ticks, but with retries the system NEVER recovers: the
#   server spends all its capacity on requests whose clients have already given
#   up, every new request times out, and retries add load. Metastable failure.
# - Without retries, it drains slowly. With load shedding, it recovers within a
#   few ticks because capacity goes only to requests someone is still waiting for.

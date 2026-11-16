"""B3. Queueing delay and metastable failure. See ../../questions/questions.md for the full spec."""

import random
import statistics


def simulate_queue(utilization, n_requests=50_000, service_ms=10.0, seed=0):
    """Single-server FIFO queue. Interarrival times ~ rng.expovariate(utilization / service_ms),
    service times ~ rng.expovariate(1 / service_ms). Return each request's response time
    (queueing delay + service time). ValueError unless 0 < utilization < 1."""
    # TODO
    raise NotImplementedError


def simulate_retry_storm(ticks=120, base_load=80, capacity=100, timeout=3,
                         spike=(10, 20, 150), max_retries=3, shed_expired=False):
    """Per tick t, in this order:
      1. arrivals = spike load if start <= t < end else base_load; add them as (t, attempt=0),
         plus retries scheduled last tick as (t, attempt)
      2. if shed_expired: drop queued requests with t - created > timeout (count as 'shed')
      3. process up to `capacity` from the front: goodput if t - created <= timeout, else wasted
      4. for each request still queued with t - created == timeout and attempt < max_retries,
         schedule a retry (attempt + 1) for next tick. The original stays queued.
    Return a list of dicts per tick with keys:
      tick, arrivals, retries, queue (length after processing), goodput, wasted, shed"""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: print mean/p99 response time for utilization 0.5..0.95,
    # then every 10th tick of the retry storm: default, max_retries=0, shed_expired=True
    pass

# What did you observe? Why does the default case never recover?
# Answer:

"""B6 (stretch). Fault injection: independent faults vs a correlated software bug."""

import random


class Replica:
    def __init__(self, name):
        self.name = name
        self.alive = True

    def handle(self, request):
        if not self.alive:
            raise ConnectionError(f"{self.name} is down")
        if request.get("leap_second"):
            # Same code on every replica -> same bug everywhere (correlated fault)
            raise RuntimeError(f"{self.name} hung on leap second")
        return f"{self.name}: ok"


def call_with_failover(replicas, request, rng):
    """Try replicas in random order; return a response or None if all fail."""
    for replica in rng.sample(replicas, len(replicas)):
        try:
            return replica.handle(request)
        except (ConnectionError, RuntimeError):
            continue
    return None


def run(n_requests, kill_prob, failover, leap_second_share=0.0, seed=0):
    rng = random.Random(seed)
    replicas = [Replica(f"r{i}") for i in range(3)]
    ok = 0
    for _ in range(n_requests):
        for r in replicas:  # chaos monkey: each replica independently down this round
            r.alive = rng.random() >= kill_prob
        request = {"leap_second": rng.random() < leap_second_share}
        if failover:
            ok += call_with_failover(replicas, request, rng) is not None
        else:
            try:
                replicas[0].handle(request)
                ok += 1
            except (ConnectionError, RuntimeError):
                pass
    return ok / n_requests


if __name__ == "__main__":
    print("Each replica randomly killed 10% of the time (independent hardware-style faults)")
    print(f"  single replica, no failover: {run(20_000, 0.10, failover=False):.2%} success")
    print(f"  3 replicas with failover:    {run(20_000, 0.10, failover=True):.2%} success")
    print("\nAdd a software bug triggered by 1% of requests on EVERY replica (correlated fault)")
    print(f"  3 replicas with failover:    {run(20_000, 0.10, failover=True, leap_second_share=0.01):.2%} success")

# Redundancy turns 90% into ~99.9% for independent faults, but cannot help with the
# leap-second-style bug: all replicas run the same code, so they all fail on the
# same input. Fault injection is valuable because it exercises the failover path
# continuously; the correlated case shows why gradual rollouts and diverse
# defences matter too.

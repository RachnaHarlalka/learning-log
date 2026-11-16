"""B6 (stretch, no tests). Fault injection: independent faults vs a correlated software bug.

Build 3 replicas of a tiny service. Each round, a "chaos monkey" kills each replica
independently with probability 10%. Compare success rates for:
  (1) always calling replica 0, no failover
  (2) failover: try replicas in random order until one answers
  (3) failover, but 1% of requests trigger a bug present in EVERY replica (like the 2012 leap second)
Explain why (2) helps so much and (3) can't be fixed by more replicas.
"""

import random

if __name__ == "__main__":
    # TODO
    pass

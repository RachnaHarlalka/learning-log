"""B4. Cloud vs self-hosting cost model: reference solution."""

import math
import random


def machines_needed(load_rps, capacity_per_machine):
    return math.ceil(load_rps / capacity_per_machine)


def self_hosted_cost(hourly_load, capacity_per_machine, cost_per_machine_hour):
    """You own enough machines for the peak, and pay for them every hour, busy or idle."""
    fleet = machines_needed(max(hourly_load), capacity_per_machine)
    return fleet * len(hourly_load) * cost_per_machine_hour


def cloud_cost(hourly_load, capacity_per_machine, cost_per_machine_hour, markup=1.5):
    """Elastic: pay only for what each hour needs, at a higher price per machine-hour."""
    machine_hours = sum(machines_needed(load, capacity_per_machine) for load in hourly_load)
    return machine_hours * cost_per_machine_hour * markup


def utilization(hourly_load, capacity_per_machine):
    """Average load divided by the capacity of the peak-sized fleet."""
    fleet_capacity = machines_needed(max(hourly_load), capacity_per_machine) * capacity_per_machine
    return sum(hourly_load) / (len(hourly_load) * fleet_capacity)


if __name__ == "__main__":
    rng = random.Random(0)
    hours = 30 * 24
    capacity, cost = 100, 10  # 100 req/s per machine, ₹10 per machine-hour

    steady = [rng.randint(900, 1100) for _ in range(hours)]
    # Analytics: nearly idle, with occasional huge bursts during office hours.
    spiky = [
        8_000 if (9 <= h % 24 <= 18 and rng.random() < 0.1) else 50
        for h in range(hours)
    ]

    for name, load in [("Steady web app", steady), ("Spiky analytics", spiky)]:
        own = self_hosted_cost(load, capacity, cost)
        cloud = cloud_cost(load, capacity, cost)
        winner = "self-host" if own < cloud else "cloud"
        print(f"{name}")
        print(f"  utilization of owned fleet: {utilization(load, capacity):.0%}")
        print(f"  self-hosted: ₹{own:>10,.0f}")
        print(f"  cloud:       ₹{cloud:>10,.0f}   -> {winner} is cheaper\n")

# What does this model ignore?
# - Staff: hiring and training people to run the system yourself (often the
#   biggest cost) and the expertise you may not have.
# - Hardware lead time, datacenter space, power, replacing failed disks.
# - Cloud pricing options: reserved/committed-use discounts (cheaper for steady
#   load), spot instances, and network egress fees.
# - Risk: vendor lock-in and outages you can't fix, vs. the value of a specialist
#   provider's operational expertise.
# - Redundancy: a real self-hosted fleet needs spare machines beyond the peak.
# So the model captures the chapter's key point (predictable load favours owning,
# variable load favours elasticity), but real decisions weigh skills and risk too.

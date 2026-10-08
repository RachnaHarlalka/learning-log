"""B4. Cloud vs self-hosting cost model. See ../../questions/questions.md for the full spec."""

import math
import random


def machines_needed(load_rps, capacity_per_machine):
    """Machines required for this load (round up)."""
    # TODO
    raise NotImplementedError


def self_hosted_cost(hourly_load, capacity_per_machine, cost_per_machine_hour):
    """Own a fleet sized for the PEAK; pay for it every hour."""
    # TODO
    raise NotImplementedError


def cloud_cost(hourly_load, capacity_per_machine, cost_per_machine_hour, markup=1.5):
    """Pay only for the machines each hour needs, at cost * markup."""
    # TODO
    raise NotImplementedError


def utilization(hourly_load, capacity_per_machine):
    """Average load / capacity of the peak-sized fleet."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: 30 days (720 hours) of a steady load vs a spiky analytics load; print costs and the winner
    pass

# What real-world costs does this model ignore?
# Answer:

"""B4. Reliability maths: hardware fault rates, redundancy, and SLO error budgets."""

import math

HOURS_PER_YEAR = 365 * 24


def expected_failures_per_day(n_components, annual_failure_rate):
    """E.g. 10,000 disks at 3%/year -> ~0.8 failures/day."""
    return n_components * annual_failure_rate / 365


def prob_at_least_one_failure(n_components, p_each):
    """Chance that at least one of n independent components fails."""
    return 1 - (1 - p_each) ** n_components


def availability_series(*availabilities):
    """All parts needed (each one is a single point of failure)."""
    return math.prod(availabilities)


def availability_parallel(*availabilities):
    """Redundant copies: the service is up if any one is up (assumes independent faults)."""
    return 1 - math.prod(1 - a for a in availabilities)


def p_data_loss_after_failure(annual_failure_rate, replicas, repair_hours):
    """After one replica fails, the chance that ALL remaining replicas also fail
    before the repair/re-replication finishes (independent faults assumed)."""
    p_fail_in_window = annual_failure_rate * repair_hours / HOURS_PER_YEAR
    return p_fail_in_window ** (replicas - 1)


def error_budget_requests(slo, total_requests):
    """How many failed requests the SLO allows, e.g. 99.9% of 1M -> 1,000."""
    return (1 - slo) * total_requests


def error_budget_minutes(slo, period_days=30):
    """Allowed full-downtime minutes in the period."""
    return (1 - slo) * period_days * 24 * 60


def burn_rate(slo, observed_error_rate):
    """How fast the budget is being spent: 1.0 = exactly on budget, 10 = 10x too fast."""
    return observed_error_rate / (1 - slo)


if __name__ == "__main__":
    print("Disk failures to expect:")
    for n in (100, 10_000, 100_000):
        print(f"  {n:>7,} disks at 3%/yr -> {expected_failures_per_day(n, 0.03):6.2f} per day")

    print("\nChance at least one of 1,000 machines has a faulty CPU core (1 in 1,000 each):",
          f"{prob_at_least_one_failure(1_000, 1 / 1_000):.0%}")

    one = 0.99
    print(f"\nOne server at 99%: {one:.2%}  |  two independent replicas: {availability_parallel(one, one):.4%}")
    print(f"Replicas behind one load balancer (99.95%): {availability_series(0.9995, availability_parallel(one, one)):.4%}")

    for replicas in (1, 2, 3):
        if replicas == 1:
            print("\n1 copy: any disk failure loses the data")
            continue
        p = p_data_loss_after_failure(0.03, replicas, repair_hours=24)
        print(f"{replicas} copies, 24 h to re-replicate: P(lose data | one disk fails) = {p:.2e}")

    slo = 0.999
    print(f"\nSLO {slo:.1%}: budget = {error_budget_minutes(slo):.1f} min/30 days, "
          f"{error_budget_requests(slo, 50_000_000):,.0f} failed requests out of 50M")
    print(f"Current error rate 0.5% -> burn rate {burn_rate(slo, 0.005):.0f}x "
          f"(budget gone in {30 / burn_rate(slo, 0.005):.0f} days)")

# The catch in every formula above: they assume INDEPENDENT faults. Disks from the
# same batch, replicas in the same rack/zone, or nodes running the same buggy
# software fail together, so real availability is lower. That's why you spread
# replicas across availability zones and roll out software gradually.

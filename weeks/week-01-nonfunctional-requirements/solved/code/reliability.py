"""B4. Reliability maths. See ../../questions/questions.md for the full spec."""

import math

HOURS_PER_YEAR = 365 * 24


def expected_failures_per_day(n_components, annual_failure_rate):
    raise NotImplementedError


def prob_at_least_one_failure(n_components, p_each):
    raise NotImplementedError


def availability_series(*availabilities):
    raise NotImplementedError


def availability_parallel(*availabilities):
    raise NotImplementedError


def p_data_loss_after_failure(annual_failure_rate, replicas, repair_hours):
    """After one replica fails: P(all remaining replicas fail within repair_hours), independent faults.
    Per-disk chance in the window = annual_failure_rate * repair_hours / HOURS_PER_YEAR."""
    raise NotImplementedError


def error_budget_requests(slo, total_requests):
    raise NotImplementedError


def error_budget_minutes(slo, period_days=30):
    raise NotImplementedError


def burn_rate(slo, observed_error_rate):
    """1.0 = spending the error budget exactly on schedule."""
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: disk failures/day for 100 / 10k / 100k disks; 1 vs 2 replicas; data-loss risk
    # for 2 and 3 copies; error budget and burn rate for a 99.9% SLO
    pass

# Which assumption makes all these numbers too optimistic in real life?
# Answer:

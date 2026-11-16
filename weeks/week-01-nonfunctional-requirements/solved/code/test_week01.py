"""Tests for Week 1. No extra libraries needed.

    python3 solved/code/test_week01.py                       # tests your code
    WEEK_IMPL=solutions python3 solved/code/test_week01.py   # tests the reference code
"""

import math
import os
import random
import statistics
import sys
from pathlib import Path

_WEEK_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_WEEK_DIR / os.environ.get("WEEK_IMPL", "solved") / "code"))
sys.dont_write_bytecode = True

import capacity  # noqa: E402
import fanout  # noqa: E402
import migration  # noqa: E402
import overload  # noqa: E402
import percentiles  # noqa: E402
import reliability  # noqa: E402


# ---------- B1: fan-out ----------

# 0 is a "celebrity" followed by everyone; 1 follows 2 and 3; 2 follows 3.
_FOLLOWS = {0: set(), 1: {0, 2, 3}, 2: {0, 3}, 3: {0}, 4: {0, 1}}


def _post_all(timeline):
    timeline.post(3, "p1", 1)
    timeline.post(0, "c1", 2)
    timeline.post(2, "p2", 3)
    timeline.post(1, "p3", 4)
    timeline.post(0, "c2", 5)
    return timeline


def test_followers_of():
    assert fanout.followers_of(_FOLLOWS)[0] == {1, 2, 3, 4}
    assert fanout.followers_of(_FOLLOWS)[3] == {1, 2}
    assert fanout.followers_of(_FOLLOWS)[4] == set()


def test_all_strategies_return_same_timeline():
    expected = {1: ["c2", "p2", "c1", "p1"], 2: ["c2", "c1", "p1"], 4: ["c2", "p3", "c1"], 0: []}
    for timeline in (fanout.PullTimeline(_FOLLOWS), fanout.PushTimeline(_FOLLOWS),
                     fanout.HybridTimeline(_FOLLOWS, celebrity_threshold=4)):
        _post_all(timeline)
        for user, posts in expected.items():
            assert timeline.home_timeline(user) == posts, (type(timeline).__name__, user)
        assert timeline.home_timeline(1, limit=2) == ["c2", "p2"]


def test_pull_costs():
    t = _post_all(fanout.PullTimeline(_FOLLOWS))
    assert t.writes == 5
    t.home_timeline(1)
    assert t.reads == 3  # one lookup per followee


def test_push_costs():
    t = _post_all(fanout.PushTimeline(_FOLLOWS))
    assert t.writes == 2 + 4 + 1 + 1 + 4  # one write per follower of each author
    t.home_timeline(1)
    assert t.reads == 1


def test_hybrid_costs():
    t = _post_all(fanout.HybridTimeline(_FOLLOWS, celebrity_threshold=4))
    assert t.celebrities == {0}
    assert t.writes == 2 + 1 + 1 + 1 + 1  # celebrity posts stored once
    t.home_timeline(1)
    assert t.reads == 2  # own timeline + one followed celebrity


# ---------- B2: percentiles ----------

def test_percentile_and_summary():
    values = list(range(1, 1001))
    assert percentiles.percentile(values, 50) == 500
    assert percentiles.percentile(values, 99.9) == 999
    s = percentiles.summarize(values)
    assert set(s) == {"mean", "p50", "p95", "p99", "p999", "max"} and s["p999"] == 999
    for bad in [([], 50), ([1], 0), ([1], 101)]:
        try:
            percentiles.percentile(*bad)
        except ValueError:
            continue
        raise AssertionError(f"expected ValueError for {bad}")


def test_tail_amplification():
    assert math.isclose(percentiles.tail_amplification(100, 0.01), 1 - 0.99 ** 100)


def test_histogram_accuracy():
    rng = random.Random(3)
    values = [rng.lognormvariate(3, 1) for _ in range(20_000)]
    hist = percentiles.Histogram(precision=0.01)
    for v in values:
        hist.record(v)
    assert hist.count == 20_000
    for p in (50, 95, 99, 99.9):
        exact = percentiles.percentile(values, p)
        assert abs(hist.percentile(p) - exact) / exact <= 0.011, p


def test_merging_histograms_beats_averaging_percentiles():
    rng = random.Random(4)
    a = [rng.uniform(20, 60) for _ in range(9_000)]
    b = [rng.uniform(20, 60) if rng.random() > 0.05 else rng.uniform(800, 1200) for _ in range(1_000)]
    ha, hb = percentiles.Histogram(), percentiles.Histogram()
    for v in a:
        ha.record(v)
    for v in b:
        hb.record(v)
    merged = ha.merge(hb)
    true_p99 = percentiles.percentile(a + b, 99)
    assert merged.count == 10_000
    assert abs(merged.percentile(99) - true_p99) / true_p99 <= 0.011
    assert percentiles.average_of_percentiles([a, b], 99) > 5 * true_p99  # badly wrong


# ---------- B3: overload ----------

def test_queueing_delay_grows_with_utilization():
    low = statistics.fmean(overload.simulate_queue(0.5, n_requests=30_000, seed=1))
    high = statistics.fmean(overload.simulate_queue(0.9, n_requests=30_000, seed=1))
    assert 15 < low < 25      # theory: 10 / (1 - 0.5) = 20 ms
    assert 75 < high < 125    # theory: 10 / (1 - 0.9) = 100 ms


def test_retry_storm_is_metastable():
    stats = overload.simulate_retry_storm()
    last = stats[-1]
    assert last["arrivals"] == 80          # the spike is long over...
    assert last["goodput"] == 0            # ...yet nobody gets a useful answer
    assert last["queue"] > stats[60]["queue"] > 1_000  # and the backlog keeps growing


def test_no_retries_recovers():
    assert overload.simulate_retry_storm(max_retries=0)[-1]["goodput"] == 80


def test_load_shedding_recovers():
    stats = overload.simulate_retry_storm(shed_expired=True)
    assert stats[-1]["goodput"] == 80 and stats[-1]["queue"] == 0
    assert all(s["wasted"] == 0 for s in stats)  # capacity never spent on abandoned requests


# ---------- B4: reliability ----------

def test_failure_rates():
    assert math.isclose(reliability.expected_failures_per_day(10_000, 0.0365), 1.0)
    assert math.isclose(reliability.prob_at_least_one_failure(2, 0.5), 0.75)


def test_redundancy_and_spof():
    assert math.isclose(reliability.availability_parallel(0.99, 0.99), 0.9999)
    assert math.isclose(reliability.availability_series(0.99, 0.99), 0.9801)
    assert math.isclose(reliability.p_data_loss_after_failure(0.0876, 3, 100), 0.001 ** 2)


def test_error_budgets():
    assert math.isclose(reliability.error_budget_requests(0.999, 1_000_000), 1_000)
    assert math.isclose(reliability.error_budget_minutes(0.999), 43.2)
    assert math.isclose(reliability.burn_rate(0.999, 0.005), 5)


# ---------- B5: capacity ----------

def test_months_until_limit():
    assert capacity.months_until_limit(4_000, 10_000, 0.08) == 12
    assert capacity.months_until_limit(12_000, 10_000, 0.08) == 0
    assert capacity.months_until_limit(4_000, 10_000, 0) == math.inf


def test_nodes_needed():
    assert capacity.nodes_needed(50_000, 2_000) == 37
    assert capacity.nodes_needed(1_000, 1_000, target_utilization=1.0, spare=0) == 1


def test_scaling_classification():
    assert capacity.scaling_efficiency({1: 100, 4: 300})[4] == 0.75
    assert capacity.classify_scaling({1: 100, 2: 200, 4: 395}) == "linear"
    assert capacity.classify_scaling({1: 100, 2: 180, 8: 400}) == "sublinear"
    assert capacity.classify_scaling({1: 100, 4: 480}) == "superlinear"


# ---------- B7: reversible migration ----------

def test_migration_phases_route_reads_and_writes():
    old, new = {"a": 1}, {}
    m = migration.MigratingStore(old, new)
    m.put("b", 2)
    assert old == {"a": 1, "b": 2} and new == {}                # old_only
    assert m.advance() == "dual_write"
    m.put("c", 3)
    assert old["c"] == 3 and new == {"c": 3}                    # writes both
    assert m.backfill() == 2 and m.backfill() == 0              # idempotent
    assert m.get("a") == 1                                      # still reads old
    m.delete("c")
    assert "c" not in old and "c" not in new


def test_shadow_reads_block_cutover_on_mismatch():
    old, new = {"a": 1}, {}
    m = migration.MigratingStore(old, new)
    m.advance(); m.backfill(); m.advance()                      # shadow_read
    new["a"] = 999                                              # corrupt the new store
    assert m.get("a") == 1                                      # users still see old data
    assert m.mismatches == ["a"]
    try:
        m.advance()
    except RuntimeError:
        pass
    else:
        raise AssertionError("cutover must be refused while shadow reads disagree")


def test_rollback_until_irreversible():
    old, new = {"a": 1}, {}
    m = migration.MigratingStore(old, new)
    m.advance(); m.backfill(); m.advance(); m.get("a")
    assert m.advance() == "new_primary"
    m.put("b", 2)
    assert m.get("b") == 2 and old["b"] == 2                    # old still current
    assert m.rollback() == "shadow_read" and m.get("b") == 2    # safe to go back
    m.advance(); m.advance()                                    # new_only
    m.put("c", 3)
    assert "c" not in old                                       # old now stale
    try:
        m.rollback()
    except migration.IrreversibleError:
        pass
    else:
        raise AssertionError("rollback from new_only must be impossible")
    try:
        m.advance()
    except ValueError:
        pass
    else:
        raise AssertionError("nothing beyond new_only")


# ---------- tiny runner so pytest is optional ----------

if __name__ == "__main__":
    passed = failed = todo = 0
    for name, fn in list(globals().items()):
        if not (name.startswith("test_") and callable(fn)):
            continue
        try:
            fn()
            passed += 1
            print(f"PASS  {name}")
        except NotImplementedError:
            todo += 1
            print(f"TODO  {name}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL  {name}: {type(e).__name__}: {e}")
    print(f"\n{passed} passed, {failed} failed, {todo} not implemented yet")
    sys.exit(1 if failed or todo else 0)

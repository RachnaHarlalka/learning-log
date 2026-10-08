"""Tests for Week 0. No extra libraries needed.

    python3 solved/code/test_week00.py                       # tests your code
    WEEK_IMPL=solutions python3 solved/code/test_week00.py   # tests the reference code
"""

import math
import os
import sqlite3
import sys
import tempfile
from pathlib import Path

_WEEK_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(_WEEK_DIR / os.environ.get("WEEK_IMPL", "solved") / "code"))
sys.dont_write_bytecode = True

import cloud_cost  # noqa: E402
import derived_data  # noqa: E402
import etl_pipeline  # noqa: E402
import oltp_vs_olap  # noqa: E402
import user_events  # noqa: E402


# ---------- B1: OLTP vs OLAP ----------

def _small_orders_db():
    conn = sqlite3.connect(":memory:")
    oltp_vs_olap.create_orders_db(conn, n_orders=1_000, n_customers=50, seed=1)
    return conn


def test_create_orders_db():
    conn = _small_orders_db()
    assert conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0] == 1_000
    stores = {r[0] for r in conn.execute("SELECT DISTINCT store FROM orders")}
    assert stores <= set(oltp_vs_olap.STORES)
    assert conn.execute("SELECT typeof(amount_paise) FROM orders LIMIT 1").fetchone()[0] == "integer"


def test_get_order():
    conn = _small_orders_db()
    assert oltp_vs_olap.get_order(conn, 1)[0] == 1
    assert oltp_vs_olap.get_order(conn, 999_999) is None


def test_orders_for_customer():
    conn = _small_orders_db()
    rows = oltp_vs_olap.orders_for_customer(conn, 7)
    expected = conn.execute("SELECT COUNT(*) FROM orders WHERE customer_id = 7").fetchone()[0]
    assert len(rows) == expected > 0


def test_revenue_by_store_matches_total():
    conn = _small_orders_db()
    revenue = oltp_vs_olap.revenue_by_store(conn)
    total = conn.execute("SELECT SUM(amount_paise) FROM orders").fetchone()[0]
    assert isinstance(revenue, dict) and sum(revenue.values()) == total


def test_add_customer_index():
    conn = _small_orders_db()
    oltp_vs_olap.add_customer_index(conn)
    indexed_cols = [
        info[2]
        for (name,) in conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='orders'")
        for info in conn.execute(f"PRAGMA index_info('{name}')")
    ]
    assert "customer_id" in indexed_cols


def test_best_time():
    t = oltp_vs_olap.best_time(sum, [1, 2, 3], repeat=3)
    assert isinstance(t, float) and t >= 0


# ---------- B2: ETL ----------

_STORES = [{"store_id": 1, "name": "Andheri West", "city": "Mumbai"}]
_ORDERS = [
    {"order_id": 1, "store_id": 1, "amount": "12.50", "status": "completed", "created_at": "2026-01-15T10:30:00"},
    {"order_id": 2, "store_id": 1, "amount": "99.99", "status": "cancelled", "created_at": "2026-01-16T10:30:00"},
    {"order_id": 3, "store_id": 1, "amount": "5.00", "status": "test", "created_at": "2026-01-16T10:30:00"},
    {"order_id": 4, "store_id": 99, "amount": "40.00", "status": "completed", "created_at": "2026-01-17T10:30:00"},
    {"order_id": 5, "store_id": 1, "amount": "0.10", "status": "completed", "created_at": "2026-02-01T00:00:00"},
]


def test_extract():
    orders_db, stores_db = etl_pipeline.setup_sources(n_orders=100, seed=1)
    orders, stores = etl_pipeline.extract(orders_db, stores_db)
    assert len(orders) == 100 and len(stores) == len(etl_pipeline.STORES)
    assert {"order_id", "store_id", "amount", "status", "created_at"} <= set(orders[0])
    assert {"store_id", "name", "city"} <= set(stores[0])


def test_transform_cleans_and_joins():
    rows = etl_pipeline.transform(_ORDERS, _STORES)
    assert [r["order_id"] for r in rows] == [1, 5]
    first = rows[0]
    assert first == {
        "order_id": 1, "store_name": "Andheri West", "city": "Mumbai",
        "amount_paise": 1250, "order_date": "2026-01-15", "month": "2026-01",
    }
    assert rows[1]["amount_paise"] == 10  # "0.10" -> 10 paise, no float error


def test_load_is_idempotent_and_query_works():
    rows = etl_pipeline.transform(_ORDERS, _STORES)
    wh = sqlite3.connect(":memory:")
    assert etl_pipeline.load(wh, rows) == 2
    etl_pipeline.load(wh, rows)
    assert wh.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == 2
    assert etl_pipeline.revenue_by_store_for_month(wh, "2026-01") == {"Andheri West": 1250}


def test_run_pipeline_end_to_end():
    wh = etl_pipeline.run_pipeline(n_orders=500, seed=2)
    orders_db, stores_db = etl_pipeline.setup_sources(n_orders=500, seed=2)
    expected = sum(
        1 for o in etl_pipeline.extract(orders_db, stores_db)[0]
        if o["status"] == "completed" and o["store_id"] != etl_pipeline.UNKNOWN_STORE_ID
    )
    assert wh.execute("SELECT COUNT(*) FROM sales").fetchone()[0] == expected


# ---------- B3: derived data ----------

def _store():
    s = derived_data.ProfileStore()
    s.put(1, {"name": "Asha", "city": "Pune"})
    s.put(2, {"name": "Ravi", "city": "Delhi"})
    s.put(3, {"name": "Meera", "city": "Pune"})
    return s


def test_build_city_index():
    assert derived_data.build_city_index(_store()) == {"Pune": {1, 3}, "Delhi": {2}}


def test_cache_hits_and_misses():
    cache = derived_data.ProfileCache(_store())
    assert cache.get(1)["name"] == "Asha"
    cache.get(1)
    assert cache.get(42) is None
    assert (cache.hits, cache.misses) == (1, 2)


def test_cache_goes_stale_without_propagation():
    store = _store()
    cache = derived_data.ProfileCache(store)
    cache.get(1)
    store.put(1, {"name": "Asha", "city": "Mumbai"})
    assert cache.get(1)["city"] == "Pune"  # stale: that's the point
    cache.invalidate(1)
    assert cache.get(1)["city"] == "Mumbai"


def test_update_profile_propagates():
    store = _store()
    cache = derived_data.ProfileCache(store)
    index = derived_data.build_city_index(store)
    cache.get(2)
    derived_data.update_profile(store, cache, index, 2, {"name": "Ravi", "city": "Pune"})
    assert store.get(2)["city"] == "Pune"
    assert cache.get(2)["city"] == "Pune"
    assert index == {"Pune": {1, 2, 3}}  # empty "Delhi" key removed
    assert index == derived_data.build_city_index(store)  # matches a fresh rebuild


def test_update_profile_new_user():
    store = _store()
    cache = derived_data.ProfileCache(store)
    index = derived_data.build_city_index(store)
    derived_data.update_profile(store, cache, index, 4, {"name": "Kabir", "city": "Goa"})
    assert index["Goa"] == {4} and cache.get(4)["name"] == "Kabir"


# ---------- B4: cloud cost ----------

def test_machines_needed():
    assert cloud_cost.machines_needed(250, 100) == 3
    assert cloud_cost.machines_needed(200, 100) == 2


def test_steady_load_favours_self_hosting():
    load = [100] * 24
    assert cloud_cost.self_hosted_cost(load, 100, 1) == 24
    assert math.isclose(cloud_cost.cloud_cost(load, 100, 1), 36)
    assert math.isclose(cloud_cost.utilization(load, 100), 1.0)


def test_spiky_load_favours_cloud():
    load = [0] * 23 + [1_000]
    assert cloud_cost.self_hosted_cost(load, 100, 1) == 240
    assert math.isclose(cloud_cost.cloud_cost(load, 100, 1), 15)
    assert math.isclose(cloud_cost.utilization(load, 100), 1_000 / (24 * 1_000))


# ---------- B6: right to be forgotten ----------

def _event_log(tmp):
    log = os.path.join(tmp, "events.jsonl")
    for user_id, ts in [(2, "2025-06-01"), (1, "2026-01-10"), (1, "2026-03-01"), (3, "2026-03-02"), (2, "2026-03-05")]:
        user_events.append_event(log, {"user_id": user_id, "type": "view", "ts": ts, "data": {}})
    return log


def test_append_and_read_events():
    with tempfile.TemporaryDirectory() as tmp:
        assert user_events.read_events(os.path.join(tmp, "missing.jsonl")) == []
        log = _event_log(tmp)
        events = user_events.read_events(log)
        assert len(events) == 5 and events[0]["user_id"] == 2 and events[-1]["ts"] == "2026-03-05"
        with open(log, encoding="utf-8") as f:
            assert len(f.readlines()) == 5  # one JSON object per line


def test_build_event_counts():
    with tempfile.TemporaryDirectory() as tmp:
        assert user_events.build_event_counts(_event_log(tmp)) == {2: 2, 1: 2, 3: 1}


def test_forget_user():
    with tempfile.TemporaryDirectory() as tmp:
        log = _event_log(tmp)
        assert user_events.forget_user(log, 1) == 2
        assert all(e["user_id"] != 1 for e in user_events.read_events(log))
        assert len(user_events.read_events(log)) == 3
        assert user_events.forget_user(log, 42) == 0
        assert os.listdir(tmp) == ["events.jsonl"]  # no leftover temp files


def test_forget_everywhere_cleans_derived_data():
    with tempfile.TemporaryDirectory() as tmp:
        log = _event_log(tmp)
        counts = user_events.build_event_counts(log)
        assert user_events.forget_everywhere(log, counts, 2) == 2
        assert 2 not in counts
        assert counts == user_events.build_event_counts(log)


def test_purge_older_than():
    with tempfile.TemporaryDirectory() as tmp:
        log = _event_log(tmp)
        assert user_events.purge_older_than(log, "2026-03-01") == 2
        assert sorted(e["ts"] for e in user_events.read_events(log)) == ["2026-03-01", "2026-03-02", "2026-03-05"]


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

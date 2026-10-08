"""B2. Mini ETL pipeline. See ../../questions/questions.md for the full spec."""

import random
import sqlite3
from decimal import Decimal

STORES = [
    (1, "Andheri West", "Mumbai"),
    (2, "Connaught Place", "Delhi"),
    (3, "Koramangala", "Bengaluru"),
    (4, "Park Street", "Kolkata"),
]
UNKNOWN_STORE_ID = 99  # dirty data: points to a store that doesn't exist


def setup_sources(n_orders=2_000, seed=0):
    """Two separate operational databases (data silos). Given; no changes needed."""
    stores_db = sqlite3.connect(":memory:")
    stores_db.execute("CREATE TABLE stores (store_id INTEGER PRIMARY KEY, name TEXT, city TEXT)")
    stores_db.executemany("INSERT INTO stores VALUES (?, ?, ?)", STORES)

    orders_db = sqlite3.connect(":memory:")
    orders_db.execute(
        "CREATE TABLE orders (order_id INTEGER PRIMARY KEY, store_id INTEGER, "
        "amount TEXT, status TEXT, created_at TEXT)"
    )
    rng = random.Random(seed)
    rows = []
    for order_id in range(1, n_orders + 1):
        store_id = UNKNOWN_STORE_ID if rng.random() < 0.02 else rng.randint(1, len(STORES))
        amount = f"{rng.randint(50, 5000)}.{rng.randint(0, 99):02d}"
        status = rng.choices(["completed", "cancelled", "test"], weights=[90, 8, 2])[0]
        created_at = (
            f"2026-{rng.randint(1, 3):02d}-{rng.randint(1, 28):02d}"
            f"T{rng.randint(0, 23):02d}:{rng.randint(0, 59):02d}:00"
        )
        rows.append((order_id, store_id, amount, status, created_at))
    orders_db.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", rows)
    return orders_db, stores_db


def extract(orders_db, stores_db):
    """E: return (orders, stores) as lists of dicts."""
    # TODO
    raise NotImplementedError


def transform(orders, stores):
    """T: keep completed orders with a known store; output keys:
    order_id, store_name, city, amount_paise, order_date, month."""
    # TODO
    raise NotImplementedError


def load(warehouse, rows):
    """L: create table `sales` and insert rows. Must be safe to run twice. Return len(rows)."""
    # TODO
    raise NotImplementedError


def revenue_by_store_for_month(warehouse, month):
    """{store_name: total_paise} for month 'YYYY-MM'."""
    # TODO
    raise NotImplementedError


def run_pipeline(n_orders=2_000, seed=0):
    """Wire E -> T -> L together; return the warehouse connection."""
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: run the pipeline, print kept/dropped counts and January revenue per store
    pass

# Is the warehouse a system of record or derived data? If deleted, what would you do?
# Answer:

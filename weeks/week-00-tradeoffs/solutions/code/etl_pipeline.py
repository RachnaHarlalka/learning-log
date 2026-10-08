"""B2. Mini ETL pipeline: reference solution."""

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
    """E: pull raw rows out of each operational system."""
    order_cols = ["order_id", "store_id", "amount", "status", "created_at"]
    store_cols = ["store_id", "name", "city"]
    orders = [dict(zip(order_cols, row)) for row in orders_db.execute(f"SELECT {', '.join(order_cols)} FROM orders")]
    stores = [dict(zip(store_cols, row)) for row in stores_db.execute(f"SELECT {', '.join(store_cols)} FROM stores")]
    return orders, stores


def transform(orders, stores):
    """T: clean, join across silos, and reshape into an analysis-friendly row."""
    stores_by_id = {s["store_id"]: s for s in stores}
    rows = []
    for order in orders:
        if order["status"] != "completed":
            continue
        store = stores_by_id.get(order["store_id"])
        if store is None:
            continue
        rows.append(
            {
                "order_id": order["order_id"],
                "store_name": store["name"],
                "city": store["city"],
                "amount_paise": int(Decimal(order["amount"]) * 100),
                "order_date": order["created_at"][:10],
                "month": order["created_at"][:7],
            }
        )
    return rows


def load(warehouse, rows):
    """L: write into the warehouse. INSERT OR REPLACE makes reruns safe (idempotent)."""
    warehouse.execute(
        "CREATE TABLE IF NOT EXISTS sales (order_id INTEGER PRIMARY KEY, store_name TEXT, "
        "city TEXT, amount_paise INTEGER, order_date TEXT, month TEXT)"
    )
    warehouse.executemany(
        "INSERT OR REPLACE INTO sales VALUES "
        "(:order_id, :store_name, :city, :amount_paise, :order_date, :month)",
        rows,
    )
    warehouse.commit()
    return len(rows)


def revenue_by_store_for_month(warehouse, month):
    """The analyst's question: total revenue of each store in a month."""
    return dict(
        warehouse.execute(
            "SELECT store_name, SUM(amount_paise) FROM sales WHERE month = ? GROUP BY store_name",
            (month,),
        ).fetchall()
    )


def run_pipeline(n_orders=2_000, seed=0):
    orders_db, stores_db = setup_sources(n_orders, seed)
    warehouse = sqlite3.connect(":memory:")
    load(warehouse, transform(*extract(orders_db, stores_db)))
    return warehouse


if __name__ == "__main__":
    orders_db, stores_db = setup_sources()
    orders, stores = extract(orders_db, stores_db)
    rows = transform(orders, stores)
    warehouse = sqlite3.connect(":memory:")
    load(warehouse, rows)
    load(warehouse, rows)  # rerun: must not duplicate
    total = warehouse.execute("SELECT COUNT(*) FROM sales").fetchone()[0]

    print(f"Extracted {len(orders)} orders, kept {len(rows)}, dropped {len(orders) - len(rows)}")
    print(f"Rows in warehouse after loading twice: {total}")
    print("\nJanuary 2026 revenue by store")
    for store, paise in sorted(revenue_by_store_for_month(warehouse, "2026-01").items()):
        print(f"  {store:<16} ₹{paise / 100:>12,.2f}")

# Is the warehouse a system of record or derived data?
# Derived. Every row was computed from the orders and stores databases, which
# are the systems of record. If the warehouse were deleted, nothing is truly
# lost: rerun the pipeline to rebuild it. (That's also why load() must be safe
# to rerun.) If the warehouse ever disagrees with the orders DB, the orders DB
# is right by definition and the pipeline has a bug or is behind.

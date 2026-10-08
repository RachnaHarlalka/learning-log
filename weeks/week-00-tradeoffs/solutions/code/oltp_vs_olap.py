"""B1. Feel the OLTP vs OLAP difference: reference solution."""

import random
import sqlite3
import time
from datetime import date, timedelta

STORES = ["Mumbai", "Delhi", "Bengaluru", "Kolkata", "Pune"]


def create_orders_db(conn, n_orders=200_000, n_customers=20_000, seed=0):
    """Create and fill the orders table. Money is integer paise (₹1 = 100 paise)."""
    rng = random.Random(seed)
    conn.execute(
        """CREATE TABLE orders (
               id           INTEGER PRIMARY KEY,
               customer_id  INTEGER NOT NULL,
               store        TEXT    NOT NULL,
               amount_paise INTEGER NOT NULL,
               created_at   TEXT    NOT NULL
           )"""
    )
    start = date(2026, 1, 1)
    rows = (
        (
            order_id,
            rng.randint(1, n_customers),
            rng.choice(STORES),
            rng.randint(5_000, 500_000),  # ₹50 to ₹5,000
            (start + timedelta(days=rng.randrange(90))).isoformat(),
        )
        for order_id in range(1, n_orders + 1)
    )
    conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", rows)
    conn.commit()


def get_order(conn, order_id):
    """OLTP point query by primary key."""
    return conn.execute("SELECT * FROM orders WHERE id = ?", (order_id,)).fetchone()


def orders_for_customer(conn, customer_id):
    """OLTP lookup: 'show my orders'."""
    return conn.execute("SELECT * FROM orders WHERE customer_id = ?", (customer_id,)).fetchall()


def revenue_by_store(conn):
    """OLAP aggregate: must read every row."""
    return dict(conn.execute("SELECT store, SUM(amount_paise) FROM orders GROUP BY store").fetchall())


def add_customer_index(conn):
    conn.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id)")


def best_time(fn, *args, repeat=5):
    """Fastest of `repeat` runs, in seconds (the minimum is the least noisy)."""
    best = float("inf")
    for _ in range(repeat):
        start = time.perf_counter()
        fn(*args)
        best = min(best, time.perf_counter() - start)
    return best


if __name__ == "__main__":
    conn = sqlite3.connect(":memory:")
    print("Creating 200,000 orders...")
    create_orders_db(conn)

    queries = [
        ("point: order by id", get_order, (conn, 123_456)),
        ("lookup: orders of a customer", orders_for_customer, (conn, 4_242)),
        ("aggregate: revenue by store", revenue_by_store, (conn,)),
    ]
    before = {name: best_time(fn, *args) for name, fn, args in queries}
    add_customer_index(conn)
    after = {name: best_time(fn, *args) for name, fn, args in queries}

    print(f"\n{'query':<30} {'before (ms)':>12} {'after (ms)':>11} {'speed-up':>9}")
    print("-" * 65)
    for name, _, _ in queries:
        b, a = before[name] * 1000, after[name] * 1000
        print(f"{name:<30} {b:>12.3f} {a:>11.3f} {b / a:>8.0f}x")

# Which query sped up, which didn't, and why?
# - Order by id: already fast. The PRIMARY KEY is itself an index, so it jumps
#   straight to the row.
# - Orders of a customer: becomes hundreds of times faster. Without the index,
#   SQLite scans all 200k rows to find ~10; with it, it jumps straight to them.
#   This is the OLTP pattern: indexes make point queries cheap.
# - Revenue by store: no faster. An aggregate must read EVERY row anyway, so an
#   index on customer_id can't help. Analytical queries are scan-heavy, which is
#   why analytical systems use different storage layouts (column stores,
#   compression; see Week 7) instead of just adding indexes, and why running them
#   on the OLTP database would steal resources from real users.

"""B1. Feel the OLTP vs OLAP difference. See ../../questions/questions.md for the full spec."""

import random
import sqlite3
import time
from datetime import date, timedelta

STORES = ["Mumbai", "Delhi", "Bengaluru", "Kolkata", "Pune"]


def create_orders_db(conn, n_orders=200_000, n_customers=20_000, seed=0):
    """Create table orders(id INTEGER PRIMARY KEY, customer_id, store, amount_paise, created_at) and fill it."""
    # TODO: rng = random.Random(seed); use conn.executemany for speed; conn.commit()
    raise NotImplementedError


def get_order(conn, order_id):
    """Point query by primary key. Return the row tuple, or None."""
    # TODO
    raise NotImplementedError


def orders_for_customer(conn, customer_id):
    """All orders of one customer (list of row tuples)."""
    # TODO
    raise NotImplementedError


def revenue_by_store(conn):
    """Aggregate: {store: total_paise}."""
    # TODO
    raise NotImplementedError


def add_customer_index(conn):
    """Create an index on orders(customer_id)."""
    # TODO
    raise NotImplementedError


def best_time(fn, *args, repeat=5):
    """Fastest of `repeat` runs of fn(*args), in seconds."""
    # TODO: time.perf_counter()
    raise NotImplementedError


if __name__ == "__main__":
    # TODO: create the DB, time all 3 queries before and after add_customer_index, print a table
    pass

# Which query sped up, which didn't, and why?
# Answer:

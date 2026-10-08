"""B7 (stretch). Mini distributed tracing: reference solution."""

import contextvars
import functools
import time
import uuid

SPANS = []
_current_span = contextvars.ContextVar("current_span", default=None)


def traced(service, operation):
    """Record a span (who called what, how long) for every call of the decorated function."""

    def decorator(fn):
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            parent = _current_span.get()
            span = {
                "trace_id": parent["trace_id"] if parent else uuid.uuid4().hex[:8],
                "span_id": uuid.uuid4().hex[:8],
                "parent_id": parent["span_id"] if parent else None,
                "service": service,
                "operation": operation,
            }
            token = _current_span.set(span)
            start = time.perf_counter()
            try:
                return fn(*args, **kwargs)
            finally:
                span["duration_ms"] = (time.perf_counter() - start) * 1000
                _current_span.reset(token)
                SPANS.append(span)

        return wrapper

    return decorator


@traced("auth", "verify_token")
def verify_token():
    time.sleep(0.01)


@traced("db", "SELECT stock")
def query_stock():
    time.sleep(0.02)


@traced("inventory", "reserve_items")
def reserve_items():
    query_stock()
    time.sleep(0.005)


@traced("payment", "charge_card")
def charge_card():
    time.sleep(0.15)  # the culprit


@traced("frontend", "checkout")
def checkout():
    verify_token()
    reserve_items()
    charge_card()


def print_tree(spans, parent_id=None, depth=0):
    for span in [s for s in spans if s["parent_id"] == parent_id]:
        name = f"{'    ' * depth}{span['service']}.{span['operation']}"
        print(f"{name:<36} {span['duration_ms']:7.1f} ms")
        print_tree(spans, span["span_id"], depth + 1)


if __name__ == "__main__":
    checkout()
    print(f"trace {SPANS[0]['trace_id']}")
    print_tree(SPANS)
    # Slowest by *self time* would subtract children; total duration is enough here
    leaf_ids = {s["span_id"] for s in SPANS} - {s["parent_id"] for s in SPANS}
    slowest = max((s for s in SPANS if s["span_id"] in leaf_ids), key=lambda s: s["duration_ms"])
    print(f"\nslowest leaf call: {slowest['service']}.{slowest['operation']} ({slowest['duration_ms']:.0f} ms)")

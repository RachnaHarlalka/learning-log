"""B7 (stretch, no tests). Mini distributed tracing.

Write a decorator @traced(service, operation) that records a span per call:
trace_id, span_id, parent_id, service, operation, duration_ms.
Use contextvars.ContextVar to remember the current span so nested calls get the
right parent. Simulate frontend.checkout -> auth, inventory (-> db), payment (slow),
using time.sleep. Print the spans as an indented tree and name the slowest call.
"""

import contextvars
import functools
import time
import uuid

SPANS = []


def traced(service, operation):
    # TODO
    raise NotImplementedError


if __name__ == "__main__":
    # TODO
    pass

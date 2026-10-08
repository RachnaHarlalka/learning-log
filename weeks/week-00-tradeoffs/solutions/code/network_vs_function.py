"""B5 (stretch). Network call vs function call: reference solution."""

import threading
import time
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse


def add(a, b):
    return a + b


class AddHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        params = parse_qs(urlparse(self.path).query)
        body = str(add(int(params["a"][0]), int(params["b"][0]))).encode()
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):  # keep the output quiet
        pass


def per_call_seconds(fn, n):
    start = time.perf_counter()
    for _ in range(n):
        fn()
    return (time.perf_counter() - start) / n


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 0), AddHandler)  # port 0 = any free port
    threading.Thread(target=server.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{server.server_address[1]}/?a=1&b=2"

    local = per_call_seconds(lambda: add(1, 2), 100_000)
    remote = per_call_seconds(lambda: urllib.request.urlopen(url).read(), 500)
    server.shutdown()

    print(f"function call: {local * 1e6:10.3f} µs")
    print(f"HTTP call:     {remote * 1e6:10.3f} µs  (same machine, no real network!)")
    print(f"ratio:         {remote / local:10,.0f}x slower")

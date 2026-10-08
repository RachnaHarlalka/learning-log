"""B5 (stretch, no tests). Network call vs function call.

Time 100,000 calls to add(a, b), then 500 HTTP requests to a local server doing
the same addition. Print the time per call for each, and the ratio.
Hints: http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler) picks a free
port; run server.serve_forever in a daemon thread; use urllib.request.urlopen.
"""


def add(a, b):
    return a + b


if __name__ == "__main__":
    # TODO
    pass

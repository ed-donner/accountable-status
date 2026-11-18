import threading
import time
from datetime import UTC, datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

import pytest

from status.db import create_schema, make_engine

T0 = datetime(2026, 6, 15, 12, 0, tzinfo=UTC)


@pytest.fixture
def engine(tmp_path):
    """A SQLite database in a temporary folder, one per test."""
    eng = make_engine(tmp_path / "test.db")
    create_schema(eng)
    yield eng
    eng.dispose()


class StandIn:
    """A small local HTTP server standing in for one address of Accountable."""

    def __init__(self, status: int = 200, delay: float = 0.0):
        outer = self
        self.status = status
        self.delay = delay

        class Handler(BaseHTTPRequestHandler):
            def do_GET(self):
                if outer.delay:
                    time.sleep(outer.delay)
                self.send_response(outer.status)
                self.send_header("Content-Length", "2")
                self.end_headers()
                self.wfile.write(b"ok")

            def log_message(self, *args):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.url = f"http://127.0.0.1:{self.server.server_address[1]}/"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def stop(self):
        self.server.shutdown()
        self.server.server_close()


@pytest.fixture
def stand_in_factory():
    made = []

    def make(**kwargs):
        s = StandIn(**kwargs)
        made.append(s)
        return s

    yield make
    for s in made:
        try:
            s.stop()
        except OSError:
            pass

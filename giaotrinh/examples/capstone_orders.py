"""Local capstone fixture: a green health check can hide bad order data.

Run with Python 3.12+: ``python examples/capstone_orders.py``. The HTTP server
binds only to loopback, and all database files live in a temporary directory.
This is a teaching fixture, not a deployment or a production HTTP service.
"""

from __future__ import annotations

import hashlib
import json
import sqlite3
import tempfile
import threading
import uuid
from contextlib import closing, contextmanager
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen


def initialize(path: Path) -> None:
    with closing(sqlite3.connect(path)) as db:
        db.execute("""CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY,
            amount_cents INTEGER NOT NULL,
            schema_version INTEGER NOT NULL
        )""")
        db.commit()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, _format: str, *_args: object) -> None:
        pass  # The demo records only explicit request IDs and outcomes.

    def reply(self, status: int, request_id: str, **payload: object) -> None:
        body = json.dumps({"request_id": request_id, "revision": self.server.revision,
                           **payload}, sort_keys=True).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Revision", self.server.revision)
        self.send_header("X-Request-ID", request_id)
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        request_id = self.headers.get("X-Request-ID", "")
        if not request_id:
            self.reply(400, "missing", error="request_id_required")
            return
        if self.path == "/health":
            self.reply(200, request_id, healthy=True)
            return
        if not self.path.startswith("/orders/"):
            self.reply(404, request_id, error="not_found")
            return
        try:
            order_id = int(self.path.removeprefix("/orders/"))
            if order_id < 1:
                raise ValueError
        except ValueError:
            self.reply(400, request_id, error="invalid_order_id")
            return
        with closing(sqlite3.connect(self.server.db_path)) as db:
            row = db.execute("SELECT amount_cents, schema_version FROM orders "
                             "WHERE order_id = ?", (order_id,)).fetchone()
        if row is None:
            self.reply(404, request_id, error="order_missing")
        elif self.server.revision == "s1" and row[1] > 1:
            self.reply(409, request_id, error="unsupported_record_version")
        else:
            self.reply(200, request_id, order_id=order_id, amount_cents=row[0],
                       schema_version=row[1])

    def do_POST(self) -> None:
        request_id = self.headers.get("X-Request-ID", "")
        if not request_id:
            self.reply(400, "missing", error="request_id_required")
            return
        if self.path != "/orders":
            self.reply(404, request_id, error="not_found")
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 1 <= length <= 1024:
                raise ValueError
            payload = json.loads(self.rfile.read(length))
            order_id = payload["order_id"]
            amount = payload["amount_cents"]
            if type(order_id) is not int or order_id < 1 or type(amount) is not int or amount < 1:
                raise ValueError
        except (ValueError, KeyError, TypeError, json.JSONDecodeError):
            self.reply(400, request_id, error="invalid_order")
            return
        stored_amount = amount + (1 if self.server.inject_fault else 0)
        version = 1 if self.server.revision == "s1" else 2
        try:
            with closing(sqlite3.connect(self.server.db_path)) as db:
                db.execute("INSERT INTO orders VALUES (?, ?, ?)",
                           (order_id, stored_amount, version))
                db.commit()
        except sqlite3.IntegrityError:
            self.reply(409, request_id, error="duplicate_order")
            return
        self.reply(201, request_id, order_id=order_id)


@contextmanager
def serve(db_path: Path, revision: str, inject_fault: bool = False):
    if revision not in {"s1", "s2"}:
        raise ValueError("unknown revision")
    server = HTTPServer(("127.0.0.1", 0), Handler)
    server.db_path = db_path
    server.revision = revision
    server.inject_fault = inject_fault
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        worker.join(timeout=3)


def call(base: str, method: str, path: str, payload: dict | None = None) -> dict:
    request_id = str(uuid.uuid4())
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    request = Request(base + path, data=body, method=method,
                      headers={"X-Request-ID": request_id,
                               "Content-Type": "application/json"})
    try:
        response = urlopen(request, timeout=3)
    except HTTPError as error:
        response = error
    with response:
        result = json.load(response)
        if (result["request_id"] != request_id or
                response.headers["X-Revision"] != result["revision"]):
            raise RuntimeError("request/revision correlation failed")
        return {"status": response.status, **result}


def backup(source: Path, destination: Path) -> None:
    with closing(sqlite3.connect(source)) as src, closing(sqlite3.connect(destination)) as dst:
        src.backup(dst)


def demo() -> dict:
    with tempfile.TemporaryDirectory(prefix="devops-capstone-") as directory:
        work = Path(directory)
        active, saved, restored = (work / name for name in
                                   ("active.sqlite", "backup.sqlite", "restored.sqlite"))
        initialize(active)
        with serve(active, "s1") as base:
            s1_write = call(base, "POST", "/orders", {"order_id": 41, "amount_cents": 100})
            s1_read = call(base, "GET", "/orders/41")
        backup(active, saved)
        with serve(active, "s2", inject_fault=True) as base:
            s2_health = call(base, "GET", "/health")
            s2_write = call(base, "POST", "/orders", {"order_id": 42, "amount_cents": 200})
            s2_read = call(base, "GET", "/orders/42")
        with serve(active, "s1") as base:
            rollback_old = call(base, "GET", "/orders/41")
            rollback_new = call(base, "GET", "/orders/42")
        backup(saved, restored)
        with serve(restored, "s1") as base:
            restored_old = call(base, "GET", "/orders/41")
            restored_new = call(base, "GET", "/orders/42")
        if ([s1_write["status"], s1_read["status"], s2_health["status"],
             s2_write["status"], s2_read["status"]] != [201, 200, 200, 201, 200] or
                s1_read["amount_cents"] != 100 or
                s2_read["amount_cents"] != 201 or  # HTTP success, wrong business value.
                (rollback_old["status"], rollback_new["status"]) != (200, 409) or
                (restored_old["status"], restored_new["status"]) != (200, 404)):
            raise RuntimeError("fixture outcome differs from the chapter")
        events = {"s1_write": s1_write, "s1_read": s1_read,
                  "s2_health": s2_health, "s2_write": s2_write, "s2_read": s2_read,
                  "rollback_old": rollback_old, "rollback_new": rollback_new,
                  "restored_old": restored_old, "restored_new": restored_new}
        if len({event["request_id"] for event in events.values()}) != len(events):
            raise RuntimeError("request IDs must be unique")
        return {"scope": "local_fixture_only", "script_sha256": hashlib.sha256(
            Path(__file__).read_bytes()).hexdigest(),
            "backup_sha256": hashlib.sha256(saved.read_bytes()).hexdigest(),
            "events": events, "decision": "STOP: S2 corrupted an acknowledged order; "
            "S1 cannot read the S2 record; restoring the older backup loses order 42."}


if __name__ == "__main__":
    print(json.dumps(demo(), ensure_ascii=False, indent=2))

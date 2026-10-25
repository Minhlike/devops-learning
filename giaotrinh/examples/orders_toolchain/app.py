"""Small single-process orders service for the textbook's local toolchain.

SQLite is deliberately a one-host choice. This example is not a distributed
database or a production deployment template.
"""

from __future__ import annotations

import json
import hashlib
import os
import socket
import sqlite3
import sys
import time
import uuid
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

DB_PATH = Path(os.environ.get("ORDERS_DB", "orders.sqlite3"))
REVISION = os.environ.get("APP_REVISION", "local")
INSTANCE = socket.gethostname()
FAIL_READINESS = os.environ.get("FAIL_READINESS", "0") == "1"
FAIL_BUSINESS = os.environ.get("FAIL_BUSINESS", "0") == "1"
COUNTS = {"requests": 0, "errors": 0}
COUNT_LOCK = Lock()


def connect():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=5)
    conn.execute("PRAGMA busy_timeout = 5000")
    return conn


def initialize_db():
    """Extend the earlier fixture in place; old orders retain their IDs."""
    conn = connect()
    try:
        with conn:
            conn.execute("BEGIN IMMEDIATE")
            conn.execute("CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, "
                         "item TEXT NOT NULL, quantity INTEGER NOT NULL, "
                         "created_at TEXT NOT NULL, idempotency_key TEXT, "
                         "payload_hash TEXT, request_id TEXT, revision TEXT, "
                         "instance_id TEXT)")
            present = {row[1] for row in conn.execute("PRAGMA table_info(orders)")}
            for name in ("idempotency_key", "payload_hash", "request_id",
                         "revision", "instance_id"):
                if name not in present:
                    conn.execute(f"ALTER TABLE orders ADD COLUMN {name} TEXT")
            conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS orders_idempotency "
                         "ON orders(idempotency_key)")
    finally:
        conn.close()


@contextmanager
def database():
    conn = connect()
    try:
        with conn:
            yield conn
    finally:
        conn.close()


def log_event(**fields):
    print(json.dumps({"ts": time.time(), "revision": REVISION, **fields},
                     ensure_ascii=False, separators=(",", ":")), flush=True)


class Handler(BaseHTTPRequestHandler):
    server_version = "orders-api"

    def log_message(self, format, *args):
        pass  # emit a structured record in finish_request instead

    def respond(self, status, payload, request_id):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Request-ID", request_id)
        self.send_header("X-App-Revision", REVISION)
        self.send_header("X-App-Instance", INSTANCE)
        self.end_headers()
        self.wfile.write(body)
        with COUNT_LOCK:
            COUNTS["requests"] += 1
            COUNTS["errors"] += status >= 500
        log_event(event="request", method=self.command, path=self.path,
                  status=status, request_id=request_id,
                  order_id=payload.get("id") if isinstance(payload, dict) else None,
                  instance_id=INSTANCE)

    def request_id(self):
        # The client value is untrusted: cap it and permit only safe characters.
        value = self.headers.get("X-Request-ID", "")
        if 1 <= len(value) <= 64 and all(c.isalnum() or c in "-_" for c in value):
            return value
        return uuid.uuid4().hex

    def do_GET(self):
        rid = self.request_id()
        if self.path == "/healthz":
            return self.respond(200, {"status": "alive", "revision": REVISION}, rid)
        if self.path == "/readyz":
            if FAIL_READINESS:
                return self.respond(503, {"status": "forced_unready"}, rid)
            try:
                with database() as conn:
                    conn.execute("SELECT 1 FROM orders LIMIT 1").fetchone()
            except sqlite3.Error:
                return self.respond(503, {"status": "db_unavailable"}, rid)
            return self.respond(200, {"status": "ready"}, rid)
        if self.path == "/metrics":
            with COUNT_LOCK:
                values = dict(COUNTS)
            body = (f"orders_http_requests_total {values['requests']}\n"
                    f"orders_http_errors_total {values['errors']}\n").encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; version=0.0.4")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path.startswith("/orders/"):
            order_id = self.path.removeprefix("/orders/")
            try:
                with database() as conn:
                    row = conn.execute("SELECT id,item,quantity,created_at,request_id,"
                                       "revision,instance_id FROM orders "
                                       "WHERE id=?", (order_id,)).fetchone()
            except sqlite3.Error:
                return self.respond(503, {"error": "db_unavailable"}, rid)
            if row is None:
                return self.respond(404, {"error": "order_missing"}, rid)
            return self.respond(200, dict(zip(("id", "item", "quantity", "created_at",
                                               "origin_request_id", "origin_revision",
                                               "origin_instance"), row)), rid)
        return self.respond(404, {"error": "route_missing"}, rid)

    def do_POST(self):
        rid = self.request_id()
        if self.path != "/orders":
            return self.respond(404, {"error": "route_missing"}, rid)
        if FAIL_BUSINESS:
            return self.respond(503, {"error": "forced_business_failure"}, rid)
        try:
            length = int(self.headers.get("Content-Length", "-1"))
        except ValueError:
            length = -1
        if not 1 <= length <= 4096:
            return self.respond(413, {"error": "invalid_length"}, rid)
        try:
            data = json.loads(self.rfile.read(length))
        except (ValueError, UnicodeDecodeError):
            return self.respond(400, {"error": "invalid_json"}, rid)
        if (not isinstance(data, dict) or not isinstance(data.get("item"), str)
                or not 1 <= len(data["item"]) <= 100
                or type(data.get("quantity")) is not int
                or not 1 <= data["quantity"] <= 1000):
            return self.respond(400, {"error": "invalid_order"}, rid)
        key = self.headers.get("Idempotency-Key", "")
        if not 1 <= len(key) <= 64 or not all(c.isalnum() or c in "-_." for c in key):
            return self.respond(428, {"error": "idempotency_key_required"}, rid)
        canonical = json.dumps({"item": data["item"], "quantity": data["quantity"]},
                               sort_keys=True, ensure_ascii=False, separators=(",", ":"))
        payload_hash = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
        order_id = uuid.uuid4().hex
        try:
            with database() as conn:
                conn.execute("BEGIN IMMEDIATE")
                previous = conn.execute("SELECT id,payload_hash FROM orders "
                                        "WHERE idempotency_key=?", (key,)).fetchone()
                if previous:
                    if previous[1] != payload_hash:
                        return self.respond(409, {"error": "idempotency_conflict"}, rid)
                    return self.respond(200, {"id": previous[0], "revision": REVISION,
                                              "instance": INSTANCE, "replayed": True}, rid)
                conn.execute("INSERT INTO orders "
                             "(id,item,quantity,created_at,idempotency_key,payload_hash,"
                             "request_id,revision,instance_id) "
                             "VALUES (?,?,?,datetime('now'),?,?,?,?,?)",
                             (order_id, data["item"], data["quantity"], key,
                              payload_hash, rid, REVISION, INSTANCE))
        except sqlite3.Error:
            return self.respond(503, {"error": "db_unavailable"}, rid)
        return self.respond(201, {"id": order_id, "revision": REVISION,
                                  "instance": INSTANCE, "replayed": False}, rid)


def main():
    port = int(os.environ.get("PORT", "8080"))
    host = os.environ.get("HOST", "127.0.0.1")
    initialize_db()
    with ThreadingHTTPServer((host, port), Handler) as server:
        log_event(event="started", port=port, instance_id=INSTANCE)
        server.serve_forever()


if __name__ == "__main__":
    main()

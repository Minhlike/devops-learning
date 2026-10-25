"""Positive and negative integration checks using a real temporary HTTP server."""

import json
from concurrent.futures import ThreadPoolExecutor
import os
import subprocess
import sys
import tempfile
import time
import unittest
import urllib.error
import urllib.request
from pathlib import Path
from socket import socket

ROOT = Path(__file__).resolve().parent


def request(url, method="GET", payload=None, key=None, request_id=None):
    body = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, method=method)
    if body is not None:
        req.add_header("Content-Type", "application/json")
    if key is not None:
        req.add_header("Idempotency-Key", key)
    if request_id is not None:
        req.add_header("X-Request-ID", request_id)
    try:
        with urllib.request.urlopen(req, timeout=2) as response:
            return response.status, dict(response.headers), json.load(response)
    except urllib.error.HTTPError as error:
        return error.code, dict(error.headers), json.load(error)


class OrdersServiceTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        with socket() as sock:
            sock.bind(("127.0.0.1", 0))
            port = sock.getsockname()[1]
        env = {**os.environ, "PORT": str(port),
               "ORDERS_DB": str(Path(self.temp.name) / "orders.sqlite3"),
               "APP_REVISION": "test-rev", "FAIL_READINESS": "0"}
        self.env = env
        self.process = subprocess.Popen([sys.executable, str(ROOT / "app.py")],
                                        env=env, stdout=subprocess.DEVNULL,
                                        stderr=subprocess.PIPE)
        self.base = f"http://127.0.0.1:{port}"
        for _ in range(80):
            try:
                if request(self.base + "/readyz")[0] == 200:
                    break
            except (urllib.error.URLError, TimeoutError):
                pass
            time.sleep(0.05)
        else:
            self.fail("service never became ready")

    def tearDown(self):
        self.process.terminate()
        try:
            self.process.wait(timeout=3)
        except subprocess.TimeoutExpired:
            self.process.kill()
            self.process.wait(timeout=3)
        self.process.stderr.close()
        self.temp.cleanup()

    def test_order_roundtrip_and_revision(self):
        status, headers, created = request(self.base + "/orders", "POST",
                                           {"item": "Sổ tay", "quantity": 2},
                                           key="test-order-1", request_id="req-1")
        self.assertEqual(status, 201)
        self.assertEqual(headers["X-App-Revision"], "test-rev")
        status, _, order = request(self.base + "/orders/" + created["id"])
        self.assertEqual((status, order["item"], order["quantity"]), (200, "Sổ tay", 2))
        self.assertEqual(order["origin_request_id"], "req-1")
        self.assertEqual(order["origin_revision"], "test-rev")
        self.assertEqual(order["origin_instance"], headers["X-App-Instance"])
        with urllib.request.urlopen(self.base + "/metrics", timeout=2) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("orders_http_requests_total", response.read().decode())

    def test_rejects_invalid_order_without_writing(self):
        status, _, result = request(self.base + "/orders", "POST",
                                    {"item": "Sổ tay", "quantity": -1})
        self.assertEqual((status, result["error"]), (400, "invalid_order"))
        self.assertEqual(request(self.base + "/orders/missing")[0], 404)

    def test_idempotency_replay_conflict_and_missing_key(self):
        payload = {"item": "Bút", "quantity": 3}
        first = request(self.base + "/orders", "POST", payload,
                        key="order-same", request_id="first")
        replay = request(self.base + "/orders", "POST", payload,
                         key="order-same", request_id="second")
        conflict = request(self.base + "/orders", "POST",
                           {"item": "Bút", "quantity": 4}, key="order-same")
        missing = request(self.base + "/orders", "POST", payload)
        self.assertEqual((first[0], replay[0], conflict[0], missing[0]),
                         (201, 200, 409, 428))
        self.assertEqual(first[2]["id"], replay[2]["id"])
        self.assertEqual(request(self.base + "/orders/" + first[2]["id"])[2]
                         ["origin_request_id"], "first")

    def test_concurrent_same_key_creates_one_record(self):
        def create(_):
            return request(self.base + "/orders", "POST",
                           {"item": "Vở", "quantity": 1}, key="race-1")
        with ThreadPoolExecutor(max_workers=2) as pool:
            outcomes = list(pool.map(create, range(2)))
        self.assertEqual(sorted(x[0] for x in outcomes), [200, 201])
        self.assertEqual(outcomes[0][2]["id"], outcomes[1][2]["id"])

    def test_health_can_be_green_while_readiness_fails(self):
        self.process.terminate()
        self.process.wait(timeout=3)
        self.process.stderr.close()
        self.process = subprocess.Popen([sys.executable, str(ROOT / "app.py")],
                                        env={**self.env, "FAIL_READINESS": "1"},
                                        stdout=subprocess.DEVNULL,
                                        stderr=subprocess.PIPE)
        for _ in range(80):
            try:
                health = request(self.base + "/healthz")[0]
                ready = request(self.base + "/readyz")[0]
                break
            except urllib.error.URLError:
                time.sleep(0.05)
        else:
            self.fail("restarted process did not listen")
        self.assertEqual((health, ready), (200, 503))


if __name__ == "__main__":
    unittest.main()

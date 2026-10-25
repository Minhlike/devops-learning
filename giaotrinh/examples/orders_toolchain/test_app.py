"""Positive and negative integration checks using a real temporary HTTP server."""

import json
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


def request(url, method="GET", payload=None):
    body = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=body, method=method)
    if body is not None:
        req.add_header("Content-Type", "application/json")
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
                                           {"item": "Sổ tay", "quantity": 2})
        self.assertEqual(status, 201)
        self.assertEqual(headers["X-App-Revision"], "test-rev")
        status, _, order = request(self.base + "/orders/" + created["id"])
        self.assertEqual((status, order["item"], order["quantity"]), (200, "Sổ tay", 2))
        with urllib.request.urlopen(self.base + "/metrics", timeout=2) as response:
            self.assertEqual(response.status, 200)
            self.assertIn("orders_http_requests_total", response.read().decode())

    def test_rejects_invalid_order_without_writing(self):
        status, _, result = request(self.base + "/orders", "POST",
                                    {"item": "Sổ tay", "quantity": -1})
        self.assertEqual((status, result["error"]), (400, "invalid_order"))
        self.assertEqual(request(self.base + "/orders/missing")[0], 404)

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

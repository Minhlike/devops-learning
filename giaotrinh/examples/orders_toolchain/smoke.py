"""Check business postcondition, not merely a green health endpoint."""

import json
import os
import urllib.request
import uuid

base = os.environ.get("ORDERS_URL", "http://127.0.0.1:8080").rstrip("/")
request_id = "smoke-" + uuid.uuid4().hex[:16]
payload = json.dumps({"item": "Bút", "quantity": 1}).encode()
req = urllib.request.Request(base + "/orders", payload, method="POST",
                             headers={"Content-Type": "application/json",
                                      "X-Request-ID": request_id})
with urllib.request.urlopen(req, timeout=5) as response:
    assert response.status == 201
    created = json.load(response)
    revision = response.headers["X-App-Revision"]
with urllib.request.urlopen(base + "/orders/" + created["id"], timeout=5) as response:
    order = json.load(response)
    assert response.status == 200
    assert order["item"] == "Bút" and order["quantity"] == 1
    assert response.headers["X-App-Revision"] == revision
print(json.dumps({"result": "PASS", "request_id": request_id,
                  "order_id": created["id"], "revision": revision}))

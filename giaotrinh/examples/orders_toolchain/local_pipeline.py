"""Run the complete single-host teaching chain against disposable Docker names.

Requires a local Docker Engine, Compose plugin, Python 3.12+ and access to the
official registry:2 image. It never touches an existing project or volume.
Outputs evidence under giaotrinh/qa/p16_runs; it does not claim remote CI.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import socket
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUN_ID = datetime.now(timezone.utc).strftime("p16-%Y%m%d-%H%M%S") + "-" + str(os.getpid())
OUT = HERE.parents[1] / "qa" / "p16_runs" / RUN_ID
OUT.mkdir(parents=True, exist_ok=False)


def command(*args: str, env: dict | None = None) -> str:
    process = subprocess.run(args, cwd=HERE, env=env, text=True,
                             stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if process.returncode:
        raise RuntimeError(f"{args[0]} {args[1:3]} exit {process.returncode}: "
                           f"{process.stdout[-1800:]}")
    return process.stdout.strip()


def free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


def http_json(url: str, payload: dict | None = None, key: str | None = None):
    body = None if payload is None else json.dumps(payload).encode()
    headers = {"Content-Type": "application/json"} if body else {}
    if key:
        headers["Idempotency-Key"] = key
    request = urllib.request.Request(url, data=body, headers=headers,
                                     method="POST" if body else "GET")
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            content = response.read().decode()
            return response.status, json.loads(content) if content.startswith("{") else content
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read())


def ready(base: str):
    for _ in range(40):
        try:
            if http_json(base + "/readyz")[0] == 200:
                return
        except (urllib.error.URLError, TimeoutError, ConnectionError):
            pass
        time.sleep(1)
    raise RuntimeError(f"readiness did not become 200 at {base}")


def smoke(base: str) -> dict:
    env = {**os.environ, "ORDERS_URL": base}
    return json.loads(command(sys.executable, str(HERE / "smoke.py"), env=env).splitlines()[-1])


def compose(project: str, image: str, port: int, failure: str = "0", *args: str) -> str:
    env = {**os.environ, "ORDERS_IMAGE": image, "PUBLISH_PORT": str(port),
           "FAIL_BUSINESS": failure}
    return command("docker", "compose", "-f", "deploy.compose.yaml", "-p", project,
                   *args, env=env)


def main():
    ledger: dict = {"schema_version": 1, "run_id": RUN_ID,
                    "scope": "single-host local lab; remote CI and GHCR not exercised",
                    "started_at": datetime.now(timezone.utc).isoformat()}
    try:
        ledger["change_id"] = uuid.uuid4().hex
        commit = command("git", "rev-parse", "HEAD")
        dirty = bool(command("git", "status", "--porcelain", "--",
                             "app.py", "Dockerfile", "smoke.py", "test_app.py",
                             "ci.yml", "deploy.compose.yaml"))
        ledger["commit"] = None if dirty else commit
        source_hash = hashlib.sha256()
        for name in ("app.py", "Dockerfile"):
            source_hash.update(name.encode() + b"\0" + (HERE / name).read_bytes())
        input_sha = source_hash.hexdigest()
        ledger["build_input_sha256"] = input_sha
        revision = commit if not dirty else "working-" + input_sha[:16]
        ledger["revision_claim"] = revision
        ledger["unit_tests"] = command(sys.executable, "-m", "unittest", "-v", "test_app.py")[-800:]

        registry_name = RUN_ID + "-registry"
        command("docker", "run", "-d", "--name", registry_name,
                "-p", "127.0.0.1::5000", "registry:2")
        registry = command("docker", "port", registry_name, "5000/tcp").splitlines()[0]
        tag = f"{registry}/orders-api:{input_sha[:16]}"
        ledger["registry_address"] = registry
        command("docker", "build", "--build-arg", f"APP_REVISION={revision}",
                "--build-arg", f"BUILD_INPUT_SHA256={input_sha}", "-t", tag, ".")
        image_id = command("docker", "image", "inspect", tag, "--format", "{{.Id}}")
        ledger["tested_image_id"] = image_id

        candidate_name = RUN_ID + "-candidate"
        command("docker", "run", "-d", "--name", candidate_name,
                "-p", "127.0.0.1::8080", "-v", RUN_ID + "-candidate-data:/data", tag)
        candidate_port = int(command("docker", "port", candidate_name, "8080/tcp")
                             .rsplit(":", 1)[1])
        candidate_url = f"http://127.0.0.1:{candidate_port}"
        ready(candidate_url)
        ledger["candidate_smoke"] = smoke(candidate_url)
        command("docker", "stop", candidate_name)

        push_output = command("docker", "push", tag)
        (OUT / "push.log").write_text(push_output + "\n", encoding="utf-8")
        found = re.search(r"digest: (sha256:[0-9a-f]{64})", push_output)
        if not found:
            raise RuntimeError("registry did not report a manifest digest")
        digest = found.group(1)
        pinned = f"{registry}/orders-api@{digest}"
        command("docker", "pull", pinned)
        pulled_id = command("docker", "image", "inspect", pinned, "--format", "{{.Id}}")
        if pulled_id != image_id:
            raise RuntimeError("pulled digest does not resolve to tested local image ID")
        ledger["registry_manifest_digest"] = digest
        ledger["pinned_image"] = pinned
        ledger["pulled_image_id"] = pulled_id

        project = RUN_ID
        deployed_port = free_port()
        compose(project, pinned, deployed_port, "0", "up", "-d", "--wait", "--no-build")
        deployed_url = f"http://127.0.0.1:{deployed_port}"
        ready(deployed_url)
        container_id = compose(project, pinned, deployed_port, "0", "ps", "-q", "api")
        runtime_id = command("docker", "inspect", container_id, "--format", "{{.Image}}")
        runtime_ref = command("docker", "inspect", container_id, "--format", "{{.Config.Image}}")
        if runtime_id != image_id or runtime_ref != pinned:
            raise RuntimeError("runtime is not the approved pinned artifact")
        ledger["deployment"] = {"project": project, "container_id": container_id,
                                "runtime_image_id": runtime_id, "runtime_image_ref": runtime_ref}
        ledger["deployed_smoke"] = smoke(deployed_url)
        order_id = ledger["deployed_smoke"]["order_id"]
        ledger["record_before_failure"] = http_json(deployed_url + "/orders/" + order_id)[1]
        ledger["metrics"] = http_json(deployed_url + "/metrics")[1]
        logs = compose(project, pinned, deployed_port, "0", "logs", "--no-color", "api")
        ledger["request_log_matched"] = (ledger["deployed_smoke"]["request_id"] in logs
                                          and order_id in logs)
        if not ledger["request_log_matched"]:
            raise RuntimeError("request ID and order ID not present in runtime logs")

        compose(project, pinned, deployed_port, "1", "up", "-d",
                "--force-recreate", "--wait", "--no-build")
        health = http_json(deployed_url + "/healthz")[0]
        readiness = http_json(deployed_url + "/readyz")[0]
        business = http_json(deployed_url + "/orders",
                             {"item": "Lỗi thử", "quantity": 1},
                             key="failure-" + RUN_ID)[0]
        ledger["failure"] = {"health": health, "readiness": readiness,
                             "business_post": business}
        if (health, readiness, business) != (200, 200, 503):
            raise RuntimeError("failure injection did not isolate business from readiness")
        compose(project, pinned, deployed_port, "0", "up", "-d",
                "--force-recreate", "--wait", "--no-build")
        ready(deployed_url)
        recovered = http_json(deployed_url + "/orders/" + order_id)[1]
        if recovered != ledger["record_before_failure"]:
            raise RuntimeError("record changed during failure and recovery")
        ledger["record_after_recovery"] = recovered

        container_id = compose(project, pinned, deployed_port, "0", "ps", "-q", "api")
        command("docker", "exec", container_id, "python", "-c",
                "import sqlite3; a=sqlite3.connect('/data/orders.sqlite3'); "
                "b=sqlite3.connect('/data/backup.sqlite3'); a.backup(b); b.close(); a.close()")
        backup = OUT / "backup.sqlite3"
        command("docker", "cp", f"{container_id}:/data/backup.sqlite3", str(backup))
        ledger["backup_sha256"] = hashlib.sha256(backup.read_bytes()).hexdigest()
        restored_volume = RUN_ID + "-restored-data"
        command("docker", "volume", "create", restored_volume)
        command("docker", "run", "--rm", "--user", "0", "-v",
                f"{restored_volume}:/data", "-v", f"{OUT}:/backup:ro",
                "--entrypoint", "python", pinned, "-c",
                "import sqlite3; a=sqlite3.connect('/backup/backup.sqlite3'); "
                "b=sqlite3.connect('/data/orders.sqlite3'); a.backup(b); b.close(); a.close()")
        restore_name = RUN_ID + "-restore"
        command("docker", "run", "-d", "--name", restore_name,
                "-p", "127.0.0.1::8080", "-v", restored_volume + ":/data", pinned)
        restore_port = int(command("docker", "port", restore_name, "8080/tcp")
                           .rsplit(":", 1)[1])
        restored_url = f"http://127.0.0.1:{restore_port}"
        ready(restored_url)
        restored = http_json(restored_url + "/orders/" + order_id)[1]
        if restored != ledger["record_before_failure"]:
            raise RuntimeError("independent restore did not reproduce the order")
        ledger["independent_restore"] = {"volume": restored_volume, "record": restored}
        command("docker", "stop", restore_name)
        ledger["result"] = "PASS"
    except Exception as error:
        ledger["result"] = "FAIL"
        ledger["error"] = str(error)
        raise
    finally:
        ledger["ended_at"] = datetime.now(timezone.utc).isoformat()
        (OUT / "evidence.json").write_text(
            json.dumps(ledger, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"EVIDENCE {OUT / 'evidence.json'}")


if __name__ == "__main__":
    main()

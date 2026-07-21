#!/usr/bin/env python3
"""Deploy the shared agent result pipeline without replacing the VM release tree."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
import time
from pathlib import Path, PurePosixPath

from remote_deploy_ui import HOST, SERVICE_NAME, USER, connect, run


REMOTE_UI_ROOT = "/opt/serbia-poc-ui"
REMOTE_BACKUP_ROOT = "/opt/serbia-poc-ui-backups"
UI_PORT = 8769
LOCAL_ROOT = Path(__file__).resolve().parent.parent
FILES = ("server.py", "app.js", "agent_result_pipeline.py")


def upload_staging(client, staging: str) -> None:
    run(client, f"install -d -m 0700 {shlex.quote(staging)}")
    sftp = client.open_sftp()
    try:
        for name in FILES:
            sftp.put(str(LOCAL_ROOT / name), str(PurePosixPath(staging) / name))
    finally:
        sftp.close()
    run(
        client,
        f"cd {shlex.quote(staging)} && /usr/bin/python3 -m py_compile server.py agent_result_pipeline.py",
    )


def deploy(client) -> tuple[str, dict]:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    staging = f"/tmp/serbia-poc-ui-slice1-{stamp}"
    backup = f"{REMOTE_BACKUP_ROOT}/slice1-{stamp}"
    root_q = shlex.quote(REMOTE_UI_ROOT)
    staging_q = shlex.quote(staging)
    backup_q = shlex.quote(backup)

    resolved = run(client, f"readlink -f {root_q}")[1].strip()
    if resolved != REMOTE_UI_ROOT:
        raise RuntimeError(f"Unexpected remote UI root: {resolved!r}")

    upload_staging(client, staging)
    run(
        client,
        f"sudo -n install -d -o root -g root -m 0755 {shlex.quote(REMOTE_BACKUP_ROOT)} {backup_q} "
        f"&& sudo -n cp -a {root_q}/server.py {root_q}/app.js {backup_q}/ "
        f"&& if test -f {root_q}/agent_result_pipeline.py; then sudo -n cp -a {root_q}/agent_result_pipeline.py {backup_q}/; fi "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/server.py {root_q}/server.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/app.js {root_q}/app.js "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/agent_result_pipeline.py {root_q}/agent_result_pipeline.py "
        f"&& rm -rf {staging_q} "
        f"&& sudo -n systemctl restart {SERVICE_NAME}",
        timeout=90,
    )

    time.sleep(3)
    checks = {
        "service": f"sudo -n systemctl is-active {SERVICE_NAME}",
        "status": f"curl -fsS http://127.0.0.1:{UI_PORT}/api/status",
        "module": f"test -f {root_q}/agent_result_pipeline.py && echo present",
        "frontend": f"grep -q 'function applyAgentResult' {root_q}/app.js && echo present",
        "logs": f"journalctl -u {SERVICE_NAME} -n 30 --no-pager",
    }
    verification = {}
    failed = False
    for name, command in checks.items():
        code, out, err = run(client, command, timeout=30, check=False)
        verification[name] = {"code": code, "output": (out or err).strip()}
        if name != "logs" and code:
            failed = True

    status_payload = {}
    try:
        status_payload = json.loads(verification["status"]["output"])
    except (TypeError, json.JSONDecodeError):
        failed = True
    if status_payload.get("dataset_version") != "v2.1" or status_payload.get("dataset_rows") != 14800:
        failed = True

    if failed:
        rollback = (
            f"sudo -n cp -a {backup_q}/server.py {root_q}/server.py "
            f"&& sudo -n cp -a {backup_q}/app.js {root_q}/app.js "
            f"&& if test -f {backup_q}/agent_result_pipeline.py; then "
            f"sudo -n cp -a {backup_q}/agent_result_pipeline.py {root_q}/agent_result_pipeline.py; "
            f"else sudo -n rm -f {root_q}/agent_result_pipeline.py; fi "
            f"&& sudo -n systemctl restart {SERVICE_NAME}"
        )
        run(client, rollback, timeout=90)
        raise RuntimeError(f"Slice 1 verification failed and rollback completed: {verification}")

    return backup, verification


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True, type=Path)
    args = parser.parse_args()

    client = connect(args.key.resolve())
    try:
        backup, verification = deploy(client)
    finally:
        client.close()
    print(json.dumps({
        "host": HOST,
        "remote_ui_root": REMOTE_UI_ROOT,
        "backup": backup,
        "verification": verification,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Deploy the isolated persistent-General A/B candidate and backend switch."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
import time
from pathlib import Path, PurePosixPath

from remote_deploy_ui import HOST, USER, connect, run


LOCAL_ROOT = Path(__file__).resolve().parent.parent
REMOTE_UI_ROOT = "/opt/serbia-poc-ui"
REMOTE_PROFILE_ASSETS = "/opt/serbia-poc/general_persistent_profile"
REMOTE_BACKUP_ROOT = "/opt/serbia-poc-ui-backups"
PROFILE_NAME = "generalpersistent"
PROFILE_HOME = f"/home/ubuntu/.hermes/profiles/{PROFILE_NAME}"
PROFILE_SERVICE = "hermes-general-persistent-gateway.service"
UI_SERVICE = "serbia-poc-ui.service"
HERMES = "/home/ubuntu/.hermes/hermes-agent/venv/bin/hermes"


def upload(client, staging: str) -> None:
    run(client, f"install -d -m 0700 {shlex.quote(staging)}/profile")
    sftp = client.open_sftp()
    try:
        sftp.put(str(LOCAL_ROOT / "server.py"), str(PurePosixPath(staging) / "server.py"))
        sftp.put(str(LOCAL_ROOT / "run_instruction_ab_test.py"), str(PurePosixPath(staging) / "run_instruction_ab_test.py"))
        for name in (
            "SOUL.md", "provision_profile.py", "configure_ui_gateway.py",
            "hermes-general-persistent-gateway.service",
        ):
            sftp.put(
                str(LOCAL_ROOT / "general_persistent_profile" / name),
                str(PurePosixPath(staging) / "profile" / name),
            )
    finally:
        sftp.close()
    run(
        client,
        f"/usr/bin/python3 -m py_compile {shlex.quote(staging)}/server.py "
        f"{shlex.quote(staging)}/run_instruction_ab_test.py "
        f"{shlex.quote(staging)}/profile/provision_profile.py "
        f"{shlex.quote(staging)}/profile/configure_ui_gateway.py",
    )


def deploy(client) -> tuple[str, dict]:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    staging = f"/tmp/general-instruction-ab-{stamp}"
    backup = f"{REMOTE_BACKUP_ROOT}/general-instruction-ab-{stamp}"
    upload(client, staging)
    staging_q = shlex.quote(staging)
    backup_q = shlex.quote(backup)
    ui_q = shlex.quote(REMOTE_UI_ROOT)
    assets_q = shlex.quote(REMOTE_PROFILE_ASSETS)
    profile_q = shlex.quote(PROFILE_HOME)
    run(
        client,
        f"sudo -n install -d -o root -g root -m 0755 {backup_q} "
        f"&& sudo -n cp -a {ui_q}/server.py {backup_q}/server.py "
        f"&& sudo -n cp -a {ui_q}/.hermes-api.json {backup_q}/hermes-api.json "
        f"&& if test -d {profile_q}; then sudo -n cp -a {profile_q} {backup_q}/profile; fi "
        f"&& if ! test -d {profile_q}; then {HERMES} profile create {PROFILE_NAME} --clone-from default --no-alias; fi "
        f"&& sudo -n install -d -o {USER} -g {USER} -m 0755 {assets_q} "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/profile/SOUL.md {assets_q}/SOUL.md "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/profile/provision_profile.py {assets_q}/provision_profile.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/profile/configure_ui_gateway.py {assets_q}/configure_ui_gateway.py "
        f"&& /usr/bin/python3 {assets_q}/provision_profile.py --profile-dir {profile_q} --soul {assets_q}/SOUL.md "
        f"&& /usr/bin/python3 {assets_q}/configure_ui_gateway.py --config {ui_q}/.hermes-api.json "
        f"&& sudo -n install -o root -g root -m 0644 {staging_q}/profile/{PROFILE_SERVICE} /etc/systemd/system/{PROFILE_SERVICE} "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/server.py {ui_q}/server.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/run_instruction_ab_test.py {ui_q}/run_instruction_ab_test.py "
        f"&& sudo -n systemctl daemon-reload "
        f"&& sudo -n systemctl enable --now {PROFILE_SERVICE} "
        f"&& sudo -n systemctl restart {PROFILE_SERVICE} {UI_SERVICE} "
        f"&& rm -rf {staging_q}",
        timeout=180,
    )
    time.sleep(5)
    checks = {
        "candidate_service": f"sudo -n systemctl is-active {PROFILE_SERVICE}",
        "ui_service": f"sudo -n systemctl is-active {UI_SERVICE}",
        "candidate_listener": "ss -ltn | grep -q ':8644 ' && echo present",
        "ui_status": "curl -fsS http://127.0.0.1:8769/api/status",
        "profile_soul": f"grep -q 'A/B candidate v1' {profile_q}/SOUL.md && echo present",
        "backend_switch": f"grep -q 'INSTRUCTION_MODE_PERSISTENT' {ui_q}/server.py && echo present",
    }
    results: dict[str, dict[str, object]] = {}
    failed = False
    for name, command in checks.items():
        code, out, err = run(client, command, timeout=40, check=False)
        results[name] = {"code": code, "output": (out or err).strip()}
        failed = failed or code != 0
    if failed:
        raise RuntimeError(f"Deployment verification failed; backup retained at {backup}: {results}")
    return backup, results


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
    print(json.dumps({"host": HOST, "backup": backup, "verification": verification}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Deploy the workstream Slice 2 UI/MCP/profile files without replacing VM state."""

from __future__ import annotations

import argparse
import json
import shlex
import time
from pathlib import Path, PurePosixPath

from remote_deploy_ui import HOST, USER, connect, run


LOCAL_ROOT = Path(__file__).resolve().parent.parent
REMOTE_UI_ROOT = "/opt/serbia-poc-ui"
REMOTE_MCP_ROOT = "/opt/serbia-poc/mcp_server"
REMOTE_PROFILE_ROOT = "/opt/serbia-poc/moshe_profile"
REMOTE_BACKUP_ROOT = "/opt/serbia-poc-ui-backups"
MOSHE_HOME = "/home/ubuntu/.hermes/profiles/moshe"
UI_SERVICE = "serbia-poc-ui.service"
MOSHE_SERVICE = "hermes-moshe-gateway.service"
UI_FILES = ("server.py", "app.js", "agent_result_pipeline.py", "workstream_artifacts.py")


def upload(client, staging: str) -> None:
    run(client, f"install -d -m 0700 {shlex.quote(staging)}/ui {shlex.quote(staging)}/mcp {shlex.quote(staging)}/profile")
    sftp = client.open_sftp()
    try:
        for name in UI_FILES:
            sftp.put(str(LOCAL_ROOT / name), str(PurePosixPath(staging) / "ui" / name))
        sftp.put(str(LOCAL_ROOT / "mcp_server" / "server.py"), str(PurePosixPath(staging) / "mcp" / "server.py"))
        for name in ("provision_profile.py", "SOUL.md"):
            sftp.put(str(LOCAL_ROOT / "moshe_profile" / name), str(PurePosixPath(staging) / "profile" / name))
    finally:
        sftp.close()
    run(
        client,
        f"cd {shlex.quote(staging)} "
        "&& /usr/bin/python3 -m py_compile ui/server.py ui/agent_result_pipeline.py ui/workstream_artifacts.py mcp/server.py profile/provision_profile.py",
    )


def deploy(client) -> tuple[str, dict]:
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    staging = f"/tmp/serbia-poc-workstream-slice2-{stamp}"
    backup = f"{REMOTE_BACKUP_ROOT}/workstream-slice2-{stamp}"
    upload(client, staging)
    root_q, mcp_q, profile_q = map(shlex.quote, (REMOTE_UI_ROOT, REMOTE_MCP_ROOT, REMOTE_PROFILE_ROOT))
    staging_q, backup_q = map(shlex.quote, (staging, backup))
    run(
        client,
        f"sudo -n install -d -o root -g root -m 0755 {shlex.quote(REMOTE_BACKUP_ROOT)} {backup_q}/ui {backup_q}/mcp {backup_q}/profile "
        f"&& for f in {' '.join(UI_FILES)}; do if test -f {root_q}/$f; then sudo -n cp -a {root_q}/$f {backup_q}/ui/; fi; done "
        f"&& sudo -n cp -a {mcp_q}/server.py {backup_q}/mcp/server.py "
        f"&& sudo -n cp -a {MOSHE_HOME}/config.yaml {backup_q}/profile/config.yaml "
        f"&& sudo -n cp -a {MOSHE_HOME}/SOUL.md {backup_q}/profile/SOUL.md "
        f"&& sudo -n install -d -o {USER} -g {USER} -m 0755 {profile_q} "
        f"&& for f in {' '.join(UI_FILES)}; do sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/ui/$f {root_q}/$f; done "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/mcp/server.py {mcp_q}/server.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/profile/provision_profile.py {profile_q}/provision_profile.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/profile/SOUL.md {profile_q}/SOUL.md "
        f"&& /usr/bin/python3 {profile_q}/provision_profile.py --profile-dir {MOSHE_HOME} --soul {profile_q}/SOUL.md "
        f"&& rm -rf {staging_q} "
        f"&& sudo -n systemctl restart {MOSHE_SERVICE} "
        f"&& sudo -n systemctl restart {UI_SERVICE}",
        timeout=120,
    )
    time.sleep(5)
    checks = {
        "ui_service": f"sudo -n systemctl is-active {UI_SERVICE}",
        "moshe_service": f"sudo -n systemctl is-active {MOSHE_SERVICE}",
        "status": "curl -fsS http://127.0.0.1:8769/api/status",
        "public": f"curl -k -LfsS https://{HOST}/app.js | grep -q 'workstreamArtifactHtml' && echo present",
        "ui_contract": f"grep -q 'workstreamArtifactHtml' {root_q}/app.js && ! grep -q 'starting_source' {root_q}/app.js && echo present",
        "server_contract": f"grep -q 'apply_workstream_action' {root_q}/server.py && test -f {root_q}/workstream_artifacts.py && echo present",
        "mcp_tools": f"grep -q 'prepare_workstream_indication_proposal' {mcp_q}/server.py && grep -q 'decide_workstream_indication_proposal' {mcp_q}/server.py && echo present",
        "moshe_tools": f"grep -q 'prepare_workstream_indication_proposal' {MOSHE_HOME}/config.yaml && grep -q 'decide_workstream_indication_proposal' {MOSHE_HOME}/config.yaml && echo present",
        "logs": f"journalctl -u {UI_SERVICE} -u {MOSHE_SERVICE} -n 50 --no-pager",
    }
    result, failed = {}, False
    for name, command in checks.items():
        code, out, err = run(client, command, timeout=40, check=False)
        result[name] = {"code": code, "output": (out or err).strip()}
        if name != "logs" and code:
            failed = True
    if failed:
        raise RuntimeError(f"Deployment verification failed; backup retained at {backup}: {result}")
    return backup, result


def main() -> int:
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

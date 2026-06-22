#!/usr/bin/env python3
"""Deploy and register the isolated intelligence MCP server on the Hermes VM."""

from __future__ import annotations

import argparse
import json
import posixpath
import shlex
import sys
import time
from pathlib import Path

import paramiko


HOST = "151.145.93.180"
USER = "ubuntu"
REMOTE_ROOT = "/opt/intelligence-poc"
HERMES = "/home/ubuntu/.hermes/hermes-agent/venv/bin/hermes"
LOCAL_ROOT = Path(__file__).resolve().parent.parent


def connect(key_path: Path) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        HOST,
        username=USER,
        key_filename=str(key_path),
        timeout=15,
        banner_timeout=15,
        auth_timeout=15,
        look_for_keys=False,
        allow_agent=False,
    )
    return client


def run(client: paramiko.SSHClient, command: str, timeout: int = 30, check: bool = True) -> tuple[int, str, str]:
    stdin, stdout, stderr = client.exec_command(command, timeout=timeout)
    stdout.channel.settimeout(timeout)
    exit_code = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    if check and exit_code != 0:
        raise RuntimeError(f"Remote command failed ({exit_code}): {command}\n{err or out}")
    return exit_code, out, err


def inspect(client: paramiko.SSHClient) -> dict:
    commands = {
        "host": "hostname",
        "python": "command -v python3 && python3 --version",
        "hermes_path": "command -v hermes || true",
        "hermes_candidates": "find ~/.local/bin ~/.hermes /opt -maxdepth 5 -type f -name hermes -perm -u+x 2>/dev/null | head -20",
        "hermes_processes": "ps -eo pid,args | grep -E '[h]ermes|[g]ateway' | head -20",
        "hermes_version": f"timeout 10s {HERMES} --version 2>&1 || true",
        "mcp_help": f"timeout 10s {HERMES} mcp add --help 2>&1 | sed -n '1,180p' || true",
        "gateway_help": f"timeout 10s {HERMES} gateway --help 2>&1 | sed -n '1,200p' || true",
        "gateway_status": f"timeout 10s {HERMES} gateway status 2>&1 || true",
        "config_exists": "test -f ~/.hermes/config.yaml && echo yes || echo no",
        "mcp_config_names": "python3 - <<'PY'\nfrom pathlib import Path\np=Path.home()/'.hermes/config.yaml'\nif not p.exists(): print('[]'); raise SystemExit\ntext=p.read_text()\ntry:\n import yaml\n data=yaml.safe_load(text) or {}\n print(sorted((data.get('mcp_servers') or {}).keys()))\nexcept Exception as e:\n print('yaml-unavailable-or-invalid:', type(e).__name__)\nPY",
    }
    result = {}
    for name, command in commands.items():
        _, out, err = run(client, command, timeout=20, check=False)
        result[name] = (out or err).strip()
    return result


def upload_tree(client: paramiko.SSHClient) -> str:
    staging = f"/tmp/intelligence-poc-{int(time.time())}"
    run(client, f"mkdir -p {shlex.quote(staging)}/mcp_server {shlex.quote(staging)}/data")
    files = {
        LOCAL_ROOT / "mcp_server" / "server.py": f"{staging}/mcp_server/server.py",
        LOCAL_ROOT / "mcp_server" / "smoke_client.py": f"{staging}/mcp_server/smoke_client.py",
        LOCAL_ROOT / "data" / "events_he_large.csv": f"{staging}/data/events_he_large.csv",
    }
    sftp = client.open_sftp()
    try:
        for local, remote in files.items():
            sftp.put(str(local), remote)
    finally:
        sftp.close()
    return staging


def install_files(client: paramiko.SSHClient, staging: str) -> None:
    quoted_root = shlex.quote(REMOTE_ROOT)
    command = (
        f"sudo -n install -d -o {USER} -g {USER} -m 0755 {quoted_root}/mcp_server {quoted_root}/data "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {shlex.quote(staging)}/mcp_server/server.py {quoted_root}/mcp_server/server.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {shlex.quote(staging)}/mcp_server/smoke_client.py {quoted_root}/mcp_server/smoke_client.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {shlex.quote(staging)}/data/events_he_large.csv {quoted_root}/data/events_he_large.csv "
        f"&& rm -rf {shlex.quote(staging)}"
    )
    run(client, command, timeout=45)


def configure_hermes(client: paramiko.SSHClient) -> str:
    timestamp = int(time.time())
    backup = f"/home/{USER}/.hermes/config.yaml.before-intelligence-poc-{timestamp}"
    run(client, f"cp /home/{USER}/.hermes/config.yaml {shlex.quote(backup)}")
    command = (
        f"{HERMES} mcp add intelligence-events-poc "
        f"--command /usr/bin/python3 "
        f"--args {REMOTE_ROOT}/mcp_server/server.py "
        f"--env INTELLIGENCE_POC_DATA={REMOTE_ROOT}/data/events_he_large.csv"
    )
    run(client, command, timeout=45)
    return backup


def verify(client: paramiko.SSHClient) -> dict:
    checks = {}
    _, smoke, _ = run(client, f"/usr/bin/python3 {REMOTE_ROOT}/mcp_server/smoke_client.py", timeout=30)
    checks["smoke"] = json.loads(smoke)
    _, config, _ = run(
        client,
        "python3 - <<'PY'\nfrom pathlib import Path\nimport yaml\ndata=yaml.safe_load((Path.home()/'.hermes/config.yaml').read_text()) or {}\nserver=(data.get('mcp_servers') or {}).get('intelligence-events-poc')\nprint(server)\nPY",
        timeout=20,
    )
    checks["config"] = config.strip()
    _, hermes_check, _ = run(client, f"timeout 20s {HERMES} config check 2>&1 || true", timeout=25, check=False)
    checks["hermes_config_check"] = hermes_check.strip()
    return checks


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True, type=Path)
    parser.add_argument("--inspect-only", action="store_true")
    args = parser.parse_args()
    client = connect(args.key)
    try:
        inspection = inspect(client)
        print(json.dumps({"inspection": inspection}, ensure_ascii=False, indent=2))
        if args.inspect_only:
            return 0
        staging = upload_tree(client)
        install_files(client, staging)
        backup = configure_hermes(client)
        verification = verify(client)
        print(json.dumps({"config_backup": backup, "verification": verification}, ensure_ascii=False, indent=2))
        return 0
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())

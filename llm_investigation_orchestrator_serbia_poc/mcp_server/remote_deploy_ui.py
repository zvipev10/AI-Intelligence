#!/usr/bin/env python3
"""Deploy the Serbia/Kosovo web UI on the Hermes VM behind localhost."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
import time
from pathlib import Path, PurePosixPath

import paramiko


HOST = "151.145.93.180"
USER = "ubuntu"
REMOTE_UI_ROOT = "/opt/serbia-poc-ui"
SERVICE_NAME = "serbia-poc-ui.service"
UI_PORT = 8769
LOCAL_ROOT = Path(__file__).resolve().parent.parent
LOCAL_HERMES_CONFIG = LOCAL_ROOT / ".hermes-api.json"

FILES = [
    "server.py",
    "index.html",
    "app.js",
    "styles.css",
    "help.html",
    "README.md",
]

DIRS = [
    "vendor",
    "data",
    "recorded_runs",
    "saved_questions",
]


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


def run(client: paramiko.SSHClient, command: str, timeout: int = 60, check: bool = True) -> tuple[int, str, str]:
    _, stdout, stderr = client.exec_command(command, timeout=timeout)
    stdout.channel.settimeout(timeout)
    code = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    if check and code:
        raise RuntimeError(f"Remote command failed ({code}): {command}\n{err or out}")
    return code, out, err


def sftp_mkdirs(sftp: paramiko.SFTPClient, path: str) -> None:
    parts = PurePosixPath(path).parts
    current = ""
    for part in parts:
        if part == "/":
            current = "/"
            continue
        current = str(PurePosixPath(current) / part)
        try:
            sftp.stat(current)
        except OSError:
            sftp.mkdir(current)


def upload_file(sftp: paramiko.SFTPClient, local: Path, remote: str) -> None:
    sftp_mkdirs(sftp, str(PurePosixPath(remote).parent))
    sftp.put(str(local), remote)


def upload_dir(sftp: paramiko.SFTPClient, local_dir: Path, remote_dir: str) -> None:
    for local in local_dir.rglob("*"):
        if local.is_dir():
            continue
        relative = local.relative_to(local_dir).as_posix()
        upload_file(sftp, local, str(PurePosixPath(remote_dir) / relative))


def upload_ui(client: paramiko.SSHClient, api_key: str) -> None:
    staging = f"/tmp/serbia-poc-ui-{int(time.time())}"
    run(client, f"rm -rf {shlex.quote(staging)} && mkdir -p {shlex.quote(staging)}")
    sftp = client.open_sftp()
    try:
        for name in FILES:
            upload_file(sftp, LOCAL_ROOT / name, str(PurePosixPath(staging) / name))
        for name in DIRS:
            upload_dir(sftp, LOCAL_ROOT / name, str(PurePosixPath(staging) / name))
        remote_config = {
            "transport": "direct",
            "remote_host": "127.0.0.1",
            "remote_port": 8642,
            "api_key": api_key,
        }
        config_tmp = LOCAL_ROOT / ".hermes-api.remote.tmp.json"
        try:
            config_tmp.write_text(json.dumps(remote_config, indent=2), encoding="utf-8")
            upload_file(sftp, config_tmp, str(PurePosixPath(staging) / ".hermes-api.json"))
        finally:
            if config_tmp.exists():
                config_tmp.unlink()
    finally:
        sftp.close()
    root_q = shlex.quote(REMOTE_UI_ROOT)
    staging_q = shlex.quote(staging)
    run(
        client,
        f"sudo -n rm -rf {root_q} "
        f"&& sudo -n install -d -o {USER} -g {USER} -m 0755 {root_q} "
        f"&& sudo -n cp -a {staging_q}/. {root_q}/ "
        f"&& sudo -n chown -R {USER}:{USER} {root_q} "
        f"&& rm -rf {staging_q}",
        timeout=120,
    )


def install_service(client: paramiko.SSHClient) -> None:
    service = f"""[Unit]
Description=Serbia POC UI
After=network.target hermes-gateway.service
Wants=hermes-gateway.service

[Service]
Type=simple
User={USER}
WorkingDirectory={REMOTE_UI_ROOT}
ExecStart=/usr/bin/python3 {REMOTE_UI_ROOT}/server.py {UI_PORT}
Restart=on-failure
RestartSec=3
Environment=PYTHONUNBUFFERED=1
Environment=PYTHONIOENCODING=utf-8
Environment=POC_UI_HOST=0.0.0.0

[Install]
WantedBy=multi-user.target
"""
    encoded = json.dumps(service)
    write_command = (
        "python3 - <<'PY'\n"
        "from pathlib import Path\n"
        f"Path('/tmp/{SERVICE_NAME}').write_text({encoded}, encoding='utf-8')\n"
        "PY"
    )
    run(client, write_command, timeout=30)
    command = (
        f"sudo -n install -o root -g root -m 0644 /tmp/{SERVICE_NAME} /etc/systemd/system/{SERVICE_NAME} "
        f"&& rm -f /tmp/{SERVICE_NAME} "
        "&& sudo -n systemctl daemon-reload "
        f"&& sudo -n systemctl enable --now {SERVICE_NAME} "
        f"&& sudo -n systemctl restart {SERVICE_NAME}"
    )
    run(client, command, timeout=90)


def verify(client: paramiko.SSHClient) -> dict:
    time.sleep(3)
    commands = {
        "service": f"sudo -n systemctl is-active {SERVICE_NAME}",
        "status": f"curl -fsS http://127.0.0.1:{UI_PORT}/api/status",
        "index": f"curl -fsS http://127.0.0.1:{UI_PORT}/ | head -5",
        "listeners": f"ss -ltnp 2>/dev/null | grep ':{UI_PORT}' || true",
        "logs": f"journalctl -u {SERVICE_NAME} -n 40 --no-pager",
    }
    result = {}
    for key, command in commands.items():
        code, out, err = run(client, command, timeout=30, check=False)
        result[key] = {"code": code, "output": (out or err).strip()}
    return result


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True, type=Path)
    parser.add_argument("--api-key", default=None)
    args = parser.parse_args()

    if args.api_key:
        api_key = args.api_key
    else:
        api_key = json.loads(LOCAL_HERMES_CONFIG.read_text(encoding="utf-8"))["api_key"]

    client = connect(args.key.resolve())
    try:
        upload_ui(client, api_key)
        install_service(client)
        verification = verify(client)
    finally:
        client.close()

    print(json.dumps({
        "remote_ui_root": REMOTE_UI_ROOT,
        "service": SERVICE_NAME,
        "port": UI_PORT,
        "verification": verification,
        "ssh_tunnel": f"ssh -i {args.key.resolve()} -L {UI_PORT}:127.0.0.1:{UI_PORT} {USER}@{HOST}",
        "local_url_after_tunnel": f"http://127.0.0.1:{UI_PORT}/",
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

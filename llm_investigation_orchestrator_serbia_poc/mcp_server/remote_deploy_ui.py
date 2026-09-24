#!/usr/bin/env python3
"""Deploy the Serbia/Kosovo web UI on the Hermes VM behind localhost."""

from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
import tempfile
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
    "demo_runtime.py",
    "demo_admission.py",
    "demo_bootstrap.js",
    "activate_demo.py",
    "provision_demo.py",
    "server.py",
    "openai_general.py",
    "mcp_server/catalog_layers.py",
    "agent_result_pipeline.py",
    "agent_routing.py",
    "scenario_playback.py",
    "workstream_artifacts.py",
    "generate_english_projection.py",
    "evidence_catalog.py",
    "mcp_server/evidence_store.py",
    "mcp_server/fusion_tools.py",
    "index.html",
    "app.js",
    "styles.css",
    "help.html",
    "investigation-user-flow.html",
    "system-capabilities-guide.html",
    "investigation-memory-update-demo-poster.png",
    "investigation-memory-update-demo.mp4",
    "moshe-specialist-response-demo-poster.png",
    "moshe-specialist-response-demo.mp4",
    "personal-assistant-filtered-layer-demo-poster.png",
    "personal-assistant-filtered-layer-demo.mp4",
    "welcome-investigations-demo-poster.png",
    "welcome-investigations-demo.mp4",
    "workstream-monitoring-demo-poster.png",
    "workstream-monitoring-demo.mp4",
    "README.md",
    "mcp_server/install_openai_general_env.sh",
    "data/serbian_intelligence_v2_1/serbia_kosovo_events_projection_v2_1.csv",
    "data/serbian_intelligence_v2_1/serbia_kosovo_locations_v2_1.json",
    "data/serbian_intelligence_v2_1/serbia_kosovo_entities_v2_1.json",
]

DIRS = [
    "demo_profiles",
    "data/syria_empty_v1",
    "data/syria_convoy_v1",
    "data/syria_convoy_v2",
    "data/syria_convoy_v3",
    "data/syria_network_v1",
    "data/syria_adint_v1",
    "data/syria_adint_v2",
    "data/syria_ipdr_v1",
    "data/syria_satellite_v1",
    "data/syria_satellite_v2",
    "data/syria_satellite_v3",
    "data/syria_adint_v3",
    "data/syria_cellular_v1",
    "data/syria_cellular_v2",
    "data/syria_cellular_v3",
    "data/syria_cellular_v4",
    "assets",
    "vendor",
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


def read_remote_ui_config(client: paramiko.SSHClient) -> dict:
    """Read existing UI credentials so interrupted deploys can recover safely."""
    sftp = client.open_sftp()
    try:
        with sftp.open(f"{REMOTE_UI_ROOT}/.hermes-api.json", "r") as handle:
            raw = handle.read()
            config = json.loads(raw.decode("utf-8") if isinstance(raw, bytes) else raw)
    except (OSError, ValueError, AttributeError):
        return {}
    finally:
        sftp.close()
    return config


def read_remote_gateway_api_key(client: paramiko.SSHClient) -> str | None:
    """Resolve the credential owned by the active gateway configuration."""
    _, out, _ = run(
        client,
        "/usr/bin/python3 -c \"import yaml; d=yaml.safe_load(open('/home/ubuntu/.hermes/config.yaml')) or {}; print((((d.get('platforms') or {}).get('api_server') or {}).get('key') or ''))\"",
        timeout=20,
    )
    return out.strip() or None


def upload_ui(client: paramiko.SSHClient, api_key: str, moshe_api_key: str, talia_api_key: str) -> None:
    staging = f"/tmp/serbia-poc-ui-{int(time.time())}"
    run(client, f"rm -rf {shlex.quote(staging)} && mkdir -p {shlex.quote(staging)}")
    catalog_temp = tempfile.TemporaryDirectory(prefix="serbia-evidence-catalog-")
    catalog_dir = Path(catalog_temp.name)
    subprocess.run([
        sys.executable, str(LOCAL_ROOT / "evidence_catalog.py"),
        "--events", str(LOCAL_ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_events_projection_v2_1.csv"),
        "--output-dir", str(catalog_dir), "--dataset-version", "v2.1",
    ], check=True, timeout=180)
    sftp = client.open_sftp()
    try:
        for name in FILES:
            upload_file(sftp, LOCAL_ROOT / name, str(PurePosixPath(staging) / name))
        for name in DIRS:
            upload_dir(sftp, LOCAL_ROOT / name, str(PurePosixPath(staging) / name))
        for name in ("he.json", "en.json", "manifest.json"):
            upload_file(sftp, catalog_dir / name, f"{staging}/data/evidence_catalog/v2.1/{name}")
    finally:
        sftp.close()
        catalog_temp.cleanup()
    root_q = shlex.quote(REMOTE_UI_ROOT)
    staging_q = shlex.quote(staging)
    backup = f"/home/{USER}/deploy-backups/cellular-calls-{int(time.time())}.tar.gz"
    run(
        client,
        f"mkdir -p /home/{USER}/deploy-backups "
        f"&& sudo -n tar -C {root_q} --exclude=.hermes-api.json --exclude=investigations --exclude=workstreams --exclude=scenario_runs -czf {shlex.quote(backup)} . "
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
Environment=INTELLIGENCE_POC_DATASET_VERSION=v2.1

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
    parser.add_argument("--moshe-api-key", default=None)
    parser.add_argument("--talia-api-key", default=None)
    args = parser.parse_args()

    local_config = json.loads(LOCAL_HERMES_CONFIG.read_text(encoding="utf-8")) if LOCAL_HERMES_CONFIG.exists() else {}

    client = connect(args.key.resolve())
    try:
        remote_config = read_remote_ui_config(client)
        api_key = args.api_key or read_remote_gateway_api_key(client) or local_config.get("api_key") or remote_config.get("api_key")
        if not api_key:
            parser.error("--api-key is required when no existing UI credential is available")
        moshe_api_key = (
            args.moshe_api_key
            or ((local_config.get("agents") or {}).get("moshe") or {}).get("api_key")
            or ((remote_config.get("agents") or {}).get("moshe") or {}).get("api_key")
        )
        if not moshe_api_key:
            parser.error("--moshe-api-key is required for the first multiplexed deployment")
        talia_api_key = (
            args.talia_api_key
            or ((local_config.get("agents") or {}).get("talia") or {}).get("api_key")
            or ((remote_config.get("agents") or {}).get("talia") or {}).get("api_key")
            or api_key
        )
        upload_ui(client, api_key, moshe_api_key, talia_api_key)
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

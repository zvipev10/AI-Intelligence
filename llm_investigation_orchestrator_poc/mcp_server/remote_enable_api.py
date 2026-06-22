#!/usr/bin/env python3
from __future__ import annotations

import json
import secrets
import sys
import time
from pathlib import Path

import paramiko


HOST = "151.145.93.180"
USER = "ubuntu"
REMOTE_CONFIG = "/home/ubuntu/.hermes/config.yaml"
API_PORT = 8642
PROJECT_ROOT = Path(__file__).resolve().parents[1]
LOCAL_CONFIG = PROJECT_ROOT / ".hermes-api.json"


def run(client: paramiko.SSHClient, command: str, timeout: int = 60):
    _, stdout, stderr = client.exec_command(command, timeout=timeout)
    code = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    if code:
        raise RuntimeError(err or out or f"remote command failed: {code}")
    return out


key_path = Path(sys.argv[1]).resolve()
api_key = secrets.token_urlsafe(36)

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USER, key_filename=str(key_path), look_for_keys=False, allow_agent=False, timeout=15)

try:
    payload = json.dumps({"api_key": api_key, "port": API_PORT})
    remote_script = f'''\
from pathlib import Path
import json, shutil, time, yaml

settings=json.loads({payload!r})
path=Path({REMOTE_CONFIG!r})
data=yaml.safe_load(path.read_text()) or {{}}
backup=path.with_name(f"config.yaml.before-api-server-{{int(time.time())}}")
shutil.copy2(path, backup)

platforms=data.setdefault("platforms", {{}})
platforms["api_server"]={{
    "enabled": True,
    "key": settings["api_key"],
    "host": "127.0.0.1",
    "port": settings["port"],
    "model_name": "gpt-5.4-mini",
}}
toolsets=data.setdefault("platform_toolsets", {{}})
toolsets["api_server"]=["mcp-intelligence-events-poc"]

temp=path.with_suffix(".yaml.tmp-api-server")
temp.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
temp.replace(path)
print(backup)
'''
    backup = run(client, "python3 - <<'PY'\n" + remote_script + "\nPY").strip()
    run(client, "sudo -n systemctl restart hermes-gateway.service")
    time.sleep(8)
    active = run(client, "sudo -n systemctl is-active hermes-gateway.service").strip()
    listener = run(client, f"ss -ltn | grep '127.0.0.1:{API_PORT}'").strip()
    probe = run(
        client,
        "python3 - <<'PY'\n"
        "import json, urllib.request\n"
        f"req=urllib.request.Request('http://127.0.0.1:{API_PORT}/v1/capabilities', headers={{'Authorization':'Bearer {api_key}'}})\n"
        "with urllib.request.urlopen(req, timeout=10) as r:\n"
        " print(json.dumps(json.load(r), ensure_ascii=False))\n"
        "PY",
    )
finally:
    client.close()

LOCAL_CONFIG.write_text(json.dumps({
    "host": HOST,
    "user": USER,
    "key_path": str(key_path),
    "remote_host": "127.0.0.1",
    "remote_port": API_PORT,
    "api_key": api_key,
}, indent=2))

capabilities = json.loads(probe)
print(json.dumps({
    "gateway": active,
    "listener": listener,
    "backup": backup,
    "toolsets": capabilities.get("toolsets"),
    "model": capabilities.get("model"),
    "local_config": str(LOCAL_CONFIG),
}, ensure_ascii=False, indent=2))


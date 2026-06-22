#!/usr/bin/env python3
"""Deploy the Serbia/Kosovo POC as a separate Hermes MCP server."""

from __future__ import annotations

import argparse
import json
import secrets
import shlex
import sys
import time
from pathlib import Path

import paramiko


HOST = "151.145.93.180"
USER = "ubuntu"
REMOTE_ROOT = "/opt/serbia-poc"
REMOTE_CONFIG = "/home/ubuntu/.hermes/config.yaml"
HERMES_SERVICE = "hermes-gateway.service"
API_PORT = 8642
SERVER_NAME = "serbia-events-poc"
TOOLSET_NAME = "mcp-serbia-events-poc"
HERMES = "/home/ubuntu/.hermes/hermes-agent/venv/bin/hermes"
LOCAL_ROOT = Path(__file__).resolve().parent.parent
LOCAL_CONFIG = LOCAL_ROOT / ".hermes-api.json"

TOOLS = [
    "classify_question_intent",
    "plan_next_investigation_step",
    "search_events",
    "get_events",
    "resolve_location",
    "resolve_event_reference",
    "find_actor_history",
    "aggregate_events",
    "explain_linkage",
    "build_event_sequence",
    "resolve_entity",
    "trace_identifier",
    "trace_semantic_clues",
    "find_related_events",
    "compare_location_claims",
    "challenge_hypothesis",
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


def upload_files(client: paramiko.SSHClient) -> str:
    staging = f"/tmp/serbia-poc-{int(time.time())}"
    run(client, f"mkdir -p {shlex.quote(staging)}/mcp_server {shlex.quote(staging)}/data")
    files = {
        LOCAL_ROOT / "mcp_server" / "server.py": f"{staging}/mcp_server/server.py",
        LOCAL_ROOT / "mcp_server" / "smoke_client.py": f"{staging}/mcp_server/smoke_client.py",
        LOCAL_ROOT / "mcp_server" / "benchmark_tools.py": f"{staging}/mcp_server/benchmark_tools.py",
        LOCAL_ROOT / "data" / "serbia_kosovo_events_projection.csv": f"{staging}/data/serbia_kosovo_events_projection.csv",
        LOCAL_ROOT / "data" / "serbia_kosovo_locations.json": f"{staging}/data/serbia_kosovo_locations.json",
    }
    sftp = client.open_sftp()
    try:
        for local, remote in files.items():
            sftp.put(str(local), remote)
    finally:
        sftp.close()
    return staging


def install_files(client: paramiko.SSHClient, staging: str) -> None:
    root = shlex.quote(REMOTE_ROOT)
    staging_q = shlex.quote(staging)
    command = (
        f"sudo -n install -d -o {USER} -g {USER} -m 0755 {root}/mcp_server {root}/data "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/mcp_server/server.py {root}/mcp_server/server.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/mcp_server/smoke_client.py {root}/mcp_server/smoke_client.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/mcp_server/benchmark_tools.py {root}/mcp_server/benchmark_tools.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbia_kosovo_events_projection.csv {root}/data/serbia_kosovo_events_projection.csv "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbia_kosovo_locations.json {root}/data/serbia_kosovo_locations.json "
        f"&& sudo -n touch {root}/mcp_audit.jsonl "
        f"&& sudo -n chown {USER}:{USER} {root}/mcp_audit.jsonl "
        f"&& chmod 0644 {root}/mcp_audit.jsonl "
        f"&& rm -rf {staging_q}"
    )
    run(client, command, timeout=90)


def configure_hermes(client: paramiko.SSHClient, api_key: str) -> str:
    payload = json.dumps({
        "server_name": SERVER_NAME,
        "toolset_name": TOOLSET_NAME,
        "remote_root": REMOTE_ROOT,
        "api_key": api_key,
        "api_port": API_PORT,
        "tools": TOOLS,
    })
    remote_script = f"""
from pathlib import Path
import json, shutil, time, yaml

settings = json.loads({payload!r})
path = Path({REMOTE_CONFIG!r})
data = yaml.safe_load(path.read_text()) or {{}}
backup = path.with_name(f"config.yaml.before-serbia-poc-{{int(time.time())}}")
shutil.copy2(path, backup)

servers = data.setdefault("mcp_servers", {{}})
servers[settings["server_name"]] = {{
    "command": "/usr/bin/python3",
    "args": [f"{{settings['remote_root']}}/mcp_server/server.py"],
    "env": {{
        "INTELLIGENCE_POC_DATA": f"{{settings['remote_root']}}/data/serbia_kosovo_events_projection.csv",
        "INTELLIGENCE_POC_LOCATIONS": f"{{settings['remote_root']}}/data/serbia_kosovo_locations.json",
        "INTELLIGENCE_POC_AUDIT": f"{{settings['remote_root']}}/mcp_audit.jsonl",
    }},
    "timeout": 30,
    "connect_timeout": 15,
    "enabled": True,
    "supports_parallel_tool_calls": True,
    "tools": {{
        "include": settings["tools"],
        "prompts": False,
        "resources": False,
    }},
    "sampling": {{"enabled": True}},
}}

platforms = data.setdefault("platforms", {{}})
api = platforms.setdefault("api_server", {{}})
api.update({{
    "enabled": True,
    "key": settings["api_key"],
    "host": "127.0.0.1",
    "port": settings["api_port"],
}})
api.setdefault("model_name", "gpt-5.4-mini")

toolsets = data.setdefault("platform_toolsets", {{}})
current = list(toolsets.get("api_server") or [])
for item in ["mcp-intelligence-events-poc", settings["toolset_name"]]:
    if item not in current:
        current.append(item)
toolsets["api_server"] = current

temp = path.with_suffix(".yaml.tmp-serbia-poc")
temp.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False))
temp.replace(path)
print(backup)
"""
    _, out, _ = run(client, "python3 - <<'PY'\n" + remote_script + "\nPY", timeout=40)
    return out.strip()


def verify(client: paramiko.SSHClient, api_key: str, rounds: int) -> dict:
    run(client, f"sudo -n systemctl restart {HERMES_SERVICE}", timeout=90)
    time.sleep(10)
    _, active, _ = run(client, f"sudo -n systemctl is-active {HERMES_SERVICE}", timeout=20)
    _, smoke, _ = run(client, f"/usr/bin/python3 {REMOTE_ROOT}/mcp_server/smoke_client.py", timeout=60)
    _, bench, _ = run(
        client,
        f"cd {REMOTE_ROOT} && PYTHONIOENCODING=utf-8 /usr/bin/python3 mcp_server/benchmark_tools.py --rounds {rounds} --json",
        timeout=180,
    )
    _, capabilities, _ = run(
        client,
        "python3 - <<'PY'\n"
        "import json, urllib.request\n"
        f"req=urllib.request.Request('http://127.0.0.1:{API_PORT}/v1/capabilities', headers={{'Authorization':'Bearer {api_key}'}})\n"
        "with urllib.request.urlopen(req, timeout=20) as r:\n"
        " print(json.dumps(json.load(r), ensure_ascii=False))\n"
        "PY",
        timeout=30,
    )
    _, config, _ = run(
        client,
        "python3 - <<'PY'\n"
        "from pathlib import Path\n"
        "import json, yaml\n"
        "d=yaml.safe_load((Path.home()/'.hermes/config.yaml').read_text()) or {}\n"
        f"e=(d.get('mcp_servers') or {{}}).get({SERVER_NAME!r}) or {{}}\n"
        "print(json.dumps({'server': e, 'api_toolsets': (d.get('platform_toolsets') or {}).get('api_server')}, ensure_ascii=False))\n"
        "PY",
        timeout=30,
    )
    return {
        "gateway": active.strip(),
        "smoke": json.loads(smoke),
        "benchmark": json.loads(bench),
        "capabilities": json.loads(capabilities),
        "config": json.loads(config),
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True, type=Path)
    parser.add_argument("--rounds", type=int, default=1)
    parser.add_argument("--api-key", default=None)
    args = parser.parse_args()

    key_path = args.key.resolve()
    api_key = args.api_key or secrets.token_urlsafe(36)
    client = connect(key_path)
    try:
        staging = upload_files(client)
        install_files(client, staging)
        backup = configure_hermes(client, api_key)
        verification = verify(client, api_key, args.rounds)
    finally:
        client.close()

    LOCAL_CONFIG.write_text(json.dumps({
        "host": HOST,
        "user": USER,
        "key_path": str(key_path),
        "remote_host": "127.0.0.1",
        "remote_port": API_PORT,
        "api_key": api_key,
    }, indent=2), encoding="utf-8")

    print(json.dumps({
        "config_backup": backup,
        "local_config": str(LOCAL_CONFIG),
        "verification": verification,
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

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
MOSHE_HOME = "/home/ubuntu/.hermes/profiles/moshe"
TALIA_HOME = "/home/ubuntu/.hermes/profiles/talia"
HERMES_SERVICE = "hermes-gateway.service"
API_PORT = 8642
SERVER_NAME = "serbia-events-poc"
TOOLSET_NAME = SERVER_NAME
HERMES = "/home/ubuntu/.hermes/hermes-agent/venv/bin/hermes"
LOCAL_ROOT = Path(__file__).resolve().parent.parent
LOCAL_CONFIG = LOCAL_ROOT / ".hermes-api.json"

TOOLS = [
    "prepare_evidence",
    "prepare_fused_evidence",
    "persist_fused_evidence",
    "get_evidence",
    "search_evidence",
    "trace_evidence_provenance",
    "present_requested_results",
    "present_saved_memory_layers",
    "open_catalog_layers",
    "classify_question_intent",
    "plan_next_investigation_step",
    "search_events",
    "semantic_search_events",
    "get_objects",
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
    run(client, f"mkdir -p {shlex.quote(staging)}/mcp_server {shlex.quote(staging)}/moshe_profile {shlex.quote(staging)}/talia_profile {shlex.quote(staging)}/data/serbian_intelligence_v2 {shlex.quote(staging)}/data/serbian_intelligence_v2_1")
    files = {
        LOCAL_ROOT / "mcp_server" / "catalog_layers.py": f"{staging}/mcp_server/catalog_layers.py",
        LOCAL_ROOT / "mcp_server" / "server.py": f"{staging}/mcp_server/server.py",
        LOCAL_ROOT / "mcp_server" / "semantic_index.py": f"{staging}/mcp_server/semantic_index.py",
        LOCAL_ROOT / "mcp_server" / "smoke_client.py": f"{staging}/mcp_server/smoke_client.py",
        LOCAL_ROOT / "mcp_server" / "benchmark_tools.py": f"{staging}/mcp_server/benchmark_tools.py",
        LOCAL_ROOT / "mcp_server" / "target_bank.py": f"{staging}/mcp_server/target_bank.py",
        LOCAL_ROOT / "mcp_server" / "target_bank_admin.py": f"{staging}/mcp_server/target_bank_admin.py",
        LOCAL_ROOT / "mcp_server" / "fusion_tools.py": f"{staging}/mcp_server/fusion_tools.py",
        LOCAL_ROOT / "mcp_server" / "evidence_store.py": f"{staging}/mcp_server/evidence_store.py",
        LOCAL_ROOT / "mcp_server" / "evidence_semantics.py": f"{staging}/mcp_server/evidence_semantics.py",
        LOCAL_ROOT / "mcp_server" / "assessment_store.py": f"{staging}/mcp_server/assessment_store.py",
        LOCAL_ROOT / "moshe_profile" / "provision_profile.py": f"{staging}/moshe_profile/provision_profile.py",
        LOCAL_ROOT / "moshe_profile" / "SOUL.md": f"{staging}/moshe_profile/SOUL.md",
        LOCAL_ROOT / "talia_profile" / "provision_profile.py": f"{staging}/talia_profile/provision_profile.py",
        LOCAL_ROOT / "talia_profile" / "SOUL.md": f"{staging}/talia_profile/SOUL.md",
        LOCAL_ROOT / "data" / "serbia_kosovo_events_projection.csv": f"{staging}/data/serbia_kosovo_events_projection.csv",
        LOCAL_ROOT / "data" / "serbia_kosovo_locations.json": f"{staging}/data/serbia_kosovo_locations.json",
        LOCAL_ROOT / "data" / "serbia_kosovo_entities.json": f"{staging}/data/serbia_kosovo_entities.json",
        LOCAL_ROOT / "data" / "serbian_intelligence_v2" / "serbia_kosovo_events_projection_v2.csv": f"{staging}/data/serbian_intelligence_v2/serbia_kosovo_events_projection_v2.csv",
        LOCAL_ROOT / "data" / "serbian_intelligence_v2" / "serbia_kosovo_locations_v2.json": f"{staging}/data/serbian_intelligence_v2/serbia_kosovo_locations_v2.json",
        LOCAL_ROOT / "data" / "serbian_intelligence_v2" / "serbia_kosovo_entities_v2.json": f"{staging}/data/serbian_intelligence_v2/serbia_kosovo_entities_v2.json",
        LOCAL_ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_events_projection_v2_1.csv": f"{staging}/data/serbian_intelligence_v2_1/serbia_kosovo_events_projection_v2_1.csv",
        LOCAL_ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_locations_v2_1.json": f"{staging}/data/serbian_intelligence_v2_1/serbia_kosovo_locations_v2_1.json",
        LOCAL_ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_entities_v2_1.json": f"{staging}/data/serbian_intelligence_v2_1/serbia_kosovo_entities_v2_1.json",
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
        f"sudo -n install -d -o {USER} -g {USER} -m 0755 {root}/mcp_server {root}/data {root}/data/serbian_intelligence_v2 {root}/data/serbian_intelligence_v2_1 "
        f"&& sudo -n install -d -o {USER} -g {USER} -m 0700 {root}/data/attack_targets {root}/data/evidence {root}/data/assessments {root}/backups/attack_targets "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/mcp_server/catalog_layers.py {root}/mcp_server/catalog_layers.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/mcp_server/server.py {root}/mcp_server/server.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/mcp_server/semantic_index.py {root}/mcp_server/semantic_index.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/mcp_server/smoke_client.py {root}/mcp_server/smoke_client.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/mcp_server/benchmark_tools.py {root}/mcp_server/benchmark_tools.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/mcp_server/target_bank.py {root}/mcp_server/target_bank.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0755 {staging_q}/mcp_server/target_bank_admin.py {root}/mcp_server/target_bank_admin.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/mcp_server/fusion_tools.py {root}/mcp_server/fusion_tools.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/mcp_server/evidence_store.py {root}/mcp_server/evidence_store.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/mcp_server/evidence_semantics.py {root}/mcp_server/evidence_semantics.py "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/mcp_server/assessment_store.py {root}/mcp_server/assessment_store.py "
        f"&& if [ ! -f {TALIA_HOME}/config.yaml ]; then sudo -n install -d -o {USER} -g {USER} -m 0700 {TALIA_HOME} && sudo -n cp {REMOTE_CONFIG} {TALIA_HOME}/config.yaml && sudo -n chown {USER}:{USER} {TALIA_HOME}/config.yaml; fi "
        f"&& sudo -n /usr/bin/python3 {staging_q}/moshe_profile/provision_profile.py --profile-dir {MOSHE_HOME} --soul {staging_q}/moshe_profile/SOUL.md "
        f"&& sudo -n /usr/bin/python3 {staging_q}/talia_profile/provision_profile.py --profile-dir {TALIA_HOME} --soul {staging_q}/talia_profile/SOUL.md "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbia_kosovo_events_projection.csv {root}/data/serbia_kosovo_events_projection.csv "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbia_kosovo_locations.json {root}/data/serbia_kosovo_locations.json "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbia_kosovo_entities.json {root}/data/serbia_kosovo_entities.json "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbian_intelligence_v2/serbia_kosovo_events_projection_v2.csv {root}/data/serbian_intelligence_v2/serbia_kosovo_events_projection_v2.csv "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbian_intelligence_v2/serbia_kosovo_locations_v2.json {root}/data/serbian_intelligence_v2/serbia_kosovo_locations_v2.json "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbian_intelligence_v2/serbia_kosovo_entities_v2.json {root}/data/serbian_intelligence_v2/serbia_kosovo_entities_v2.json "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbian_intelligence_v2_1/serbia_kosovo_events_projection_v2_1.csv {root}/data/serbian_intelligence_v2_1/serbia_kosovo_events_projection_v2_1.csv "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbian_intelligence_v2_1/serbia_kosovo_locations_v2_1.json {root}/data/serbian_intelligence_v2_1/serbia_kosovo_locations_v2_1.json "
        f"&& sudo -n install -o {USER} -g {USER} -m 0644 {staging_q}/data/serbian_intelligence_v2_1/serbia_kosovo_entities_v2_1.json {root}/data/serbian_intelligence_v2_1/serbia_kosovo_entities_v2_1.json "
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
        "INTELLIGENCE_POC_DATASET_VERSION": "v2.1",
        "INTELLIGENCE_POC_DATA": f"{{settings['remote_root']}}/data/serbian_intelligence_v2_1/serbia_kosovo_events_projection_v2_1.csv",
        "INTELLIGENCE_POC_LOCATIONS": f"{{settings['remote_root']}}/data/serbian_intelligence_v2_1/serbia_kosovo_locations_v2_1.json",
        "INTELLIGENCE_POC_ENTITIES": f"{{settings['remote_root']}}/data/serbian_intelligence_v2_1/serbia_kosovo_entities_v2_1.json",
        "INTELLIGENCE_POC_SEMANTIC_INDEX": f"{{settings['remote_root']}}/data/semantic_index/v2.1",
        "INTELLIGENCE_POC_AUDIT": f"{{settings['remote_root']}}/mcp_audit.jsonl",
        "INTELLIGENCE_POC_TARGET_BANK": f"{{settings['remote_root']}}/data/attack_targets/attack_targets.db",
        "INTELLIGENCE_POC_TARGET_BACKUPS": f"{{settings['remote_root']}}/backups/attack_targets",
        "INTELLIGENCE_POC_EVIDENCE_STORE": f"{{settings['remote_root']}}/data/evidence/evidence.db",
        "INTELLIGENCE_POC_EVIDENCE_CATALOG": "/opt/serbia-poc-ui/data/evidence_catalog/v2.1/he.json",
        "INTELLIGENCE_POC_ASSESSMENT_STORE": f"{{settings['remote_root']}}/data/assessments/assessments.db",
        "INTELLIGENCE_POC_PLAYBACK_VISIBILITY": "/opt/serbia-poc-ui/scenario_runs/v2.1/active_visibility.json",
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
legacy_names = {{
    "mcp-intelligence-events-poc": "intelligence-events-poc",
    "mcp-serbia-events-poc": "serbia-events-poc",
}}

moshe_config_path = Path({str(Path(MOSHE_HOME) / 'config.yaml')!r})
if moshe_config_path.exists():
    moshe_config = yaml.safe_load(moshe_config_path.read_text()) or {{}}
    moshe_server = (moshe_config.get("mcp_servers") or {{}}).get("serbia-events-poc-moshe")
    if moshe_server:
        servers["serbia-events-poc-moshe"] = moshe_server
talia_config_path = Path({str(Path(TALIA_HOME) / 'config.yaml')!r})
if talia_config_path.exists():
    talia_config = yaml.safe_load(talia_config_path.read_text()) or {{}}
    talia_server = (talia_config.get("mcp_servers") or {{}}).get("serbia-events-poc-talia")
    if talia_server:
        servers["serbia-events-poc-talia"] = talia_server
talia_env_path = Path({str(Path(TALIA_HOME) / '.env')!r})
retained_env = []
if talia_env_path.exists():
    retained_env = [line for line in talia_env_path.read_text().splitlines() if not line.startswith("API_SERVER_KEY=")]
retained_env.extend([f"API_SERVER_KEY={{settings['api_key']}}", "HERMES_PARALLEL_TOOL_CALLS=false"])
talia_env_path.write_text("\\n".join(dict.fromkeys(retained_env)) + "\\n")
talia_env_path.chmod(0o600)
gateway = data.setdefault("gateway", {{}})
gateway["multiplex_profiles"] = True
allowlist = list(gateway.get("multiplex_profile_allowlist") or [])
for profile in ["moshe", "talia"]:
    if profile not in allowlist:
        allowlist.append(profile)
gateway["multiplex_profile_allowlist"] = allowlist
current = []
for item in toolsets.get("api_server") or []:
    item = legacy_names.get(item, item)
    if item not in current:
        current.append(item)
for item in ["intelligence-events-poc", settings["toolset_name"]]:
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
    client = connect(key_path)
    try:
        if args.api_key:
            api_key = args.api_key
        else:
            _, current_key, _ = run(
                client,
                "/usr/bin/python3 -c \"import yaml; d=yaml.safe_load(open('/home/ubuntu/.hermes/config.yaml')) or {}; print((((d.get('platforms') or {}).get('api_server') or {}).get('key') or ''))\"",
                timeout=20,
                check=False,
            )
            api_key = current_key.strip() or secrets.token_urlsafe(36)
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

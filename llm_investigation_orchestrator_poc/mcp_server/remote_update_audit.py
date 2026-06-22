#!/usr/bin/env python3
from pathlib import Path
import sys
import time
import paramiko

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HOST = "151.145.93.180"
USER = "ubuntu"
LOCAL_SERVER = Path(__file__).resolve().parent / "server.py"
LOCAL_SMOKE = Path(__file__).resolve().parent / "smoke_client.py"
REMOTE_SERVER = "/opt/intelligence-poc/mcp_server/server.py"
REMOTE_SMOKE = "/opt/intelligence-poc/mcp_server/smoke_client.py"

TOOLS = [
    "classify_question_intent",
    "plan_next_investigation_step",
    "search_events", "get_events", "resolve_location", "resolve_event_reference",
    "find_actor_history", "aggregate_events", "explain_linkage", "build_event_sequence", "resolve_entity",
    "trace_identifier", "trace_semantic_clues", "find_related_events", "challenge_hypothesis",
]

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USER, key_filename=str(Path(sys.argv[1])), look_for_keys=False, allow_agent=False, timeout=15)
try:
    sftp = client.open_sftp()
    staging = f"/tmp/intelligence-server-{int(time.time())}.py"
    smoke_staging = f"/tmp/intelligence-smoke-{int(time.time())}.py"
    sftp.put(str(LOCAL_SERVER), staging)
    sftp.put(str(LOCAL_SMOKE), smoke_staging)
    sftp.close()
    tools_literal = repr(TOOLS)
    commands = [
        f"sudo -n install -o {USER} -g {USER} -m 0755 {staging} {REMOTE_SERVER} && sudo -n install -o {USER} -g {USER} -m 0755 {smoke_staging} {REMOTE_SMOKE} && rm -f {staging} {smoke_staging}",
        "python3 - <<'PY'\nfrom pathlib import Path\nimport shutil, time, yaml\np=Path.home()/'.hermes/config.yaml'\nbackup=p.with_name(f'config.yaml.before-intelligence-tools-{int(time.time())}')\nshutil.copy2(p, backup)\nd=yaml.safe_load(p.read_text()) or {}\ne=(d.get('mcp_servers') or {}).get('intelligence-events-poc') or {}\nenv=e.setdefault('env', {})\nenv['INTELLIGENCE_POC_AUDIT']='/opt/intelligence-poc/mcp_audit.jsonl'\ntools=e.setdefault('tools', {})\ntools['include']=" + tools_literal + "\nt=p.with_suffix('.yaml.tmp-intelligence-tools')\nt.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False))\nt.replace(p)\nprint(backup)\nPY",
        f"sudo -n touch /opt/intelligence-poc/mcp_audit.jsonl && sudo -n chown {USER}:{USER} /opt/intelligence-poc/mcp_audit.jsonl && chmod 0644 /opt/intelligence-poc/mcp_audit.jsonl",
        "sudo -n systemctl restart hermes-gateway.service",
    ]
    outputs = []
    for command in commands:
        _, stdout, stderr = client.exec_command(command, timeout=60)
        code = stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        error = stderr.read().decode()
        if code:
            raise RuntimeError(error or output)
        outputs.append(output.strip())
    time.sleep(8)
    verify = (
        "sudo -n systemctl is-active hermes-gateway.service && "
        f"/usr/bin/python3 {REMOTE_SMOKE} && "
        "python3 - <<'PY'\nfrom pathlib import Path\nimport json, yaml\nd=yaml.safe_load((Path.home()/'.hermes/config.yaml').read_text()) or {}\ne=(d.get('mcp_servers') or {}).get('intelligence-events-poc') or {}\nprint(json.dumps({'tools':(e.get('tools') or {}).get('include'),'audit':(e.get('env') or {}).get('INTELLIGENCE_POC_AUDIT')},ensure_ascii=False))\nPY"
    )
    _, stdout, stderr = client.exec_command(verify, timeout=60)
    code = stdout.channel.recv_exit_status()
    output = stdout.read().decode()
    error = stderr.read().decode()
    if code:
        raise RuntimeError(error or output)
    print(output.strip())
finally:
    client.close()

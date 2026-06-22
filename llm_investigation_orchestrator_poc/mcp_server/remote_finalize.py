#!/usr/bin/env python3
"""Finish Hermes MCP registration after the interactive CLI probe blocks."""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

import paramiko


HOST = "151.145.93.180"
USER = "ubuntu"
KEY = Path(sys.argv[1])
CONFIG = "/home/ubuntu/.hermes/config.yaml"
ROOT = "/opt/intelligence-poc"
HERMES = "/home/ubuntu/.hermes/hermes-agent/venv/bin/hermes"


def run(client: paramiko.SSHClient, command: str, timeout: int = 40, check: bool = True):
    _, stdout, stderr = client.exec_command(command, timeout=timeout)
    code = stdout.channel.recv_exit_status()
    out = stdout.read().decode("utf-8", errors="replace")
    err = stderr.read().decode("utf-8", errors="replace")
    if check and code:
        raise RuntimeError(f"Remote command failed ({code}): {err or out}")
    return code, out, err


client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(HOST, username=USER, key_filename=str(KEY), look_for_keys=False, allow_agent=False, timeout=15)

try:
    run(client, "python3 - <<'PY'\nimport os, signal, subprocess\nout=subprocess.check_output(['ps','-eo','pid=,args='], text=True)\nfor line in out.splitlines():\n    if 'hermes mcp add intelligence-events-poc' in line:\n        pid=int(line.strip().split(None,1)[0])\n        os.kill(pid, signal.SIGTERM)\n        print(f'terminated {pid}')\nPY", check=False)

    block = '''  intelligence-events-poc:
    command: /usr/bin/python3
    args:
      - /opt/intelligence-poc/mcp_server/server.py
    env:
      INTELLIGENCE_POC_DATA: /opt/intelligence-poc/data/events_he_large.csv
    timeout: 30
    connect_timeout: 15
    enabled: true
    supports_parallel_tool_calls: true
    tools:
      include:
        - search_events
        - get_events
        - resolve_location
        - resolve_event_reference
        - find_actor_history
        - aggregate_events
        - build_event_sequence
      prompts: false
      resources: false
    sampling:
      enabled: false
'''
    encoded_block = json.dumps(block)
    edit_script = f'''
from pathlib import Path
import re, shutil, time, yaml

path=Path({CONFIG!r})
text=path.read_text()
data=yaml.safe_load(text) or {{}}
servers=data.get('mcp_servers') or {{}}
if 'intelligence-events-poc' in servers:
    print('already-configured')
    raise SystemExit
backup=path.with_name(f'config.yaml.before-intelligence-poc-final-{{int(time.time())}}')
shutil.copy2(path, backup)
block={encoded_block}
match=re.search(r'(?m)^mcp_servers:\\s*(?:{{}}|null)?\\s*$', text)
if match:
    replacement='mcp_servers:\\n'+block
    updated=text[:match.start()]+replacement+text[match.end():]
elif 'mcp_servers' not in data:
    updated=text.rstrip()+'\\n\\nmcp_servers:\\n'+block
else:
    raise SystemExit('mcp_servers exists in an unsupported textual form; refusing automatic edit')
parsed=yaml.safe_load(updated) or {{}}
entry=(parsed.get('mcp_servers') or {{}}).get('intelligence-events-poc')
if not entry or entry.get('command') != '/usr/bin/python3':
    raise SystemExit('validation failed')
temp=path.with_suffix('.yaml.tmp-intelligence-poc')
temp.write_text(updated)
temp.replace(path)
print(backup)
'''
    _, edit_out, _ = run(client, "python3 - <<'PY'\n" + edit_script + "\nPY")

    _, restart_out, restart_err = run(client, "sudo -n systemctl restart hermes-gateway.service && sudo -n systemctl is-active hermes-gateway.service", timeout=60)
    time.sleep(8)
    _, smoke_out, _ = run(client, f"/usr/bin/python3 {ROOT}/mcp_server/smoke_client.py")
    _, config_out, _ = run(client, "python3 - <<'PY'\nfrom pathlib import Path\nimport yaml\ndata=yaml.safe_load((Path.home()/'.hermes/config.yaml').read_text()) or {}\ne=(data.get('mcp_servers') or {}).get('intelligence-events-poc') or {}\nprint({'command':e.get('command'),'args':e.get('args'),'tools':(e.get('tools') or {}).get('include'),'parallel':e.get('supports_parallel_tool_calls')})\nPY")
    _, log_out, _ = run(client, "grep -R -i -E 'intelligence-events-poc|mcp.*intelligence' ~/.hermes/logs 2>/dev/null | tail -50", check=False)
    _, gateway_out, _ = run(client, "tail -120 ~/.hermes/logs/gateway.log 2>/dev/null | grep -i -E 'mcp|intelligence|error|failed' | tail -50", check=False)
    _, process_out, _ = run(client, "ps -eo pid,args | grep -E '[i]ntelligence-poc/mcp_server/server.py' || true", check=False)
    print(json.dumps({
        "config_edit": edit_out.strip(),
        "gateway_restart": (restart_out or restart_err).strip(),
        "smoke": json.loads(smoke_out),
        "config": config_out.strip(),
        "gateway_log_matches": log_out.strip(),
        "gateway_recent": gateway_out.strip(),
        "mcp_processes": process_out.strip(),
    }, ensure_ascii=False, indent=2))
finally:
    client.close()

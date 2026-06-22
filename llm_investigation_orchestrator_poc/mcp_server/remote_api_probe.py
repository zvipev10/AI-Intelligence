#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

import paramiko

client = paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect("151.145.93.180", username="ubuntu", key_filename=str(Path(sys.argv[1])), look_for_keys=False, allow_agent=False, timeout=15)

commands = {
    "listeners": "ss -ltnp 2>/dev/null | sed -n '1,120p'",
    "api_files": "cd ~/.hermes/hermes-agent && grep -R -l -E '/v1/(runs|responses|chat/completions)|FastAPI\\(' --include='*.py' . 2>/dev/null | head -80",
    "api_routes": "cd ~/.hermes/hermes-agent && grep -R -n -E '/v1/(runs|responses|chat/completions)|api_server|FastAPI\\(' --include='*.py' gateway hermes_cli agent web 2>/dev/null | head -240",
    "cli_help": "~/.hermes/hermes-agent/venv/bin/hermes --help 2>&1 | sed -n '1,220p'",
    "gateway_unit": "systemctl cat hermes-gateway.service 2>/dev/null | sed -n '1,180p'",
    "web_processes": "ps -eo pid,args | grep -E '[u]vicorn|[f]astapi|[h]ermes.*api|[h]ermes.*web' | head -40",
    "api_config_shape": "cd ~/.hermes/hermes-agent && sed -n '1425,1485p' gateway/config.py; sed -n '3450,3585p' gateway/platforms/api_server.py",
    "run_request_shape": "cd ~/.hermes/hermes-agent && sed -n '2880,3275p' gateway/platforms/api_server.py",
    "platform_config_sanitized": "python3 - <<'PY'\nfrom pathlib import Path\nimport yaml, json\nd=yaml.safe_load((Path.home()/'.hermes/config.yaml').read_text()) or {}\np=d.get('platforms') or {}\nfor k,v in list(p.items()):\n if isinstance(v,dict):\n  v={kk:('***' if any(x in kk.lower() for x in ['key','token','secret','password']) else vv) for kk,vv in v.items()}\n  p[k]=v\nprint(json.dumps({'platforms':p,'platform_toolsets':d.get('platform_toolsets'),'model':d.get('model')},ensure_ascii=False,indent=2))\nPY",
}

result = {}
try:
    for key, command in commands.items():
        _, stdout, stderr = client.exec_command(command, timeout=30)
        code = stdout.channel.recv_exit_status()
        out = stdout.read().decode("utf-8", errors="replace")
        err = stderr.read().decode("utf-8", errors="replace")
        result[key] = {"code": code, "output": (out or err).strip()}
finally:
    client.close()

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))

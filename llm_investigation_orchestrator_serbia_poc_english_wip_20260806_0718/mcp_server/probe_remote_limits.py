#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

import paramiko


ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / ".hermes-api.json"


def main() -> int:
    cfg = json.loads(CONFIG.read_text(encoding="utf-8"))
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        cfg["host"],
        username=cfg["user"],
        key_filename=cfg["key_path"],
        look_for_keys=False,
        allow_agent=False,
        timeout=15,
    )
    try:
        commands = {
            "limits": (
                "python3 -c \"from pathlib import Path; "
                "lines=Path('/opt/serbia-poc/mcp_server/server.py').read_text().splitlines(); "
                "print('\\n'.join(f'{i+1}:{line}' for i,line in enumerate(lines) "
                "if line.startswith(('DEFAULT_LIMIT =','MAX_LIMIT ='))))\""
            ),
            "service": "sudo -n systemctl is-active hermes-gateway.service",
            "audit_lines": (
                "python3 -c \"from pathlib import Path; "
                "p=Path('/opt/serbia-poc/mcp_audit.jsonl'); "
                "print(len(p.read_text().splitlines()) if p.exists() else 0)\""
            ),
        }
        result = {}
        for name, command in commands.items():
            _, stdout, stderr = client.exec_command(command, timeout=20)
            code = stdout.channel.recv_exit_status()
            result[name] = {
                "code": code,
                "stdout": stdout.read().decode("utf-8", errors="replace").strip(),
                "stderr": stderr.read().decode("utf-8", errors="replace").strip(),
            }
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

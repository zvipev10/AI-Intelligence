#!/usr/bin/env python3
"""Deploy a non-overwriting dataset file and point Hermes MCP at it."""

from __future__ import annotations

from pathlib import Path
import sys
import time

import paramiko


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HOST = "151.145.93.180"
USER = "ubuntu"
LOCAL_DATA = Path(__file__).resolve().parent.parent / "data" / "events_he_expanded_5000.csv"
REMOTE_DATA = "/opt/intelligence-poc/data/events_he_expanded_5000.csv"
REMOTE_SMOKE = "/opt/intelligence-poc/mcp_server/smoke_client.py"


def run(client: paramiko.SSHClient, command: str, timeout: int = 60) -> str:
    _, stdout, stderr = client.exec_command(command, timeout=timeout)
    code = stdout.channel.recv_exit_status()
    output = stdout.read().decode("utf-8", errors="replace")
    error = stderr.read().decode("utf-8", errors="replace")
    if code:
        raise RuntimeError(error or output or f"SSH command failed: {code}")
    return output.strip()


def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: remote_deploy_dataset.py <ssh-private-key>", file=sys.stderr)
        return 2
    if not LOCAL_DATA.exists():
        raise FileNotFoundError(LOCAL_DATA)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, key_filename=str(Path(sys.argv[1])), look_for_keys=False, allow_agent=False, timeout=45)
    try:
        staging = f"/tmp/{LOCAL_DATA.name}.{int(time.time())}"
        sftp = client.open_sftp()
        sftp.put(str(LOCAL_DATA), staging)
        sftp.close()
        run(client, f"sudo -n mkdir -p /opt/intelligence-poc/data && sudo -n install -o {USER} -g {USER} -m 0644 {staging} {REMOTE_DATA} && rm -f {staging}")
        run(
            client,
            "python3 - <<'PY'\n"
            "from pathlib import Path\n"
            "import shutil, time, yaml\n"
            "p=Path.home()/'.hermes/config.yaml'\n"
            "backup=p.with_name(f'config.yaml.before-expanded-dataset-{int(time.time())}')\n"
            "shutil.copy2(p, backup)\n"
            "d=yaml.safe_load(p.read_text()) or {}\n"
            "e=(d.get('mcp_servers') or {}).get('intelligence-events-poc') or {}\n"
            "env=e.setdefault('env', {})\n"
            f"env['INTELLIGENCE_POC_DATA']='{REMOTE_DATA}'\n"
            "env['INTELLIGENCE_POC_AUDIT']='/opt/intelligence-poc/mcp_audit.jsonl'\n"
            "t=p.with_suffix('.yaml.tmp-expanded-dataset')\n"
            "t.write_text(yaml.safe_dump(d, allow_unicode=True, sort_keys=False))\n"
            "t.replace(p)\n"
            "print(backup)\n"
            "PY",
        )
        run(client, "sudo -n systemctl restart hermes-gateway.service")
        time.sleep(8)
        verify = run(
            client,
            "sudo -n systemctl is-active hermes-gateway.service && "
            f"INTELLIGENCE_POC_DATA={REMOTE_DATA} /usr/bin/python3 {REMOTE_SMOKE} && "
            "python3 - <<'PY'\n"
            "from pathlib import Path\n"
            "import csv, json, yaml\n"
            "d=yaml.safe_load((Path.home()/'.hermes/config.yaml').read_text()) or {}\n"
            "env=((d.get('mcp_servers') or {}).get('intelligence-events-poc') or {}).get('env') or {}\n"
            "data=Path(env.get('INTELLIGENCE_POC_DATA',''))\n"
            "count=sum(1 for _ in csv.DictReader(data.open(encoding='utf-8-sig')))\n"
            "print(json.dumps({'data':str(data),'rows':count,'exists':data.exists()},ensure_ascii=False))\n"
            "PY",
            timeout=90,
        )
        print(verify)
        return 0
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())

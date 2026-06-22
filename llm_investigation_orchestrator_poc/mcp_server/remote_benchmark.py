#!/usr/bin/env python3
"""Upload and run the MCP benchmark on the Hermes VM."""

from __future__ import annotations

from pathlib import Path
import sys
import time

import paramiko


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HOST = "151.145.93.180"
USER = "ubuntu"
LOCAL_BENCHMARK = Path(__file__).resolve().parent / "benchmark_tools.py"
REMOTE_BENCHMARK = "/opt/intelligence-poc/mcp_server/benchmark_tools.py"
REMOTE_DATA = "/opt/intelligence-poc/data/events_he_expanded_5000.csv"


def run(client: paramiko.SSHClient, command: str, timeout: int = 120) -> str:
    _, stdout, stderr = client.exec_command(command, timeout=timeout)
    code = stdout.channel.recv_exit_status()
    output = stdout.read().decode("utf-8", errors="replace")
    error = stderr.read().decode("utf-8", errors="replace")
    if code:
        raise RuntimeError(error or output or f"SSH command failed: {code}")
    return output.strip()


def main() -> int:
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: remote_benchmark.py <ssh-private-key> [rounds]", file=sys.stderr)
        return 2
    rounds = int(sys.argv[2]) if len(sys.argv) == 3 else 10
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, key_filename=str(Path(sys.argv[1])), look_for_keys=False, allow_agent=False, timeout=45)
    try:
        staging = f"/tmp/intelligence-benchmark-{int(time.time())}.py"
        sftp = client.open_sftp()
        sftp.put(str(LOCAL_BENCHMARK), staging)
        sftp.close()
        run(client, f"sudo -n install -o {USER} -g {USER} -m 0755 {staging} {REMOTE_BENCHMARK} && rm -f {staging}")
        output = run(
            client,
            f"cd /opt/intelligence-poc && INTELLIGENCE_POC_DATA={REMOTE_DATA} PYTHONIOENCODING=utf-8 /usr/bin/python3 {REMOTE_BENCHMARK} --rounds {rounds}",
            timeout=180,
        )
        print(output)
        return 0
    finally:
        client.close()


if __name__ == "__main__":
    raise SystemExit(main())

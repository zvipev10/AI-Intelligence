#!/usr/bin/env python3
"""Run target-bank persistence, backup, reset, and permission tests on the Linux VM."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
import time
from pathlib import Path, PurePosixPath

from remote_deploy_ui import HOST, connect, run


LOCAL_ROOT = Path(__file__).resolve().parent
FILES = ("target_bank.py", "target_bank_admin.py", "test_target_bank.py")


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True, type=Path)
    args = parser.parse_args()

    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    staging = f"/tmp/serbia-target-bank-validation-{stamp}"
    staging_q = shlex.quote(staging)
    client = connect(args.key.resolve())
    try:
        run(client, f"install -d -m 0700 {staging_q}")
        sftp = client.open_sftp()
        try:
            for name in FILES:
                sftp.put(str(LOCAL_ROOT / name), str(PurePosixPath(staging) / name))
        finally:
            sftp.close()
        code, out, err = run(
            client,
            f"cd {staging_q} && /usr/bin/python3 test_target_bank.py",
            timeout=120,
            check=False,
        )
        permission_code, permission_out, permission_err = run(
            client,
            f"cd {staging_q} && /usr/bin/python3 target_bank_admin.py initialize "
            f"--db {staging_q}/runtime/attack_targets.db --backup-dir {staging_q}/backups "
            f"&& stat -c '%a %n' {staging_q}/runtime {staging_q}/runtime/attack_targets.db",
            timeout=60,
            check=False,
        )
        result = {
            "host": HOST,
            "tests": {"code": code, "output": (out or err).strip()},
            "permissions": {"code": permission_code, "output": (permission_out or permission_err).strip()},
        }
        if code or permission_code:
            raise RuntimeError(json.dumps(result, ensure_ascii=False))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    finally:
        run(client, f"rm -rf {staging_q}", check=False)
        client.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

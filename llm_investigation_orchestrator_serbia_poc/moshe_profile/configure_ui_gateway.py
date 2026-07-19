#!/usr/bin/env python3
"""Add Moshe's local gateway override without printing or replacing shared credentials."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", required=True, type=Path)
    args = parser.parse_args()
    path = args.config.resolve()
    config = json.loads(path.read_text(encoding="utf-8-sig"))
    agents = dict(config.get("agents") or {})
    agents["moshe"] = {
        "remote_port": 8643,
        "audit_path": "/opt/serbia-poc/mcp_audit_moshe.jsonl",
    }
    config["agents"] = agents
    config.setdefault("audit_path", "/opt/serbia-poc/mcp_audit.jsonl")
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(config, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    os.chmod(temporary, path.stat().st_mode & 0o777)
    temporary.replace(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

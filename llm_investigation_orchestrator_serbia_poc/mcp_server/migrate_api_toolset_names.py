#!/usr/bin/env python3
"""Migrate legacy MCP aliases in Hermes API platform toolsets."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

import yaml


LEGACY_NAMES = {
    "mcp-intelligence-events-poc": "intelligence-events-poc",
    "mcp-serbia-events-poc": "serbia-events-poc",
}


def migrated_config(config: dict) -> dict:
    result = dict(config)
    servers = result.get("mcp_servers") or {}
    platform_toolsets = dict(result.get("platform_toolsets") or {})
    api_toolsets = platform_toolsets.get("api_server") or []
    migrated = []
    for value in api_toolsets:
        candidate = LEGACY_NAMES.get(value, value)
        if candidate not in migrated:
            migrated.append(candidate)
    unknown = [value for value in migrated if value not in servers]
    if unknown:
        raise ValueError(f"API toolsets do not match configured MCP servers: {', '.join(unknown)}")
    platform_toolsets["api_server"] = migrated
    result["platform_toolsets"] = platform_toolsets
    return result


def migrate_file(path: Path) -> None:
    source = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    updated = migrated_config(source)
    mode = path.stat().st_mode
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        yaml.safe_dump(updated, handle, allow_unicode=True, sort_keys=False)
        temporary = Path(handle.name)
    os.chmod(temporary, mode)
    temporary.replace(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()
    for path in args.paths:
        migrate_file(path.resolve())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

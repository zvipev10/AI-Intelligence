#!/usr/bin/env python3
"""Configure the persistent General profile used by the instruction A/B test."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Any

import yaml


GENERAL_PERSISTENT_PORT = 8644
GENERAL_PERSISTENT_AUDIT_PATH = "/opt/serbia-poc/mcp_audit_general_persistent.jsonl"
MESSAGING_ENV_PREFIXES = (
    "TELEGRAM_", "DISCORD_", "WHATSAPP_", "SLACK_", "SIGNAL_", "TEAMS_",
    "GOOGLE_CHAT_", "FEISHU_", "QQBOT_", "YUANBAO_", "HOMEASSISTANT_",
)


def configured_profile(config: dict[str, Any]) -> dict[str, Any]:
    result = dict(config)
    platforms = dict(result.get("platforms") or {})
    api = dict(platforms.get("api_server") or {})
    api.update({"enabled": True, "host": "127.0.0.1", "port": GENERAL_PERSISTENT_PORT})
    result["platforms"] = {"api_server": api}
    servers = dict(result.get("mcp_servers") or {})
    serbia = dict(servers.get("serbia-events-poc") or {})
    if not serbia:
        raise ValueError("source profile is missing serbia-events-poc")
    environment = dict(serbia.get("env") or {})
    environment["INTELLIGENCE_POC_AUDIT"] = GENERAL_PERSISTENT_AUDIT_PATH
    serbia["env"] = environment
    servers["serbia-events-poc"] = serbia
    result["mcp_servers"] = servers
    result["platform_toolsets"] = {"api_server": list(servers)}
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-dir", required=True, type=Path)
    parser.add_argument("--soul", required=True, type=Path)
    args = parser.parse_args()
    profile_dir = args.profile_dir.resolve()
    config_path = profile_dir / "config.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    config_path.write_text(
        yaml.safe_dump(configured_profile(config), allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    (profile_dir / "SOUL.md").write_text(args.soul.read_text(encoding="utf-8"), encoding="utf-8")
    env_path = profile_dir / ".env"
    if env_path.exists():
        retained = []
        for line in env_path.read_text(encoding="utf-8").splitlines():
            key = line.split("=", 1)[0].strip().upper() if "=" in line and not line.lstrip().startswith("#") else ""
            if key and any(key.startswith(prefix) for prefix in MESSAGING_ENV_PREFIXES):
                continue
            retained.append(line)
        env_path.write_text("\n".join(retained) + "\n", encoding="utf-8")
        os.chmod(env_path, env_path.stat().st_mode & 0o777)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

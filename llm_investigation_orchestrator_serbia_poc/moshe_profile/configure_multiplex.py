#!/usr/bin/env python3
"""Configure the default gateway and Moshe profile for one multiplexed process."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tempfile

import yaml

try:
    from .provision_profile import MESSAGING_ENV_PREFIXES, MOSHE_AUDIT_PATH, restricted_config
except ImportError:  # Direct script execution on the VM.
    from provision_profile import MESSAGING_ENV_PREFIXES, MOSHE_AUDIT_PATH, restricted_config


DISABLED_PROFILE_PLATFORM_FLAGS = (
    "WHATSAPP_ENABLED", "TELEGRAM_ENABLED", "DISCORD_ENABLED", "SLACK_ENABLED",
    "SIGNAL_ENABLED", "TEAMS_ENABLED", "GOOGLE_CHAT_ENABLED", "FEISHU_ENABLED",
    "QQBOT_ENABLED", "YUANBAO_ENABLED", "HOMEASSISTANT_ENABLED",
)


def atomic_text(path: Path, content: str) -> None:
    mode = path.stat().st_mode if path.exists() else 0o600
    with tempfile.NamedTemporaryFile(
        "w", encoding="utf-8", dir=path.parent, prefix=f".{path.name}.", delete=False
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.chmod(temporary, mode & 0o777)
    temporary.replace(path)


def configure_default(config: dict, moshe_server: dict | None = None) -> dict:
    result = dict(config)
    gateway = dict(result.get("gateway") or {})
    gateway["multiplex_profiles"] = True
    allowlist = list(gateway.get("multiplex_profile_allowlist") or [])
    if "moshe" not in allowlist:
        allowlist.append("moshe")
    gateway["multiplex_profile_allowlist"] = allowlist
    result["gateway"] = gateway
    if moshe_server:
        servers = dict(result.get("mcp_servers") or {})
        servers["serbia-events-poc-moshe"] = dict(moshe_server)
        result["mcp_servers"] = servers
    return result


def configure_env(content: str, api_key: str) -> str:
    retained = []
    for line in content.splitlines():
        key = line.split("=", 1)[0].strip().upper() if "=" in line and not line.lstrip().startswith("#") else ""
        if key in {"API_SERVER_KEY", "HERMES_PARALLEL_TOOL_CALLS", *DISABLED_PROFILE_PLATFORM_FLAGS}:
            continue
        if key and any(key.startswith(prefix) for prefix in MESSAGING_ENV_PREFIXES):
            continue
        retained.append(line)
    retained.extend([f"API_SERVER_KEY={api_key}", "HERMES_PARALLEL_TOOL_CALLS=false"])
    return "\n".join(retained) + "\n"


def configure_ui(config: dict, api_key: str) -> dict:
    result = dict(config)
    agents = dict(result.get("agents") or {})
    agents["moshe"] = {
        "remote_port": int(result.get("remote_port") or 8642),
        "api_key": api_key,
        "api_path_prefix": "/p/moshe",
        "mcp_tool_prefix": "mcp_serbia_events_poc_moshe_",
        "audit_path": MOSHE_AUDIT_PATH,
    }
    result["agents"] = agents
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--default-config", required=True, type=Path)
    parser.add_argument("--moshe-config", required=True, type=Path)
    parser.add_argument("--moshe-env", required=True, type=Path)
    parser.add_argument("--ui-config", required=True, type=Path)
    parser.add_argument("--api-key", required=True)
    args = parser.parse_args()

    default = yaml.safe_load(args.default_config.read_text(encoding="utf-8")) or {}
    moshe = yaml.safe_load(args.moshe_config.read_text(encoding="utf-8")) or {}
    ui = json.loads(args.ui_config.read_text(encoding="utf-8-sig"))
    restricted_moshe = restricted_config(moshe)
    moshe_server = restricted_moshe["mcp_servers"]["serbia-events-poc-moshe"]
    atomic_text(args.default_config, yaml.safe_dump(configure_default(default, moshe_server), allow_unicode=True, sort_keys=False))
    atomic_text(args.moshe_config, yaml.safe_dump(restricted_moshe, allow_unicode=True, sort_keys=False))
    atomic_text(args.moshe_env, configure_env(args.moshe_env.read_text(encoding="utf-8") if args.moshe_env.exists() else "", args.api_key))
    atomic_text(args.ui_config, json.dumps(configure_ui(ui, args.api_key), ensure_ascii=False, indent=2) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

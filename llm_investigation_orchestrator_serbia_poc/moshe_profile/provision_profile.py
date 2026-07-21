#!/usr/bin/env python3
"""Apply Moshe's restricted, evaluator-isolated configuration to a cloned Hermes profile."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


MOSHE_PORT = 8643
MOSHE_AUDIT_PATH = "/opt/serbia-poc/mcp_audit_moshe.jsonl"
MOSHE_DB_PATH = "/opt/serbia-poc/data/attack_targets/attack_targets.db"
MOSHE_BACKUP_PATH = "/opt/serbia-poc/backups/attack_targets"
MOSHE_TOOLS = [
    "classify_question_intent", "plan_next_investigation_step", "search_events",
    "semantic_search_events", "get_objects", "resolve_location", "resolve_event_reference",
    "find_actor_history", "aggregate_events", "explain_linkage", "build_event_sequence",
    "resolve_entity", "trace_identifier", "trace_semantic_clues", "find_related_events",
    "compare_location_claims", "challenge_hypothesis", "prepare_target_candidate",
    "find_duplicate_target_candidates", "search_target_candidates", "get_target_candidate",
    "create_target_candidate", "update_target_candidate", "attach_target_evidence",
]
FORBIDDEN_TOOL_FRAGMENTS = ("sql", "shell", "filesystem", "delete", "reset", "backup", "truth", "evaluator", "status")
MESSAGING_ENV_PREFIXES = (
    "TELEGRAM_", "DISCORD_", "WHATSAPP_", "SLACK_", "SIGNAL_", "TEAMS_",
    "GOOGLE_CHAT_", "FEISHU_", "QQBOT_", "YUANBAO_", "HOMEASSISTANT_",
)


def restricted_config(config: dict[str, Any]) -> dict[str, Any]:
    result = dict(config)
    platforms = dict(result.get("platforms") or {})
    api = dict(platforms.get("api_server") or {})
    api.update({"enabled": True, "host": "127.0.0.1", "port": MOSHE_PORT})
    result["platforms"] = {"api_server": api}
    result["platform_toolsets"] = {"api_server": ["mcp-serbia-events-poc"]}

    servers = result.get("mcp_servers") or {}
    serbia = dict(servers.get("serbia-events-poc") or {})
    if not serbia:
        raise ValueError("source profile is missing serbia-events-poc")
    environment = dict(serbia.get("env") or {})
    environment.update({
        "INTELLIGENCE_POC_AUDIT": MOSHE_AUDIT_PATH,
        "INTELLIGENCE_POC_TARGET_BANK": MOSHE_DB_PATH,
        "INTELLIGENCE_POC_TARGET_BACKUPS": MOSHE_BACKUP_PATH,
    })
    serbia["env"] = environment
    tools = dict(serbia.get("tools") or {})
    tools.update({"include": list(MOSHE_TOOLS), "prompts": False, "resources": False})
    serbia["tools"] = tools
    result["mcp_servers"] = {"serbia-events-poc": serbia}
    validate_restricted_config(result)
    return result


def validate_restricted_config(config: dict[str, Any]) -> None:
    servers = config.get("mcp_servers") or {}
    if set(servers) != {"serbia-events-poc"}:
        raise ValueError("Moshe profile may expose only serbia-events-poc")
    included = servers["serbia-events-poc"]["tools"]["include"]
    if included != MOSHE_TOOLS or len(included) != len(set(included)):
        raise ValueError("Moshe tool allowlist does not match the approved contract")
    forbidden = [tool for tool in included if any(fragment in tool.casefold() for fragment in FORBIDDEN_TOOL_FRAGMENTS)]
    if forbidden:
        raise ValueError(f"forbidden Moshe tools: {', '.join(forbidden)}")
    serialized = yaml.safe_dump(config, allow_unicode=True).casefold()
    for marker in ("fusion_target_truth", "evaluator_labels", "truth_id", "expected_target"):
        if marker in serialized:
            raise ValueError(f"evaluator contract leaked into Moshe profile: {marker}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-dir", required=True, type=Path)
    parser.add_argument("--soul", required=True, type=Path)
    args = parser.parse_args()
    profile_dir = args.profile_dir.resolve()
    config_path = profile_dir / "config.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    updated = restricted_config(config)
    config_path.write_text(yaml.safe_dump(updated, allow_unicode=True, sort_keys=False), encoding="utf-8")
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
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

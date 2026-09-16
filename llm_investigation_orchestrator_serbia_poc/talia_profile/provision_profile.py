#!/usr/bin/env python3
"""Apply Talia's assessment-only configuration to a multiplexed Hermes profile."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

import yaml


TALIA_MCP_SERVER_NAME = "serbia-events-poc-talia"
TALIA_AUDIT_PATH = "/opt/serbia-poc/mcp_audit_talia.jsonl"
ASSESSMENT_STORE_PATH = "/opt/serbia-poc/data/assessments/assessments.db"
EVIDENCE_STORE_PATH = "/opt/serbia-poc/data/evidence/evidence.db"
PLAYBACK_VISIBILITY_PATH = "/opt/serbia-poc-ui/scenario_runs/v2.1/active_visibility.json"
TALIA_TOOLS = [
    "prepare_evidence", "prepare_fused_evidence", "persist_fused_evidence", "get_evidence",
    "search_evidence", "trace_evidence_provenance", "create_enemy_assessment",
    "update_enemy_assessment", "get_enemy_assessment", "search_enemy_assessments",
    "attach_assessment_evidence", "supersede_enemy_assessment", "present_requested_results",
    "classify_question_intent", "plan_next_investigation_step", "search_events",
    "semantic_search_events", "get_objects", "resolve_location", "resolve_event_reference",
    "find_actor_history", "aggregate_events", "explain_linkage", "build_event_sequence",
    "resolve_entity", "trace_identifier", "trace_semantic_clues", "find_related_events",
    "compare_location_claims", "challenge_hypothesis",
]
FORBIDDEN_TOOL_FRAGMENTS = ("target", "workstream", "sql", "shell", "filesystem", "delete", "reset", "truth", "evaluator")
MESSAGING_ENV_PREFIXES = ("TELEGRAM_", "DISCORD_", "WHATSAPP_", "SLACK_", "SIGNAL_", "TEAMS_", "GOOGLE_CHAT_", "FEISHU_", "QQBOT_", "YUANBAO_")


def restricted_config(config: dict[str, Any]) -> dict[str, Any]:
    result = dict(config)
    result["platforms"] = {"api_server": {"enabled": False}, "whatsapp": {"enabled": False}}
    result["platform_toolsets"] = {"api_server": [TALIA_MCP_SERVER_NAME]}
    servers = result.get("mcp_servers") or {}
    serbia = dict(servers.get(TALIA_MCP_SERVER_NAME) or servers.get("serbia-events-poc") or {})
    if not serbia:
        raise ValueError("source profile is missing serbia-events-poc")
    environment = dict(serbia.get("env") or {})
    environment.update({
        "INTELLIGENCE_POC_AUDIT": TALIA_AUDIT_PATH,
        "INTELLIGENCE_POC_EVIDENCE_STORE": EVIDENCE_STORE_PATH,
        "INTELLIGENCE_POC_ASSESSMENT_STORE": ASSESSMENT_STORE_PATH,
        "INTELLIGENCE_POC_PLAYBACK_VISIBILITY": PLAYBACK_VISIBILITY_PATH,
    })
    serbia["env"] = environment
    serbia["tools"] = {"include": list(TALIA_TOOLS), "prompts": False, "resources": False}
    result["mcp_servers"] = {TALIA_MCP_SERVER_NAME: serbia}
    validate_restricted_config(result)
    return result


def validate_restricted_config(config: dict[str, Any]) -> None:
    servers = config.get("mcp_servers") or {}
    if set(servers) != {TALIA_MCP_SERVER_NAME}:
        raise ValueError("Talia profile may expose only its assessment MCP server")
    included = servers[TALIA_MCP_SERVER_NAME]["tools"]["include"]
    if included != TALIA_TOOLS or len(included) != len(set(included)):
        raise ValueError("Talia tool allowlist does not match the approved contract")
    forbidden = [tool for tool in included if any(fragment in tool.casefold() for fragment in FORBIDDEN_TOOL_FRAGMENTS)]
    if forbidden:
        raise ValueError(f"forbidden Talia tools: {', '.join(forbidden)}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile-dir", required=True, type=Path)
    parser.add_argument("--soul", required=True, type=Path)
    args = parser.parse_args()
    profile_dir = args.profile_dir.resolve()
    config_path = profile_dir / "config.yaml"
    config = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
    config_path.write_text(yaml.safe_dump(restricted_config(config), allow_unicode=True, sort_keys=False), encoding="utf-8")
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

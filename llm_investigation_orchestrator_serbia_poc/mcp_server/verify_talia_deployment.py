#!/usr/bin/env python3
"""Verify the deployed Talia profile and create an idempotent real-data assessment."""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

import paramiko


HOST = "151.145.93.180"
USER = "ubuntu"

REMOTE_CHECK = r'''
import hashlib
import importlib.util
import json
import os
import sys
import urllib.request
from pathlib import Path

import yaml

default = yaml.safe_load(Path("/home/ubuntu/.hermes/config.yaml").read_text()) or {}
talia = yaml.safe_load(Path("/home/ubuntu/.hermes/profiles/talia/config.yaml").read_text()) or {}
server_config = (talia.get("mcp_servers") or {}).get("serbia-events-poc-talia") or {}
tools = (server_config.get("tools") or {}).get("include") or []
for key, value in (server_config.get("env") or {}).items():
    os.environ[str(key)] = str(value)
sys.path.insert(0, "/opt/serbia-poc/mcp_server")
spec = importlib.util.spec_from_file_location("talia_deployed_mcp", "/opt/serbia-poc/mcp_server/server.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

evidence_id = "EVD-REC-V2-006594"
if module.resolve_evidence(evidence_id) is None:
    raise RuntimeError(f"real projected evidence missing: {evidence_id}")
target_path = Path(os.environ.get("INTELLIGENCE_POC_TARGET_BANK", "/opt/serbia-poc/data/attack_targets/attack_targets.db"))
before = hashlib.sha256(target_path.read_bytes()).hexdigest() if target_path.exists() else None
payload = {
    "title": "KFOR activity-area assessment — deployment verification",
    "status": "current",
    "scope": {"location_ids": ["LOC-V2-001"]},
    "key_judgments": [{
        "judgment": "Reported activity supports a bounded operating-area assessment.",
        "confidence": "medium",
        "evidence_ids": [evidence_id],
    }],
    "alternatives": ["Routine patrol or training activity"],
    "contradictions": [],
    "intelligence_gaps": ["Independent temporal corroboration"],
    "indicators": ["Additional independent observations on the same axis"],
    "summary": "A demonstration assessment grounded in the deployed evidence projection.",
    "overlays": [{
        "type": "assessed_area", "meaning": "assessed activity area", "confidence": "medium",
        "supporting_evidence_ids": [evidence_id],
        "geometry": {"type": "Polygon", "coordinates": [[[20.82, 42.87], [20.88, 42.87], [20.88, 42.91], [20.82, 42.87]]]},
    }],
}
created = module.create_enemy_assessment({"assessment": payload})["assessment"]
reopened = module.get_enemy_assessment({"assessment_id": created["assessment_id"]})["assessment"]
layer = module._materialize_presentation_layers([{
    "kind": "assessments", "ids": [created["assessment_id"]],
    "label": "Enemy assessment", "view": "map",
}], id_prefix="deployment")[0]
after = hashlib.sha256(target_path.read_bytes()).hexdigest() if target_path.exists() else None
forbidden = [name for name in tools if "target" in name or "workstream" in name]
result = {
    "gateway_active_profile": "talia" in ((default.get("gateway") or {}).get("multiplex_profile_allowlist") or []),
    "tool_count": len(tools),
    "assessment_tools": sorted(name for name in tools if "assessment" in name),
    "forbidden_tools": forbidden,
    "assessment_id": created["assessment_id"],
    "revision": reopened["revision"],
    "evidence_id": evidence_id,
    "overlay_type": reopened["overlays"][0]["geometry"]["type"],
    "presentation_kind": layer["kind"],
    "presentation_map": layer["capabilities"]["map"],
    "target_bank_unchanged": before == after,
}
assert result["gateway_active_profile"] and not forbidden and result["target_bank_unchanged"]
request_body = json.dumps({
    "prompt": f"פתחי את ההערכה {created['assessment_id']} והציגי אותה על המפה.",
    "routing_prompt": f"@טליה פתחי את ההערכה {created['assessment_id']} והציגי אותה על המפה.",
    "history": [], "investigation_id": "talia-deployment-verification", "locale": "he",
}).encode("utf-8")
request = urllib.request.Request("http://127.0.0.1:8769/api/investigate", data=request_body, headers={"Content-Type": "application/json"}, method="POST")
with urllib.request.urlopen(request, timeout=240) as response:
    routed = json.load(response)
result["responding_agent"] = routed.get("responding_agent")
result["routed_layer_kinds"] = [item.get("kind") for item in routed.get("requested_result_layers") or []]
result["routed_answer"] = routed.get("answer")
result["routed_tools"] = [item.get("tool") for item in routed.get("investigation_steps") or []]
print(json.dumps(result, ensure_ascii=False))
assert result["responding_agent"] == "talia"
assert "assessments" in result["routed_layer_kinds"]
'''


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True, type=Path)
    parser.add_argument("--repair-profile-key", action="store_true")
    args = parser.parse_args()
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(HOST, username=USER, key_filename=str(args.key.resolve()), look_for_keys=False, allow_agent=False, timeout=15)
    try:
        if args.repair_profile_key:
            repair = r'''
import json
from pathlib import Path
import yaml
config = json.loads(Path("/opt/serbia-poc-ui/.hermes-api.json").read_text())
key = config["agents"]["talia"]["api_key"]
path = Path("/home/ubuntu/.hermes/profiles/talia/.env")
lines = [line for line in (path.read_text().splitlines() if path.exists() else []) if not line.startswith("API_SERVER_KEY=") and line != "HERMES_PARALLEL_TOOL_CALLS=false"]
path.write_text("\n".join(lines + [f"API_SERVER_KEY={key}", "HERMES_PARALLEL_TOOL_CALLS=false"]) + "\n")
path.chmod(0o600)
default_path = Path("/home/ubuntu/.hermes/config.yaml")
profile_path = Path("/home/ubuntu/.hermes/profiles/talia/config.yaml")
default = yaml.safe_load(default_path.read_text()) or {}
profile = yaml.safe_load(profile_path.read_text()) or {}
talia_server = (profile.get("mcp_servers") or {})["serbia-events-poc-talia"]
default.setdefault("mcp_servers", {})["serbia-events-poc-talia"] = talia_server
gateway = default.setdefault("gateway", {})
gateway["multiplex_profiles"] = True
allowlist = list(gateway.get("multiplex_profile_allowlist") or [])
if "talia" not in allowlist:
    allowlist.append("talia")
gateway["multiplex_profile_allowlist"] = allowlist
temporary = default_path.with_suffix(".yaml.talia-tmp")
temporary.write_text(yaml.safe_dump(default, allow_unicode=True, sort_keys=False))
temporary.replace(default_path)
'''
            _, repair_stdout, repair_stderr = client.exec_command("python3 - <<'PY'\n" + repair + "\nPY\nsudo -n systemctl restart hermes-gateway.service", timeout=90)
            repair_code = repair_stdout.channel.recv_exit_status()
            if repair_code:
                raise RuntimeError(repair_stderr.read().decode("utf-8", errors="replace"))
            time.sleep(8)
        command = "python3 - <<'PY'\n" + REMOTE_CHECK + "\nPY"
        _, stdout, stderr = client.exec_command(command, timeout=120)
        code = stdout.channel.recv_exit_status()
        output = stdout.read().decode("utf-8", errors="replace").strip()
        error = stderr.read().decode("utf-8", errors="replace").strip()
    finally:
        client.close()
    if code:
        raise RuntimeError("\n".join(value for value in (error, output) if value))
    print(json.dumps(json.loads(output), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

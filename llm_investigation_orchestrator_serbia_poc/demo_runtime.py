"""Validated scenario identity shared by the UI, MCP and activation operator."""
from __future__ import annotations

import hashlib
import json
import os
import re
import uuid
from pathlib import Path


def load_profile(root: Path, name: str, verify: bool = False) -> dict:
    if not re.fullmatch(r"[a-z][a-z0-9-]{0,40}", name):
        raise ValueError("Invalid demo scenario")
    profile = json.loads((root / "demo_profiles" / f"{name}.json").read_text(encoding="utf-8"))
    if profile.get("schema_version") != 1 or profile.get("state_schema_version") != 1:
        raise ValueError("Unsupported scenario or state schema")
    if profile.get("scenario_id") != name:
        raise ValueError("Scenario identity mismatch")
    for relative in [*profile["files"].values(), *profile["checksums"]]:
        path = (root / relative).resolve()
        if not path.is_relative_to(root.resolve()) or not path.is_file():
            raise ValueError(f"Missing or unsafe scenario asset: {relative}")
        if verify and relative in profile["checksums"]:
            if hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest() != profile["checksums"][relative]:
                raise ValueError(f"Scenario checksum mismatch: {relative}")
    return profile


class DemoRuntime:
    def __init__(self, root: Path):
        self.root = root
        self.enabled = bool(os.environ.get("INTELLIGENCE_POC_SCENARIO"))
        self.profile = load_profile(root, os.environ.get("INTELLIGENCE_POC_SCENARIO", "kosovo")) if self.enabled else None
        self.scenario = self.profile["scenario_id"] if self.profile else "kosovo"
        self.dataset = self.profile["dataset_version"] if self.profile else os.environ.get("INTELLIGENCE_POC_DATASET_VERSION", "v2")
        self.generation = os.environ.get("INTELLIGENCE_POC_ACTIVATION", "") or uuid.uuid4().hex
        self.state = Path(os.environ.get("INTELLIGENCE_POC_STATE_ROOT", str(root / ".demo-state"))) / self.scenario / self.dataset
        self.control = Path(os.environ.get("INTELLIGENCE_POC_CONTROL_ROOT", str(root / ".demo-control")))

    @property
    def identity(self):
        return {"scenario_id": self.scenario, "dataset_version": self.dataset, "activation_generation": self.generation}

    @property
    def maintenance(self):
        return self.enabled and (self.control / "maintenance.json").exists()

    def bind_mcp_environment(self):
        """Set before importing stores; profile selection overrides legacy env paths."""
        if not self.enabled:
            return
        for key, kind in [("DATA", "events"), ("LOCATIONS", "locations"), ("ENTITIES", "entities")]:
            os.environ[f"INTELLIGENCE_POC_{key}"] = str(self.root / self.profile["files"][kind])
        for key, relative in {
            "SEMANTIC_INDEX": "semantic_index", "EVIDENCE_STORE": "evidence/evidence.db",
            "TARGET_BANK": "attack_targets/attack_targets.db", "TARGET_BACKUPS": "backups/attack_targets",
            "ASSESSMENT_STORE": "assessments/assessments.db", "PLAYBACK_VISIBILITY": "scenario_runs/active_visibility.json",
            "EVIDENCE_CATALOG": "evidence_catalog/he.json",
        }.items():
            os.environ[f"INTELLIGENCE_POC_{key}"] = str(self.state / relative)
        os.environ["INTELLIGENCE_POC_DATASET_VERSION"] = self.dataset
        os.environ.setdefault("INTELLIGENCE_POC_AUDIT", str(self.state / "audit" / "openai_general.jsonl"))


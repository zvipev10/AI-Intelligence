"""One-time, stopped-service migration. Run as ubuntu using Hermes venv Python.

This copies existing Kosovo state, never deletes it. Syria receives configuration
and credentials only: no memories, sessions, cron jobs, or learned state.
"""
import hashlib
import json
import os
import shutil
import sqlite3
import subprocess
import uuid
from pathlib import Path

import yaml

from activate_demo import Activator, atomic_json
from demo_runtime import load_profile


def copy_checked(source, target):
    if not source.exists():
        return []
    if target.exists():
        raise ValueError(f"Migration destination already exists: {target}")
    if source.is_file() and source.suffix == ".db":
        target.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(f"file:{source}?mode=ro", uri=True) as origin:
            with sqlite3.connect(target) as destination:
                origin.backup(destination)
                if destination.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
                    raise ValueError(f"Database backup failed: {source}")
        return [{"source": str(source), "target": str(target), "sqlite_backup": True, "sha256": hashlib.sha256(target.read_bytes()).hexdigest()}]
    if source.is_dir():
        shutil.copytree(source, target)
        files = [p for p in source.rglob("*") if p.is_file()]
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        files = [source]
    report = []
    for path in files:
        destination = target / path.relative_to(source) if source.is_dir() else target
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if hashlib.sha256(destination.read_bytes()).hexdigest() != digest:
            raise ValueError(f"Migration verification failed: {path}")
        report.append({"source": str(path), "target": str(destination), "sha256": digest})
    return report


def main():
    app = Path("/opt/serbia-poc-ui")
    mcp = Path("/opt/serbia-poc")
    root = Path("/opt/demo-runtime")
    home = Path("/home/ubuntu/.hermes")
    for unit in ["serbia-poc-ui", "hermes-gateway"]:
        if subprocess.run(["systemctl", "is-active", "--quiet", unit]).returncode == 0:
            raise RuntimeError(f"Stop {unit} before migration")
    if (root / "control/current.json").exists():
        raise RuntimeError("Already provisioned; use activate_demo.py")
    report = []
    for scenario in ["kosovo", "syria"]:
        profile = load_profile(app, scenario, verify=True)
        load_profile(mcp, scenario, verify=True)
        state = root / "state" / scenario / profile["dataset_version"]
        state.mkdir(parents=True, exist_ok=True)
        if scenario == "kosovo":
            for name in ["investigations", "saved_questions", "recorded_runs", "recorded_runs_en", "performance_logs", "scenario_runs"]:
                report += copy_checked(app / name / "v2.1", state / name)
            report += copy_checked(app / "workstreams", state / "workstreams")
            report += copy_checked(app / "data/evidence_catalog/v2.1", state / "evidence_catalog")
            for name in ["attack_targets", "evidence", "assessments"]:
                report += copy_checked(mcp / "data" / name, state / name)
            report += copy_checked(mcp / "data/semantic_index/v2.1", state / "semantic_index")
        atomic_json(state / "state.json", {"schema_version": 1, "scenario_id": scenario, "dataset_version": profile["dataset_version"]})
        for role in ["general", "moshe", "talia"]:
            source = home if role == "general" else home / "profiles" / role
            target = root / "hermes-homes" / scenario / role
            target.mkdir(parents=True, mode=0o700, exist_ok=True)
            for name in [".env", "auth.json", "SOUL.md", "skills"]:
                report += copy_checked(source / name, target / name)
            if scenario == "kosovo":
                for name in ["memories", "sessions", "state", "state.db", "response_store.db"]:
                    report += copy_checked(source / name, target / name)
            config = yaml.safe_load((source / "config.yaml").read_text())
            # Only the API route is enabled for demo profiles; root integrations stay intact.
            config["platforms"] = {key: {**value, "enabled": key == "api_server"} for key, value in config.get("platforms", {}).items() if isinstance(value, dict)}
            config.setdefault("gateway", {})["multiplex_profiles"] = False
            config["gateway"]["multiplex_profile_allowlist"] = []
            selected = "serbia-events-poc" + ("" if role == "general" else "-" + role)
            server = config["mcp_servers"][selected]
            server["env"] = {
                "INTELLIGENCE_POC_SCENARIO": scenario,
                "INTELLIGENCE_POC_STATE_ROOT": str(root / "state"),
                "INTELLIGENCE_POC_CONTROL_ROOT": str(root / "control"),
                "INTELLIGENCE_POC_AUDIT": str(state / "audit" / (role + ".jsonl")),
            }
            config["mcp_servers"] = {selected: server}
            (target / "config.yaml").write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False))
            (target / "config.yaml").chmod(0o600)
            # Shared roles remain versioned; scenario grounding is supplied by UI instructions.
    config = yaml.safe_load((home / "config.yaml").read_text())
    config.setdefault("gateway", {})["multiplex_profiles"] = True
    config["gateway"]["multiplex_profile_allowlist"] = ["demo-general", "demo-moshe", "demo-talia"]
    # Demo tools belong only to active named roles. Keeping legacy root bindings
    # would expose inactive Kosovo data and duplicate resident MCP data stores.
    config["mcp_servers"] = {key: value for key, value in config.get("mcp_servers", {}).items() if not key.startswith("serbia-events-poc")}
    (home / "config.yaml").write_text(yaml.safe_dump(config, allow_unicode=True, sort_keys=False))
    api_path = app / ".hermes-api.json"
    api = json.loads(api_path.read_text())
    for role in ["general", "moshe", "talia"]:
        settings = api.setdefault("agents", {}).setdefault(role, {})
        settings["api_path_prefix"] = "/p/demo-" + role
        # Paths selected at runtime; server load_agent_hermes_config supplies audit namespace.
    atomic_json(api_path, api)
    api_path.chmod(0o600)
    identity = {"scenario_id": "kosovo", "dataset_version": "v2.1", "activation_generation": uuid.uuid4().hex}
    Activator().select(identity)
    atomic_json(root / "control/current.json", identity)
    atomic_json(root / "control/migration-report.json", {"schema_version": 1, "files": report})
    print(json.dumps({"migrated_files": len(report), "identity": identity}))


if __name__ == "__main__":
    main()

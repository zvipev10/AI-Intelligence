#!/usr/bin/env python3
"""Linux operator: one installed release, one active scenario, preserved state.

Run with the Hermes venv Python as the service user (sudo systemctl permitted).
Never edits datasets or credentials. Provision profiles before first activation.
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import time
import uuid
from pathlib import Path
from urllib.request import urlopen

from demo_runtime import load_profile


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(".tmp")
    with temp.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2)
        handle.flush()
        os.fsync(handle.fileno())
    os.replace(temp, path)


class Activator:
    def __init__(self, app=Path("/opt/serbia-poc-ui"), root=Path("/opt/demo-runtime")):
        self.app, self.root = app, root
        self.control = root / "control"
        self.current = self.control / "current.json"
        self.journal = self.control / "transition.json"

    def services(self, action):
        # Stop the UI first to prevent admission, then the single gateway/MCP tree.
        units = ["serbia-poc-ui", "hermes-gateway"]
        if action == "start":
            units.reverse()
        for unit in units:
            subprocess.run(["sudo", "systemctl", action, unit], check=True, timeout=90)
        if action == "stop":
            for unit in units:
                result = subprocess.run(["systemctl", "is-active", unit], capture_output=True)
                if result.returncode == 0:
                    raise RuntimeError(f"Old service still active: {unit}")

    def select(self, identity):
        scenario = identity["scenario_id"]
        load_profile(self.app, scenario, verify=True)
        state = self.root / "state" / scenario / identity["dataset_version"]
        metadata = json.loads((state / "state.json").read_text())
        if metadata != {"schema_version": 1, "scenario_id": scenario, "dataset_version": identity["dataset_version"]}:
            raise ValueError("Incompatible persistent state")
        # Named aliases only change with all demo workers stopped.
        profiles = Path("/home/ubuntu/.hermes/profiles")
        for role in ["general", "moshe", "talia"]:
            home = self.root / "hermes-homes" / scenario / role
            if not (home / "config.yaml").is_file():
                raise ValueError(f"Missing agent home: {scenario}/{role}")
            alias = profiles / f"demo-{role}"
            if alias.exists() and not alias.is_symlink():
                raise ValueError(f"Refusing to replace non-symlink profile: {alias}")
            pending = alias.with_name(alias.name + ".next")
            pending.unlink(missing_ok=True)
            pending.symlink_to(home, target_is_directory=True)
            os.replace(pending, alias)
        environment = {
            "INTELLIGENCE_POC_SCENARIO": scenario,
            "INTELLIGENCE_POC_DATASET_VERSION": identity["dataset_version"],
            "INTELLIGENCE_POC_ACTIVATION": identity["activation_generation"],
            "INTELLIGENCE_POC_STATE_ROOT": str(self.root / "state"),
            "INTELLIGENCE_POC_CONTROL_ROOT": str(self.control),
        }
        temp = self.root / "active.env.next"
        temp.write_text("".join(f"{key}={value}\n" for key, value in environment.items()))
        os.replace(temp, self.root / "active.env")
        atomic_json(self.control / "selected.json", identity)
        # Gateway profile MCP env must carry the same generation, not its predecessor.
        import yaml
        root_config_path = Path("/home/ubuntu/.hermes/config.yaml")
        root_config = yaml.safe_load(root_config_path.read_text())
        root_servers = root_config.setdefault("mcp_servers", {})
        for role in ["general", "moshe", "talia"]:
            config = self.root / "hermes-homes" / scenario / role / "config.yaml"
            content = yaml.safe_load(config.read_text())
            for name, server in content.get("mcp_servers", {}).items():
                server.setdefault("env", {}).update(environment)
                # Installed Hermes registers named-profile toolsets from the
                # gateway root registry. Every definition points at the active
                # scenario; keeping only profile copies yields no callable tools.
                root_servers[name] = server
            temp = config.with_suffix(".next")
            temp.write_text(yaml.safe_dump(content, allow_unicode=True, sort_keys=False))
            temp.chmod(0o600)
            os.replace(temp, config)
        temporary_root_config = root_config_path.with_suffix(".demo-next")
        temporary_root_config.write_text(yaml.safe_dump(root_config, allow_unicode=True, sort_keys=False))
        temporary_root_config.chmod(0o600)
        os.replace(temporary_root_config, root_config_path)

    def health(self, identity, timeout=90):
        deadline = time.monotonic() + timeout
        last = None
        while time.monotonic() < deadline:
            try:
                with urlopen("http://127.0.0.1:8769/api/status", timeout=5) as response:
                    status = json.load(response)
                if any(status.get(k) != v for k, v in identity.items() if k in {"scenario_id", "dataset_version", "activation_generation"}):
                    raise RuntimeError("Runtime identity mismatch")
                with urlopen("http://127.0.0.1:8769/api/layers?locale=en", timeout=10) as response:
                    layers = json.load(response)["layers"]
                if not layers or (identity["scenario_id"] == "syria" and any(layer["count"] for layer in layers)):
                    raise RuntimeError("Scenario catalog readiness failed")
                # Gateway readiness is required even when the target has no data.
                with urlopen("http://127.0.0.1:8642/health", timeout=5) as response:
                    if response.status != 200:
                        raise RuntimeError("Gateway not ready")
                import yaml
                for role in ["general", "moshe", "talia"]:
                    config = yaml.safe_load((self.root / "hermes-homes" / identity["scenario_id"] / role / "config.yaml").read_text())
                    for tool in config["mcp_servers"].values():
                        query = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call", "params": {"name": "demo_runtime_status", "arguments": {}}}) + "\n"
                        result = subprocess.run([tool["command"], *tool["args"]], input=query, text=True, capture_output=True, env={**os.environ, **tool["env"]}, timeout=20, check=True)
                        tool_status = json.loads(result.stdout.strip())["result"]["structuredContent"]
                        if any(tool_status.get(key) != value for key, value in identity.items()):
                            raise RuntimeError(f"Tool identity mismatch for {role}")
                        if tool_status["event_count"] != status["dataset_rows"]:
                            raise RuntimeError(f"Tool dataset mismatch for {role}")
                return status
            except Exception as exc:
                last = exc
                time.sleep(1)
        raise RuntimeError(f"Readiness failed: {last}")

    def drain(self, timeout):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            with urlopen("http://127.0.0.1:8769/api/status", timeout=5) as response:
                status = json.load(response)
            queue = status.get("agent_queue")
            if queue is not None and queue["running"] == 0 and queue["queued"] == 0 and status.get("background_workers", 0) == 0:
                return
            time.sleep(.5)
        raise RuntimeError("Drain timed out; current scenario retained")

    def activate(self, scenario, timeout=120):
        import fcntl
        self.control.mkdir(parents=True, exist_ok=True)
        with (self.control / "activation.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            profile = load_profile(self.app, scenario, verify=True)
            load_profile(Path("/opt/serbia-poc"), scenario, verify=True)
            if shutil.disk_usage(self.root).free < 512 * 1024 * 1024:
                raise RuntimeError("Less than 512 MiB free; activation aborted")
            previous = json.loads(self.current.read_text())
            target = {"scenario_id": scenario, "dataset_version": profile["dataset_version"], "activation_generation": uuid.uuid4().hex}
            atomic_json(self.journal, {"phase": "draining", "previous": previous, "target": target})
            atomic_json(self.control / "maintenance.json", {"target": scenario})
            try:
                self.drain(timeout)
            except Exception:
                self.journal.unlink(missing_ok=True)
                (self.control / "maintenance.json").unlink(missing_ok=True)
                raise
            try:
                atomic_json(self.journal, {"phase": "stopping", "previous": previous, "target": target})
                self.services("stop")
                self.select(target)
                atomic_json(self.journal, {"phase": "starting", "previous": previous, "target": target})
                self.services("start")
                status = self.health(target)
                atomic_json(self.current, target)
                self.journal.unlink(missing_ok=True)
                (self.control / "maintenance.json").unlink(missing_ok=True)
                return status
            except Exception:
                self.services("stop")
                previous["activation_generation"] = uuid.uuid4().hex
                self.select(previous)
                self.services("start")
                self.health(previous)
                atomic_json(self.current, previous)
                self.journal.unlink(missing_ok=True)
                (self.control / "maintenance.json").unlink(missing_ok=True)
                raise

    def recover_before_start(self):
        """Boot-only recovery runs before UI/gateway; never starts overlapping workers."""
        if self.journal.exists():
            journal = json.loads(self.journal.read_text())
            previous = journal["previous"]
            previous["activation_generation"] = uuid.uuid4().hex
            self.select(previous)
            atomic_json(self.current, previous)
            # Keep maintenance until operator health verification clears it.
            atomic_json(self.journal, {**journal, "phase": "recovered-awaiting-health"})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("scenario", nargs="?", choices=["kosovo", "syria"])
    parser.add_argument("--drain-timeout", type=int, default=120)
    parser.add_argument("--recover-before-start", action="store_true")
    args = parser.parse_args()
    operator = Activator()
    if args.recover_before_start:
        operator.recover_before_start()
    elif args.scenario:
        print(json.dumps(operator.activate(args.scenario, args.drain_timeout), indent=2))
    else:
        parser.error("Supply a scenario or --recover-before-start")


if __name__ == "__main__":
    main()

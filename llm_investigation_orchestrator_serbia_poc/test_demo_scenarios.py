import json
import os
import socket
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch
from types import SimpleNamespace

from demo_admission import AgentAdmission, AdmissionError
from demo_runtime import DemoRuntime, load_profile
from activate_demo import Activator

ROOT = Path(__file__).resolve().parent


class Profiles(unittest.TestCase):
    def test_activation_rejects_missing_or_modified_search_cache(self):
        import hashlib
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            operator = Activator(ROOT, root)
            profile = load_profile(ROOT, "kosovo")
            with self.assertRaisesRegex(RuntimeError, "offline search cache"):
                operator.verify_search_cache(profile)
            cache = root / "state/kosovo/v2.1/semantic_index/semantic_event_index_hybrid_embedding.pkl"
            cache.parent.mkdir(parents=True)
            cache.write_bytes(b"trusted-test-cache")
            manifest = {}
            for label in ["events", "locations", "entities"]:
                data = (ROOT / profile["files"][label]).read_bytes()
                manifest[label + "_sha256"] = hashlib.sha256(data).hexdigest()
                manifest[label + "_size"] = len(data)
            cache.with_suffix(".json").write_text(json.dumps({"manifest": manifest, "sha256": hashlib.sha256(cache.read_bytes()).hexdigest()}))
            operator.verify_search_cache(profile)
            cache.write_bytes(b"changed")
            with self.assertRaises(RuntimeError):
                operator.verify_search_cache(profile)

    def test_search_never_builds_on_demo_cache_miss(self):
        from mcp_server.semantic_index import SemanticEventIndex
        with tempfile.TemporaryDirectory() as directory:
            records = [{"event_id": "1", "event_summary": "reported movements"}]
            with patch.object(SemanticEventIndex, "_build", side_effect=AssertionError("must not build")):
                with self.assertRaisesRegex(RuntimeError, "Build with build_demo_index"):
                    SemanticEventIndex(records, directory, require_prebuilt=True)
            SemanticEventIndex(records, directory, signature={"dataset": "one"})
            with patch.object(SemanticEventIndex, "_build", side_effect=AssertionError("must not build")):
                cached = SemanticEventIndex(records, directory, signature={"dataset": "one"}, require_prebuilt=True)
                self.assertEqual(len(cached.search("movements", {}, 1)), 1)
                with self.assertRaises(RuntimeError):
                    SemanticEventIndex(records, directory, signature={"dataset": "two"}, require_prebuilt=True)

    def test_packages_and_state_isolation(self):
        for scenario in ["kosovo", "syria"]:
            load_profile(ROOT, scenario, verify=True)
        with patch.dict(os.environ, {"INTELLIGENCE_POC_SCENARIO": "kosovo"}):
            kosovo = DemoRuntime(ROOT)
        with patch.dict(os.environ, {"INTELLIGENCE_POC_SCENARIO": "syria"}):
            syria = DemoRuntime(ROOT)
        self.assertNotEqual(kosovo.state, syria.state)
        self.assertEqual(kosovo.profile["sources"]["en"], syria.profile["sources"]["en"][:-5])
        self.assertNotEqual(kosovo.generation, syria.generation)

    def test_invalid_selection_never_falls_back(self):
        for scenario in ["../kosovo", "uninstalled"]:
            with self.assertRaises((ValueError, FileNotFoundError)):
                load_profile(ROOT, scenario)

    def test_syria_mcp_has_no_kosovo_records(self):
        result = subprocess.run([sys.executable, "-c", "import mcp_server.server as s; assert len(s.EVENTS)==444; assert len(s.LOCATIONS)==102; assert all(e['event_id'].startswith('REC-SYR-') for e in s.EVENTS)"], cwd=ROOT, env={**os.environ, "INTELLIGENCE_POC_SCENARIO": "syria"}, capture_output=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr.decode())


class Admission(unittest.TestCase):
    def test_serial_and_reentrant(self):
        gate = AgentAdmission()
        active = []
        peaks = []
        def run():
            with gate.slot():
                with gate.slot():
                    active.append(1)
                    peaks.append(len(active))
                    time.sleep(.01)
                    active.pop()
        threads = [threading.Thread(target=run) for _ in range(5)]
        for thread in threads: thread.start()
        for thread in threads: thread.join()
        self.assertEqual(max(peaks), 1)
        self.assertEqual(gate.status()["queued"], 0)

    def test_drain_cancels_pending_not_running(self):
        maintenance = [False]
        gate = AgentAdmission(lambda: maintenance[0])
        failures = []
        def pending():
            try:
                with gate.slot(): failures.append("unexpected execution")
            except AdmissionError:
                failures.append("cancelled")
        with gate.slot():
            thread = threading.Thread(target=pending)
            thread.start()
            while not gate.status()["queued"]: time.sleep(.001)
            maintenance[0] = True
            thread.join(timeout=2)
            self.assertEqual(gate.status()["running"], 1)
        self.assertEqual(failures, ["cancelled"])


class SyriaHTTP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.directory = tempfile.TemporaryDirectory()
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]
        cls.url = f"http://127.0.0.1:{port}"
        cls.process = subprocess.Popen([sys.executable, "server.py", str(port)], cwd=ROOT, env={**os.environ, "POC_UI_HOST":"127.0.0.1", "INTELLIGENCE_POC_SCENARIO":"syria", "INTELLIGENCE_POC_STATE_ROOT":cls.directory.name, "INTELLIGENCE_POC_ACTIVATION":"test-generation"}, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(100):
            try:
                with urlopen(cls.url + "/api/status", timeout=1): break
            except OSError: time.sleep(.1)
        else: raise RuntimeError("test server did not start")

    @classmethod
    def tearDownClass(cls):
        cls.process.terminate(); cls.process.wait(timeout=10); cls.directory.cleanup()

    def test_syria_layer_catalog_and_map(self):
        with urlopen(self.url + "/api/status") as response: status = json.load(response)
        self.assertEqual(status["scenario_id"], "syria")
        self.assertEqual(status["dataset_rows"], 444)
        self.assertEqual(status["demo_profile"]["map"]["center"], [36.2765, 33.5138])
        self.assertEqual(status["demo_profile"]["map"]["zoom"], 11)
        for locale in ["en", "he"]:
            with urlopen(self.url + "/api/layers?locale=" + locale) as response: layers = json.load(response)["layers"]
            self.assertEqual(len(layers), 21)
            self.assertEqual({layer["id"]: layer["count"] for layer in layers if layer["id"] in {"events:CCTV", "events:Satellite"}}, {"events:CCTV": 2, "events:Satellite": 2})
        with urlopen(self.url + "/api/investigations") as response: self.assertEqual(json.load(response)["investigations"], [])

    def test_stale_write_and_read_rejected(self):
        for method in ["GET", "POST", "PUT", "DELETE"]:
            request = Request(self.url + "/api/investigations", headers={"X-Demo-Generation":"old-generation"}, method=method)
            with self.assertRaises(HTTPError) as error: urlopen(request)
            self.assertEqual(error.exception.code, 409)

    def test_inactive_data_and_secrets_not_served(self):
        for path in ["/.hermes-api.json", "/data/serbian_intelligence_v2_1/serbia_kosovo_events_projection_v2_1.csv", "/investigations/"]:
            with self.assertRaises(HTTPError) as error: urlopen(self.url + path)
            self.assertEqual(error.exception.code, 404)


class Activation(unittest.TestCase):
    def test_crash_recovery_keeps_maintenance_until_verified(self):
        with tempfile.TemporaryDirectory() as directory:
            operator = Activator(ROOT, Path(directory)); operator.control.mkdir()
            previous = {"scenario_id":"kosovo", "dataset_version":"v2.1", "activation_generation":"old"}
            operator.current.write_text(json.dumps(previous))
            operator.journal.write_text(json.dumps({"previous":previous, "phase":"starting", "target":{"scenario_id":"syria"}}))
            (operator.control / "maintenance.json").write_text("{}")
            selected = []
            operator.select = lambda identity: selected.append(dict(identity))
            operator.recover_before_start()
            self.assertEqual(selected[0]["scenario_id"], "kosovo")
            self.assertNotEqual(selected[0]["activation_generation"], "old")
            self.assertTrue((operator.control / "maintenance.json").exists())
            self.assertEqual(json.loads(operator.journal.read_text())["phase"], "recovered-awaiting-health")

    def test_failed_target_restores_previous_with_new_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            operator = Activator(ROOT, Path(directory))
            operator.control.mkdir()
            previous = {"scenario_id":"kosovo", "dataset_version":"v2.1", "activation_generation":"original"}
            operator.current.write_text(json.dumps(previous))
            actions = []
            operator.services = lambda action: actions.append(action)
            operator.select = lambda identity: actions.append(identity["scenario_id"])
            operator.drain = lambda timeout: None
            def health(identity):
                if identity["scenario_id"] == "syria": raise RuntimeError("simulated startup failure")
                return identity
            operator.health = health
            stub = SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *args: None)
            with patch.dict(sys.modules, {"fcntl":stub}), patch("activate_demo.load_profile", return_value={"dataset_version":"empty-v1", "empty_dataset":True}):
                with self.assertRaisesRegex(RuntimeError, "simulated startup"):
                    operator.activate("syria")
            self.assertEqual(actions, ["stop", "syria", "start", "stop", "kosovo", "start"])
            restored = json.loads(operator.current.read_text())
            self.assertEqual(restored["scenario_id"], "kosovo")
            self.assertNotEqual(restored["activation_generation"], "original")
            self.assertFalse((operator.control / "maintenance.json").exists())

    def test_drain_failure_never_stops_current(self):
        with tempfile.TemporaryDirectory() as directory:
            operator = Activator(ROOT, Path(directory)); operator.control.mkdir()
            operator.current.write_text(json.dumps({"scenario_id":"kosovo"}))
            actions = []
            operator.services = lambda action: actions.append(action)
            operator.drain = lambda timeout: (_ for _ in ()).throw(RuntimeError("busy"))
            stub = SimpleNamespace(LOCK_EX=1, LOCK_NB=2, flock=lambda *args: None)
            with patch.dict(sys.modules, {"fcntl":stub}), patch("activate_demo.load_profile", return_value={"dataset_version":"empty-v1", "empty_dataset":True}):
                with self.assertRaisesRegex(RuntimeError, "busy"): operator.activate("syria")
            self.assertEqual(actions, [])
            self.assertFalse((operator.control / "maintenance.json").exists())


if __name__ == "__main__":
    unittest.main()

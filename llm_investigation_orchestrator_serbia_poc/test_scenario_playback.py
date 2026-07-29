import json
import tempfile
import threading
import unittest
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch

import scenario_playback
import server


class ScenarioPlaybackApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = tempfile.TemporaryDirectory()
        root = Path(self.temp_root.name)
        self.manifests_dir = root / "manifests"
        self.runs_dir = root / "runs"
        self.workstreams_dir = root / "workstreams"
        self.manifests_dir.mkdir()
        self.write_manifest({
            "scenario_id": "timeframe-demo",
            "version": 1,
            "title": "Timeframe demo",
            "playback_label": "Historical simulation",
            "scope": {"dataset": "v2.1", "layers": []},
            "stages": [
                {
                    "id": "stage-1",
                    "label": "First window",
                    "from": "2026-09-17T02:00:00Z",
                    "to": "2026-09-17T06:00:00Z",
                },
                {
                    "id": "stage-2",
                    "label": "Second window",
                    "from": "2026-09-17T06:00:00Z",
                    "to": "2026-09-17T09:00:00Z",
                },
                {
                    "id": "stage-3",
                    "label": "Third window",
                    "from": "2026-09-17T09:00:00Z",
                    "to": "2026-09-17T10:00:00Z",
                },
            ],
        })
        self.write_manifest({
            "scenario_id": "filtered-demo",
            "version": 2,
            "title": "Filtered demo",
            "scope": {"dataset": "alternate", "layers": ["events:reports"]},
            "stages": [{
                "id": "only-stage",
                "from": "2026-01-01T00:00:00+00:00",
                "to": "2026-01-02T00:00:00+00:00",
            }],
        })
        self.patches = [
            patch.object(server, "SCENARIO_MANIFESTS_DIR", self.manifests_dir),
            patch.object(server, "SCENARIO_RUNS_DIR", self.runs_dir),
            patch.object(server, "WORKSTREAMS_DIR", self.workstreams_dir),
            patch.object(server, "DATASET_VERSION", "v2.1"),
        ]
        for item in self.patches:
            item.start()
        self.httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.httpd.server_port}"
        status, self.workstream = self.request("POST", "/api/workstreams", {
            "investigation_id": "investigation-playback",
            "title": "Playback validation",
            "objective": "Validate generic playback state.",
            "participants": [],
            "assignments": [],
        })
        self.assertEqual(201, status)

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)
        for item in reversed(self.patches):
            item.stop()
        self.temp_root.cleanup()

    def write_manifest(self, payload):
        path = self.manifests_dir / f"{payload['scenario_id']}-v{payload['version']}.json"
        path.write_text(json.dumps(payload), encoding="utf-8")

    def request(self, method, path, payload=None):
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            self.base_url + path,
            data=body,
            method=method,
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        try:
            with urlopen(request, timeout=5) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8"))

    def start_payload(self, key="start-1"):
        return {
            "scenario_id": "timeframe-demo",
            "version": 1,
            "workstream_id": self.workstream["workstream_id"],
            "investigation_id": "investigation-playback",
            "idempotency_key": key,
        }

    def start(self):
        status, run = self.request("POST", "/api/scenario-runs", self.start_payload())
        self.assertEqual(201, status)
        return run

    def test_lists_two_structurally_distinct_manifests_without_future_stages(self):
        status, listing = self.request("GET", "/api/scenarios")
        self.assertEqual(200, status)
        self.assertEqual(2, len(listing["scenarios"]))
        by_id = {item["scenario_id"]: item for item in listing["scenarios"]}
        self.assertEqual(3, by_id["timeframe-demo"]["stage_count"])
        self.assertEqual(["events:reports"], by_id["filtered-demo"]["scope"]["layers"])
        self.assertNotIn("stages", by_id["timeframe-demo"])

        status, details = self.request("GET", "/api/scenarios/timeframe-demo?version=1")
        self.assertEqual(200, status)
        self.assertEqual(3, details["stage_count"])
        self.assertNotIn("stages", details)

    def test_start_reopen_and_persist_initial_stage(self):
        run = self.start()
        self.assertRegex(run["run_id"], r"^run_")
        self.assertEqual("active", run["status"])
        self.assertEqual(1, run["revision"])
        self.assertEqual("stage-1", run["current_stage"]["id"])
        self.assertEqual("2026-09-17T02:00:00Z", run["visible_timeframe"]["from"])
        self.assertEqual("2026-09-17T06:00:00Z", run["visible_timeframe"]["to"])
        self.assertNotIn("_idempotency", run)

        status, reopened = self.request("GET", f"/api/scenario-runs/{run['run_id']}")
        self.assertEqual(200, status)
        self.assertEqual(run["run_id"], reopened["run_id"])

        status, same = self.request("POST", "/api/scenario-runs", self.start_payload("start-2"))
        self.assertEqual(200, status)
        self.assertEqual(run["run_id"], same["run_id"])
        self.assertEqual(1, len(list(self.runs_dir.glob("run_*.json"))))
        self.assertFalse(next(self.runs_dir.glob("run_*.json")).with_suffix(".json.tmp").exists())

    def test_advance_is_ordered_cumulative_and_idempotent(self):
        run = self.start()
        transition = {"expected_revision": 1, "idempotency_key": "advance-1"}
        status, advanced = self.request(
            "POST", f"/api/scenario-runs/{run['run_id']}/advance", transition
        )
        self.assertEqual(200, status)
        self.assertFalse(advanced["idempotent_replay"])
        self.assertEqual("stage-2", advanced["current_stage"]["id"])
        self.assertEqual(2, advanced["revision"])
        self.assertEqual("2026-09-17T02:00:00Z", advanced["visible_timeframe"]["from"])
        self.assertEqual("2026-09-17T09:00:00Z", advanced["visible_timeframe"]["to"])

        status, replayed = self.request(
            "POST", f"/api/scenario-runs/{run['run_id']}/advance", transition
        )
        self.assertEqual(200, status)
        self.assertTrue(replayed["idempotent_replay"])
        self.assertEqual("stage-2", replayed["current_stage"]["id"])
        self.assertEqual(2, replayed["revision"])

        status, stale = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/advance",
            {"expected_revision": 1, "idempotency_key": "advance-stale"},
        )
        self.assertEqual(409, status)
        self.assertEqual(2, stale["current_revision"])

        status, wrong_action = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/reset",
            {"expected_revision": 2, "idempotency_key": "advance-1"},
        )
        self.assertEqual(400, status)
        self.assertEqual(
            "Idempotency key is already bound to another action",
            wrong_action["error"],
        )

    def test_concurrent_advance_applies_once(self):
        run = self.start()

        def advance(key):
            return self.request(
                "POST",
                f"/api/scenario-runs/{run['run_id']}/advance",
                {"expected_revision": 1, "idempotency_key": key},
            )

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(advance, ["concurrent-a", "concurrent-b"]))
        self.assertEqual([200, 409], sorted(status for status, _ in results))
        status, reopened = self.request("GET", f"/api/scenario-runs/{run['run_id']}")
        self.assertEqual(200, status)
        self.assertEqual(2, reopened["revision"])
        self.assertEqual("stage-2", reopened["current_stage"]["id"])
        self.assertEqual(2, len(reopened["transition_history"]))

    def test_complete_and_reset_retain_audit_history(self):
        run = self.start()
        status, completed = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/complete",
            {"expected_revision": 1, "idempotency_key": "complete-1"},
        )
        self.assertEqual(200, status)
        self.assertEqual("completed", completed["status"])
        self.assertIsNotNone(completed["completed_at_utc"])

        status, error = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/advance",
            {"expected_revision": 2, "idempotency_key": "advance-after-complete"},
        )
        self.assertEqual(400, status)
        self.assertEqual("Completed scenario run cannot advance", error["error"])

        status, reset = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/reset",
            {"expected_revision": 2, "idempotency_key": "reset-1"},
        )
        self.assertEqual(200, status)
        self.assertEqual("active", reset["status"])
        self.assertEqual("stage-1", reset["current_stage"]["id"])
        self.assertEqual(3, reset["revision"])
        self.assertEqual(["start", "complete", "reset"], [
            item["action"] for item in reset["transition_history"]
        ])

    def test_publishes_visibility_policy_and_allows_only_one_active_run(self):
        run = self.start()
        policy_path = scenario_playback.visibility_policy_path(self.runs_dir)
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        self.assertTrue(policy["active"])
        self.assertEqual(run["run_id"], policy["run_id"])
        self.assertEqual(run["visible_timeframe"], policy["visible_timeframe"])

        status, second_workstream = self.request("POST", "/api/workstreams", {
            "investigation_id": "investigation-playback",
            "title": "Second playback",
            "objective": "Must not run concurrently.",
            "participants": [],
            "assignments": [],
        })
        self.assertEqual(201, status)
        second_payload = self.start_payload("start-second")
        second_payload["workstream_id"] = second_workstream["workstream_id"]
        status, error = self.request("POST", "/api/scenario-runs", second_payload)
        self.assertEqual(409, status)
        self.assertEqual("Another scenario run is already active", error["error"])
        self.assertEqual(1, len(list(self.runs_dir.glob("run_*.json"))))

        status, completed = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/complete",
            {"expected_revision": 1, "idempotency_key": "complete-policy"},
        )
        self.assertEqual(200, status)
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        self.assertFalse(policy["active"])

        status, reset = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/reset",
            {"expected_revision": completed["revision"], "idempotency_key": "reset-policy"},
        )
        self.assertEqual(200, status)
        policy = json.loads(policy_path.read_text(encoding="utf-8"))
        self.assertTrue(policy["active"])
        self.assertEqual(reset["revision"], policy["revision"])

    def test_single_next_endpoint_starts_advances_and_triggers_moshe_once_per_stage(self):
        workstream_id = self.workstream["workstream_id"]
        status, initial = self.request(
            "GET", f"/api/workstreams/{workstream_id}/playback"
        )
        self.assertEqual(200, status)
        self.assertIsNone(initial["run"])
        self.assertEqual(
            "2026-09-17T02:00:00Z", initial["next_stage"]["timeframe"]["from"]
        )

        with patch.object(
            server,
            "run_moshe_playback_reevaluation",
            return_value={"answer": "Updated assessment", "responding_agent": "moshe"},
        ) as moshe:
            first_request = {"idempotency_key": "playback-first"}
            status, first = self.request(
                "POST",
                f"/api/workstreams/{workstream_id}/playback/next",
                first_request,
            )
            self.assertEqual(200, status)
            self.assertTrue(first["moshe_triggered"])
            self.assertEqual(1, first["run"]["revision"])
            self.assertEqual(
                "2026-09-17T06:00:00Z",
                first["run"]["next_stage"]["timeframe"]["from"],
            )

            status, replay = self.request(
                "POST",
                f"/api/workstreams/{workstream_id}/playback/next",
                first_request,
            )
            self.assertEqual(200, status)
            self.assertFalse(replay["moshe_triggered"])
            self.assertEqual(1, replay["run"]["revision"])

            status, second = self.request(
                "POST",
                f"/api/workstreams/{workstream_id}/playback/next",
                {"expected_revision": 1, "idempotency_key": "playback-second"},
            )
            self.assertEqual(200, status)
            self.assertTrue(second["moshe_triggered"])
            self.assertEqual(2, second["run"]["revision"])
            self.assertEqual(2, moshe.call_count)
            self.assertEqual(
                {
                    "from": "2026-09-17T06:00:00Z",
                    "to": "2026-09-17T09:00:00Z",
                    "from_inclusive": True,
                    "to_exclusive": True,
                },
                second["released_timeframe"],
            )

    def test_investigation_next_endpoint_releases_once_without_workstream_selection(self):
        status, initial = self.request(
            "GET", "/api/playback?investigation_id=investigation-playback"
        )
        self.assertEqual(200, status)
        self.assertIsNone(initial["run"])
        self.assertEqual("historical", initial["mode"])

        status, real_time = self.request("POST", "/api/playback/mode", {
            "investigation_id": "investigation-playback",
            "mode": "real_time",
        })
        self.assertEqual(200, status)
        self.assertEqual("real_time", real_time["mode"])
        self.assertEqual("stage-1", real_time["run"]["current_stage"]["id"])

        with patch.object(
            server,
            "run_moshe_playback_reevaluation",
            return_value={"answer": "All relevant assessments updated"},
        ) as moshe:
            request = {
                "investigation_id": "investigation-playback",
                "expected_revision": real_time["run"]["revision"],
                "idempotency_key": "investigation-first",
            }
            status, first = self.request("POST", "/api/playback/next", request)
            self.assertEqual(200, status)
            self.assertTrue(first["moshe_triggered"])
            self.assertIsNone(first["run"]["workstream_id"])
            self.assertEqual("investigation-playback", first["run"]["investigation_id"])

            status, replay = self.request("POST", "/api/playback/next", request)
            self.assertEqual(200, status)
            self.assertFalse(replay["moshe_triggered"])
            self.assertEqual(2, replay["run"]["revision"])
            self.assertEqual(1, moshe.call_count)

        status, historical = self.request("POST", "/api/playback/mode", {
            "investigation_id": "investigation-playback",
            "mode": "historical",
        })
        self.assertEqual(200, status)
        self.assertEqual("historical", historical["mode"])
        policy = scenario_playback.load_playback_visibility(self.runs_dir)
        self.assertFalse(policy["active"])

        status, resumed = self.request("POST", "/api/playback/mode", {
            "investigation_id": "investigation-playback",
            "mode": "real_time",
        })
        self.assertEqual(200, status)
        self.assertEqual(2, resumed["run"]["revision"])

    def test_investigation_next_skips_moshe_without_active_workstreams(self):
        investigation_id = "investigation-without-workstreams"
        status, real_time = self.request("POST", "/api/playback/mode", {
            "investigation_id": investigation_id,
            "mode": "real_time",
        })
        self.assertEqual(200, status)

        with patch.object(server, "run_moshe_playback_reevaluation") as moshe:
            status, result = self.request("POST", "/api/playback/next", {
                "investigation_id": investigation_id,
                "expected_revision": real_time["run"]["revision"],
                "idempotency_key": "no-workstreams",
            })

        self.assertEqual(200, status)
        self.assertFalse(result["moshe_triggered"])
        self.assertEqual("no_active_workstreams", result["moshe_skipped_reason"])
        self.assertIsNone(result["run"]["reevaluation"])
        moshe.assert_not_called()

    def test_real_time_mode_with_reset_restarts_existing_playback(self):
        investigation_id = "investigation-refresh-reset"
        status, initial = self.request("POST", "/api/playback/mode", {
            "investigation_id": investigation_id,
            "mode": "real_time",
        })
        self.assertEqual(200, status)
        status, advanced = self.request("POST", "/api/playback/next", {
            "investigation_id": investigation_id,
            "expected_revision": initial["run"]["revision"],
            "idempotency_key": "refresh-reset-advance",
        })
        self.assertEqual(200, status)
        self.assertEqual(1, advanced["run"]["current_stage_index"])

        status, restarted = self.request("POST", "/api/playback/mode", {
            "investigation_id": investigation_id,
            "mode": "real_time",
            "reset": True,
        })

        self.assertEqual(200, status)
        self.assertEqual("real_time", restarted["mode"])
        self.assertEqual(0, restarted["run"]["current_stage_index"])
        self.assertIsNotNone(restarted["run"]["next_stage"])

    def test_final_stage_requires_explicit_complete(self):
        run = self.start()
        _, second = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/advance",
            {"expected_revision": 1, "idempotency_key": "advance-1"},
        )
        _, final = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/advance",
            {"expected_revision": second["revision"], "idempotency_key": "advance-2"},
        )
        self.assertEqual("stage-3", final["current_stage"]["id"])
        self.assertEqual("active", final["status"])
        status, error = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/advance",
            {"expected_revision": final["revision"], "idempotency_key": "advance-3"},
        )
        self.assertEqual(400, status)
        self.assertEqual("Scenario run is already at the final stage", error["error"])

    def test_rejects_cross_investigation_and_invalid_transition_inputs(self):
        invalid = self.start_payload()
        invalid["investigation_id"] = "another-investigation"
        status, error = self.request("POST", "/api/scenario-runs", invalid)
        self.assertEqual(404, status)
        self.assertEqual("Workstream not found for investigation", error["error"])

        run = self.start()
        status, error = self.request(
            "POST",
            f"/api/scenario-runs/{run['run_id']}/advance",
            {"expected_revision": 1, "idempotency_key": "../escape"},
        )
        self.assertEqual(400, status)
        self.assertEqual("Invalid idempotency key", error["error"])

        status, _ = self.request(
            "POST", f"/api/workstreams/{self.workstream['workstream_id']}/archive"
        )
        self.assertEqual(200, status)
        archived_payload = self.start_payload("archived-start")
        archived_payload["scenario_id"] = "filtered-demo"
        archived_payload["version"] = 2
        status, error = self.request("POST", "/api/scenario-runs", archived_payload)
        self.assertEqual(404, status)
        self.assertEqual("Workstream not found for investigation", error["error"])


class ScenarioManifestValidationTests(unittest.TestCase):
    def test_rejects_overlap_naive_time_and_embedded_record_fields(self):
        base = {
            "scenario_id": "demo",
            "version": 1,
            "title": "Demo",
            "scope": {"dataset": "v2.1"},
            "stages": [
                {
                    "id": "first",
                    "from": "2026-01-01T00:00:00Z",
                    "to": "2026-01-02T00:00:00Z",
                    "record_ids": ["REC-V2-007215"],
                },
                {
                    "id": "second",
                    "from": "2026-01-01T12:00:00Z",
                    "to": "2026-01-03T00:00:00Z",
                },
            ],
        }
        with self.assertRaisesRegex(ValueError, "Unsupported scenario stage field"):
            scenario_playback.normalize_manifest(base)
        del base["stages"][0]["record_ids"]
        with self.assertRaisesRegex(ValueError, "ordered and non-overlapping"):
            scenario_playback.normalize_manifest(base)
        base["stages"][1]["from"] = "2026-01-02T00:00:00"
        with self.assertRaisesRegex(ValueError, "must include a timezone"):
            scenario_playback.normalize_manifest(base)

        base["stages"][1]["from"] = "2026-01-02T00:00:00Z"
        normalized = scenario_playback.normalize_manifest(base)
        self.assertEqual(["first", "second"], [item["id"] for item in normalized["stages"]])


if __name__ == "__main__":
    unittest.main()

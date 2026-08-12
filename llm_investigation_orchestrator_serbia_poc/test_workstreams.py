import json
import tempfile
import threading
import unittest
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from unittest.mock import patch

import server


class WorkstreamApiTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workstreams_patch = patch.object(server, "WORKSTREAMS_DIR", Path(self.temp_dir.name))
        self.workstreams_patch.start()
        self.httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.httpd.server_port}"

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)
        self.workstreams_patch.stop()
        self.temp_dir.cleanup()

    def request(self, method, path, payload=None):
        body = None if payload is None else json.dumps(payload).encode("utf-8")
        request = Request(
            self.base_url + path,
            data=body,
            method=method,
            headers={"Content-Type": "application/json; charset=utf-8"},
        )
        try:
            with urlopen(request, timeout=3) as response:
                return response.status, json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            return exc.code, json.loads(exc.read().decode("utf-8"))

    @staticmethod
    def create_payload():
        return {
            "investigation_id": "investigation-42",
            "title": "Regional assessment",
            "objective": "Maintain one durable shared unit of analytical work.",
            "participants": [
                {
                    "participant_id": "analyst-1",
                    "kind": "human",
                    "display_name": "Analyst",
                    "role": "owner",
                },
                {
                    "participant_id": "agent-1",
                    "kind": "agent",
                    "display_name": "Agent",
                    "role": "analyst",
                },
            ],
            "assignments": [
                {
                    "assignment_id": "assignment-1",
                    "owner_id": "agent-1",
                    "responsibility": "Maintain the working assessment.",
                }
            ],
        }

    def test_create_list_load_update_and_archive(self):
        status, created = self.request("POST", "/api/workstreams", self.create_payload())
        self.assertEqual(status, 201)
        self.assertRegex(created["workstream_id"], r"^ws_")
        self.assertEqual(created["status"], "active")
        self.assertEqual(created["artifacts"], [])
        self.assertEqual(created["activity"], [])
        self.assertEqual(created["attention_requests"], [])
        self.assertIsNone(created["archived_at_utc"])

        workstream_id = created["workstream_id"]
        stored_path = Path(self.temp_dir.name) / "v2" / "he" / f"{workstream_id}.json"
        self.assertTrue(stored_path.exists())
        self.assertFalse(stored_path.with_suffix(".json.tmp").exists())

        status, listing = self.request(
            "GET", "/api/workstreams?investigation_id=investigation-42"
        )
        self.assertEqual(status, 200)
        self.assertEqual([item["workstream_id"] for item in listing["workstreams"]], [workstream_id])

        status, loaded = self.request("GET", f"/api/workstreams/{workstream_id}")
        self.assertEqual(status, 200)
        self.assertEqual(loaded["objective"], self.create_payload()["objective"])

        status, updated = self.request(
            "PUT",
            f"/api/workstreams/{workstream_id}",
            {"title": "Updated regional assessment", "status": "paused"},
        )
        self.assertEqual(status, 200)
        self.assertEqual(updated["title"], "Updated regional assessment")
        self.assertEqual(updated["status"], "paused")
        self.assertEqual(updated["investigation_id"], "investigation-42")

        status, error = self.request(
            "PUT",
            f"/api/workstreams/{workstream_id}",
            {"investigation_id": "investigation-99"},
        )
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Workstream investigation cannot be changed")

        status, archived = self.request(
            "POST", f"/api/workstreams/{workstream_id}/archive"
        )
        self.assertEqual(status, 200)
        self.assertEqual(archived["status"], "archived")
        self.assertIsNotNone(archived["archived_at_utc"])

        status, archived_again = self.request(
            "POST", f"/api/workstreams/{workstream_id}/archive"
        )
        self.assertEqual(status, 200)
        self.assertEqual(archived_again["archived_at_utc"], archived["archived_at_utc"])

        status, error = self.request(
            "PUT", f"/api/workstreams/{workstream_id}", {"title": "Too late"}
        )
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Archived workstream cannot be updated")

    def test_moshe_creation_handoff_persists_owned_workstream(self):
        created = server.apply_workstream_creation("investigation-42", {
            "title": "UAV indications",
            "objective": "Track indications of a command position.",
            "responsibility": "Corroborate reports and expose gaps.",
            "target_ids": ["TGT-F2CA47CB9859", "TGT-F2CA47CB9859"],
        })
        self.assertEqual("investigation-42", created["investigation_id"])
        self.assertEqual("moshe-targets-officer", created["assignments"][0]["owner_id"])
        self.assertEqual("משה", created["participants"][1]["display_name"])
        self.assertEqual(["TGT-F2CA47CB9859"], created["target_ids"])
        self.assertIn("TGT-F2CA47CB9859", created["title"])
        self.assertIn("TGT-F2CA47CB9859", created["objective"])

        answer = server.workstream_created_answer(created)
        self.assertIn("המעקב נפתח ונשמר בהצלחה.", answer)
        self.assertIn("UAV indications", answer)
        self.assertIn("Corroborate reports and expose gaps.", answer)
        self.assertNotIn("prepare_workstream_creation", answer)

    def test_target_ids_are_not_duplicated_in_existing_workstream_wording(self):
        created = server.apply_workstream_creation("investigation-labeled", {
            "title": "Track TGT-F2CA47CB9859",
            "objective": "Assess TGT-F2CA47CB9859 for changes.",
            "responsibility": "Corroborate reports.",
            "target_ids": ["TGT-F2CA47CB9859"],
            "record_ids": [],
        })
        self.assertEqual(1, created["title"].count("TGT-F2CA47CB9859"))
        self.assertEqual(1, created["objective"].count("TGT-F2CA47CB9859"))

    def test_root_targets_are_presented_without_an_assessment_artifact(self):
        created = server.apply_workstream_creation("investigation-42", {
            "title": "Target tracking",
            "objective": "Track changes.",
            "responsibility": "Corroborate reports.",
            "target_ids": ["TGT-F2CA47CB9859"],
        })
        target = {"target_id": "TGT-F2CA47CB9859", "title": "KFOR target"}
        with patch.object(server, "load_playback_visibility", return_value={
            "mode": "real_time", "active": True,
        }), patch.object(server, "get_ui_layer_rows", return_value=(None, [target])):
            result = server.workstream_presentation(created["workstream_id"])
        self.assertIsNone(result["artifact_revision"])
        self.assertEqual([target], result["requested_result_layers"][0]["rows"])

    def test_root_target_reference_is_presented_when_catalog_row_is_unavailable(self):
        created = server.apply_workstream_creation("investigation-42", {
            "title": "Target tracking",
            "objective": "Track changes.",
            "responsibility": "Corroborate reports.",
            "target_ids": ["TGT-F2CA47CB9859"],
        })
        with patch.object(server, "load_playback_visibility", return_value={
            "mode": "real_time", "active": True,
        }), patch.object(server, "get_ui_layer_rows", return_value=(None, [])):
            result = server.workstream_presentation(created["workstream_id"])
        self.assertEqual(
            [{"target_id": "TGT-F2CA47CB9859", "title": "TGT-F2CA47CB9859"}],
            result["requested_result_layers"][0]["rows"],
        )

    def test_raw_records_are_persisted_as_initial_workstream_artifact(self):
        event = {
            "record_id": "REC-V2-000001",
            "text": "Observed movement",
            "timestamp_utc": "2026-08-09T10:00:00Z",
            "source_type": "report",
            "collection_family": "public_report",
            "_canonical_layer_id": "events:report",
        }
        with patch.object(server, "resolve_workstream_event", return_value=event):
            created = server.apply_workstream_creation("investigation-record", {
                "title": "Record tracking",
                "objective": "Assess the supplied indication.",
                "responsibility": "Corroborate reports.",
                "target_ids": [],
                "record_ids": ["REC-V2-000001", "REC-V2-000001"],
            })
        self.assertEqual([], created["target_ids"])
        self.assertEqual(1, len(created["artifacts"]))
        artifact = created["artifacts"][0]
        self.assertEqual("target_assessment_lead", artifact["artifact_type"])
        self.assertEqual("Assess the supplied indication.", artifact["content"]["lead_statement"])
        self.assertEqual(
            "REC-V2-000001",
            artifact["content"]["indications"][0]["source_reference"]["record_id"],
        )
        persisted = server.load_workstream(created["workstream_id"])
        self.assertEqual(artifact["artifact_id"], persisted["artifacts"][0]["artifact_id"])

    def test_mixed_creation_links_artifact_to_validated_root_target_without_catalog_row(self):
        event = {"record_id": "REC-V2-000001", "_canonical_layer_id": "events:report"}
        with patch.object(server, "resolve_workstream_event", return_value=event), patch.object(
            server, "resolve_workstream_target", return_value=None
        ):
            created = server.apply_workstream_creation("investigation-mixed", {
                "title": "Mixed tracking",
                "objective": "Assess the supplied target and indication.",
                "responsibility": "Corroborate reports.",
                "target_ids": ["TGT-F2CA47CB9859"],
                "record_ids": ["REC-V2-000001"],
            })
        self.assertEqual(
            {"kind": "target", "target_id": "TGT-F2CA47CB9859", "label": "TGT-F2CA47CB9859"},
            created["artifacts"][0]["content"]["subject_reference"],
        )

    def test_rejects_invalid_input_and_cross_participant_assignment(self):
        invalid = self.create_payload()
        invalid["investigation_id"] = "../escape"
        status, error = self.request("POST", "/api/workstreams", invalid)
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Invalid investigation id")

        invalid = self.create_payload()
        invalid["assignments"][0]["owner_id"] = "missing-participant"
        status, error = self.request("POST", "/api/workstreams", invalid)
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Assignment owner is not a participant")

        status, error = self.request("GET", "/api/workstreams/../escape")
        self.assertIn(status, {400, 404})

    def test_workstream_contract_has_no_starting_source(self):
        status, created = self.request("POST", "/api/workstreams", self.create_payload())
        self.assertEqual(status, 201)
        self.assertNotIn("starting_source", created)

    def test_listing_is_scoped_to_investigation(self):
        first = self.create_payload()
        second = self.create_payload()
        second["investigation_id"] = "investigation-99"
        self.assertEqual(self.request("POST", "/api/workstreams", first)[0], 201)
        self.assertEqual(self.request("POST", "/api/workstreams", second)[0], 201)

        status, listing = self.request(
            "GET", "/api/workstreams?investigation_id=investigation-42"
        )
        self.assertEqual(status, 200)
        self.assertEqual(len(listing["workstreams"]), 1)
        self.assertEqual(listing["workstreams"][0]["investigation_id"], "investigation-42")

    def test_latest_fallback_returns_canonical_workstream_investigation(self):
        payload = self.create_payload()
        payload["investigation_id"] = "investigation-mobile"
        status, created = self.request("POST", "/api/workstreams", payload)
        self.assertEqual(status, 201)

        status, listing = self.request(
            "GET", "/api/workstreams?investigation_id=investigation-desktop&fallback=latest"
        )
        self.assertEqual(status, 200)
        self.assertTrue(listing["fallback_used"])
        self.assertEqual(listing["canonical_investigation_id"], "investigation-mobile")
        self.assertEqual(
            [item["workstream_id"] for item in listing["workstreams"]],
            [created["workstream_id"]],
        )

    def test_latest_fallback_never_overrides_an_exact_match(self):
        first = self.create_payload()
        second = self.create_payload()
        second["investigation_id"] = "investigation-99"
        self.assertEqual(self.request("POST", "/api/workstreams", first)[0], 201)
        self.assertEqual(self.request("POST", "/api/workstreams", second)[0], 201)

        status, listing = self.request(
            "GET", "/api/workstreams?investigation_id=investigation-42&fallback=latest"
        )
        self.assertEqual(status, 200)
        self.assertFalse(listing["fallback_used"])
        self.assertEqual(listing["canonical_investigation_id"], "investigation-42")
        self.assertEqual(len(listing["workstreams"]), 1)
        self.assertEqual(
            listing["workstreams"][0]["investigation_id"], "investigation-42"
        )


if __name__ == "__main__":
    unittest.main()

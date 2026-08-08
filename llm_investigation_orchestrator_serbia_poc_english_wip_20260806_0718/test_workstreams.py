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
        stored_path = server.workstream_dir("he") / f"{workstream_id}.json"
        self.assertTrue(stored_path.exists())
        self.assertFalse(stored_path.with_suffix(".json.tmp").exists())
        self.assertEqual(created["locale"], "he")

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
        })
        self.assertEqual("investigation-42", created["investigation_id"])
        self.assertEqual("moshe-targets-officer", created["assignments"][0]["owner_id"])
        self.assertEqual("משה", created["participants"][1]["display_name"])

        answer = server.workstream_created_answer(created)
        self.assertIn("המעקב נפתח ונשמר בהצלחה.", answer)
        self.assertIn("UAV indications", answer)
        self.assertIn("Corroborate reports and expose gaps.", answer)
        self.assertNotIn("prepare_workstream_creation", answer)

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

    def test_listing_exposes_latest_activity_marker_for_new_item_badges(self):
        status, created = self.request("POST", "/api/workstreams", self.create_payload())
        self.assertEqual(status, 201)
        workstream_id = created["workstream_id"]
        payload = server.load_workstream(workstream_id)
        payload["activity"].append({
            "activity_id": "playback-12",
            "type": "playback_assessment",
            "created_at_utc": "2026-08-05T20:06:36Z",
        })
        payload["updated_at_utc"] = "2026-08-05T20:06:36Z"
        server.write_workstream(payload)

        status, listing = self.request(
            "GET", "/api/workstreams?investigation_id=investigation-42"
        )
        self.assertEqual(status, 200)
        self.assertEqual("playback-12", listing["workstreams"][0]["latest_activity_id"])
        self.assertEqual("playback_assessment", listing["workstreams"][0]["latest_activity_type"])
        self.assertEqual("2026-08-05T20:06:36Z", listing["workstreams"][0]["latest_activity_at_utc"])

    def test_workstreams_are_physically_isolated_by_locale(self):
        he_payload = self.create_payload()
        he_payload["title"] = "Hebrew-owned workstream"
        status, he_created = self.request("POST", "/api/workstreams", he_payload)
        self.assertEqual(status, 201)

        en_payload = self.create_payload()
        en_payload["locale"] = "en"
        en_payload["title"] = "English workstream"
        en_payload["objective"] = "Maintain an English analytical flow."
        en_payload["participants"][0]["display_name"] = "Analyst"
        en_payload["participants"][0]["role"] = "Owner"
        en_payload["participants"][1]["display_name"] = "Moshe"
        en_payload["participants"][1]["role"] = "Targets officer"
        en_payload["assignments"][0]["responsibility"] = "Maintain the English working assessment."
        status, en_created = self.request("POST", "/api/workstreams", en_payload)
        self.assertEqual(status, 201)

        self.assertTrue((server.workstream_dir("he") / f"{he_created['workstream_id']}.json").exists())
        self.assertTrue((server.workstream_dir("en") / f"{en_created['workstream_id']}.json").exists())

        status, en_listing = self.request(
            "GET", "/api/workstreams?investigation_id=investigation-42&locale=en"
        )
        self.assertEqual(status, 200)
        self.assertEqual([item["workstream_id"] for item in en_listing["workstreams"]], [en_created["workstream_id"]])

        status, missing = self.request(
            "GET", f"/api/workstreams/{he_created['workstream_id']}?locale=en"
        )
        self.assertEqual(status, 404)
        self.assertEqual(missing["error"], "Workstream not found")

    def test_english_workstream_rejects_hebrew_without_partial_write(self):
        payload = self.create_payload()
        payload["locale"] = "en"
        payload["title"] = "English workstream"
        payload["objective"] = "בדיקה"
        status, error = self.request("POST", "/api/workstreams", payload)
        self.assertEqual(status, 400)
        self.assertIn("English workstream field contains Hebrew", error["error"])
        self.assertEqual([], list(server.workstream_dir("en").glob("ws_*.json")))


if __name__ == "__main__":
    unittest.main()

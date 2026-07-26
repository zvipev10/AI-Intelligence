import json
import tempfile
import threading
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.error import HTTPError
from urllib.request import Request, urlopen

import server

REAL_RESOLVE_WORKSTREAM_EVENT = server.resolve_workstream_event


class WorkstreamArtifactApiTests(unittest.TestCase):
    def test_real_event_resolver_accepts_rec_id_without_layer(self):
        event = REAL_RESOLVE_WORKSTREAM_EVENT("", "REC-V2-000001")
        self.assertEqual("REC-V2-000001", event["record_id"])
        self.assertTrue(event["summary"])
        self.assertTrue(event["_canonical_layer_id"].startswith("events:"))

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.workstreams_patch = patch.object(server, "WORKSTREAMS_DIR", Path(self.temp_dir.name))
        self.workstreams_patch.start()
        self.event_patch = patch.object(server, "resolve_workstream_event", side_effect=self.resolve_event)
        self.target_patch = patch.object(server, "resolve_workstream_target", side_effect=self.resolve_target)
        self.event_patch.start()
        self.target_patch.start()
        self.httpd = server.ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        self.thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        self.thread.start()
        self.base_url = f"http://127.0.0.1:{self.httpd.server_port}"
        status, self.workstream = self.request("POST", "/api/workstreams", self.workstream_payload())
        self.assertEqual(status, 201)

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        self.thread.join(timeout=2)
        self.target_patch.stop()
        self.event_patch.stop()
        self.workstreams_patch.stop()
        self.temp_dir.cleanup()

    @staticmethod
    def resolve_event(layer_id, record_id):
        events = {
            "REC-V2-000001": {
                "record_id": "REC-V2-000001",
                "text": "First observed activity.",
                "timestamp_utc": "2026-06-01T10:00:00Z",
                "source_type": "UAV",
                "collection_family": "airborne",
            },
            "REC-V2-000002": {
                "record_id": "REC-V2-000002",
                "text": "Independent public report.",
                "timestamp_utc": "2026-06-01T10:05:00Z",
                "source_type": "Public",
                "collection_family": "public_source",
            },
        }
        event = events.get(record_id)
        if not event:
            return None
        return {**event, "_canonical_layer_id": f"events:{event['source_type']}"}

    @staticmethod
    def resolve_target(target_id):
        if target_id == "TGT-D4DC7A7EBE02":
            return {"target_id": target_id, "title": "Existing candidate"}
        return None

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
    def workstream_payload():
        return {
            "investigation_id": "investigation-42",
            "title": "Indication tracking",
            "objective": "Review indications before assessment.",
            "participants": [
                {"participant_id": "analyst-1", "kind": "human", "display_name": "Analyst"},
                {"participant_id": "moshe", "kind": "agent", "display_name": "Moshe"},
            ],
            "assignments": [{
                "assignment_id": "assignment-1",
                "owner_id": "moshe",
                "responsibility": "Review indications.",
            }],
        }

    @staticmethod
    def confirmation(message_id="message-2", text="Yes, save it."):
        return {"message_id": message_id, "text": text}

    def artifact_payload(self):
        return {
            "artifact_type": "target_assessment_lead",
            "actor": {"participant_id": "analyst-1"},
            "confirmation_turn": self.confirmation(),
            "content": {
                "subject_reference": {"kind": "target", "target_id": "TGT-D4DC7A7EBE02"},
                "lead_statement": "The records may justify reassessment.",
                "indications": [{
                    "source_reference": {
                        "kind": "event_record",
                        "layer_id": "events:UAV",
                        "record_id": "REC-V2-000001",
                    },
                    "role": "supports",
                    "relevance": "Possible change in activity.",
                }],
                "gaps": ["Source independence"],
                "assigned_to": "moshe",
            },
        }

    def create_artifact(self):
        workstream_id = self.workstream["workstream_id"]
        status, artifact = self.request(
            "POST", f"/api/workstreams/{workstream_id}/artifacts", self.artifact_payload()
        )
        self.assertEqual(status, 201)
        return artifact

    def test_chat_bridge_applies_only_a_distinct_confirmed_turn(self):
        context = server.bounded_workstream_context({
            "workstream_id": self.workstream["workstream_id"],
            "current_turn_message_id": "turn-2",
            "pending_proposal": {
                "proposal_type": "target_assessment_lead",
                "action": "create",
                "proposed_turn_message_id": "turn-1",
                "lead_statement": "The records may justify reassessment.",
                "indications": [{
                    "record_id": "REC-V2-000001",
                    "role": "supports",
                    "relevance": "Possible change in activity.",
                }],
            },
        }, "investigation-42")
        self.assertEqual([], server.list_artifacts(server.load_workstream(self.workstream["workstream_id"])))
        artifact, conflict = server.apply_workstream_action(context, {
            "decision": "confirm",
            "proposal": context["pending_proposal"],
            "current_turn_message_id": "turn-2",
            "confirmation_text": "Yes, save it.",
        })
        self.assertIsNone(conflict)
        self.assertEqual(1, artifact["revision"])
        self.assertEqual(
            ["REC-V2-000001"],
            [item["source_reference"]["record_id"] for item in artifact["content"]["indications"]],
        )

    def test_chat_bridge_rejects_same_turn_confirmation(self):
        context = {
            "workstream_id": self.workstream["workstream_id"],
            "current_turn_message_id": "turn-1",
        }
        with self.assertRaisesRegex(ValueError, "distinct later"):
            server.apply_workstream_action(context, {
                "decision": "confirm",
                "proposal": {
                    "proposal_type": "target_assessment_lead",
                    "action": "create",
                    "proposed_turn_message_id": "turn-1",
                },
                "current_turn_message_id": "turn-1",
            })

    def test_create_list_load_and_persist_validated_artifact(self):
        artifact = self.create_artifact()
        self.assertRegex(artifact["artifact_id"], r"^artifact_")
        self.assertEqual(artifact["revision"], 1)
        self.assertEqual(artifact["status"], "active")
        self.assertEqual(artifact["content"]["subject_reference"]["target_id"], "TGT-D4DC7A7EBE02")
        indication = artifact["content"]["indications"][0]
        self.assertEqual(indication["observed_claim"], "First observed activity.")
        self.assertEqual(indication["provenance"]["collection_family"], "airborne")
        self.assertNotIn("target_id", indication["source_reference"])
        self.assertEqual(artifact["revisions"][0]["confirmation_turn"]["message_id"], "message-2")

        workstream_id = self.workstream["workstream_id"]
        status, listing = self.request("GET", f"/api/workstreams/{workstream_id}/artifacts")
        self.assertEqual(status, 200)
        self.assertEqual([item["artifact_id"] for item in listing["artifacts"]], [artifact["artifact_id"]])
        status, loaded = self.request(
            "GET", f"/api/workstreams/{workstream_id}/artifacts/{artifact['artifact_id']}"
        )
        self.assertEqual(status, 200)
        self.assertEqual(loaded, artifact)
        status, reopened = self.request("GET", f"/api/workstreams/{workstream_id}")
        self.assertEqual(status, 200)
        self.assertEqual(reopened["artifacts"][0]["artifact_id"], artifact["artifact_id"])

    def test_revision_conflict_and_append_only_removal(self):
        artifact = self.create_artifact()
        workstream_id = self.workstream["workstream_id"]
        revision_path = (
            f"/api/workstreams/{workstream_id}/artifacts/{artifact['artifact_id']}/revisions"
        )
        add_request = {
            "expected_revision": 1,
            "actor": {"participant_id": "analyst-1"},
            "confirmation_turn": self.confirmation("message-4", "Add the second record."),
            "action": "add_indication",
            "payload": {"indication": {
                "source_reference": {
                    "kind": "event_record",
                    "layer_id": "events:UAV",
                    "record_id": "REC-V2-000002",
                },
                "role": "contradicts",
            }},
        }
        status, revised = self.request("POST", revision_path, add_request)
        self.assertEqual(status, 200)
        self.assertEqual(revised["revision"], 2)
        self.assertEqual(len(revised["content"]["indications"]), 2)

        status, conflict = self.request("POST", revision_path, add_request)
        self.assertEqual(status, 409)
        self.assertEqual(conflict["current_revision"], 2)

        second_id = revised["content"]["indications"][1]["indication_id"]
        status, removed = self.request("POST", revision_path, {
            "expected_revision": 2,
            "actor": {"participant_id": "analyst-1"},
            "confirmation_turn": self.confirmation("message-6", "Remove it."),
            "action": "remove_indication",
            "payload": {"indication_id": second_id},
        })
        self.assertEqual(status, 200)
        self.assertEqual(removed["revision"], 3)
        self.assertEqual(removed["content"]["indications"][1]["state"], "removed")
        self.assertEqual([item["revision"] for item in removed["revisions"]], [1, 2, 3])

        add_request["expected_revision"] = 3
        add_request["confirmation_turn"] = self.confirmation("message-8", "Add it again.")
        status, error = self.request("POST", revision_path, add_request)
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Duplicate indication record_id")

        first_id = removed["content"]["indications"][0]["indication_id"]
        status, error = self.request("POST", revision_path, {
            "expected_revision": 3,
            "actor": {"participant_id": "analyst-1"},
            "confirmation_turn": self.confirmation("message-9", "Remove the final record."),
            "action": "remove_indication",
            "payload": {"indication_id": first_id},
        })
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Cannot remove the last active indication")

    def test_only_human_can_create_or_send_to_assessment(self):
        payload = self.artifact_payload()
        payload["actor"] = {"participant_id": "moshe"}
        workstream_id = self.workstream["workstream_id"]
        status, error = self.request("POST", f"/api/workstreams/{workstream_id}/artifacts", payload)
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Action requires a human participant")

        artifact = self.create_artifact()
        revision_path = (
            f"/api/workstreams/{workstream_id}/artifacts/{artifact['artifact_id']}/revisions"
        )
        status, error = self.request("POST", revision_path, {
            "expected_revision": 1,
            "actor": {"participant_id": "moshe"},
            "confirmation_turn": self.confirmation("message-7", "Send it."),
            "action": "send_to_assessment",
            "payload": {},
        })
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Action requires a human participant")
        status, ready = self.request("POST", revision_path, {
            "expected_revision": 1,
            "actor": {"participant_id": "analyst-1"},
            "confirmation_turn": self.confirmation("message-8", "Send it to assessment."),
            "action": "send_to_assessment",
            "payload": {},
        })
        self.assertEqual(status, 200)
        self.assertEqual(ready["status"], "ready_for_assessment")

    def test_canonicalizes_sources_and_rejects_invalid_references_and_second_artifact(self):
        workstream_id = self.workstream["workstream_id"]
        path = f"/api/workstreams/{workstream_id}/artifacts"
        payload = self.artifact_payload()
        payload["content"]["indications"][0]["source_reference"]["layer_id"] = "events:Public"
        status, artifact = self.request("POST", path, payload)
        self.assertEqual(status, 201)
        self.assertEqual(
            "events:UAV",
            artifact["content"]["indications"][0]["source_reference"]["layer_id"],
        )
        artifact["status"] = "rejected"
        stored = server.load_workstream(workstream_id)
        stored["artifacts"][0]["status"] = "rejected"
        server.write_workstream(stored)

        payload = self.artifact_payload()
        payload["content"]["indications"][0]["source_reference"]["record_id"] = "REC-V2-999999"
        status, error = self.request("POST", path, payload)
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Unknown event reference: REC-V2-999999")

        payload = self.artifact_payload()
        payload["content"]["subject_reference"]["target_id"] = "TGT-UNKNOWN"
        status, error = self.request("POST", path, payload)
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Unknown target reference: TGT-UNKNOWN")

        payload = self.artifact_payload()
        payload["content"]["gaps"] = {"unexpected": "object"}
        status, error = self.request("POST", path, payload)
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "Invalid gaps")

        self.create_artifact()
        status, error = self.request("POST", path, self.artifact_payload())
        self.assertEqual(status, 400)
        self.assertEqual(error["error"], "An active artifact of this type already exists")


if __name__ == "__main__":
    unittest.main()

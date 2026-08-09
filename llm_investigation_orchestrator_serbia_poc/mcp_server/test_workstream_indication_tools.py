import unittest
from unittest.mock import patch

import server


class WorkstreamIndicationToolsTest(unittest.TestCase):
    def test_prepares_complete_workstream_creation_handoff(self):
        with patch.object(server.TARGET_BANK, "initialize"), patch.object(
            server.TARGET_BANK, "get_candidate", return_value={"target_id": "TGT-ONE"}
        ):
            result = server.prepare_workstream_creation({
                "title": "מעקב רחפנים",
                "objective": "לזהות אינדיקציות למרכז פיקוד",
                "responsibility": "לאתר, להצליב ולהציג פערים",
                "target_ids": ["TGT-ONE", "TGT-ONE"],
            })
        self.assertFalse(result["persisted"])
        self.assertEqual("מעקב רחפנים", result["workstream_creation"]["title"])
        self.assertEqual(["TGT-ONE"], result["workstream_creation"]["target_ids"])

    def test_workstream_creation_rejects_unknown_target(self):
        with patch.object(server.TARGET_BANK, "initialize"), patch.object(
            server.TARGET_BANK, "get_candidate", return_value=None
        ), self.assertRaisesRegex(ValueError, "unknown target_id"):
            server.prepare_workstream_creation({
                "title": "Target tracking",
                "objective": "Track changes",
                "responsibility": "Corroborate reports",
                "target_ids": ["TGT-MISSING"],
            })

    def test_workstream_creation_requires_conversationally_complete_data(self):
        with self.assertRaisesRegex(ValueError, "responsibility is required"):
            server.prepare_workstream_creation({
                "title": "מעקב רחפנים",
                "objective": "לזהות אינדיקציות למרכז פיקוד",
                "target_ids": [],
            })

    def test_prepare_resolves_records_without_persisting(self):
        record_id = next(iter(server.EVENT_BY_ID))
        result = server.prepare_workstream_indication_proposal({
            "action": "create",
            "proposed_turn_message_id": "turn-1",
            "record_ids": [record_id],
            "lead_statement": "Lead to assess",
            "indications": [{"record_id": record_id, "role": "supports"}],
        })
        proposal = result["workstream_proposal"]
        self.assertFalse(result["persisted"])
        self.assertEqual([record_id], [item["record_id"] for item in proposal["indications"]])
        self.assertEqual("supports", proposal["indications"][0]["role"])

    def test_target_id_is_not_accepted_as_evidence(self):
        with self.assertRaisesRegex(ValueError, "unknown event_id"):
            server.prepare_workstream_indication_proposal({
                "action": "create",
                "proposed_turn_message_id": "turn-1",
                "record_ids": ["TGT-D4DC7A7EBE02"],
                "lead_statement": "Lead to assess",
            })

    def test_confirmation_requires_later_turn(self):
        proposal = {
            "proposal_type": "target_assessment_lead",
            "proposed_turn_message_id": "turn-1",
            "action": "create",
        }
        with self.assertRaisesRegex(ValueError, "distinct later"):
            server.decide_workstream_indication_proposal({
                "proposal": proposal,
                "decision": "confirm",
                "current_turn_message_id": "turn-1",
            })
        result = server.decide_workstream_indication_proposal({
            "proposal": proposal,
            "decision": "confirm",
            "current_turn_message_id": "turn-2",
            "confirmation_text": "כן, שמור",
        })
        self.assertFalse(result["persisted"])
        self.assertEqual("confirm", result["workstream_action"]["decision"])


if __name__ == "__main__":
    unittest.main()

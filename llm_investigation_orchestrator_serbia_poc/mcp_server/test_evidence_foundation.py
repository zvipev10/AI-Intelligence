import tempfile
import unittest
from pathlib import Path

import server
from evidence_store import EvidenceStore, prepare_fused_object, project_event


IBAR_EVIDENCE = ["REC-V2-006594", "REC-V2-011917", "REC-V2-010002"]


class EvidenceFoundationTests(unittest.TestCase):
    def test_uav_and_public_records_project_without_persistence(self):
        uav = project_event(server.public_event(server.EVENTS_BY_ID["REC-V2-006594"]))
        public = project_event(server.public_event(server.EVENTS_BY_ID["REC-V2-011917"]))
        self.assertEqual(uav["evidence_status"], "observed")
        self.assertEqual(public["evidence_status"], "reported")
        self.assertEqual(uav["source_record_ids"], ["REC-V2-006594"])
        self.assertFalse(uav["persisted"])

    def test_ibar_records_prepare_and_persist_one_neutral_fused_object(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = server.EVIDENCE_STORE
            server.EVIDENCE_STORE = EvidenceStore(Path(directory) / "evidence.db")
            try:
                prepared = server.prepare_fused_evidence({
                    "event_ids": IBAR_EVIDENCE,
                    "confidence": "medium",
                    "discover_corroboration": False,
                })["evidence"]
                self.assertTrue(prepared["persistence_eligible"])
                self.assertEqual(prepared["evidence_status"], "fused")
                self.assertEqual(prepared["location_ids"], ["LOC-V2-010"])
                self.assertEqual(prepared["subject_entity_ids"], ["ENT-KOSOVO-SPECIAL-POLICE"])
                persisted = server.persist_fused_evidence({
                    "event_ids": IBAR_EVIDENCE,
                    "confidence": "medium",
                    "discover_corroboration": False,
                })["evidence"]
                self.assertTrue(persisted["persisted"])
                self.assertEqual(server.get_evidence({"evidence_id": persisted["evidence_id"]})["evidence"], persisted)
                provenance = server.trace_evidence_provenance({"evidence_id": persisted["evidence_id"]})
                self.assertEqual(set(provenance["source_record_ids"]), set(IBAR_EVIDENCE))
                self.assertEqual(len(provenance["source_records"]), 3)
                layer = server.present_requested_results({"layers": [{
                    "kind": "evidence", "ids": [persisted["evidence_id"]],
                    "label": "Ibar bridge fused evidence", "view": "map",
                }]})["requested_result_layers"][0]
                self.assertEqual(layer["kind"], "evidence")
                self.assertEqual(layer["rows"][0]["evidence_id"], persisted["evidence_id"])
            finally:
                server.EVIDENCE_STORE = previous

    def test_incoherent_locations_cannot_persist(self):
        result = server.prepare_fused_evidence({
            "event_ids": ["REC-V2-006594", "REC-V2-014446"],
            "confidence": "medium",
            "discover_corroboration": False,
        })["evidence"]
        self.assertFalse(result["persistence_eligible"])
        self.assertIn("fused evidence requires one canonical location", result["persistence_block_reasons"])

    def test_target_preparation_uses_same_neutral_evidence_result(self):
        target = server.prepare_target_candidate({
            "event_ids": IBAR_EVIDENCE,
            "confidence": "medium",
            "discover_corroboration": False,
        })
        neutral = server.prepare_fused_evidence({
            "event_ids": IBAR_EVIDENCE,
            "confidence": "medium",
            "discover_corroboration": False,
        })
        self.assertEqual(target["prepared_evidence"], neutral["evidence"])
        self.assertEqual(target["persistence_eligible"], neutral["fusion"]["persistence_eligible"])

    def test_projected_evidence_can_be_presented_without_database_write(self):
        evidence_id = "EVD-REC-V2-006594"
        layer = server.present_requested_results({"evidence_layers": [{
            "kind": "evidence", "ids": [evidence_id], "label": "Observed evidence", "view": "map",
        }]})["evidence_reference_layers"][0]
        self.assertEqual(layer["rows"][0]["evidence_status"], "observed")
        self.assertFalse(layer["rows"][0]["persisted"])

    def test_contradicting_source_remains_explicit(self):
        rows = [
            {"event_id": "REC-1", "location_id": "LOC-1", "entity_id": "ENT-1", "object_class": "vehicle", "timestamp_utc": "2026-09-15T01:00:00Z", "event_summary": "observed"},
            {"event_id": "REC-2", "location_id": "LOC-1", "entity_id": "ENT-1", "timestamp_utc": "2026-09-15T02:00:00Z", "event_summary": "הדובר מכחיש את הדיווח"},
        ]
        fusion = {
            "confidence": "medium", "persistence_eligible": True, "persistence_block_reasons": [],
            "quantity": {}, "evidence": [
                {"record_id": "REC-1", "source_group": "one"},
                {"record_id": "REC-2", "source_group": "two"},
            ],
        }
        evidence = prepare_fused_object(rows, fusion)
        self.assertEqual(evidence["contradicting_evidence_ids"], ["EVD-REC-2"])
        self.assertEqual(evidence["supporting_evidence_ids"], ["EVD-REC-1"])


if __name__ == "__main__":
    unittest.main()

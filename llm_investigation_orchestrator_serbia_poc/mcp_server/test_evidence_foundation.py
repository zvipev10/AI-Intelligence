import json
import tempfile
import unittest
from pathlib import Path

import server
from evidence_store import EvidenceStore, prepare_fused_object, project_event
from evidence_semantics import normalize_evidence_event


IBAR_EVIDENCE = ["REC-V2-006594", "REC-V2-011917", "REC-V2-010002"]


class EvidenceFoundationTests(unittest.TestCase):
    def test_specific_location_name_beats_broad_municipality_alias(self):
        result = server.resolve_location({"query": "ציר פרישטינה–מיטרוביצה"})
        self.assertEqual(result["location_ids"], ["LOC-V2-013"])

        hyphenated = server.resolve_location({"query": "ציר פרישטינה-מיטרוביצה"})
        self.assertEqual(hyphenated["location_ids"], ["LOC-V2-013"])

        approaches = server.resolve_location({"query": "הגישות הצפוניות לצפון מיטרוביצה"})
        self.assertEqual(approaches["location_ids"], ["LOC-V2-009"])

    def test_v21_location_resolution_excludes_legacy_ids_and_supports_english_aliases(self):
        if server.DATASET_VERSION != "v2.1":
            self.skipTest("Production-only V2.1 location namespace contract")

        for query in ("אזור גשר איבר", "גשר איבר", "Ibar bridge", "Mitrovica bridge"):
            with self.subTest(query=query):
                result = server.resolve_location({"query": query})
                self.assertEqual(result["location_ids"], ["LOC-V2-010"])
                self.assertNotIn("LOC-001", result["location_ids"])

        broad = server.resolve_location({"query": "צפון מיטרוביצה"})
        self.assertTrue(broad["location_ids"])
        self.assertTrue(all(location_id.startswith("LOC-V2-") for location_id in broad["location_ids"]))
        self.assertIsNone(server.scoped_location_presentation("LOC-001"))

    def test_search_evidence_defaults_to_fused_objects(self):
        class SearchStub:
            def __init__(self):
                self.filters = None

            def search(self, filters):
                self.filters = filters
                return [{"evidence_id": "EVD-FUSED-TEST", "evidence_status": "fused"}]

        previous = server.EVIDENCE_STORE
        stub = SearchStub()
        server.EVIDENCE_STORE = stub
        try:
            result = server.search_evidence({"location_id": "LOC-V2-013", "limit": 100})
            self.assertEqual(stub.filters["evidence_status"], "fused")
            self.assertEqual(result["evidence"][0]["evidence_status"], "fused")
        finally:
            server.EVIDENCE_STORE = previous

    def test_prepare_evidence_reuses_shared_semantic_object_concepts(self):
        cases = {
            "תושבים דיווחו על רכב כבד ממוגן באזור": "רכב משוריין",
            "נראו כלים שביצעו הכשרת שטח": "עבודות הנדסיות",
            "נראה כלי טיס סובב כנף": "מסוק",
        }
        for summary, expected in cases.items():
            with self.subTest(summary=summary):
                normalized = normalize_evidence_event({"event_summary": summary})
                self.assertEqual(normalized["object_class"], expected)
                self.assertEqual(normalized["object_class_resolution"]["method"], "shared_semantic_concept")

    def test_structured_object_class_remains_authoritative(self):
        normalized = normalize_evidence_event({"object_class": "מסוק", "event_summary": "רכב כבד ממוגן"})
        self.assertEqual(normalized["object_class"], "מסוק")
        self.assertEqual(normalized["object_class_resolution"]["method"], "structured_source")

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

    def test_catalog_fused_evidence_is_available_without_sqlite_materialization(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            catalog_path = root / "he.json"
            evidence = {
                "evidence_id": "EVD-FUSED-CATALOG",
                "evidence_status": "fused",
                "confidence": "medium",
                "location_ids": ["LOC-V2-010"],
                "subject_entity_ids": ["ENT-KSF"],
                "source_record_ids": ["REC-V2-1", "REC-V2-2"],
                "valid_from": "2026-09-16T09:00:00Z",
            }
            catalog_path.write_text(json.dumps({"rows": [evidence]}), encoding="utf-8")
            store = EvidenceStore(root / "missing.db", catalog_path=catalog_path)
            self.assertEqual(store.get(evidence["evidence_id"]), evidence)
            self.assertEqual(store.search({"entity_id": "ENT-KSF"}), [evidence])
            self.assertFalse((root / "missing.db").exists())

    def test_three_ibar_object_chains_prepare_as_separate_fused_evidence(self):
        chains = {
            "רכב משוריין": ["REC-V2-008274", "REC-V2-014170", "REC-V2-012466"],
            "מסוק": ["REC-V2-004792", "REC-V2-008463", "REC-V2-011590"],
            "עבודות הנדסיות": ["REC-V2-006374", "REC-V2-012738", "REC-V2-014708"],
        }
        for expected_class, event_ids in chains.items():
            with self.subTest(object_class=expected_class):
                prepared = server.prepare_fused_evidence({
                    "event_ids": event_ids,
                    "confidence": "medium",
                    "discover_corroboration": False,
                })["evidence"]
                self.assertTrue(prepared["persistence_eligible"])
                self.assertEqual(prepared["object_class"], expected_class)
                self.assertEqual(prepared["source_record_ids"], sorted(event_ids))

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

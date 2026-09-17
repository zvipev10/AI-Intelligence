import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    from .assessment_store import AssessmentStore
except ImportError:  # pragma: no cover - direct script execution
    from assessment_store import AssessmentStore


def sample():
    return {
        "title": "Assessed KFOR aviation operating area",
        "status": "current",
        "scope": {"location_ids": ["LOC-V2-001"], "entity_ids": ["ENT-KFOR-AVIATION"]},
        "key_judgments": [{"judgment": "Aviation activity is concentrated north of the bridge.", "confidence": "medium", "evidence_ids": ["EVD-REC-V2-000001"]}],
        "alternatives": ["Training activity"], "intelligence_gaps": ["No night coverage"],
        "summary": "A bounded operating-area assessment.",
        "overlays": [{"type": "assessed_area", "meaning": "likely_operating_area", "confidence": "medium",
                      "supporting_evidence_ids": ["EVD-REC-V2-000001"],
                      "geometry": {"type": "Polygon", "coordinates": [[[20.8, 42.9], [20.9, 42.9], [20.9, 43.0], [20.8, 42.9]]]}}],
    }


class AssessmentStoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.store = AssessmentStore(Path(self.temp.name) / "assessments.db")

    def tearDown(self): self.temp.cleanup()

    def test_create_update_search_and_supersede(self):
        created = self.store.create(sample())
        self.assertTrue(created["assessment_id"].startswith("ASM-"))
        updated = self.store.update(created["assessment_id"], {"summary": "Revised."}, 1)
        self.assertEqual(2, updated["revision"])
        self.assertEqual(created["assessment_id"], self.store.search(query="KFOR")[0]["assessment_id"])
        self.assertEqual("superseded", self.store.supersede(created["assessment_id"], 2)["status"])

    def test_stale_revision_and_invalid_geometry_fail_closed(self):
        created = self.store.create(sample())
        with self.assertRaisesRegex(ValueError, "stale"):
            self.store.update(created["assessment_id"], {"summary": "No"}, 2)
        invalid = sample(); invalid["overlays"][0]["geometry"]["coordinates"][0][-1] = [20.7, 42.8]
        with self.assertRaisesRegex(ValueError, "closed"):
            self.store.create(invalid)

    def test_duplicate_create_is_idempotent(self):
        first = self.store.create(sample())
        second = self.store.create(sample())
        self.assertEqual(first["assessment_id"], second["assessment_id"])
        self.assertEqual(1, second["revision"])

    def test_overlay_without_supporting_evidence_fails_closed(self):
        invalid = sample()
        invalid["overlays"][0]["supporting_evidence_ids"] = []
        with self.assertRaisesRegex(ValueError, "requires supporting_evidence_ids"):
            self.store.create(invalid)


class AssessmentToolContractTests(unittest.TestCase):
    def test_tool_create_and_present_materialize_assessment_layer(self):
        from . import server
        with tempfile.TemporaryDirectory() as directory, patch.object(server, "ASSESSMENT_STORE", AssessmentStore(Path(directory) / "assessments.db")), patch.object(server, "resolve_evidence", return_value={"evidence_id": "EVD-REC-V2-000001"}):
            created = server.create_enemy_assessment({"assessment": sample()})["assessment"]
            layer = server._materialize_presentation_layers([{
                "kind": "assessments", "ids": [created["assessment_id"]],
                "label": "Enemy assessment", "view": "map",
            }], id_prefix="requested")[0]
        self.assertEqual("assessments", layer["kind"])
        self.assertTrue(layer["capabilities"]["map"])
        self.assertEqual(created["assessment_id"], layer["rows"][0]["assessment_id"])


if __name__ == "__main__": unittest.main()

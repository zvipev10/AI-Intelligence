import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import server


class InvestigationRegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        root = Path(self.temp_dir.name)
        self.investigations_dir = root / "investigations"
        self.workstreams_dir = root / "workstreams"
        self.runs_dir = root / "scenario_runs"
        self.patches = [
            patch.object(server, "INVESTIGATIONS_DIR", self.investigations_dir),
            patch.object(server, "WORKSTREAMS_DIR", self.workstreams_dir),
            patch.object(server, "SCENARIO_RUNS_DIR", self.runs_dir),
        ]
        for item in self.patches:
            item.start()

    def tearDown(self):
        for item in reversed(self.patches):
            item.stop()
        self.temp_dir.cleanup()

    def test_registration_preserves_distinct_ids_with_the_same_name(self):
        server.register_investigation({
            "investigation_id": "investigation-a",
            "name": "New investigation",
        })
        server.register_investigation({
            "investigation_id": "investigation-b",
            "name": "New investigation",
        })

        items = server.list_investigation_memory_metadata()

        self.assertEqual(
            {"investigation-a", "investigation-b"},
            {item["investigation_id"] for item in items},
        )

    def test_listing_discovers_workstream_and_scenario_investigations(self):
        server.create_workstream({
            "investigation_id": "investigation-workstream",
            "title": "Tracked investigation",
            "objective": "Keep this investigation discoverable.",
            "participants": [],
            "assignments": [],
        })
        self.runs_dir.mkdir(parents=True)
        (self.runs_dir / "run_registry.json").write_text(json.dumps({
            "run_id": "run_registry",
            "investigation_id": "investigation-scenario",
            "created_at_utc": "2026-08-11T00:00:00Z",
            "updated_at_utc": "2026-08-11T00:00:00Z",
        }), encoding="utf-8")

        items = server.list_investigation_memory_metadata()

        self.assertEqual(
            {"investigation-workstream", "investigation-scenario"},
            {item["investigation_id"] for item in items},
        )

    def test_memory_artifacts_are_additive_and_keep_analyst_comments(self):
        object_saved = server.create_memory_artifact({
            "investigation_id": "investigation-a",
            "name": "Syria convoy lead",
            "comment": "Check the call pattern before assessment.",
            "artifact": {
                "kind": "object", "object_kind": "record", "object_id": "CALL-001",
                "label": "Cell call CALL-001", "source_type": "cellular_calls",
            },
        })
        polygon_saved = server.create_memory_artifact({
            "investigation_id": "investigation-a",
            "comment": "Area of convoy activity.",
            "artifact": {
                "kind": "polygon", "label": "Convoy search area",
                "geometry": {"type": "Polygon", "coordinates": [[[35.0, 33.0], [35.1, 33.0], [35.1, 33.1], [35.0, 33.0]]]},
            },
        })

        memory = server.load_investigation_memory("investigation-a")["memory"]

        self.assertEqual("object", object_saved["saved"]["kind"])
        self.assertEqual("polygon", polygon_saved["saved"]["kind"])
        self.assertEqual(2, len(memory["artifacts"]))
        self.assertEqual("Check the call pattern before assessment.", memory["artifacts"][0]["analyst_comment"])
        self.assertEqual("Area of convoy activity.", memory["artifacts"][1]["analyst_comment"])
        self.assertTrue(server.investigation_memory_has_content({"memory": memory}))


if __name__ == "__main__":
    unittest.main()

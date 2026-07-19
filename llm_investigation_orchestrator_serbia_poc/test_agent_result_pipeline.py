import unittest

from agent_result_pipeline import (
    build_agent_result,
    normalize_entity_layers,
    normalize_location_layers,
    normalize_map_locations,
    normalize_typed_layers,
)
from server import HermesClient


class AgentResultPipelineTests(unittest.TestCase):
    def test_general_result_preserves_legacy_payload_and_adds_identity(self):
        payload = {"run_id": "run-7", "answer": "ok", "event_ids": ["REC-V2-000001"]}
        result = build_agent_result(payload, session_id="session-3")
        self.assertEqual(result["answer"], "ok")
        self.assertEqual(result["event_ids"], ["REC-V2-000001"])
        self.assertEqual(result["responding_agent"], "general")
        self.assertEqual(result["session_id"], "session-3")
        self.assertNotIn("mission_run_id", result)

    def test_result_supports_other_agent_and_optional_mission(self):
        result = build_agent_result(
            {"run_id": "run-8", "answer": "candidate"},
            responding_agent="moshe",
            session_id="session-4",
            mission_run_id="mission-2",
        )
        self.assertEqual(result["responding_agent"], "moshe")
        self.assertEqual(result["session_id"], "session-4")
        self.assertEqual(result["mission_run_id"], "mission-2")

    def test_typed_layers_reject_unknown_or_malformed_layers(self):
        layers = normalize_typed_layers([
            {"kind": "events", "rows": [{"event_id": "REC-1"}]},
            {"kind": "moshe-only", "rows": []},
            {"kind": "locations", "rows": "bad"},
        ])
        self.assertEqual(layers, [{"kind": "events", "rows": [{"event_id": "REC-1"}]}])

    def test_existing_location_and_entity_shapes_are_preserved(self):
        locations = normalize_location_layers({"location_layers": [{"location_id": "LOC-1", "name": "A", "count": 2}]})
        entities = normalize_entity_layers({"entity_layers": [{"entity_id": "ENT-1", "canonical_name": "B", "count": 3}]})
        self.assertEqual(locations[0]["location_name"], "A")
        self.assertEqual(locations[0]["event_count"], 2)
        self.assertEqual(entities[0]["canonical_name"], "B")
        self.assertEqual(entities[0]["event_count"], 3)

    def test_map_locations_dedupe_using_largest_count(self):
        result = {
            "map_locations": [{"location_id": "LOC-1", "name": "A", "count": 1}],
            "locations": [{"location_id": "LOC-1", "name": "A", "count": 4}],
        }
        self.assertEqual(normalize_map_locations("search_events", result)[0]["count"], 4)

    def test_general_audit_steps_use_extracted_normalizers(self):
        steps = HermesClient.summarize_audit([{
            "tool": "get_objects",
            "arguments": {"object_type": "all", "location_ids": ["LOC-1"]},
            "result": {
                "location_layers": [{"location_id": "LOC-1", "name": "A", "count": 2}],
                "entity_layers": [{"entity_id": "ENT-1", "canonical_name": "B", "count": 1}],
            },
        }])
        self.assertEqual(len(steps), 1)
        self.assertEqual(steps[0]["location_layers"][0]["location_id"], "LOC-1")
        self.assertEqual(steps[0]["entity_layers"][0]["entity_id"], "ENT-1")


if __name__ == "__main__":
    unittest.main()

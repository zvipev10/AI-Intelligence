import unittest

from agent_result_pipeline import (
    build_agent_result,
    evidence_reference_layers_from_audit,
    normalize_entity_layers,
    normalize_location_layers,
    normalize_map_locations,
    normalize_attack_targets,
    normalize_typed_layers,
    normalize_workstream_collaboration,
    requested_result_layers_from_audit,
)
from server import HermesClient


class AgentResultPipelineTests(unittest.TestCase):
    def test_normalizes_successful_workstream_handoffs(self):
        records = [
            {"tool": "prepare_workstream_indication_proposal", "result": {
                "workstream_proposal": {"proposal_type": "target_assessment_lead", "action": "create"}
            }},
            {"tool": "decide_workstream_indication_proposal", "result": {
                "workstream_action": {"decision": "confirm"}
            }},
            {"tool": "prepare_workstream_indication_proposal", "is_error": True, "result": {
                "workstream_proposal": {"action": "bad"}
            }},
        ]
        self.assertEqual({
            "workstream_proposal": {"proposal_type": "target_assessment_lead", "action": "create"},
            "workstream_action": {"decision": "confirm"},
        }, normalize_workstream_collaboration(records))

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

    def test_attack_target_is_a_shared_typed_layer(self):
        layers = normalize_typed_layers([{"kind": "attack_targets", "rows": [{"target_id": "TGT-1"}]}])
        self.assertEqual(layers[0]["kind"], "attack_targets")

    def test_only_last_explicit_requested_result_selection_becomes_final_layers(self):
        records = [
            {"tool": "search_events", "result": {"event_ids": ["REC-SUPPORT"]}},
            {"tool": "present_requested_results", "result": {"requested_result_layers": [
                {"kind": "events", "rows": [{"event_id": "REC-OLD"}]},
            ]}},
            {"tool": "present_requested_results", "result": {"requested_result_layers": [
                {"kind": "events", "rows": [{"event_id": "REC-REQUESTED"}]},
            ]}},
        ]
        layers = requested_result_layers_from_audit(records)
        self.assertEqual([row["event_id"] for row in layers[0]["rows"]], ["REC-REQUESTED"])
        self.assertNotIn("REC-SUPPORT", str(layers))

    def test_result_envelope_keeps_requested_layers_separate_from_legacy_layers(self):
        result = build_agent_result(
            {"answer": "ok"},
            layers=[{"kind": "events", "rows": [{"event_id": "REC-SUPPORT"}]}],
            requested_result_layers=[{"kind": "events", "rows": [{"event_id": "REC-REQUESTED"}]}],
        )
        self.assertEqual(result["layers"][0]["rows"][0]["event_id"], "REC-SUPPORT")
        self.assertEqual(result["requested_result_layers"][0]["rows"][0]["event_id"], "REC-REQUESTED")

    def test_evidence_references_are_explicit_separate_and_last_call_wins(self):
        records = [
            {"tool": "search_events", "result": {"event_ids": ["REC-NOISE"]}},
            {"tool": "present_requested_results", "result": {
                "requested_result_layers": [{"kind": "locations", "rows": [{"location_id": "LOC-1"}]}],
                "evidence_reference_layers": [{"kind": "events", "rows": [{"event_id": "REC-OLD"}]}],
            }},
            {"tool": "present_requested_results", "result": {
                "requested_result_layers": [],
                "evidence_reference_layers": [{"kind": "events", "rows": [{"event_id": "REC-EVIDENCE"}]}],
            }},
        ]
        evidence = evidence_reference_layers_from_audit(records)
        requested = requested_result_layers_from_audit(records)
        self.assertEqual([row["event_id"] for row in evidence[0]["rows"]], ["REC-EVIDENCE"])
        self.assertEqual(requested, [])
        self.assertNotIn("REC-NOISE", str(evidence))

    def test_result_envelope_keeps_evidence_references_separate(self):
        result = build_agent_result(
            {"answer": "ok"},
            requested_result_layers=[{"kind": "locations", "rows": [{"location_id": "LOC-1"}]}],
            evidence_reference_layers=[{"kind": "events", "rows": [{"event_id": "REC-1"}]}],
        )
        self.assertEqual(result["requested_result_layers"][0]["kind"], "locations")
        self.assertEqual(result["evidence_reference_layers"][0]["rows"][0]["event_id"], "REC-1")

    def test_target_results_are_deduped_enriched_and_keep_full_evidence(self):
        records = [
            {"tool": "get_target_candidate", "result": {"candidate": {
                "target_id": "TGT-1", "title": "A", "location_id": "LOC-1", "entity_id": "ENT-1",
                "evidence": [{"record_id": "REC-1", "source_group": "G1"}],
            }}},
            {"tool": "search_target_candidates", "result": {"candidates": [{
                "target_id": "TGT-1", "title": "A updated", "location_id": "LOC-1", "entity_id": "ENT-1",
                "source_group_count": 2,
            }]}},
        ]
        rows = normalize_attack_targets(
            records,
            locations={"LOC-1": {"name": "Area B", "latitude": 1.5, "longitude": 2.5}},
            entities={"ENT-1": {"canonical_name": "Unit One"}},
        )
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["title"], "A updated")
        self.assertEqual(rows[0]["location_name"], "Area B")
        self.assertEqual(rows[0]["entity_name"], "Unit One")
        self.assertEqual(rows[0]["evidence"][0]["record_id"], "REC-1")
        self.assertEqual(rows[0]["raw_data_references"], ["REC-1"])
        self.assertEqual(rows[0]["source_group_count"], 2)

    def test_target_presentation_ignores_errors_and_empty_results(self):
        rows = normalize_attack_targets([
            {"tool": "get_target_candidate", "is_error": True, "result": {"candidate": {"target_id": "TGT-BAD"}}},
            {"tool": "search_target_candidates", "result": {"candidates": []}},
            {"tool": "search_events", "result": {"candidate": {"target_id": "TGT-WRONG-TOOL"}}},
        ])
        self.assertEqual(rows, [])

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

    def test_moshe_prepare_summary_is_bounded_and_keeps_identifiers(self):
        result = {
            "independent_source_group_count": 2,
            "confidence": "high",
            "persistence_eligible": True,
            "evidence": [
                {"record_id": "REC-1", "relevant_text": "x" * 2000},
                {"record_id": "REC-2", "relevant_text": "y" * 2000},
            ],
        }
        step = HermesClient.summarize_audit([{
            "tool": "prepare_target_candidate",
            "arguments": {"event_ids": ["REC-1"]},
            "result": result,
        }])[0]
        self.assertIn("REC-1", step["result"])
        self.assertIn("REC-2", step["result"])
        self.assertIn("כשיר לשמירה", step["result"])
        self.assertLess(len(step["result"]), 500)
        self.assertNotIn("relevant_text", step["result"])

    def test_moshe_target_update_summary_keeps_target_id_without_raw_json(self):
        step = HermesClient.summarize_audit([{
            "tool": "update_target_candidate",
            "arguments": {"target_id": "TGT-1", "changes": {"summary": "z" * 2000}},
            "result": {"candidate": {"target_id": "TGT-1", "title": "Target", "summary": "z" * 2000}},
        }])[0]
        self.assertIn("TGT-1", step["result"])
        self.assertLess(len(step["action"]), 250)
        self.assertLess(len(step["result"]), 250)
        self.assertNotIn("z" * 100, step["action"] + step["result"])


if __name__ == "__main__":
    unittest.main()

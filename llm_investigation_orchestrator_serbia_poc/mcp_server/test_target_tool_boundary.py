import ast
import tempfile
import unittest
from pathlib import Path

import server
from target_bank import TargetBank


def general_deployment_tools():
    source = (Path(__file__).resolve().parent / "remote_deploy_serbia.py").read_text(encoding="utf-8")
    module = ast.parse(source)
    assignment = next(
        node for node in module.body
        if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == "TOOLS" for target in node.targets)
    )
    return ast.literal_eval(assignment.value)


class TargetToolBoundaryTests(unittest.TestCase):
    def test_attachment_preserves_stored_groups_when_only_ordinal_labels_swap(self):
        current = [
            {"record_id": "REC-A", "source_group": "visible-report:002"},
            {"record_id": "REC-B", "source_group": "visible-report:001"},
            {"record_id": "REC-C", "source_group": "visible-report:003"},
        ]
        fused = [
            {"record_id": "REC-A", "source_group": "visible-report:001"},
            {"record_id": "REC-B", "source_group": "visible-report:002"},
            {"record_id": "REC-C", "source_group": "visible-report:003"},
            {"record_id": "REC-D", "source_group": "uav-mission:UAV-MSN-021"},
            {"record_id": "REC-E", "source_group": "uav-mission:UAV-MSN-021"},
        ]

        attached = server.reconcile_attached_evidence_groups(current, fused, {"REC-D", "REC-E"})

        self.assertEqual({item["source_group"] for item in attached}, {"uav-mission:UAV-MSN-021"})

    def test_attachment_rejects_real_merge_of_existing_groups(self):
        current = [
            {"record_id": "REC-A", "source_group": "visible-report:a"},
            {"record_id": "REC-B", "source_group": "visible-report:b"},
        ]
        fused = [
            {"record_id": "REC-A", "source_group": "visible-report:001"},
            {"record_id": "REC-B", "source_group": "visible-report:001"},
            {"record_id": "REC-C", "source_group": "visible-report:001"},
        ]

        with self.assertRaisesRegex(ValueError, "merge existing immutable source groups"):
            server.reconcile_attached_evidence_groups(current, fused, {"REC-C"})

    def test_new_visible_report_group_gets_stable_non_ordinal_id(self):
        attached = server.reconcile_attached_evidence_groups(
            [{"record_id": "REC-A", "source_group": "visible-report:001"}],
            [
                {"record_id": "REC-A", "source_group": "visible-report:001"},
                {"record_id": "REC-B", "source_group": "visible-report:002"},
            ],
            {"REC-B"},
        )
        self.assertRegex(attached[0]["source_group"], r"^visible-report:[0-9a-f]{12}$")
        self.assertNotEqual(attached[0]["source_group"], "visible-report:001")

    def test_exact_production_label_swap_case_attaches_in_temporary_bank(self):
        existing_ids = ["REC-V2-009058", "REC-V2-014385", "REC-V2-014425"]
        new_ids = ["REC-V2-006452", "REC-V2-007655", "REC-V2-004558"]
        initial = server.prepare_candidate(server._fusion_events(existing_ids), "medium")["evidence"]
        first_group, second_group = initial[0]["source_group"], initial[1]["source_group"]
        initial[0]["source_group"], initial[1]["source_group"] = second_group, first_group
        with tempfile.TemporaryDirectory() as directory:
            previous = server.TARGET_BANK
            server.TARGET_BANK = TargetBank(Path(directory) / "targets.db", Path(directory) / "backups")
            server.TARGET_BANK.initialize()
            try:
                created = server.TARGET_BANK.create_candidate({
                    "title": "Production regression",
                    "summary": "Ordinal labels must not block valid evidence.",
                    "object_class": "observation_post",
                    "entity_id": "ENT-KFOR",
                    "location_id": "LOC-V2-005",
                    "confidence": "medium",
                    "count_assessment": "unresolved",
                    "fusion_explanation": "Three independent visible reports.",
                    "mission_run_id": "regression-run",
                    "created_by": "moshe",
                }, initial)
                updated = server.attach_target_evidence({
                    "target_id": created["target_id"],
                    "evidence": [{"record_id": record_id} for record_id in new_ids],
                })["candidate"]
                self.assertEqual(len(updated["evidence"]), 6)
                self.assertEqual(
                    {item["source_group"] for item in updated["evidence"] if item["record_id"] in new_ids},
                    {"uav-mission:UAV-MSN-021"},
                )
                stored_existing = {
                    item["record_id"]: item["source_group"] for item in updated["evidence"]
                    if item["record_id"] in existing_ids
                }
                self.assertEqual(stored_existing, {item["record_id"]: item["source_group"] for item in initial})
            finally:
                server.TARGET_BANK = previous

    def test_mcp_registry_contains_only_constrained_target_tools(self):
        target_tools = {item["name"] for item in server.TOOLS if "target" in item["name"]}
        self.assertEqual(target_tools, {
            "prepare_target_candidate",
            "find_duplicate_target_candidates",
            "search_target_candidates",
            "get_target_candidate",
            "create_target_candidate",
            "update_target_candidate",
            "attach_target_evidence",
        })
        forbidden_markers = ("sql", "delete", "reset", "backup", "filesystem", "status")
        self.assertFalse(any(marker in name for name in target_tools for marker in forbidden_markers))

    def test_general_deployment_allowlist_does_not_expose_target_writes(self):
        write_tools = {"create_target_candidate", "update_target_candidate", "attach_target_evidence"}
        self.assertTrue(write_tools.isdisjoint(general_deployment_tools()))

    def test_tool_schemas_do_not_expose_lifecycle_or_review_mutation(self):
        by_name = {item["name"]: item for item in server.TOOLS}
        create_properties = by_name["create_target_candidate"]["inputSchema"]["properties"]["candidate"]["properties"]
        update_properties = by_name["update_target_candidate"]["inputSchema"]["properties"]["changes"]["properties"]
        for field in ("status", "reviewed_by", "reviewed_at", "review_note"):
            self.assertNotIn(field, create_properties)
            self.assertNotIn(field, update_properties)
        self.assertNotIn("created_by", update_properties)
        self.assertNotIn("created_by", create_properties)

    def test_target_search_exposes_exact_raw_record_lookup(self):
        search_tool = next(item for item in server.TOOLS if item["name"] == "search_target_candidates")
        self.assertIn("record_id", search_tool["inputSchema"]["properties"])
        self.assertIn("raw record ID", search_tool["description"])

    def test_admin_operations_are_not_mcp_handlers(self):
        for name in ("backup_target_bank", "reset_target_bank", "delete_target", "execute_sql"):
            self.assertNotIn(name, server.TOOL_HANDLERS)

    def test_target_runtime_contains_no_evaluator_truth_contract(self):
        root = Path(__file__).resolve().parent
        runtime_text = "\n".join((root / name).read_text(encoding="utf-8") for name in ("target_bank.py", "target_bank_admin.py", "fusion_tools.py"))
        for forbidden in ("fusion_target_truth", "truth_id", "expected_target", "evaluator_label"):
            self.assertNotIn(forbidden, runtime_text)

    def test_create_handler_assigns_moshe_and_validates_canonical_records(self):
        with tempfile.TemporaryDirectory() as directory:
            previous = server.TARGET_BANK
            server.TARGET_BANK = TargetBank(Path(directory) / "targets.db", Path(directory) / "backups")
            first, second = server.EVENTS[:2]
            arguments = {
                "candidate": {
                    "title": "Candidate", "summary": "Summary", "object_class": "vehicle",
                    "location_id": first["location_id"], "confidence": "medium",
                    "count_assessment": "unresolved", "fusion_explanation": "Two sources",
                    "mission_run_id": "mission-1",
                },
                "evidence": [
                    {
                        "record_id": first["event_id"], "source_group": "group-a", "source_type": first["source_type"],
                        "observed_at": first["timestamp_utc"], "location_id": first["location_id"],
                        "reported_object": "vehicle", "relevant_text": "First evidence snapshot", "evidence_role": "support",
                    },
                    {
                        "record_id": second["event_id"], "source_group": "group-b", "source_type": second["source_type"],
                        "observed_at": second["timestamp_utc"], "location_id": second["location_id"],
                        "reported_object": "vehicle", "relevant_text": "Second evidence snapshot", "evidence_role": "support",
                    },
                ],
            }
            try:
                created = server.create_target_candidate(arguments)["candidate"]
                self.assertEqual(created["created_by"], "moshe")
                self.assertNotEqual(created["evidence"][0]["source_group"], "group-a")
                with self.assertRaisesRegex(ValueError, "unknown event_id"):
                    server.attach_target_evidence({"target_id": created["target_id"], "evidence": [{**arguments["evidence"][0], "record_id": "TRUTH-001"}]})
            finally:
                server.TARGET_BANK = previous


if __name__ == "__main__":
    unittest.main()

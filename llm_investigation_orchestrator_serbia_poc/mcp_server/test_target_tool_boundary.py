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
    def test_mcp_registry_contains_only_constrained_target_tools(self):
        target_tools = {item["name"] for item in server.TOOLS if "target" in item["name"]}
        self.assertEqual(target_tools, {
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

    def test_admin_operations_are_not_mcp_handlers(self):
        for name in ("backup_target_bank", "reset_target_bank", "delete_target", "execute_sql"):
            self.assertNotIn(name, server.TOOL_HANDLERS)

    def test_target_runtime_contains_no_evaluator_truth_contract(self):
        root = Path(__file__).resolve().parent
        runtime_text = "\n".join((root / name).read_text(encoding="utf-8") for name in ("target_bank.py", "target_bank_admin.py"))
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
                with self.assertRaisesRegex(ValueError, "unknown evidence record_id"):
                    server.attach_target_evidence({"target_id": created["target_id"], "evidence": [{**arguments["evidence"][0], "record_id": "TRUTH-001"}]})
            finally:
                server.TARGET_BANK = previous


if __name__ == "__main__":
    unittest.main()

import os
import sqlite3
import tempfile
import unittest
from pathlib import Path

from target_bank import TargetBank


def candidate(**overrides):
    value = {
        "target_id": "TGT-TEST-001",
        "title": "Candidate title",
        "summary": "Fused candidate summary",
        "object_class": "vehicle",
        "entity_id": "ENT-001",
        "location_id": "LOC-001",
        "confidence": "medium",
        "count_min": 1,
        "count_max": 2,
        "count_estimate": 1,
        "count_assessment": "range",
        "fusion_explanation": "Two independent reports support the same final state.",
        "mission_run_id": "mission-001",
        "created_by": "moshe",
    }
    value.update(overrides)
    return value


def evidence(record_id, source_group, **overrides):
    value = {
        "record_id": record_id,
        "source_group": source_group,
        "source_type": "uav" if source_group == "uav-1" else "public-report",
        "observed_at": "2026-06-01T12:00:00Z",
        "location_id": "LOC-001",
        "reported_object": "vehicle",
        "reported_count": 1,
        "relevant_text": f"Evidence {record_id}",
        "evidence_role": "corroboration",
    }
    value.update(overrides)
    return value


class TargetBankTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        root = Path(self.temp.name)
        self.bank = TargetBank(root / "data" / "attack_targets.db", root / "backups")
        self.bank.initialize()

    def tearDown(self):
        self.temp.cleanup()

    def test_schema_is_candidate_only_and_creation_is_atomic(self):
        created = self.bank.create_candidate(candidate(), [
            evidence("REC-001", "uav-1"),
            evidence("REC-002", "public-1"),
        ])
        self.assertEqual(created["status"], "candidate")
        self.assertEqual(created["source_group_count"], 2)
        self.assertEqual(len(created["evidence"]), 2)
        connection = sqlite3.connect(self.bank.db_path)
        try:
            sql = connection.execute("SELECT sql FROM sqlite_master WHERE name = 'targets'").fetchone()[0]
        finally:
            connection.close()
        self.assertIn("CHECK(status = 'candidate')", sql)
        self.assertNotIn("approved", sql)
        self.assertNotIn("rejected", sql)

    def test_creation_rejects_one_source_group_without_partial_target(self):
        with self.assertRaisesRegex(ValueError, "two independent source groups"):
            self.bank.create_candidate(candidate(), [
                evidence("REC-001", "same-mission"),
                evidence("REC-002", "same-mission"),
            ])
        self.assertEqual(self.bank.counts(), {"targets": 0, "evidence": 0})

    def test_duplicate_evidence_rolls_back_target_and_evidence(self):
        with self.assertRaisesRegex(ValueError, "record_id values must be unique"):
            self.bank.create_candidate(candidate(), [
                evidence("REC-001", "uav-1"),
                evidence("REC-001", "public-1"),
            ])
        self.assertEqual(self.bank.counts(), {"targets": 0, "evidence": 0})

    def test_constraints_reject_low_confidence_and_invalid_counts(self):
        with self.assertRaisesRegex(ValueError, "medium or high"):
            self.bank.create_candidate(candidate(confidence="low"), [evidence("REC-1", "a"), evidence("REC-2", "b")])
        with self.assertRaisesRegex(ValueError, "cannot exceed"):
            self.bank.create_candidate(candidate(count_min=3, count_max=2), [evidence("REC-1", "a"), evidence("REC-2", "b")])

    def test_update_cannot_change_status_creator_or_review_fields(self):
        self.bank.create_candidate(candidate(), [evidence("REC-001", "a"), evidence("REC-002", "b")])
        for forbidden in ("status", "created_by", "reviewed_by", "review_note"):
            with self.assertRaisesRegex(ValueError, "unsupported candidate fields"):
                self.bank.update_candidate("TGT-TEST-001", {forbidden: "x"})
        updated = self.bank.update_candidate("TGT-TEST-001", {"confidence": "high", "summary": "Updated"})
        self.assertEqual(updated["confidence"], "high")
        self.assertEqual(updated["summary"], "Updated")

    def test_evidence_is_append_only_and_unique(self):
        self.bank.create_candidate(candidate(), [evidence("REC-001", "a"), evidence("REC-002", "b")])
        updated = self.bank.attach_evidence("TGT-TEST-001", [evidence("REC-003", "c")])
        self.assertEqual(len(updated["evidence"]), 3)
        with self.assertRaisesRegex(ValueError, "already attached"):
            self.bank.attach_evidence("TGT-TEST-001", [evidence("REC-003", "d")])
        self.assertEqual(len(self.bank.get_candidate("TGT-TEST-001")["evidence"]), 3)

    def test_parameterized_search_does_not_interpret_filter_as_sql(self):
        self.bank.create_candidate(candidate(), [evidence("REC-001", "a"), evidence("REC-002", "b")])
        self.assertEqual(self.bank.search_candidates({"object_class": "vehicle' OR 1=1 --"}), [])
        self.assertEqual(len(self.bank.search_candidates({"location_id": "LOC-001"})), 1)

    def test_backup_retains_latest_five_and_reset_requires_confirmation(self):
        self.bank.create_candidate(candidate(), [evidence("REC-001", "a"), evidence("REC-002", "b")])
        backups = [self.bank.backup() for _ in range(7)]
        self.assertEqual(len(list(self.bank.backup_dir.glob("attack_targets-*.db"))), 5)
        self.assertTrue(all(path.exists() for path in backups[-5:]))
        with self.assertRaisesRegex(ValueError, "explicit confirmation"):
            self.bank.reset(confirm=False)
        reset_backup = self.bank.reset(confirm=True)
        self.assertTrue(reset_backup.exists())
        self.assertEqual(self.bank.counts(), {"targets": 0, "evidence": 0})

    def test_restore_requires_confirmation_and_recovers_verified_counts(self):
        self.bank.create_candidate(candidate(), [evidence("REC-001", "a"), evidence("REC-002", "b")])
        source = self.bank.backup()
        self.bank.reset(confirm=True)
        self.assertEqual(self.bank.counts(), {"targets": 0, "evidence": 0})
        with self.assertRaisesRegex(ValueError, "explicit confirmation"):
            self.bank.restore(source, confirm=False)
        safety = self.bank.restore(source, confirm=True)
        self.assertTrue(safety.exists())
        self.assertEqual(self.bank.counts(), {"targets": 1, "evidence": 2})

    @unittest.skipIf(os.name == "nt", "POSIX permission bits are enforced on the production VM")
    def test_posix_permissions(self):
        self.assertEqual(self.bank.db_path.parent.stat().st_mode & 0o777, 0o700)
        self.assertEqual(self.bank.db_path.stat().st_mode & 0o777, 0o600)


if __name__ == "__main__":
    unittest.main()

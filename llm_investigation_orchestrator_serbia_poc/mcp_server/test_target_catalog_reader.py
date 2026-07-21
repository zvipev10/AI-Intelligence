import tempfile
import unittest
from pathlib import Path

from target_bank import SCHEMA
from target_catalog_reader import read_target_catalog
import sqlite3


class TargetCatalogReaderTests(unittest.TestCase):
    def test_returns_bounded_target_summaries_and_raw_references(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "targets.db"
            connection = sqlite3.connect(db_path)
            connection.executescript(SCHEMA)
            connection.execute(
                """INSERT INTO targets (
                    target_id, title, summary, status, object_class, entity_id, location_id, confidence,
                    count_min, count_max, count_estimate, count_assessment, fusion_explanation,
                    mission_run_id, created_by, created_at, updated_at, reviewed_by, reviewed_at, review_note
                ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                ("TGT-1", "Target", "Summary", "candidate", "vehicle", "ENT-1", "LOC-1", "high",
                 1, 1, 1, "exact", "Fusion", "RUN-1", "moshe", "2026-01-01Z", "2026-01-01Z", None, None, None),
            )
            evidence = ("TGT-1", "REC-1", "SG-1", "report", "2026-01-01Z", "LOC-1", "vehicle", 1,
                        "Observed", "corroboration", "2026-01-01Z")
            connection.execute("INSERT INTO target_evidence VALUES (?,?,?,?,?,?,?,?,?,?,?)", evidence)
            connection.commit()
            connection.close()

            rows = read_target_catalog(db_path)

            self.assertEqual(rows[0]["target_id"], "TGT-1")
            self.assertEqual(rows[0]["raw_data_references"], ["REC-1"])
            self.assertEqual(rows[0]["source_group_count"], 1)
            self.assertEqual(rows[0]["source_types"], ["report"])


if __name__ == "__main__":
    unittest.main()

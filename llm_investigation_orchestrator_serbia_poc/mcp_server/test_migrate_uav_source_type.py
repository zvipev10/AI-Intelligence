import sqlite3
import tempfile
import unittest
from pathlib import Path

from migrate_uav_source_type import CANONICAL_SOURCE_TYPE, LEGACY_SOURCE_TYPE, migrate


class UavSourceTypeMigrationTests(unittest.TestCase):
    def test_exact_migration_is_idempotent(self):
        with tempfile.TemporaryDirectory() as directory:
            db_path = Path(directory) / "targets.db"
            connection = sqlite3.connect(db_path)
            connection.execute("CREATE TABLE target_evidence (source_type TEXT NOT NULL)")
            connection.executemany("INSERT INTO target_evidence VALUES (?)", [(LEGACY_SOURCE_TYPE,), ("X",)])
            connection.commit()
            connection.close()

            first = migrate(db_path)
            second = migrate(db_path)

            self.assertEqual(first, {"matched": 1, "updated": 1, "legacy_remaining": 0, "canonical": 1})
            self.assertEqual(second, {"matched": 0, "updated": 0, "legacy_remaining": 0, "canonical": 1})


if __name__ == "__main__":
    unittest.main()

"""One-time exact migration to the canonical V2.1 UAV-video source type."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path


LEGACY_SOURCE_TYPE = "חיל האוויר הסרבי - ניצול וידאו מכטב״ם"
CANONICAL_SOURCE_TYPE = 'וידאו מכטב"מ'


def migrate(db_path: Path | str) -> dict[str, int]:
    connection = sqlite3.connect(Path(db_path), timeout=15)
    try:
        before = connection.execute(
            "SELECT COUNT(*) FROM target_evidence WHERE source_type = ?", (LEGACY_SOURCE_TYPE,),
        ).fetchone()[0]
        cursor = connection.execute(
            "UPDATE target_evidence SET source_type = ? WHERE source_type = ?",
            (CANONICAL_SOURCE_TYPE, LEGACY_SOURCE_TYPE),
        )
        connection.commit()
        remaining = connection.execute(
            "SELECT COUNT(*) FROM target_evidence WHERE source_type = ?", (LEGACY_SOURCE_TYPE,),
        ).fetchone()[0]
        canonical = connection.execute(
            "SELECT COUNT(*) FROM target_evidence WHERE source_type = ?", (CANONICAL_SOURCE_TYPE,),
        ).fetchone()[0]
        return {"matched": before, "updated": cursor.rowcount, "legacy_remaining": remaining, "canonical": canonical}
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    args = parser.parse_args()
    print(json.dumps(migrate(args.db), ensure_ascii=False))


if __name__ == "__main__":
    main()

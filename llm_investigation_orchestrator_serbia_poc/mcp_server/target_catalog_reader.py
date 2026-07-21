"""Bounded, read-only projection of persisted attack targets for the UI catalog."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any


MAX_ROWS = 500


def read_target_catalog(db_path: Path | str, limit: int = MAX_ROWS) -> list[dict[str, Any]]:
    bounded_limit = max(1, min(int(limit), MAX_ROWS))
    uri = Path(db_path).resolve().as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True, timeout=5)
    connection.row_factory = sqlite3.Row
    try:
        rows = connection.execute(
            """
            SELECT t.*,
                   COUNT(e.record_id) AS evidence_count,
                   COUNT(DISTINCT e.source_group) AS source_group_count,
                   GROUP_CONCAT(DISTINCT e.source_type) AS source_types_csv,
                   GROUP_CONCAT(e.record_id) AS raw_record_ids
            FROM targets AS t
            LEFT JOIN target_evidence AS e ON e.target_id = t.target_id
            GROUP BY t.target_id
            ORDER BY t.updated_at DESC, t.target_id ASC
            LIMIT ?
            """,
            (bounded_limit,),
        ).fetchall()
    finally:
        connection.close()

    result = []
    for row in rows:
        item = dict(row)
        item["source_types"] = [value for value in str(item.pop("source_types_csv") or "").split(",") if value]
        raw_ids = [value for value in str(item.pop("raw_record_ids") or "").split(",") if value]
        item["raw_data_references"] = list(dict.fromkeys(raw_ids))
        result.append(item)
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--db", required=True)
    parser.add_argument("--limit", type=int, default=MAX_ROWS)
    args = parser.parse_args()
    print(json.dumps({"rows": read_target_catalog(args.db, args.limit)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

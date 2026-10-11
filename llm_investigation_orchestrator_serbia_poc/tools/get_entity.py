#!/usr/bin/env python3
"""Read-only lookup of an i360 entity by id: its type, the record in full, its type's fields,
and the items linked to it.

    HL_API_URL=https://<platform-hl-api host> python tools/get_entity.py <entity_id> [--type PERSON]

Run it yourself, signed in with your own i360 login. Without --type it finds the type with one
cross-type search (POST /api/v1/entities/search, include_ids). Saves everything to --out.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hl.client import HlClient, HlError, list_hits  # noqa: E402


def safe(call, *args, **kwargs) -> Any:
    try:
        return call(*args, **kwargs)
    except HlError as exc:
        return {"error": exc.to_dict()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("entity_id")
    parser.add_argument("--type", default="", help="entity type, if known (otherwise found by search)")
    parser.add_argument("--username", default=os.environ.get("I360_USER"))
    parser.add_argument("--out", default="get_entity.json")
    args = parser.parse_args()

    base_url = os.environ.get("HL_API_URL", "")
    if not base_url:
        print("Set HL_API_URL first.", file=sys.stderr)
        return 2
    username = args.username or input("i360 username: ").strip()
    password = os.environ.get("I360_PASS") or getpass.getpass("i360 password: ")
    client = HlClient(base_url, HlClient(base_url).token_exchange(username, password)["access_token"])
    print(f"Signed in as {client.whoami().get('user_name')}\n")

    report: dict[str, Any] = {"entity_id": args.entity_id}
    found = safe(client.post, "/api/v1/entities/search",
                 {"include_ids": [args.entity_id], "include": ["related_item_count"], "page_number": 1, "page_size": 5},
                 read=True)
    report["cross_type_search"] = found
    hits = found.get("entities") or list_hits(found) if isinstance(found, dict) and "error" not in found else []
    entity_type = args.type or next((str(h.get("entity_type") or h.get("type") or "") for h in hits if h), "")
    if not entity_type:
        # Fallback: try the person-like types on this estate, by id.
        listing = safe(client.list_entity_types)
        entries = listing.get("entity_types") or listing.get("types") or listing.get("items") or [] if isinstance(listing, dict) else listing
        names = [str(e.get("type") or e.get("name") or "") if isinstance(e, dict) else str(e) for e in entries or []]
        report["person_like_types"] = [n for n in names if "PERSON" in n.upper()]
        for name in report["person_like_types"]:
            if "error" not in safe(client.get_entity, name, args.entity_id):
                entity_type = name
                break
    report["entity_type"] = entity_type
    if entity_type:
        report["record"] = safe(client.get_entity, entity_type, args.entity_id)
        report["type_definition"] = safe(client.get_entity_type, entity_type)
    report["related_items"] = safe(client.search_items, {
        "related_to": {"ids": [args.entity_id]},
        "time": {"from": "1970-01-01T00:00:00Z", "to": "2100-01-01T00:00:00Z", "field": "event"},
        "page_number": 1, "page_size": 20, "sort": "time", "order": "desc"})
    Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    if isinstance(found, dict) and "error" in found:
        print(f"Cross-type search failed: {found['error'].get('status')} {found['error'].get('message')}")
    print(f"Entity type: {entity_type or 'NOT FOUND'}")
    record = report.get("record") or {}
    if "error" in record:
        print(f"Record: ERROR {record['error'].get('status')} {record['error'].get('message')}")
    elif record:
        print(f"Record: {record.get('entity_name') or (record.get('general') or {}).get('entity_name') or '(no name)'}")
    related = report["related_items"]
    if "error" in related:
        print(f"Related items: ERROR {related['error'].get('status')} {related['error'].get('message')}")
    else:
        print(f"Related items: {related.get('total')}")
    print(f"\nFull answer: {Path(args.out).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

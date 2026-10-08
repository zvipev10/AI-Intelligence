#!/usr/bin/env python3
"""Read-only: describe one i360 entity type, so the app can be mapped onto it.

Run it yourself, signed in with your own i360 login:

    HL_API_URL=https://<platform-hl-api host> python tools/describe_entity_type.py intelligence_investigation

It reads the type definition (sections, fields, title path), how many records you can see, and a
couple of sample records with each value cut to 80 characters. It also lists the entity types
whose name contains "investigation", in case the name differs. Nothing is written to i360.
The report goes to describe_<type>.json next to where you run it.
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


def trimmed(value: Any, limit: int = 80) -> Any:
    if isinstance(value, dict):
        return {key: trimmed(item, limit) for key, item in value.items()}
    if isinstance(value, list):
        return [trimmed(item, limit) for item in value[:5]]
    if isinstance(value, str) and len(value) > limit:
        return value[:limit] + "…"
    return value


def type_names(listing: Any) -> list[str]:
    entries = listing if isinstance(listing, list) else []
    if isinstance(listing, dict):
        entries = list_hits(listing) or next((v for v in listing.values() if isinstance(v, list)), [])
    names = []
    for entry in entries:
        name = entry if isinstance(entry, str) else (entry.get("type") or entry.get("type_name") or entry.get("name"))
        if name:
            names.append(str(name))
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("type_name", nargs="?", default="intelligence_investigation")
    parser.add_argument("--samples", type=int, default=2, help="sample records to include (default 2, 0 for none)")
    parser.add_argument("--username", default=os.environ.get("I360_USER"))
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    base_url = os.environ.get("HL_API_URL", "")
    if not base_url:
        print("Set HL_API_URL first.", file=sys.stderr)
        return 2
    username = args.username or input("i360 username: ").strip()
    password = os.environ.get("I360_PASS") or getpass.getpass("i360 password: ")
    token = HlClient(base_url).token_exchange(username, password)["access_token"]
    client = HlClient(base_url, token)
    print(f"Signed in as {client.whoami().get('user_name')}")

    listing = safe(client.list_entity_types)
    names = type_names(listing) if "error" not in (listing if isinstance(listing, dict) else {}) else []
    search = safe(client.search_entities, args.type_name, {"page_number": 1, "page_size": max(args.samples, 1)})
    report: dict[str, Any] = {
        "type_name": args.type_name,
        "similar_types": sorted(name for name in names if "investigat" in name.lower()),
        "definition": safe(client.get_entity_type, args.type_name),
        "visible_records": (search.get("total", len(list_hits(search))) if "error" not in search else search),
        "samples": [trimmed(hit) for hit in list_hits(search)[: args.samples]] if "error" not in search else [],
    }
    if isinstance(listing, dict) and "error" in listing:
        report["type_listing_error"] = listing["error"]

    out = Path(args.out or f"describe_{args.type_name}.json")
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    definition = report["definition"]
    print(f"Similar types: {', '.join(report['similar_types']) or '-'}")
    if "error" in definition:
        print(f"Definition: {definition['error']}")
    else:
        for section in definition.get("sections") or []:
            fields = ", ".join(f"{f.get('name')}:{f.get('type')}" for f in section.get("fields") or [])
            print(f"Section {section.get('name')}: {fields}")
    print(f"Records you can see: {report['visible_records']}")
    print(f"\nFull report: {out.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

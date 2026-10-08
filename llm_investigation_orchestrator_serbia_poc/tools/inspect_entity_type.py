#!/usr/bin/env python3
"""Read-only look at one i360 entity type: its definition, a few instances, and what links to them.

Run it yourself, signed in with your own i360 login:

    HL_API_URL=https://<platform-hl-api host> python tools/inspect_entity_type.py intelligence_investigation

It never writes. It prints a short summary and saves the full answers to --out (default
inspect_<type>.json) so the app's mapping can be written from them.
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


def type_names(listing: Any) -> list[str]:
    entries = listing.get("entity_types") or listing.get("types") or listing.get("items") or [] if isinstance(listing, dict) else listing
    names = []
    for entry in entries or []:
        if isinstance(entry, str):
            names.append(entry)
        elif isinstance(entry, dict):
            names.append(str(entry.get("type") or entry.get("type_name") or entry.get("name") or ""))
    return [name for name in names if name]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("entity_type", help="type name to inspect, e.g. intelligence_investigation")
    parser.add_argument("--samples", type=int, default=5, help="instances to fetch (default 5)")
    parser.add_argument("--username", default=os.environ.get("I360_USER"))
    parser.add_argument("--out", default="")
    args = parser.parse_args()

    base_url = os.environ.get("HL_API_URL", "")
    if not base_url:
        print("Set HL_API_URL first.", file=sys.stderr)
        return 2
    username = args.username or input("i360 username: ").strip()
    password = os.environ.get("I360_PASS") or getpass.getpass("i360 password: ")
    client = HlClient(base_url, HlClient(base_url).token_exchange(username, password)["access_token"])
    print(f"Signed in as {client.whoami().get('user_name')}")

    listing = safe(client.list_entity_types)
    names = type_names(listing) if "error" not in (listing if isinstance(listing, dict) else {}) else []
    wanted = args.entity_type.lower()
    matches = [name for name in names if name.lower() == wanted] or [name for name in names if wanted in name.lower()]
    related = [name for name in names if "investigation" in name.lower()]
    type_name = matches[0] if matches else args.entity_type

    report: dict[str, Any] = {
        "requested": args.entity_type,
        "resolved_type": type_name,
        "all_type_count": len(names),
        "types_named_like_investigation": related,
        "entity_types_listing_error": listing.get("error") if isinstance(listing, dict) else None,
        "definition": safe(client.get_entity_type, type_name),
        "docs_entities": safe(client.get, "/api/v1/meta/docs", params={"q": "dynamic entity investigation search instances"}),
    }
    instances = safe(client.search_entities, type_name, {"page_number": 1, "page_size": max(1, args.samples)})
    report["instances_total"] = instances.get("total") if "error" not in instances else None
    report["instances"] = instances if "error" in instances else list_hits(instances)
    if isinstance(report["instances"], list) and report["instances"]:
        first = report["instances"][0]
        entity_id = first.get("entity_id") or first.get("id")
        if entity_id:
            report["first_instance_full"] = safe(client.get_entity, type_name, str(entity_id))
            report["items_related_to_first"] = safe(client.search_items, {
                "related_to": [str(entity_id)], "page_number": 1, "page_size": 5})

    out = Path(args.out or f"inspect_{type_name}.json")
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    print(f"\nTypes on this estate: {len(names)}; named like 'investigation': {', '.join(related) or '-'}")
    print(f"Inspected type: {type_name}")
    definition = report["definition"]
    print("Definition:", "ERROR " + json.dumps(definition["error"]) if "error" in definition else "ok")
    print(f"Instances: {report['instances_total']}")
    related_items = report.get("items_related_to_first") or {}
    if related_items:
        print("Items related to the first instance:",
              "ERROR " + json.dumps(related_items["error"]) if "error" in related_items else related_items.get("total"))
    print(f"\nFull report: {out.resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

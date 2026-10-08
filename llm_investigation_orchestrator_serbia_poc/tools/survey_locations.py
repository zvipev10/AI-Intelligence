#!/usr/bin/env python3
"""Read-only survey: which i360 items on an estate carry a geographic location.

Run it yourself, signed in with your own i360 login:

    HL_API_URL=https://<platform-hl-api host> python tools/survey_locations.py

It only reads (search, capabilities, docs). For each item type it counts how many of the scanned
items have a location, and keeps a few sample locations and a bounding box. It also saves the
platform's own docs on searching by place, so the app can filter by location later.
The report goes to survey_locations.json next to where you run it; it holds no item text.
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hl.client import HlClient, HlError, list_hits  # noqa: E402

LAT_KEYS = ("lat", "latitude", "y")
LON_KEYS = ("lon", "lng", "long", "longitude", "x")


def coordinates(location: Any) -> tuple[float, float] | None:
    """Best-effort (lat, lon) from whatever shape the platform uses for a location."""
    if not isinstance(location, dict):
        return None
    for nested in ("point", "geo", "coordinates", "center", "centroid"):
        value = location.get(nested)
        if isinstance(value, dict):
            found = coordinates(value)
            if found:
                return found
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            try:
                return float(value[1]), float(value[0])  # GeoJSON order: lon, lat
            except (TypeError, ValueError):
                pass
    lat = next((location[k] for k in LAT_KEYS if location.get(k) not in (None, "")), None)
    lon = next((location[k] for k in LON_KEYS if location.get(k) not in (None, "")), None)
    try:
        return (float(lat), float(lon)) if lat is not None and lon is not None else None
    except (TypeError, ValueError):
        return None


def safe(call, *args, **kwargs) -> Any:
    try:
        return call(*args, **kwargs)
    except HlError as exc:
        return {"error": exc.to_dict()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--days", type=int, default=3650, help="how far back to look (default about 10 years)")
    parser.add_argument("--pages", type=int, default=20, help="pages of 100 items to scan (default 20)")
    parser.add_argument("--username", default=os.environ.get("I360_USER"))
    parser.add_argument("--out", default="survey_locations.json")
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

    report: dict[str, Any] = {
        "estate": safe(client.estate),
        "capabilities": safe(client.get, "/api/v1/items/search/capabilities"),
        "docs_searching_items": safe(client.get, "/api/v1/meta/docs/searching-items"),
        "docs_location_query": safe(client.get, "/api/v1/meta/docs", params={"q": "location place geo"}),
    }

    now = datetime.now(timezone.utc)
    window = {"from": (now - timedelta(days=args.days)).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "to": now.strftime("%Y-%m-%dT%H:%M:%SZ"), "field": "event"}

    # Ask the platform directly for items that have a location; the hint says so if it can't.
    probe = safe(client.search_items, {"time": window, "filters": [{"field": "location", "exists": True}],
                                        "page_number": 1, "page_size": 1})
    report["location_filter_probe"] = probe if "error" in probe else {
        "total": probe.get("total"), "total_semantics": probe.get("total_semantics")}

    per_type: dict[str, dict[str, Any]] = defaultdict(lambda: {
        "scanned": 0, "with_location": 0, "sources": set(), "samples": [], "bbox": None, "first": None, "last": None})
    overall_total = None
    for page in range(1, args.pages + 1):
        response = safe(client.search_items, {"time": window, "page_number": page, "page_size": 100,
                                               "sort": "time", "order": "desc"})
        if "error" in response:
            report["scan_error"] = response["error"]
            break
        overall_total = response.get("total", overall_total)
        hits = list_hits(response)
        for hit in hits:
            entry = per_type[str(hit.get("item_type") or "unknown")]
            entry["scanned"] += 1
            if hit.get("source_application"):
                entry["sources"].add(str(hit["source_application"]))
            stamp = hit.get("event_time")
            if stamp:
                entry["first"] = min(filter(None, [entry["first"], stamp]))
                entry["last"] = max(filter(None, [entry["last"], stamp]))
            point = coordinates(hit.get("location"))
            if not point:
                continue
            entry["with_location"] += 1
            if len(entry["samples"]) < 3:
                entry["samples"].append({"item_id": hit.get("item_id"), "location": hit.get("location")})
            lat, lon = point
            box = entry["bbox"] or [lat, lon, lat, lon]
            entry["bbox"] = [min(box[0], lat), min(box[1], lon), max(box[2], lat), max(box[3], lon)]
        if page >= int(response.get("total_pages") or page):
            break

    report["time_window"] = window
    report["total_items_in_window"] = overall_total
    report["item_types"] = {name: {**entry, "sources": sorted(entry["sources"])}
                            for name, entry in sorted(per_type.items(), key=lambda kv: -kv[1]["with_location"])}
    Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    print(f"\nItems in window: {overall_total}")
    if "error" not in probe:
        print(f"Items the platform says have a location: {probe.get('total')}")
    print(f"{'item type':32} {'scanned':>8} {'located':>8}  bbox (lat/lon min .. max)")
    for name, entry in report["item_types"].items():
        box = entry["bbox"]
        span = f"{box[0]:.3f},{box[1]:.3f} .. {box[2]:.3f},{box[3]:.3f}" if box else "-"
        print(f"{name[:32]:32} {entry['scanned']:>8} {entry['with_location']:>8}  {span}")
    print(f"\nFull report: {Path(args.out).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

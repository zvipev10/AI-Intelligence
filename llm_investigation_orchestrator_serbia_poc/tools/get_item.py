#!/usr/bin/env python3
"""Read-only lookup of i360 items by id: type, source, time, location and files.

    HL_API_URL=https://<platform-hl-api host> python tools/get_item.py <item_id> [<item_id> ...]

Run it yourself, signed in with your own i360 login. Prints a summary per id and saves the
full answers to --out (default get_item.json).
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hl.client import HlClient, HlError  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("item_ids", nargs="+")
    parser.add_argument("--username", default=os.environ.get("I360_USER"))
    parser.add_argument("--out", default="get_item.json")
    args = parser.parse_args()

    base_url = os.environ.get("HL_API_URL", "")
    if not base_url:
        print("Set HL_API_URL first.", file=sys.stderr)
        return 2
    username = args.username or input("i360 username: ").strip()
    password = os.environ.get("I360_PASS") or getpass.getpass("i360 password: ")
    client = HlClient(base_url, HlClient(base_url).token_exchange(username, password)["access_token"])
    print(f"Signed in as {client.whoami().get('user_name')}\n")

    try:
        response = client.get_items(args.item_ids, ["parties", "locations", "source_details"])
    except HlError as exc:
        print(f"items/get failed: {exc.status} {exc}")
        Path(args.out).write_text(json.dumps({"items_get_error": exc.to_dict()}, indent=2, ensure_ascii=False), encoding="utf-8")
        print(f"\nFull answer: {Path(args.out).resolve()}")
        return 1
    by_id = {str(item.get("item_id")): item for item in response.get("items") or []}
    report = {"warnings": response.get("warnings"), "items": {}}
    for item_id in args.item_ids:
        item = by_id.get(item_id)
        if not item or item.get("found") is False:
            print(f"{item_id}: NOT FOUND (or not visible to this user)")
            report["items"][item_id] = item or {"found": False}
            continue
        try:
            files = client.item_files(item_id)
        except HlError as exc:
            files = {"error": exc.to_dict()}
        report["items"][item_id] = {"item": item, "files": files}
        location = item.get("location") or {}
        point = location.get("point") if isinstance(location, dict) else None
        file_count = len(files.get("files") or files.get("items") or []) if isinstance(files, dict) else 0
        print(f"{item_id}: FOUND")
        print(f"  type={item.get('item_type')}  source={item.get('source_application')}  event_time={item.get('event_time')}")
        print(f"  location={point or 'none'}  files={file_count if 'error' not in files else files['error'].get('status')}")
    Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")
    print(f"\nFull answer: {Path(args.out).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

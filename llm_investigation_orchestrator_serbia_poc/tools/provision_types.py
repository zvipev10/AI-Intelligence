#!/usr/bin/env python3
"""Create the app's three entity types on an i360 estate, with one publish.

Run it yourself, signed in with your i360 building login (not an admin account):

    HL_API_URL=https://<platform-hl-api host> python tools/provision_types.py            # dry run
    HL_API_URL=https://<platform-hl-api host> python tools/provision_types.py --apply    # one publish

Steps, as the HL API skill prescribes: look before you create (``GET /entity-types``), dry run
first, then ONE batch publish. A publish restarts platform services for everyone on the estate,
so ``--apply`` asks for confirmation. Types that already exist are left alone.
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
from hl.state import type_definitions  # noqa: E402


def existing_types(client: HlClient) -> set[str]:
    listing = client.list_entity_types()
    entries = listing.get("entity_types") or listing.get("types") or listing.get("items") or [] if isinstance(listing, dict) else listing
    names = set()
    for entry in entries or []:
        if isinstance(entry, str):
            names.add(entry)
        elif isinstance(entry, dict):
            names.add(str(entry.get("type") or entry.get("type_name") or entry.get("name") or ""))
    return names


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="publish (default is a dry run)")
    parser.add_argument("--prefix", default=os.environ.get("APP_TYPE_PREFIX", "AII_"))
    parser.add_argument("--grant-profile", default=None, help="permission profile to grant the types in")
    parser.add_argument("--username", default=os.environ.get("I360_USER"))
    parser.add_argument("--yes", action="store_true", help="do not ask before publishing")
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

    definitions = type_definitions(args.prefix)
    if args.grant_profile:
        for definition in definitions:
            definition["grant_profile"] = args.grant_profile
    present = existing_types(client)
    missing = [d for d in definitions if d["type"] not in present]
    for definition in definitions:
        print(f"  {definition['type']}: {'exists, left alone' if definition['type'] in present else 'to create'}")
    if not missing:
        print("Nothing to create.")
        return 0

    plan = client.batch_create_entity_types({"types": missing}, dry_run=True)
    print("Dry run:")
    print(json.dumps(plan, indent=2, ensure_ascii=False)[:4000])
    if not args.apply:
        print("\nDry run only. Re-run with --apply to publish.")
        return 0
    if not args.yes and input("Publish now? This restarts platform services for everyone (type 'publish'): ").strip() != "publish":
        print("Not published.")
        return 1
    try:
        result = client.batch_create_entity_types({"types": missing}, dry_run=False)
    except HlError as exc:
        # Never blind-retry a write: read the hint and check the estate before trying again.
        print(f"Publish failed: {exc} ({exc.code}). Hint: {exc.hint}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, ensure_ascii=False)[:4000])
    not_ready = [t.get("type") for t in result.get("types") or [] if not t.get("instance_ready")]
    if not_ready:
        print(f"\nNot ready yet: {', '.join(not_ready)}. Wait about two minutes, then check "
              "GET /api/v1/entity-types/<type>/status before using them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

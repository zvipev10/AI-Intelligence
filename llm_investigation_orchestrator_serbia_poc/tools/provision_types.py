#!/usr/bin/env python3
"""Create the app's three entity types on an i360 estate, with one publish.

Run it yourself, signed in with your i360 building login (not an admin account):

    HL_API_URL=https://<platform-hl-api host> python tools/provision_types.py --grant-profile <profile>            # dry run
    HL_API_URL=https://<platform-hl-api host> python tools/provision_types.py --grant-profile <profile> --apply    # one publish

Steps, as the HL API skill prescribes: look before you create (``GET /entity-types``), dry run
first, then ONE batch publish. A publish restarts platform services for everyone on the estate,
so ``--apply`` asks for confirmation. Types that already exist are left alone.

To let a profile read a type that already exists (e.g. INTELLIGENCE_INVESTIGATION), use
``--grant-existing``. It creates nothing; the dry run prints HL API's access-control docs, checks
the profile name, and shows the exact request. Only ``--apply`` sends it:

    HL_API_URL=... python tools/provision_types.py --grant-profile <profile> --grant-existing INTELLIGENCE_INVESTIGATION
    HL_API_URL=... python tools/provision_types.py --grant-profile <profile> --grant-existing INTELLIGENCE_INVESTIGATION --apply
"""
from __future__ import annotations

import argparse
import getpass
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hl.client import HlClient, HlError, list_hits  # noqa: E402
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


def profile_names(client: HlClient) -> list[str] | None:
    """Permission profiles the signed-in user can see, or None when HL API will not list them."""
    try:
        response = client.search_entities("PERMISSION_PROFILE", {"page_number": 1, "page_size": 100})
    except HlError:
        return None
    names = []
    for hit in list_hits(response):
        name = hit.get("entity_name") or (hit.get("general") or {}).get("entity_name") or hit.get("name")
        if name:
            names.append(str(name))
    return names


def grant_existing(client: HlClient, args: argparse.Namespace) -> int:
    type_names = [name.strip() for name in args.grant_existing.split(",") if name.strip()]
    permissions = args.permission or ["VIEW"]
    docs = None
    for path, params in (("/api/v1/meta/docs/access-control", None), ("/api/v1/meta/docs", {"q": "grants permission profile"})):
        try:
            docs = client.get(path, params=params)
            break
        except HlError:
            continue
    if docs is not None:
        print("HL API access-control docs (check the request shape below against them):")
        print((docs if isinstance(docs, str) else json.dumps(docs, indent=2, ensure_ascii=False))[:3000])
    profiles = profile_names(client)
    if profiles is None:
        print("\nCould not list permission profiles; check the profile name yourself.")
    elif args.grant_profile not in profiles:
        print(f"\nProfile {args.grant_profile!r} not found. Profiles you can see: {', '.join(sorted(profiles)) or '-'}")
        return 1
    present = existing_types(client)
    requests = []
    for type_name in type_names:
        if type_name not in present:
            print(f"  {type_name}: not on this estate, skipped")
            continue
        body = {"profile": args.grant_profile, "permissions": permissions}
        requests.append((type_name, body))
        print(f"  POST /api/v1/entity-types/{type_name}/grants {json.dumps(body)}")
    if not requests:
        return 1
    if not args.apply:
        print("\nDry run only: nothing was sent. Re-run with --apply to grant.")
        return 0
    if not args.yes and input("Grant now? This changes who can see these records, and may publish and restart "
                              "platform services for everyone (type 'grant'): ").strip() != "grant":
        print("Not granted.")
        return 1
    for type_name, body in requests:
        try:
            result = client.grant_entity_type(type_name, body)
        except HlError as exc:
            # Never blind-retry a permission write: read the hint, then fix the request.
            print(f"{type_name}: grant failed: {exc} ({exc.code}). Hint: {exc.hint}", file=sys.stderr)
            return 1
        print(f"{type_name}: {json.dumps(result, ensure_ascii=False)[:2000]}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--apply", action="store_true", help="publish (default is a dry run)")
    parser.add_argument("--prefix", default=os.environ.get("APP_TYPE_PREFIX", "AII_"))
    parser.add_argument("--grant-profile", required=True,
                        help="permission profile your analysts are in (HL API defaults to Superuser, which most users are not in)")
    parser.add_argument("--grant-existing", default="",
                        help="comma-separated existing types to grant to --grant-profile instead of creating the app's types")
    parser.add_argument("--permission", action="append", choices=["VIEW", "CREATE", "EDIT", "DELETE"],
                        help="with --grant-existing; repeat for several (default VIEW)")
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
    if args.grant_existing:
        return grant_existing(client, args)

    definitions = type_definitions(args.prefix)
    for definition in definitions:
        definition["grant_profile"] = args.grant_profile
        definition["create_sample_instance"] = False
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

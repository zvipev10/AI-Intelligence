#!/usr/bin/env python3
"""Create demo investigations in an i360 investigation type, one per welcome-page card.

The app's welcome page sorts i360 investigations by ``investigation_details.status``:
``invited`` -> "Invited", ``recommended`` -> "Recommended", anything else -> "My investigations".
This creates the same investigations the app shows locally, so every section comes from i360.

Run it yourself, signed in with your own i360 login:

    HL_API_URL=https://<platform-hl-api host> python tools/seed_investigations.py            # dry run
    HL_API_URL=https://<platform-hl-api host> python tools/seed_investigations.py --apply    # create

Records carry fixed entity_ids (aii-demo-...), so running it again skips what already exists.
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

DETAILS = "investigation_details"

DEMO_INVESTIGATIONS = [
    {"entity_id": "aii-demo-tel-aviv-tracking", "entity_name": "Tracking devices around Tel Aviv",
     "status": "active", "activity_level": "High",
     "research_question": "Which tracked devices share movement patterns around Tel Aviv, and where do they stop?",
     "next_milstone": "Group stops into places and review the top five"},
    {"entity_id": "aii-demo-ankle-bracelet", "entity_name": "Ankle bracelet location review",
     "status": "active", "activity_level": "Medium",
     "research_question": "Do ankle-bracelet tracks show visits outside the permitted areas?",
     "next_milstone": "Mark permitted areas on the map"},
    {"entity_id": "aii-demo-military-convoy", "entity_name": "Suspicious military convoy",
     "status": "invited", "activity_level": "High",
     "research_question": "A collaborative investigation of convoy observations, vehicle movement, and supporting visual sources.",
     "next_milstone": "Join the VISINT team's review"},
    {"entity_id": "aii-demo-regional-infrastructure", "entity_name": "Critical infrastructure in North Kosovo",
     "status": "recommended", "activity_level": "Medium",
     "research_question": "Regional monitoring of disruptions, roadblocks, and activity around critical infrastructure.",
     "next_milstone": "High geographic overlap with your work"},
    {"entity_id": "aii-demo-cross-border-movement", "entity_name": "Cross-border movement in the Western Balkans",
     "status": "recommended", "activity_level": "High",
     "research_question": "A collaborative investigation of movement reports, transit routes, and escalation indicators.",
     "next_milstone": "Shared topics and sources"},
    {"entity_id": "aii-demo-information-environment", "entity_name": "Regional information and influence environment",
     "status": "recommended", "activity_level": "Low",
     "research_question": "Identifying coordinated narratives, recurring rumors, and relationships between distribution channels.",
     "next_milstone": "Matches your expertise"},
]


def body_for(record: dict) -> dict:
    details = {key: record[key] for key in ("research_question", "next_milstone", "activity_level", "status")}
    return {"entity_id": record["entity_id"], "entity_name": record["entity_name"], "sections": {DETAILS: details}}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--type", default=os.environ.get("APP_INVESTIGATION_TYPE") or "INTELLIGENCE_INVESTIGATION")
    parser.add_argument("--apply", action="store_true", help="create the records (default is a dry run)")
    parser.add_argument("--username", default=os.environ.get("I360_USER"))
    args = parser.parse_args()

    if not args.apply:
        print(f"Dry run: would create these {args.type} records (existing ids are skipped):\n")
        for record in DEMO_INVESTIGATIONS:
            print(json.dumps(body_for(record), ensure_ascii=False))
        print("\nAdd --apply to create them.")
        return 0

    base_url = os.environ.get("HL_API_URL", "")
    if not base_url:
        print("Set HL_API_URL first.", file=sys.stderr)
        return 2
    username = args.username or input("i360 username: ").strip()
    password = os.environ.get("I360_PASS") or getpass.getpass("i360 password: ")
    client = HlClient(base_url, HlClient(base_url).token_exchange(username, password)["access_token"])
    print(f"Signed in as {client.whoami().get('user_name')}")

    failures = 0
    for record in DEMO_INVESTIGATIONS:
        label = f"{record['status']:12} {record['entity_name']}"
        try:
            client.get_entity(args.type, record["entity_id"])
            print(f"exists   {label}")
            continue
        except HlError as exc:
            if exc.status not in {400, 404}:
                print(f"FAILED   {label}: {exc.status} {exc}")
                failures += 1
                continue
        try:
            client.create_entity(args.type, body_for(record))
            client.get_entity(args.type, record["entity_id"])  # read back before reporting success
            print(f"created  {label}")
        except HlError as exc:
            print(f"FAILED   {label}: {exc.status} {exc}")
            failures += 1
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())

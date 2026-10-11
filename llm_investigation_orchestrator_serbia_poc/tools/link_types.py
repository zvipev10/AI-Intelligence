#!/usr/bin/env python3
"""Read-only: which i360 link types join two entity types, with their side names.

    HL_API_URL=https://<platform-hl-api host> python tools/link_types.py INTELLIGENCE_INVESTIGATION PERSON_OF_INTEREST

Run it yourself, signed in with your own i360 login. Uses GET /api/v1/link-types?between=A,B&include=sides
(and, for context, every link type that relates to A). Saves the answers to --out.
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

from hl.client import HlClient, HlError  # noqa: E402


def safe(call, *args, **kwargs) -> Any:
    try:
        return call(*args, **kwargs)
    except HlError as exc:
        return {"error": exc.to_dict()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("type_a")
    parser.add_argument("type_b")
    parser.add_argument("--username", default=os.environ.get("I360_USER"))
    parser.add_argument("--out", default="link_types.json")
    args = parser.parse_args()

    base_url = os.environ.get("HL_API_URL", "")
    if not base_url:
        print("Set HL_API_URL first.", file=sys.stderr)
        return 2
    username = args.username or input("i360 username: ").strip()
    password = os.environ.get("I360_PASS") or getpass.getpass("i360 password: ")
    client = HlClient(base_url, HlClient(base_url).token_exchange(username, password)["access_token"])
    print(f"Signed in as {client.whoami().get('user_name')}\n")

    report = {
        "between": safe(client.get, "/api/v1/link-types", params={"between": f"{args.type_a},{args.type_b}", "include": "sides"}),
        "related_to_a": safe(client.get, "/api/v1/link-types", params={"between": args.type_a, "include": "sides"}),
    }
    Path(args.out).write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str), encoding="utf-8")

    for title, answer in (("Joining both types", report["between"]), (f"Relating to {args.type_a}", report["related_to_a"])):
        if isinstance(answer, dict) and "error" in answer:
            print(f"{title}: ERROR {answer['error'].get('status')} {answer['error'].get('message')}")
            continue
        sides = (answer.get("sides") if isinstance(answer, dict) else None) or []
        print(f"{title}: {len(sides)}")
        for entry in sides[:20]:
            ends = " / ".join(f"{s.get('field')}={s.get('entity_types') or 'any'}" for s in entry.get("sides") or [])
            print(f"  {entry.get('link_type')} ({entry.get('display_name')}): {ends}")
    print(f"\nFull answer: {Path(args.out).resolve()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

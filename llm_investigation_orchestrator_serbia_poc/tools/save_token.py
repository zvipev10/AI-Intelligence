#!/usr/bin/env python3
"""Sign in to HL API once and save the bearer token for the other tools.

    HL_API_URL=https://<platform-hl-api host> python tools/save_token.py --username manager

You type the password at the prompt; it is not stored. Only the token is written, to
~/.i360_token (or I360_TOKEN_FILE), readable by your Windows account only. The tools then use it
until it expires (HL API's expires_in), after which you run this again.
"""
from __future__ import annotations

import argparse
import getpass
import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hl.client import HlClient  # noqa: E402
from tools.auth import TOKEN_FILE  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--username", default=os.environ.get("I360_USER"))
    args = parser.parse_args()
    base_url = os.environ.get("HL_API_URL", "")
    if not base_url:
        print("Set HL_API_URL first.", file=sys.stderr)
        return 2
    username = args.username or input("i360 username: ").strip()
    answer = HlClient(base_url).token_exchange(username, getpass.getpass("i360 password: "))
    TOKEN_FILE.write_text(answer["access_token"], encoding="utf-8")
    if os.name == "nt":  # owner-only: drop inherited permissions, grant the current user full control
        user = f"{os.environ.get('USERDOMAIN', '')}\\{os.environ.get('USERNAME', '')}".lstrip("\\")
        subprocess.run(["icacls", str(TOKEN_FILE), "/inheritance:r", "/grant:r", f"{user}:F"],
                       check=False, capture_output=True)
    else:
        TOKEN_FILE.chmod(0o600)
    who = HlClient(base_url, answer["access_token"]).whoami().get("user_name")
    print(f"Saved a token for {who} to {TOKEN_FILE}; it expires in {answer.get('expires_in', '?')} seconds.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""How the command-line tools sign in to HL API, without each tool asking for a password.

In order, the first that is available wins:

1. ``I360_TOKEN`` or the token file (``I360_TOKEN_FILE``, default ``~/.i360_token``): a bearer token
   saved by ``tools/save_token.py``, which a person runs once and signs in to. Used until it expires.
2. ``I360_CLIENT_ID`` + ``I360_CLIENT_SECRET`` (or the JSON file ``I360_CLIENT_FILE``, default
   ``~/.i360_client.json`` with ``client_id`` / ``client_secret``): OAuth client credentials an i360
   operator issued for a program (``grant_type=client_credentials``). A fresh token per run.
3. A person's sign-in: username and password typed at the prompt.
"""
from __future__ import annotations

import getpass
import json
import os
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from hl.client import HlClient, HlError  # noqa: E402

TOKEN_FILE = Path(os.environ.get("I360_TOKEN_FILE") or Path.home() / ".i360_token")
CLIENT_FILE = Path(os.environ.get("I360_CLIENT_FILE") or Path.home() / ".i360_client.json")


def _saved_token() -> str:
    token = os.environ.get("I360_TOKEN", "").strip()
    if not token and TOKEN_FILE.is_file():
        token = TOKEN_FILE.read_text(encoding="utf-8").strip()
    return token


def _client_credentials() -> tuple[str, str]:
    client_id = os.environ.get("I360_CLIENT_ID", "").strip()
    secret = os.environ.get("I360_CLIENT_SECRET", "").strip()
    if not (client_id and secret) and CLIENT_FILE.is_file():
        data: dict[str, Any] = json.loads(CLIENT_FILE.read_text(encoding="utf-8"))
        client_id, secret = str(data.get("client_id") or ""), str(data.get("client_secret") or "")
    return client_id, secret


def signed_in_client(base_url: str, username: str | None = None) -> HlClient:
    token = _saved_token()
    if token:
        client = HlClient(base_url, token)
        try:
            print(f"Signed in as {client.whoami().get('user_name')} (saved token)")
            return client
        except HlError as exc:
            print(f"The saved token no longer works ({exc.status}); run tools/save_token.py again.", file=sys.stderr)
    client_id, secret = _client_credentials()
    if client_id and secret:
        answer = HlClient(base_url)._request("POST", "/api/v1/auth/token", form={
            "grant_type": "client_credentials", "client_id": client_id, "client_secret": secret})
        client = HlClient(base_url, answer["access_token"])
        print(f"Signed in as {client.whoami().get('user_name')} (client credentials)")
        return client
    username = username or os.environ.get("I360_USER") or input("i360 username: ").strip()
    password = os.environ.get("I360_PASS") or getpass.getpass("i360 password: ")
    client = HlClient(base_url, HlClient(base_url).token_exchange(username, password)["access_token"])
    print(f"Signed in as {client.whoami().get('user_name')}")
    return client

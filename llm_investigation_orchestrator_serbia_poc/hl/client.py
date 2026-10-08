"""Thin HTTP client for platform-hl-api.

Rules taken from the HL API documentation (contract 252):
- every call except the token exchange carries ``Authorization: Bearer <token>``;
- every error has one envelope with a ``hint`` naming the next action;
- 401 means the token is gone (sign in again), 501 means this estate lacks the feature;
- never blind-retry a write. Only reads are retried, and only on transport errors or 502-504.
"""
from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.parse
import urllib.request
from typing import Any


class HlError(Exception):
    def __init__(self, status: int, code: str = "", message: str = "", hint: str = "", body: Any = None):
        self.status = status
        self.code = code or f"http_{status}"
        self.hint = hint
        self.body = body
        super().__init__(message or self.code)

    def to_dict(self) -> dict[str, Any]:
        return {"error": self.code, "message": str(self), "hint": self.hint, "status": self.status}


class AuthExpired(HlError):
    """The token is missing, expired or revoked. The user has to sign in again."""


class NotOnThisEstate(HlError):
    """501: this deployment does not run the feature. Not a bug, not worth retrying."""


class Unreachable(HlError):
    """The API could not be reached at all."""


def _parse_error(status: int, raw: bytes) -> HlError:
    body: Any = None
    code = message = hint = ""
    try:
        body = json.loads(raw.decode("utf-8")) if raw else None
    except (UnicodeDecodeError, json.JSONDecodeError):
        body = raw.decode("utf-8", "replace")[:500] if raw else None
    if isinstance(body, dict):
        envelope = body.get("error") if isinstance(body.get("error"), dict) else body
        code = str(envelope.get("code") or (body.get("error") if isinstance(body.get("error"), str) else "") or "")
        message = str(envelope.get("message") or envelope.get("detail") or body.get("error_description") or "")
        hint = str(envelope.get("hint") or "")
        if isinstance(body.get("detail"), (list, dict)) and not message:
            message = json.dumps(body["detail"])[:500]
    cls = AuthExpired if status == 401 else NotOnThisEstate if status == 501 else HlError
    return cls(status, code, message, hint, body)


class HlClient:
    READ_RETRIES = 2

    def __init__(self, base_url: str, token: str | None = None, timeout: int = 30):
        if not base_url:
            raise ValueError("HL_API_URL is not configured")
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.timeout = timeout

    # -- transport -----------------------------------------------------------------
    def _request(self, method: str, path: str, *, json_body: Any = None, form: dict | None = None,
                 params: dict | None = None, read: bool = False, raw: bool = False,
                 headers: dict | None = None) -> Any:
        url = self.base_url + path
        if params:
            url += "?" + urllib.parse.urlencode({k: v for k, v in params.items() if v is not None}, doseq=True)
        data = None
        request_headers = {"Accept": "application/json"}
        if json_body is not None:
            data = json.dumps(json_body).encode("utf-8")
            request_headers["Content-Type"] = "application/json"
        elif form is not None:
            data = urllib.parse.urlencode(form).encode("utf-8")
            request_headers["Content-Type"] = "application/x-www-form-urlencoded"
        if self.token:
            request_headers["Authorization"] = f"Bearer {self.token}"
        request_headers.update(headers or {})
        attempts = 1 + (self.READ_RETRIES if read else 0)
        last: HlError | None = None
        for attempt in range(attempts):
            req = urllib.request.Request(url, data=data, method=method, headers=request_headers)
            try:
                with urllib.request.urlopen(req, timeout=self.timeout) as response:
                    payload = response.read()
                    if raw:
                        return payload, response.headers
                    if not payload:
                        return {}
                    return json.loads(payload.decode("utf-8"))
            except urllib.error.HTTPError as exc:
                error = _parse_error(exc.code, exc.read())
                if read and exc.code in {502, 503, 504} and attempt + 1 < attempts:
                    last = error
                    time.sleep(0.4 * (attempt + 1))
                    continue
                raise error from None
            except (urllib.error.URLError, socket.timeout, ConnectionError) as exc:
                last = Unreachable(503, "hl_api_unreachable", "platform-hl-api is not reachable")
                last.__cause__ = exc
                if read and attempt + 1 < attempts:
                    time.sleep(0.4 * (attempt + 1))
                    continue
                raise last from None
        raise last or Unreachable(503, "hl_api_unreachable")

    def get(self, path: str, **kwargs) -> Any:
        return self._request("GET", path, read=True, **kwargs)

    def post(self, path: str, body: Any = None, *, read: bool = False, **kwargs) -> Any:
        """``read=True`` marks a POST that only reads (searches), so it may be retried."""
        return self._request("POST", path, json_body=body if body is not None else {}, read=read, **kwargs)

    def patch(self, path: str, body: Any) -> Any:
        return self._request("PATCH", path, json_body=body)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)

    # -- auth ----------------------------------------------------------------------
    def token_exchange(self, username: str, password: str) -> dict[str, Any]:
        """OAuth2 password grant. Form-encoded, raw password (the API hashes it)."""
        return self._request("POST", "/api/v1/auth/token", form={
            "grant_type": "password", "username": username, "password": password,
        })

    def whoami(self) -> dict[str, Any]:
        return self.get("/api/v1/auth/whoami")

    # -- items ---------------------------------------------------------------------
    def search_items(self, body: dict) -> dict[str, Any]:
        return self.post("/api/v1/items/search", body, read=True)

    def get_items(self, item_ids: list[str], include: list[str] | None = None) -> dict[str, Any]:
        return self.post("/api/v1/items/get", {"item_ids": item_ids, "include": include or []}, read=True)

    def aggregate_items(self, body: dict) -> dict[str, Any]:
        return self.post("/api/v1/items/aggregate", body, read=True)

    def item_files(self, item_id: str, signed_urls: bool = True) -> dict[str, Any]:
        return self.get(f"/api/v1/items/{urllib.parse.quote(item_id, safe='')}/files",
                        params={"signed_urls": "true" if signed_urls else None})

    # -- entities ------------------------------------------------------------------
    def search_entities(self, entity_type: str, body: dict) -> dict[str, Any]:
        return self.post(f"/api/v1/entities/{urllib.parse.quote(entity_type, safe='')}/search", body, read=True)

    def get_entity(self, entity_type: str, entity_id: str) -> dict[str, Any]:
        return self.get(f"/api/v1/entities/{urllib.parse.quote(entity_type, safe='')}/{urllib.parse.quote(entity_id, safe='')}")

    def create_entity(self, entity_type: str, body: dict) -> dict[str, Any]:
        return self.post(f"/api/v1/entities/{urllib.parse.quote(entity_type, safe='')}", body)

    def patch_entity(self, entity_type: str, entity_id: str, body: dict) -> dict[str, Any]:
        return self.patch(f"/api/v1/entities/{urllib.parse.quote(entity_type, safe='')}/{urllib.parse.quote(entity_id, safe='')}", body)

    def delete_entity(self, entity_type: str, entity_id: str) -> dict[str, Any]:
        return self.delete(f"/api/v1/entities/{urllib.parse.quote(entity_type, safe='')}/{urllib.parse.quote(entity_id, safe='')}")

    def list_entity_types(self) -> Any:
        return self.get("/api/v1/entity-types")

    def get_entity_type(self, type_name: str) -> dict[str, Any]:
        return self.get(f"/api/v1/entity-types/{urllib.parse.quote(type_name, safe='')}")

    def grant_entity_type(self, type_name: str, body: dict) -> dict[str, Any]:
        return self.post(f"/api/v1/entity-types/{urllib.parse.quote(type_name, safe='')}/grants", body)

    def batch_create_entity_types(self, body: dict, dry_run: bool = True) -> dict[str, Any]:
        return self._request("POST", "/api/v1/entity-types/batch", json_body=body,
                             params={"dry_run": "true" if dry_run else "false"})

    # -- meta ----------------------------------------------------------------------
    def estate(self) -> dict[str, Any]:
        return self.get("/api/v1/meta/estate")


def list_hits(response: Any) -> list[dict[str, Any]]:
    """Entity search answers an open object; find its list of instances whatever it is called."""
    if isinstance(response, list):
        return [item for item in response if isinstance(item, dict)]
    if not isinstance(response, dict):
        return []
    for key in ("items", "results", "instances", "entities", "hits", "data"):
        value = response.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def total_pages(response: Any) -> int:
    if not isinstance(response, dict):
        return 1
    meta = response.get("searchResponseMetadata") or response.get("metadata") or {}
    for value in (meta.get("totalPages"), response.get("total_pages")):
        try:
            if value is not None:
                return max(1, int(value))
        except (TypeError, ValueError):
            pass
    return 1

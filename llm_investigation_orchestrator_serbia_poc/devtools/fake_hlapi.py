#!/usr/bin/env python3
"""A small stand-in for platform-hl-api, for development and CI only.

It implements just the operations AI-Intelligence calls, with HL API's request and response
shapes and its documented behaviour (contract 252):

- ``POST /api/v1/auth/token`` is form-encoded (JSON gets 422) and errors in the flat OAuth
  shape; ``GET /api/v1/auth/whoami``
- ``POST /api/v1/items/search``: time / item_types / source_applications / include_ids /
  field filters / text.any, paging capped by ``result_window``; hits carry only the
  english/synopsis/summary text buckets and no tags or parties
- ``POST /api/v1/items/get`` (max 100 ids), ``GET /api/v1/items/{id}/files``
- entity types: list, read, batch create (``dry_run``)
- entity instances: create (platform-assigned id), read (``deleted`` flag), patch (merge),
  soft delete, per-type search with ``fields`` exact matches; records a user creates are
  visible to that user only, as with HL API's default grant
- one error envelope ``{"error": {"code", "message", "hint"}}``

It is not the real API. Recorded responses from a real estate are the check on it.

    python devtools/fake_hlapi.py --port 9100 --fixture devtools/fixtures/syria.json.gz --provision
"""
from __future__ import annotations

import argparse
import copy
import gzip
import json
import math
import secrets
import sys
import threading
import time
import uuid
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

CONTRACT_VERSION = 252
SEARCH_TEXT_BUCKETS = ("english", "synopsis", "summary")


class ApiError(Exception):
    def __init__(self, status: int, code: str, message: str = "", hint: str = ""):
        super().__init__(message or code)
        self.status, self.code, self.hint = status, code, hint


class FakeEstate:
    def __init__(self, users: dict[str, str], result_window: int = 10000, token_ttl: int = 3600):
        self.users = users
        self.result_window = result_window
        self.token_ttl = token_ttl
        self.tokens: dict[str, tuple[str, float]] = {}
        self.items: dict[str, dict[str, Any]] = {}
        self.types: dict[str, dict[str, Any]] = {}
        self.instances: dict[str, dict[str, dict[str, Any]]] = {}
        self.lock = threading.RLock()
        self.calls: list[tuple[str, str]] = []

    # -- seeding -----------------------------------------------------------------------
    def load_fixture(self, path: Path) -> None:
        raw = gzip.decompress(path.read_bytes()) if path.suffix == ".gz" else path.read_bytes()
        fixture = json.loads(raw.decode("utf-8"))
        for item in fixture.get("items") or []:
            self.items[item["item_id"]] = item
        for type_name, instances in (fixture.get("entities") or {}).items():
            self.types.setdefault(type_name, {"type": type_name, "canBeCreated": False})
            store = self.instances.setdefault(type_name, {})
            for instance in instances:
                record = copy.deepcopy(instance)
                record.setdefault("general", {"modification_time": int(time.time() * 1000)})
                record["_owner"] = None  # reference data: visible to everyone
                store[record["entity_id"]] = record

    def provision(self, definitions: list[dict[str, Any]]) -> None:
        for definition in definitions:
            name = definition.get("type") or definition.get("type_name")
            self.types[name] = {**definition, "type": name, "canBeCreated": True}
            self.instances.setdefault(name, {})

    # -- auth ----------------------------------------------------------------------------
    def issue(self, username: str, password: str) -> dict[str, Any]:
        if self.users.get(username) != password:
            raise ApiError(400, "invalid_grant")
        token = secrets.token_urlsafe(24)
        self.tokens[token] = (username, time.time() + self.token_ttl)
        return {"access_token": token, "token_type": "bearer", "expires_in": self.token_ttl}

    def user(self, header: str | None) -> str:
        if not header or not header.lower().startswith("bearer "):
            raise ApiError(401, "missing_token", "Send Authorization: Bearer <token>.", "POST /api/v1/auth/token first.")
        username, expires = self.tokens.get(header[7:].strip(), ("", 0))
        if not username or expires < time.time():
            raise ApiError(401, "invalid_token", "The token is unknown or expired.", "POST /api/v1/auth/token again.")
        return username

    # -- items ---------------------------------------------------------------------------
    @staticmethod
    def _field_value(item: dict[str, Any], field: str) -> list[str]:
        values = []
        if field in item and item[field] not in (None, ""):
            values.append(str(item[field]))
        values.extend(str(t.get("value")) for t in item.get("tags") or [] if t.get("type") == field)
        return values

    def _matches(self, item: dict[str, Any], body: dict[str, Any]) -> bool:
        time_filter = body.get("time") or {}
        stamp = item.get("event_time") or ""
        if time_filter.get("from") and stamp < _norm(time_filter["from"]):
            return False
        if time_filter.get("to") and stamp > _norm(time_filter["to"]):
            return False
        if body.get("item_types") and item.get("item_type") not in body["item_types"]:
            return False
        if body.get("source_applications") and item.get("source_application") not in body["source_applications"]:
            return False
        if body.get("include_ids") and item["item_id"] not in body["include_ids"]:
            return False
        if body.get("exclude_ids") and item["item_id"] in body["exclude_ids"]:
            return False
        related = (body.get("related_to") or {}).get("ids") or []
        if related and not {str(o.get("id")) for o in item.get("related_objects") or []} & set(map(str, related)):
            return False
        for condition in body.get("filters") or []:
            values = self._field_value(item, str(condition.get("field") or ""))
            if condition.get("values") is not None:
                hit = any(v in condition["values"] for v in values)
                if hit == bool(condition.get("negated")):
                    return False
            if condition.get("exists") is not None and bool(values) != bool(condition["exists"]):
                return False
        text = (body.get("text") or {}).get("any")
        if text:
            needle = str(text).strip('"').casefold().rstrip("*")
            haystack = " ".join([*(str(v) for v in (item.get("text") or {}).values() if v),
                                 *(str(t.get("value")) for t in item.get("tags") or [])]).casefold()
            if needle not in haystack:
                return False
        return True

    def related_objects(self, method: str, body: dict[str, Any], query: dict[str, list[str]]) -> dict[str, Any]:
        """Like HL API's related-objects door: a person's (manual) relation from items to an entity."""
        entity = body.get("entity") or {}
        entity_id, entity_type = str(entity.get("id") or ""), str(entity.get("type") or "")
        if not entity_id or not entity_type or not body.get("item_ids"):
            raise ApiError(422, "validation_error", "entity and item_ids are required")
        if method == "DELETE" and (query.get("confirm") or [""])[0] != entity_id:
            raise ApiError(409, "confirm_required", "confirm must be the entity id")
        if method == "POST" and entity_id not in self._type(entity_type):
            raise ApiError(404, "entity_not_found", f"No {entity_type} {entity_id}.")
        results = []
        for item_id in dict.fromkeys(map(str, body["item_ids"])):
            item = self.items.get(item_id)
            if item is None:
                results.append({"item_id": item_id, "outcome": "item_not_found"})
                continue
            held = item.setdefault("related_objects", [])
            mine = [o for o in held if str(o.get("id")) == entity_id and o.get("source") == "manual"]
            if method == "POST":
                if mine:
                    outcome = "already_linked"
                else:
                    held.append({"id": entity_id, "type": entity_type, "source": "manual",
                                 "relation_type": body.get("relation_type") or "associated"})
                    outcome = "linked"
            else:
                item["related_objects"] = [o for o in held if o not in mine]
                outcome = "unlinked" if mine else "not_linked"
            results.append({"item_id": item_id, "outcome": outcome, "verified": True, "held": []})
        ok = sum(r["outcome"] in {"linked", "already_linked", "unlinked", "not_linked"} for r in results)
        return {"entity": entity, "succeeded": ok, "not_applied": 0, "failed": len(results) - ok, "results": results}

    def search_items(self, body: dict[str, Any]) -> dict[str, Any]:
        if not any(body.get(k) for k in ("text", "semantic", "time", "location", "item_types", "source_applications",
                                         "include_ids", "filters", "related_to", "facet_filters")):
            raise ApiError(422, "empty_search", "Send at least one option.", "Add time, item_types or text.")
        page = max(1, int(body.get("page_number") or 1))
        size = max(1, min(100, int(body.get("page_size") or 25)))
        if page * size > self.result_window:
            raise ApiError(400, "result_window_exceeded", f"page_number * page_size must be <= {self.result_window}.",
                           "Narrow the search, for example with a smaller time window.")
        matched = [item for item in self.items.values() if self._matches(item, body)]
        reverse = (body.get("order") or "desc") != "asc"
        matched.sort(key=lambda i: (i.get("event_time") or "", i["item_id"]), reverse=reverse)
        total = len(matched)
        pages = min(math.ceil(total / size) if total else 1, max(1, self.result_window // size))
        include_text = "text" in (body.get("include") or [])
        hits = []
        for item in matched[(page - 1) * size: page * size]:
            text = {k: (item.get("text") or {}).get(k) for k in SEARCH_TEXT_BUCKETS} if include_text else None
            has_text = any((item.get("text") or {}).get(k) for k in SEARCH_TEXT_BUCKETS)
            hits.append({
                "item_id": item["item_id"], "item_type": item.get("item_type"), "sub_type": None, "name": None,
                "event_time": item.get("event_time"), "end_time": None,
                "source_application": item.get("source_application"), "language": item.get("language"),
                "score": None, "highlight": ((item.get("text") or {}).get("english") or "")[:200] or None,
                "text": text, "related_objects": None,
                "text_available_via_get": bool(not has_text and any((item.get("text") or {}).values())),
                "parent_ids": [], "location": copy.deepcopy(item.get("location")),
                "secrecy_holder_status": "VALID", "media": item.get("media"),
            })
        return {"items": hits, "total": total, "total_semantics": "match_count", "page_number": page,
                "page_size": size, "total_pages": pages, "max_page_number": pages,
                "result_window": self.result_window, "search_mode": "filter", "warnings": [], "resolved_places": []}

    def get_items(self, body: dict[str, Any]) -> dict[str, Any]:
        ids = body.get("item_ids") or []
        if len(ids) > 100:
            raise ApiError(422, "too_many_ids", "Up to 100 item ids at a time.")
        include = set(body.get("include") or [])
        out = []
        for item_id in ids:
            item = self.items.get(item_id)
            if item is None:
                out.append({"item_id": item_id, "found": False})
                continue
            out.append({
                "item_id": item_id, "found": True, "item_type": item.get("item_type"), "sub_type": None, "name": None,
                "event_time": item.get("event_time"), "end_time": None,
                "source_application": item.get("source_application"), "language": item.get("language"),
                "text": copy.deepcopy(item.get("text")), "parent_ids": [], "insights": [],
                "tags": copy.deepcopy(item.get("tags") or []),
                "location": copy.deepcopy(item.get("location")), "flags": [], "secrecy_holder_status": "VALID",
                "media": item.get("media"), "duration_ms": None, "call_direction": None, "synopsis": None,
                "topic": [], "keywords": [],
                "parties": copy.deepcopy(item.get("parties") or []) if "parties" in include else None,
                "related_objects": [] if "related_objects" in include else None,
                "detections": [] if "detections" in include else None,
            })
        return {"items": out, "warnings": []}

    # -- entities ------------------------------------------------------------------------
    def _type(self, type_name: str) -> dict[str, dict[str, Any]]:
        if type_name not in self.types:
            raise ApiError(404, "entity_type_not_found", f"No entity type {type_name}.",
                           "GET /api/v1/entity-types lists the types this deployment has.")
        return self.instances.setdefault(type_name, {})

    @staticmethod
    def _visible(record: dict[str, Any], user: str) -> bool:
        return record.get("_owner") in (None, user)

    @staticmethod
    def _public(record: dict[str, Any]) -> dict[str, Any]:
        return {k: copy.deepcopy(v) for k, v in record.items() if not k.startswith("_")}

    def create_instance(self, type_name: str, body: dict[str, Any], user: str) -> dict[str, Any]:
        store = self._type(type_name)
        if not self.types[type_name].get("canBeCreated"):
            raise ApiError(403, "type_not_writable", f"{type_name} is platform-owned.")
        # Like the real HL API: the caller supplies entity_id (general.entity_id is mandatory).
        entity_id = str(body.get("entity_id") or "").strip()
        if not entity_id:
            raise ApiError(422, "validation_error", "entity_id: Field required")
        if entity_id in store:
            raise ApiError(409, "conflict", f"{type_name} {entity_id} already exists")
        store[entity_id] = {
            "entity_id": entity_id, "entity_type": type_name, "entity_name": body.get("entity_name") or "",
            "sections": copy.deepcopy(body.get("sections") or {}), "deleted": False,
            "general": {"modification_time": int(time.time() * 1000), "entity_status": "Active"},
            "_owner": user,
        }
        return {"entity_id": entity_id, "status": "created"}

    def read_instance(self, type_name: str, entity_id: str, user: str) -> dict[str, Any]:
        record = self._type(type_name).get(entity_id)
        if record is None or not self._visible(record, user):
            raise ApiError(404, "entity_not_found", "No such instance.")
        return {**self._public(record), "files": []}

    def patch_instance(self, type_name: str, entity_id: str, body: dict[str, Any], user: str) -> dict[str, Any]:
        record = self._type(type_name).get(entity_id)
        if record is None or not self._visible(record, user):
            raise ApiError(404, "entity_not_found", "No such instance.")
        expected = body.get("expected_modification_time")
        if expected is not None and expected != record["general"]["modification_time"]:
            raise ApiError(409, "stale_write", "Someone changed this record first.", "Read it again and reapply.")
        if body.get("entity_name"):
            record["entity_name"] = body["entity_name"]
        for section, fields in (body.get("sections") or {}).items():
            target = record["sections"].setdefault(section, {})
            for key, value in (fields or {}).items():
                if value is None:
                    target.pop(key, None)
                else:
                    target[key] = value
        record["general"]["modification_time"] = int(time.time() * 1000) + 1
        return {"status": "updated", "deleted": record.get("deleted", False)}

    def delete_instance(self, type_name: str, entity_id: str, user: str) -> dict[str, Any]:
        record = self._type(type_name).get(entity_id)
        if record is None or not self._visible(record, user):
            raise ApiError(404, "entity_not_found", "No such instance.")
        record["deleted"] = True
        return {"status": "deleted", "deleted": True}

    def search_instances(self, type_name: str, body: dict[str, Any], user: str) -> dict[str, Any]:
        store = self._type(type_name)
        page = max(1, int(body.get("page_number") or 1))
        size = max(1, min(100, int(body.get("page_size") or 25)))
        warnings = []
        matched = []
        for record in store.values():
            if record.get("deleted") or not self._visible(record, user):
                continue
            if body.get("include_ids") and record["entity_id"] not in body["include_ids"]:
                continue
            ok = True
            for condition in body.get("fields") or []:
                section, _, name = str(condition.get("field") or "").partition(".")
                value = (record.get("sections") or {}).get(section, {}).get(name)
                if condition.get("values") is not None and str(value) not in [str(v) for v in condition["values"]]:
                    ok = False
                    if value is None:
                        warnings.append(f"unknown or empty field {condition.get('field')}")
            if ok:
                matched.append(record)
        total = len(matched)
        return {"items": [self._public(r) for r in matched[(page - 1) * size: page * size]],
                "searchResponseMetadata": {"totalItems": total, "totalPages": max(1, math.ceil(total / size))},
                "warnings": sorted(set(warnings))}


def _norm(value: str) -> str:
    value = str(value)
    return value if value.endswith("Z") else value.replace("+00:00", "Z")


class FakeHandler(BaseHTTPRequestHandler):
    estate: FakeEstate

    def log_message(self, fmt, *args):
        if self.server.verbose:  # type: ignore[attr-defined]
            sys.stdout.write("fake-hlapi %s\n" % (fmt % args))

    def _json(self, status: int, value: Any) -> None:
        body = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _body(self) -> dict[str, Any]:
        length = int(self.headers.get("Content-Length", "0") or 0)
        raw = self.rfile.read(length) if length else b""
        if not raw:
            return {}
        return json.loads(raw.decode("utf-8"))

    def _dispatch(self, method: str) -> None:
        url = urlparse(self.path)
        path, query = url.path, parse_qs(url.query)
        estate = self.estate
        estate.calls.append((method, path))
        try:
            with estate.lock:
                if path in {"/health/liveness", "/health/readiness"}:
                    return self._json(200, {"status": "ok"})
                if path == "/map":
                    return self._json(200, {"service": "platform-hl-api (fake)", "contract_version": CONTRACT_VERSION})
                if path == "/api/v1/auth/token" and method == "POST":
                    if "application/x-www-form-urlencoded" not in (self.headers.get("Content-Type") or ""):
                        return self._json(422, {"detail": [{"loc": ["body", "grant_type"], "msg": "field required"},
                                                           {"loc": ["body", "username"], "msg": "field required"},
                                                           {"loc": ["body", "password"], "msg": "field required"}]})
                    length = int(self.headers.get("Content-Length", "0") or 0)
                    form = {k: v[0] for k, v in parse_qs(self.rfile.read(length).decode("utf-8")).items()}
                    if form.get("grant_type") != "password":
                        return self._json(400, {"error": "unsupported_grant_type"})
                    try:
                        return self._json(200, estate.issue(form.get("username", ""), form.get("password", "")))
                    except ApiError as exc:
                        return self._json(exc.status, {"error": exc.code})
                user = estate.user(self.headers.get("Authorization"))
                if path == "/api/v1/auth/whoami":
                    return self._json(200, {"user_name": user, "id": f"user-{user}"})
                if path == "/api/v1/meta/estate":
                    return self._json(200, {"contract_version": CONTRACT_VERSION, "generation": "fake", "fake": True})
                if path == "/api/v1/items/search" and method == "POST":
                    return self._json(200, estate.search_items(self._body()))
                if path == "/api/v1/items/related-objects" and method in {"POST", "DELETE"}:
                    return self._json(200, estate.related_objects(method, self._body(), query))
                if path == "/api/v1/items/get" and method == "POST":
                    return self._json(200, estate.get_items(self._body()))
                if path.startswith("/api/v1/items/") and path.endswith("/files"):
                    item_id = unquote(path[len("/api/v1/items/"):-len("/files")])
                    if item_id not in estate.items:
                        raise ApiError(404, "item_not_found", "No such item.")
                    return self._json(200, {"item_id": item_id, "files": []})
                if path == "/api/v1/entity-types" and method == "GET":
                    return self._json(200, {"entity_types": [{"type": n, "canBeCreated": t.get("canBeCreated", False)} for n, t in estate.types.items()]})
                if path == "/api/v1/entity-types/batch" and method == "POST":
                    body = self._body()
                    definitions = body.get("types") or []
                    dry_run = (query.get("dry_run") or ["false"])[0].lower() == "true"
                    names = [d.get("type") for d in definitions]
                    if len(set(names)) != len(names) or not all(names):
                        raise ApiError(422, "invalid_batch", "Each type needs a unique `type`.")
                    existing = [n for n in names if n in estate.types]
                    if existing:
                        raise ApiError(409, "type_exists", f"Already defined: {', '.join(existing)}.",
                                       "Reuse it, or PATCH it to add fields.")
                    if not dry_run:
                        estate.provision(definitions)
                    state = "SKIPPED" if dry_run else "SUCCEEDED"
                    return self._json(200, {
                        "types": [{"type": n, "dry_run": dry_run, "instance_ready": not dry_run,
                                   "publish": {"state": state}} for n in names],
                        "publish": {"state": state}, "publishes_performed": 0 if dry_run else 1,
                        "dry_run": dry_run, "plan": {"create": names} if dry_run else None})
                if path.startswith("/api/v1/entity-types/") and path.endswith("/grants") and method == "POST":
                    name = unquote(path[len("/api/v1/entity-types/"):-len("/grants")])
                    if name not in estate.types:
                        raise ApiError(404, "entity_type_not_found", f"No entity type {name}.")
                    body = self._body()
                    if not body.get("profile") or not body.get("permissions"):
                        raise ApiError(422, "invalid_grant", "Send `profile` and `permissions`.")
                    estate.types[name].setdefault("grants", []).append(body)
                    return self._json(200, {"type": name, "granted": body})
                if path.startswith("/api/v1/entity-types/") and method == "GET":
                    name = unquote(path[len("/api/v1/entity-types/"):])
                    if name not in estate.types:
                        raise ApiError(404, "entity_type_not_found", f"No entity type {name}.")
                    return self._json(200, estate.types[name])
                if path.startswith("/api/v1/entities/"):
                    parts = [unquote(p) for p in path[len("/api/v1/entities/"):].split("/")]
                    if len(parts) == 2 and parts[1] == "search" and method == "POST":
                        return self._json(200, estate.search_instances(parts[0], self._body(), user))
                    if len(parts) == 1 and method == "POST":
                        return self._json(200, estate.create_instance(parts[0], self._body(), user))
                    if len(parts) == 2 and method == "GET":
                        return self._json(200, estate.read_instance(parts[0], parts[1], user))
                    if len(parts) == 2 and method == "PATCH":
                        return self._json(200, estate.patch_instance(parts[0], parts[1], self._body(), user))
                    if len(parts) == 2 and method == "DELETE":
                        return self._json(200, estate.delete_instance(parts[0], parts[1], user))
                raise ApiError(404, "not_found", f"{method} {path} is not served by the fake.",
                               "The fake implements only what AI-Intelligence calls.")
        except ApiError as exc:
            return self._json(exc.status, {"error": {"code": exc.code, "message": str(exc), "hint": exc.hint}})
        except (ValueError, json.JSONDecodeError) as exc:
            return self._json(422, {"error": {"code": "invalid_request", "message": str(exc), "hint": ""}})

    def do_GET(self):
        self._dispatch("GET")

    def do_POST(self):
        self._dispatch("POST")

    def do_PATCH(self):
        self._dispatch("PATCH")

    def do_DELETE(self):
        self._dispatch("DELETE")


def make_server(host: str, port: int, estate: FakeEstate, verbose: bool = False) -> ThreadingHTTPServer:
    handler = type("BoundFakeHandler", (FakeHandler,), {"estate": estate})
    server = ThreadingHTTPServer((host, port), handler)
    server.daemon_threads = True
    server.verbose = verbose  # type: ignore[attr-defined]
    return server


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9100)
    parser.add_argument("--fixture", type=Path, action="append", default=[])
    parser.add_argument("--user", action="append", default=[], help="username:password (default analyst:analyst)")
    parser.add_argument("--provision", action="store_true", help="pre-create the app's entity types")
    parser.add_argument("--prefix", default="AII_")
    parser.add_argument("--result-window", type=int, default=10000)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()
    users = dict(entry.split(":", 1) for entry in (args.user or ["analyst:analyst"]))
    estate = FakeEstate(users, result_window=args.result_window)
    for fixture in args.fixture:
        estate.load_fixture(fixture)
    if args.provision:
        from hl.state import type_definitions
        estate.provision(type_definitions(args.prefix))
    server = make_server(args.host, args.port, estate, args.verbose)
    print(f"fake platform-hl-api on http://{args.host}:{args.port} ({len(estate.items)} items, users: {', '.join(users)})", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()

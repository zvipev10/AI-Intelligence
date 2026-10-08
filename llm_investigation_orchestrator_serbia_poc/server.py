#!/usr/bin/env python3
"""AI-Intelligence analyst UI on i360.

A stateless Python standard-library web server:
- serves the static UI;
- signs users in against i360 (``POST /api/v1/auth/token``) and keeps only their token, in an
  HttpOnly cookie;
- reads records, entities and locations from i360 through platform-hl-api with that token;
- stores investigations, saved items and telecom-identity reviews as i360 entity records.

Configuration is in environment variables (see ``hl/config.py``). There is no local data,
no local state and no secret.
"""
from __future__ import annotations

import csv
import io
import json
import mimetypes
import re
import sys
import time
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote, unquote, urlparse

import analysis
from analysis import Dataset, normalize_locale, require_investigation_id
from hl.client import AuthExpired, HlClient, HlError
from hl.config import ROOT, Settings, load_settings
from hl.items import ItemReader, Snapshot, SnapshotCache, item_fields
from hl.mapping import Mapping, load_mapping
from hl.state import MEMORY_GROUPS, StateStore

SESSION_COOKIE = "aii_session"
# With Secure cookies the "__Host-" prefix pins the cookie to this exact host (no Domain, Path=/),
# so a sibling subdomain cannot plant a session.
SECURE_SESSION_COOKIE = "__Host-aii_session"
TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9._~+/=-]{1,4096}$")
MAX_BODY = 2_000_000

STATIC_FILES = {
    "/": "index.html", "/index.html": "index.html", "/app.js": "app.js", "/styles.css": "styles.css",
    "/polygon_draw.js": "polygon_draw.js", "/demo_bootstrap.js": "demo_bootstrap.js",
    "/help.html": "help.html", "/investigation-user-flow.html": "investigation-user-flow.html",
    "/system-capabilities-guide.html": "system-capabilities-guide.html",
}
STATIC_DIRS = ("/vendor/", "/assets/")


def load_profile(settings: Settings) -> dict[str, Any]:
    path = ROOT / "demo_profiles" / f"{settings.scenario}.json"
    try:
        profile = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        profile = {"scenario_id": settings.scenario}
    return profile


def normalize_record_files(files: Any, origin: str) -> list[dict[str, Any]]:
    """HL API file entries -> what the viewer reads: absolute url/thumbnail_url, the media file first.

    HL API returns signed links as ``urls.primary`` / ``urls.thumbnail`` paths on its own origin, and lists
    a record's source grab (raw JSON) next to its media; the viewer shows the first file.
    """
    out = []
    for entry in files if isinstance(files, list) else []:
        if not isinstance(entry, dict):
            continue
        entry = dict(entry)
        urls = entry.get("urls") if isinstance(entry.get("urls"), dict) else {}
        entry.setdefault("url", urls.get("primary"))
        entry.setdefault("thumbnail_url", urls.get("thumbnail"))
        for key in ("url", "signed_url", "thumbnail_url"):
            value = entry.get(key)
            if isinstance(value, str) and value.startswith("/"):
                entry[key] = origin + value
        out.append(entry)
    return sorted(out, key=lambda e: (e.get("role") != "media", e.get("raw_type") == "rawdata"))


class App:
    """Process-wide objects. Nothing here holds user data except the snapshot cache."""

    def __init__(self, settings: Settings):
        self.settings = settings
        self.mapping: Mapping = load_mapping(str(settings.mapping_path))
        self.profile = load_profile(settings)
        self.snapshots = SnapshotCache(settings.snapshot_ttl_seconds)

    def client(self, token: str | None = None) -> HlClient:
        return HlClient(self.settings.hl_api_url, token, self.settings.request_timeout_seconds)

    def state(self, token: str) -> StateStore:
        s = self.settings
        return StateStore(self.client(token), investigation_type=s.investigation_type,
                          memory_item_type=s.memory_item_type, approval_type=s.approval_type,
                          scenario=s.scenario, external_investigation_type=s.external_investigation_type)

    def item_layer_label(self, item: dict[str, Any]) -> str:
        """The layer an item belongs to: the first profile query it matches that names a layer, else its source."""
        query = self.profile.get("items_query") or {}
        for spec in query.get("queries") or [query]:
            if not spec.get("layer"):
                continue
            if spec.get("item_types") and item.get("item_type") not in spec["item_types"]:
                continue
            if spec.get("source_applications") and item.get("source_application") not in spec["source_applications"]:
                continue
            return str(spec["layer"])
        return str(item.get("source_application") or item.get("item_type") or "i360")

    def investigation_item_layers(self, token: str, investigation_id: str, locale: str) -> list[dict[str, Any]]:
        """Items attached to an i360 investigation, as rows with every field, grouped by layer."""
        groups: dict[str, list[dict[str, str]]] = {}
        for item in self.state(token).attached_items(investigation_id, self.mapping.get_include):
            label = self.item_layer_label(item)
            row = self.mapping.item_to_row(item, locale)
            row["source_type"] = label
            row.update(item_fields(item))
            groups.setdefault(label, []).append(row)
        return [{"label": label, "rows": rows} for label, rows in groups.items()]

    def known_sources(self, locale: str) -> list[str]:
        return list(((self.profile.get("sources") or {}).get(locale)) or [])

    def snapshot(self, token: str, refresh: bool = False) -> Snapshot:
        def build() -> Snapshot:
            reader = ItemReader(self.client(token), self.mapping, self.profile.get("items_query") or {},
                                self.settings.snapshot_max_rows, self.settings.items_per_type)
            items = reader.items()
            entities = reader.entities()
            locations = reader.locations()
            reviews = self.state(token).load_reviews()
            for stats in reader.query_stats:
                print(f"snapshot query: {json.dumps(stats)}", flush=True)  # ASCII-escaped: Windows consoles are not UTF-8
            for warning in reader.warnings:
                print(f"snapshot warning: {json.dumps(warning)}", flush=True)
            return Snapshot(items=items, entities=entities, locations=locations, reviews=reviews,
                            fetched_at=time.time(), truncated=reader.truncated, warnings=reader.warnings)
        return self.snapshots.get(token, build, refresh=refresh)

    def reload_reviews(self, token: str) -> None:
        """After a review, re-read only the reviews and drop the assembled datasets."""
        snap = self.snapshot(token)
        reviews = self.state(token).load_reviews()
        with snap.lock:
            snap.reviews = reviews
            for key in [k for k in snap.derived if k.startswith("dataset:")]:
                snap.derived.pop(key, None)

    def rows(self, snap: Snapshot, locale: str) -> list[dict[str, str]]:
        return snap.memo(f"rows:{locale}", lambda: [ItemReader._with_layer(self.mapping.item_to_row(item, locale), item) for item in snap.items])

    def dataset(self, token: str, locale: str) -> Dataset:
        snap = self.snapshot(token)
        return snap.memo(f"dataset:{locale}", lambda: Dataset(self.rows(snap, locale), snap.entities,
                                                               snap.locations, snap.reviews, locale))


def rows_to_csv(rows: list[dict[str, str]]) -> bytes:
    columns: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                columns.append(key)
    buffer = io.StringIO()
    writer = csv.DictWriter(buffer, fieldnames=columns, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    for row in rows:
        writer.writerow({k: ("" if v is None else v) for k, v in row.items()})
    return buffer.getvalue().encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    app: App
    server_version = "AIIntelligence/1"
    sys_version = ""

    # -- plumbing --------------------------------------------------------------------
    quiet = False

    def log_message(self, fmt, *args):
        if not self.quiet:
            sys.stdout.write("%s %s\n" % (self.log_date_time_string(), fmt % args))

    def _send(self, status: int, body: bytes, content_type: str, extra: dict[str, str] | None = None,
              cookie: str | None = None) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Referrer-Policy", "same-origin")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        if cookie:
            self.send_header("Set-Cookie", cookie)
        self.end_headers()
        if self.command != "HEAD":
            try:
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    def send_json(self, status: int, value: Any, cookie: str | None = None) -> None:
        self._send(status, json.dumps(value, ensure_ascii=False).encode("utf-8"),
                   "application/json; charset=utf-8", cookie=cookie)

    def read_json(self, limit: int = MAX_BODY) -> dict[str, Any]:
        try:
            length = int(self.headers.get("Content-Length", "0") or 0)
        except ValueError:
            raise ValueError("Invalid Content-Length") from None
        if length < 0 or length > limit:
            raise ValueError("Request too large or malformed")
        value = json.loads(self.rfile.read(length).decode("utf-8-sig") or "{}")
        if not isinstance(value, dict):
            raise ValueError("Invalid request body")
        return value

    @property
    def cookie_name(self) -> str:
        return SECURE_SESSION_COOKIE if self.app.settings.cookie_secure else SESSION_COOKIE

    def token(self) -> str | None:
        # Parse by hand: SimpleCookie silently drops every cookie after one it cannot parse,
        # and other apps on the same host may set such cookies.
        for part in (self.headers.get("Cookie") or "").split(";"):
            name, _, value = part.strip().partition("=")
            if name == self.cookie_name and TOKEN_PATTERN.fullmatch(value.strip()):
                return value.strip()
        return None

    def session_cookie(self, token: str, max_age: int) -> str:
        if not TOKEN_PATTERN.fullmatch(token):
            raise HlError(502, "unexpected_token", "i360 returned a token this app cannot store")
        parts = [f"{self.cookie_name}={token}", "Path=/", "HttpOnly", "SameSite=Strict", f"Max-Age={max(60, max_age)}"]
        if self.app.settings.cookie_secure:
            parts.append("Secure")
        return "; ".join(parts)

    def clear_cookie(self) -> str:
        parts = [f"{self.cookie_name}=", "Path=/", "HttpOnly", "SameSite=Strict", "Max-Age=0"]
        if self.app.settings.cookie_secure:
            parts.append("Secure")
        return "; ".join(parts)

    def same_origin_json(self) -> bool:
        """Writes must be JSON from this origin: blocks form-based cross-site and same-site posts."""
        if not (self.headers.get("Content-Type") or "").lower().startswith("application/json"):
            return False
        origin = self.headers.get("Origin")
        if origin is None:
            return True  # non-browser clients; browsers always send Origin on POST
        return urlparse(origin).netloc == (self.headers.get("X-Forwarded-Host") or self.headers.get("Host") or "")

    def handle_error_response(self, exc: Exception) -> None:
        if isinstance(exc, AuthExpired):
            token = self.token()
            if token:
                self.app.snapshots.drop(token)
            self.send_json(401, {"error": "signed_out", "message": "Sign in again.", "hint": exc.hint},
                           cookie=self.clear_cookie())
        elif isinstance(exc, HlError):
            status = exc.status if exc.status in {400, 403, 404, 409, 422, 501} else 502
            self.log_message("HL API error on %s: %s %s %s", self.path.split("?")[0], exc.status, exc.code, exc)
            self.send_json(status, exc.to_dict())
        elif isinstance(exc, (ValueError, json.JSONDecodeError)):
            self.send_json(400, {"error": str(exc)})
        else:
            self.log_message("unhandled error: %r", exc)
            self.send_json(500, {"error": "internal_error"})

    # -- static ----------------------------------------------------------------------
    def serve_static(self, path: str) -> bool:
        try:
            return self._serve_static(path)
        except (ValueError, OSError):
            return False

    def _serve_static(self, path: str) -> bool:
        relative = STATIC_FILES.get(path)
        allowed_root = ROOT
        if relative is None and path.startswith(STATIC_DIRS):
            relative = unquote(path.lstrip("/"))
            allowed_root = (ROOT / path.strip("/").split("/", 1)[0]).resolve()
        if relative is None:
            return False
        file_path = (ROOT / relative).resolve()
        # Static directories serve only files inside themselves: no "..", no symlink escapes.
        if allowed_root not in file_path.parents or not file_path.is_file():
            return False
        content_type = mimetypes.guess_type(str(file_path))[0] or "application/octet-stream"
        if content_type.startswith("text/") or content_type in {"application/javascript", "application/json"}:
            content_type += "; charset=utf-8"
        self._send(200, file_path.read_bytes(), content_type)
        return True

    # -- verbs -----------------------------------------------------------------------
    def do_HEAD(self):
        self.do_GET()

    def do_GET(self):
        url = urlparse(self.path)
        path, query = url.path, parse_qs(url.query)
        if path == "/healthz":
            self.send_json(200, {"status": "ok", "build": self.app.settings.build})
            return
        if not path.startswith("/api/"):
            if not self.serve_static(path):
                self.send_json(404, {"error": "not_found"})
            return
        try:
            self.route_get(path, query)
        except Exception as exc:  # noqa: BLE001 - one place turns failures into responses
            self.handle_error_response(exc)

    def do_POST(self):
        path = urlparse(self.path).path
        if not self.same_origin_json():
            self.send_json(403, {"error": "cross_origin_or_not_json"})
            return
        try:
            self.route_post(path)
        except Exception as exc:  # noqa: BLE001
            self.handle_error_response(exc)

    def do_PUT(self):
        self.send_json(405, {"error": "method_not_allowed"})

    do_DELETE = do_PUT

    # -- GET routes ------------------------------------------------------------------
    def route_get(self, path: str, query: dict[str, list[str]]) -> None:
        app = self.app
        locale = normalize_locale((query.get("lang") or query.get("locale") or ["he"])[0])
        if path == "/api/status":
            token = self.token()
            user = None
            cookie = None
            if token:
                try:
                    user = app.client(token).whoami()
                except AuthExpired:
                    app.snapshots.drop(token)
                    token, cookie = None, self.clear_cookie()
            self.send_json(200, {
                "authenticated": bool(token),
                "user": user,
                "scenario_id": app.profile.get("scenario_id") or app.settings.scenario,
                "dataset_version": app.profile.get("dataset_version") or "i360",
                "demo_profile": {k: app.profile.get(k) for k in ("scenario_id", "label", "map", "sources")},
                "features": {"ai": False, "playback": False},
                "build": app.settings.build,
                "locale": locale,
                "backend": "i360",
                "dataset_url": f"/api/dataset/events?lang={locale}",
                "locations_url": f"/api/dataset/locations?lang={locale}",
            }, cookie=cookie)
            return
        token = self.token()
        if not token:
            self.send_json(401, {"error": "signed_out", "message": "Sign in first."})
            return
        if path == "/api/me":
            self.send_json(200, app.client(token).whoami())
            return
        if path == "/api/dataset/events":
            snap = app.snapshot(token)
            body = rows_to_csv(app.rows(snap, locale))
            self._send(200, body, "text/csv; charset=utf-8",
                       extra={"X-Dataset-Truncated": "true" if snap.truncated else "false"})
            return
        if path == "/api/dataset/locations":
            self.send_json(200, app.snapshot(token).locations)
            return
        if path == "/api/dataset/info":
            snap = app.snapshot(token)
            self.send_json(200, {"rows": len(snap.items), "entities": len(snap.entities),
                                 "locations": len(snap.locations), "truncated": snap.truncated,
                                 "warnings": snap.warnings[:20], "fetched_at": snap.fetched_at})
            return
        if path == "/api/layers":
            self.send_json(200, {"layers": analysis.list_layers(app.dataset(token, locale), app.known_sources(locale))})
            return
        if path.startswith("/api/layers/") and path.endswith("/rows"):
            layer_id = unquote(path[len("/api/layers/"):-len("/rows")])
            filters = json.loads((query.get("filters") or ["{}"])[0])
            result = analysis.layer_rows(app.dataset(token, locale), layer_id, filters, app.known_sources(locale))
            if result is None:
                self.send_json(404, {"error": "Layer not found"})
            else:
                self.send_json(200, {"layer": result[0], "rows": result[1]})
            return
        if path == "/api/links":
            data = app.dataset(token, locale)
            object_id = str((query.get("object_id") or query.get("record_id") or [""])[0]).strip()
            links = data.links
            if object_id:
                links = [l for l in links if object_id in {str((l.get("from") or {}).get("object_id") or ""),
                                                           str((l.get("to") or {}).get("object_id") or "")}]
            self.send_json(200, {"schema_version": 1, "links": links})
            return
        if path == "/api/derivations":
            data = app.dataset(token, locale)
            entity_id = str((query.get("subject_id") or query.get("entity_id") or [""])[0]).strip()
            derivation = analysis.derive_subscriber_identity(data.events, data.links, entity_id) if entity_id else None
            self.send_json(200, {"schema_version": 1, "derivations": [derivation] if derivation else []})
            return
        if path.startswith("/api/records/") and path.endswith("/files"):
            self.send_json(200, self.record_files(token, unquote(path[len("/api/records/"):-len("/files")])))
            return
        if path == "/api/investigations":
            self.send_json(200, {"investigations": app.state(token).list_investigations()})
            return
        if path == "/api/investigation-memory":
            investigation_id = require_investigation_id((query.get("id") or [""])[0])
            self.send_json(200, app.state(token).load_memory(investigation_id))
            return
        if path == "/api/investigation-items":
            investigation_id = require_investigation_id((query.get("id") or [""])[0])
            self.send_json(200, {"layers": app.investigation_item_layers(token, investigation_id, locale)})
            return
        if path.startswith("/api/investigation-memory/layers/") and path.endswith("/presentation"):
            memory_layer_id = unquote(path[len("/api/investigation-memory/layers/"):-len("/presentation")].rstrip("/"))
            investigation_id = require_investigation_id((query.get("investigation_id") or [""])[0])
            memory = app.state(token).load_memory(investigation_id)
            result = analysis.memory_layer_presentation(memory, memory_layer_id, app.dataset(token, locale))
            if result is None:
                self.send_json(404, {"error": "Saved memory layer not found"})
            else:
                self.send_json(200, result)
            return
        self.send_json(404, {"error": "not_found"})

    def record_files(self, token: str, record_id: str) -> dict[str, Any]:
        """Files of one record, with signed URLs the browser can load directly from HL API."""
        data = self.app.dataset(token, "he")
        row = next((r for r in data.events if record_id in {r.get("event_id"), r.get("record_id"), r.get("i360_item_id")}), None)
        if row is None:
            raise HlError(404, "record_not_found", "Record not found")
        response = self.app.client(token).item_files(row.get("i360_item_id") or record_id, signed_urls=True)
        if isinstance(response, dict):
            response["files"] = normalize_record_files(response.get("files"), self.app.settings.hl_api_public_origin)
        return response

    # -- POST routes -----------------------------------------------------------------
    def route_post(self, path: str) -> None:
        app = self.app
        if path == "/api/login":
            request = self.read_json(10_000)
            username = str(request.get("username") or "").strip()
            password = str(request.get("password") or "")
            if not username or not password:
                raise ValueError("Username and password are required")
            try:
                answer = app.client().token_exchange(username, password)
            except HlError as exc:
                if exc.status in {400, 401}:
                    self.send_json(401, {"error": "invalid_credentials", "message": "Wrong username or password."})
                    return
                raise
            token = str(answer.get("access_token") or "")
            if not token:
                raise HlError(502, "no_token", "i360 returned no token")
            user = app.client(token).whoami()
            self.send_json(200, {"user": user}, cookie=self.session_cookie(token, int(answer.get("expires_in") or 3600)))
            return
        if path == "/api/logout":
            token = self.token()
            if token:
                app.snapshots.drop(token)
            self.send_json(200, {"signed_out": True}, cookie=self.clear_cookie())
            return
        token = self.token()
        if not token:
            self.send_json(401, {"error": "signed_out", "message": "Sign in first."})
            return
        state = app.state(token)
        if path == "/api/refresh":
            snap = app.snapshot(token, refresh=True)
            self.send_json(200, {"rows": len(snap.items), "truncated": snap.truncated})
            return
        if path == "/api/investigations":
            request = self.read_json()
            investigation_id = require_investigation_id(request.get("investigation_id"))
            name = analysis.compact_text(request.get("name"), 240)
            if not name:
                raise ValueError("Missing investigation name")
            self.send_json(200, state.register_investigation(investigation_id, name))
            return
        if path in {"/api/investigation-memory/layer", "/api/investigation-memory/artifact"}:
            request = self.read_json()
            investigation_id = require_investigation_id(request.get("investigation_id"))
            if path.endswith("/layer"):
                group, item = "layers", analysis.layer_memory_item(request)
            else:
                group, item = "artifacts", analysis.artifact_memory_item(request)
                if item.get("object_kind") == "record":
                    # The record's i360 item id, for attaching it to an i360 investigation.
                    data = app.dataset(token, "he")
                    row = next((r for r in data.events if item["object_id"] in {r.get("record_id"), r.get("event_id"), r.get("i360_item_id")}), None)
                    if row and row.get("i360_item_id"):
                        item["i360_item_id"] = row["i360_item_id"]
            saved = state.add_memory_item(investigation_id, group, item, request.get("name"))
            self.send_json(201, {"saved": saved, "memory": state.load_memory(investigation_id)})
            return
        if path == "/api/collection-request":
            request = self.read_json(200_000)
            investigation_id = require_investigation_id(request.get("investigation_id"))
            user = app.client(token).whoami()
            item = analysis.collection_request_item(request, str(user.get("user_name") or ""))
            state.add_memory_item(investigation_id, "collection_requests", item, request.get("name"))
            self.send_json(201, {"saved": item, "memory": state.load_memory(investigation_id)})
            return
        if path == "/api/investigation-memory/delete":
            request = self.read_json(100_000)
            investigation_id = require_investigation_id(request.get("investigation_id"))
            group = str(request.get("group") or "").strip()
            item_id = analysis.compact_text(request.get("item_id"), 240)
            if group not in MEMORY_GROUPS:
                raise ValueError("Invalid memory group")
            if not item_id:
                raise ValueError("Missing memory item id")
            if not state.delete_memory_item(investigation_id, group, item_id):
                raise ValueError("Memory item not found")
            self.send_json(200, {"deleted_id": item_id, "group": group, "memory": state.load_memory(investigation_id)})
            return
        if path in {"/api/derivations/review", "/api/entity/telecom-correlation/approve"}:
            request = self.read_json(100_000)
            entity_id = analysis.compact_text(request.get("entity_id"), 240)
            if not entity_id:
                raise ValueError("Entity id is required")
            action = "approve" if path.endswith("/approve") else analysis.compact_text(request.get("action") or "approve", 20).lower()
            data = app.dataset(token, "en")
            snap = app.snapshot(token)
            previous = next((r for r in snap.reviews.values()
                             if str((r.get("subject") or {}).get("object_id") or "") == entity_id), None)
            user = app.client(token).whoami()
            review = analysis.subscriber_identity_review(data, entity_id, action, previous, str(user.get("user_name") or "analyst"))
            state.save_review(review, str(user.get("user_name") or "analyst"))
            app.reload_reviews(token)
            entity = app.dataset(token, "en").entities.get(entity_id)
            self.send_json(201, {"saved": {**review, "method": review.get("rule_id")}, "entity": entity})
            return
        self.send_json(404, {"error": "not_found"})


def main(argv: list[str]) -> int:
    settings = load_settings()
    if not settings.hl_api_url:
        print("HL_API_URL is not set. Point it at platform-hl-api (or devtools/fake_hlapi.py).", file=sys.stderr)
        return 2
    Handler.app = App(settings)
    server = ThreadingHTTPServer((settings.host, settings.port), Handler)
    server.daemon_threads = True
    print(f"AI-Intelligence listening on http://{settings.host}:{settings.port} -> {settings.hl_api_url} "
          f"(scenario {settings.scenario})", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

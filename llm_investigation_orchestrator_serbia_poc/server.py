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

import copy
import csv
import io
import json
import mimetypes
import os
import re
import sys
import time
from http import cookies
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Callable
from urllib.parse import parse_qs, quote, unquote, urlparse

import analysis
from analysis import Dataset, normalize_locale, require_investigation_id
from hl.chat import ChatServiceClient, ChatTurn, ClientGone, LlmClient, TurnContext, answer_entities
from hl.internal import Catalogue, InternalTurn

INTERNAL_COMMAND = r"^\s*/(?:i|internal)\b"  # /i (and the older /internal): the assistant over the loaded data
from hl.client import AuthExpired, HlClient, HlError, Unreachable
from hl.config import ROOT, Settings, load_settings
from hl.items import TELECOM_APPROVED, ItemReader, Snapshot, SnapshotCache, entity_presentation, item_fields, layers_search
from hl.mapping import Mapping, load_mapping
from hl import report
from hl.state import MEMORY_GROUPS, MemoryTypeMissing, StateStore

SESSION_COOKIE = "aii_session"
# With Secure cookies the "__Host-" prefix pins the cookie to this exact host (no Domain, Path=/),
# so a sibling subdomain cannot plant a session.
SECURE_SESSION_COOKIE = "__Host-aii_session"
TOKEN_PATTERN = re.compile(r"^[A-Za-z0-9._~+/=-]{1,4096}$")
MAX_BODY = 2_000_000

STATIC_FILES = {
    "/": "index.html", "/index.html": "index.html", "/app.js": "app.js", "/styles.css": "styles.css",
    "/polygon_draw.js": "polygon_draw.js", "/demo_bootstrap.js": "demo_bootstrap.js", "/chat.js": "chat.js", "/chat.css": "chat.css",
    "/help.html": "help.html", "/investigation-user-flow.html": "investigation-user-flow.html",
    "/system-capabilities-guide.html": "system-capabilities-guide.html",
    "/home": "home.html", "/home.html": "home.html",  # the launcher, opened after sign-in
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
        is_video = str(entry.get("content_type") or "").startswith("video/") or entry.get("raw_type") == "video"
        # Videos: i360's web_preview is an H.264 copy every browser plays; the original may be H.265/HEVC.
        if is_video and urls.get("web_preview"):
            entry.setdefault("original_url", urls.get("primary"))
            entry.setdefault("url", urls["web_preview"])
        entry.setdefault("url", urls.get("primary"))
        entry.setdefault("thumbnail_url", urls.get("thumbnail"))
        for key in ("url", "signed_url", "thumbnail_url", "original_url"):
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
        if isinstance(self.profile.get("entity_mapping"), dict):
            # The scenario's own entity mapping (e.g. i360 PERSON_OF_INTEREST) replaces the default one,
            # on a copy: load_mapping() is cached and shared.
            self.mapping = copy.copy(self.mapping)
            self.mapping.entities = self.profile["entity_mapping"]
        self.snapshots = SnapshotCache(settings.snapshot_ttl_seconds)

    def client(self, token: str | None = None) -> HlClient:
        return HlClient(self.settings.hl_api_url, token, self.settings.request_timeout_seconds)

    def state(self, token: str) -> StateStore:
        s = self.settings
        return StateStore(self.client(token), investigation_type=s.investigation_type,
                          memory_item_type=s.memory_item_type, approval_type=s.approval_type,
                          scenario=s.scenario, external_investigation_type=s.external_investigation_type,
                          investigation_links=self.profile.get("investigation_links") or [],
                          item_layer=self.item_layer_label)

    def layer_field_labels(self, layer_name: Any, by_id: bool = False) -> dict[str, str]:
        """A layer's display names for its i360 fields (profile query "labels": path -> name), as row keys.

        HL API's search and get-by-id do not return the same fields (e.g. "language" comes from search only),
        so rows read by id (items/get alone: chat, investigation records, the report's extra records) use the
        query's "labels_by_id" where it has one: its entries replace the "labels" entries of the same name."""
        query = self.profile.get("items_query") or {}
        spec = next((q for q in query.get("queries") or [] if q.get("layer") and q.get("layer") == layer_name), None)
        labels = dict((spec or {}).get("labels") or {})
        if by_id and (spec or {}).get("labels_by_id"):
            override = spec["labels_by_id"]
            names = {str(name) for name in override.values()}
            labels = {**{p: n for p, n in labels.items() if str(n) not in names}, **override}
        return {f"i360.{path}": str(name) for path, name in labels.items() if not str(path).startswith("_")}

    def row_field_labels(self, row: dict[str, Any]) -> dict[str, str]:
        """The display names for one row: its layer's, by how the row was read (see layer_field_labels)."""
        return self.layer_field_labels(row.get("source_type"), by_id=row.get("i360_read") == "by_id")

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

    def item_groups(self, items: list[dict[str, Any]], locale: str) -> list[dict[str, Any]]:
        """i360 items read by id, as rows with every field, grouped by the layer each belongs to; each group
        carries its layer's by-id display names (see layer_field_labels)."""
        groups: dict[str, list[dict[str, str]]] = {}
        for item in items:
            label = self.item_layer_label(item)
            row = self.mapping.item_to_row(item, locale)
            row["source_type"] = label
            row.update(item_fields(item))
            row["i360_read"] = "by_id"
            groups.setdefault(label, []).append(row)
        return [{"label": label, "rows": rows, "field_labels": self.layer_field_labels(label, by_id=True)}
                for label, rows in groups.items()]

    def investigation_item_layers(self, token: str, investigation_id: str, locale: str) -> list[dict[str, Any]]:
        """Items attached to an i360 investigation, as rows with every field, grouped by layer."""
        return self.item_groups(self.state(token).attached_items(investigation_id, self.mapping.get_include), locale)

    def entity_record(self, token: str, entity_type: str, entity_id: str) -> dict[str, Any] | None:
        """One entity by id (its type from i360, or else the scenario's entity types), as the viewer draws it."""
        client = self.client(token)
        for candidate in [entity_type] if entity_type else list(self.mapping.entities.get("types") or []):
            try:
                instance = client.get_entity(candidate, entity_id)
            except HlError as exc:
                if exc.status in {400, 403, 404, 422}:
                    continue
                raise
            record = entity_presentation(self.mapping.instance_to_entity(instance), candidate)
            record["entity_id"] = record.get("entity_id") or entity_id
            if not record.get("entity_type"):
                record["entity_type"] = "person" if "PERSON" in candidate.upper() else candidate.lower()
            record.setdefault("canonical_name", instance.get("entity_name") or (instance.get("general") or {}).get("entity_name") or entity_id)
            return record
        return None

    def item_layers(self, token: str, item_ids: list[str], locale: str) -> list[dict[str, Any]]:
        """Given i360 items (read in full, in the order asked), grouped by layer; unknown ids are skipped."""
        client = self.client(token)
        found: dict[str, dict[str, Any]] = {}

        def read(batch: list[str]) -> None:
            try:
                items = client.get_items(batch, self.mapping.get_include).get("items") or []
            except HlError as exc:
                # A server error on a batch (seen: digestserver 500 on items/get-items) is narrowed down by halves,
                # so one unreadable id costs only itself.
                if exc.status < 500 or isinstance(exc, Unreachable):
                    raise
                if len(batch) == 1:
                    print(f"items/get failed for {batch[0]}: {exc.status} {str(exc)[:200]}", flush=True)
                    return
                read(batch[:len(batch) // 2])
                read(batch[len(batch) // 2:])
                return
            for item in items:
                if isinstance(item, dict) and item.get("item_id") and item.get("found") is not False:
                    found[str(item["item_id"])] = item

        for start in range(0, len(item_ids), 100):
            read(item_ids[start:start + 100])
        return self.item_groups([found[i] for i in item_ids if i in found], locale)

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

    def approve_i360_telecom(self, token: str, entity_type: str, entity_id: str) -> None:
        """Set the status of the person's derived MSISDN / IMSI entries (details.device_msisdn,
        details.device_imsi) to Approved in i360, then re-read the entities. The record keeps its shapes;
        the write refuses if someone changed the record since it was read."""
        client = self.client(token)
        instance = client.get_entity(entity_type, entity_id)
        record = instance.get("entity") if isinstance(instance.get("entity"), dict) else instance
        details = (record.get("details") or (record.get("sections") or {}).get("details") or {})
        changed: dict[str, Any] = {}

        def approve(value: Any) -> Any:
            if isinstance(value, list):
                return [approve(v) for v in value]
            if isinstance(value, dict):
                return {k: (TELECOM_APPROVED if k == "status" else approve(v)) for k, v in value.items()}
            return value

        for field in ("device_msisdn", "device_imsi"):
            if details.get(field) not in (None, "", [], {}):
                changed[field] = approve(details[field])
        if not changed:
            raise ValueError("The person has no derived MSISDN / IMSI to approve")
        modified = ((record.get("general") or {}).get("modification_time"))
        body: dict[str, Any] = {"sections": {"details": changed}}
        if modified:
            body["expected_modification_time"] = modified
        client.patch_entity(entity_type, entity_id, body)
        snap = self.snapshot(token)
        with snap.lock:
            snap.entities = ItemReader(client, self.mapping, {}, 1).entities()
            for key in [k for k in snap.derived if k.startswith("dataset:")]:
                snap.derived.pop(key, None)

    def report_inputs(self, token: str, investigation_id: str, subject_id: str = "") -> dict[str, Any]:
        """The records and persons saved to the investigation, the subject person, and the report's facts."""
        memory = self.state(token).load_memory(investigation_id)
        saved = [a for a in (memory.get("memory") or {}).get("artifacts") or [] if a.get("kind") == "object"]
        record_ids = [str(a.get("object_id")) for a in saved if a.get("object_kind") == "record" and a.get("object_id")]
        person_ids = [str(a.get("object_id")) for a in saved if a.get("object_kind") == "person" and a.get("object_id")]
        data = self.dataset(token, "en")
        by_id = {str(e.get("i360_item_id") or e.get("event_id")): e for e in data.events}
        rows = [by_id[i] for i in record_ids if i in by_id]
        missing = [i for i in record_ids if i not in by_id]
        if missing:  # saved records outside the app's layers: read them from i360
            rows += [row for group in self.item_layers(token, missing, "en") for row in group["rows"]]
        if not rows and not person_ids:
            raise ValueError("Nothing is saved to this investigation yet")
        persons = [data.entities[i] for i in person_ids if i in data.entities]
        subject_id = subject_id if any(str(p.get("entity_id")) == subject_id for p in persons) else report.default_subject(persons, rows)
        facts = report.compute_facts(str(memory.get("name") or investigation_id), rows, persons, subject_id, self.row_field_labels)
        names = {eid: str(e.get("canonical_name") or eid) for eid, e in data.entities.items()}
        return {"rows": rows, "persons": persons, "subject_id": subject_id, "facts": facts, "names": names}

    def report_facts(self, token: str, investigation_id: str, subject_id: str = "") -> dict[str, Any]:
        inputs = self.report_inputs(token, investigation_id, subject_id)
        return {**inputs["facts"], "investigation_id": investigation_id, "subject_id": inputs["subject_id"]}

    def report_block(self, token: str, investigation_id: str, block: str, subject_id: str = "") -> dict[str, Any]:
        """One analysis block of the report, written by HL API's language model."""
        inputs = self.report_inputs(token, investigation_id, subject_id)
        llm = LlmClient(self.client(token), self.settings.llm_model, timeout=self.settings.llm_timeout_seconds)
        return report.run_block(llm.complete_json, block, inputs["facts"], inputs["rows"], self.row_field_labels,
                                inputs["persons"], inputs["subject_id"], inputs["names"])

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
            sys.stdout.flush()

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
                "features": {"ai": bool(app.settings.chat_service_url), "playback": False},
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
        if path == "/api/launcher":
            # The launcher page's applications and workspace tools (profile "launcher"; links are per deployment).
            self.send_json(200, app.profile.get("launcher") or {})
            return
        if path == "/api/dataset/events":
            snap = app.snapshot(token)
            linked = {str(e.get("event_id")): ";".join(e.get("related_entity_ids") or [])
                      for e in app.dataset(token, locale).events if e.get("related_entity_ids")}
            rows = [{**row, "related_entity_ids": linked[str(row.get("event_id"))]} if str(row.get("event_id")) in linked else row
                    for row in app.rows(snap, locale)]
            body = rows_to_csv(rows)
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
            layers = analysis.list_layers(app.dataset(token, locale), app.known_sources(locale))
            for layer in layers:
                labels = app.layer_field_labels(layer.get("source_type"))
                if labels:
                    layer["field_labels"] = labels
                by_id = app.layer_field_labels(layer.get("source_type"), by_id=True)
                if by_id != labels:
                    layer["field_labels_by_id"] = by_id
            self.send_json(200, {"layers": layers})
            return
        if path.startswith("/api/layers/") and path.endswith("/rows"):
            layer_id = unquote(path[len("/api/layers/"):-len("/rows")])
            filters = json.loads((query.get("filters") or ["{}"])[0])
            result = analysis.layer_rows(app.dataset(token, locale), layer_id, filters, app.known_sources(locale))
            if result is None:
                self.send_json(404, {"error": "Layer not found"})
            else:
                layer = dict(result[0])
                labels = app.layer_field_labels(layer.get("source_type"))
                if labels:
                    layer["field_labels"] = labels
                self.send_json(200, {"layer": layer, "rows": result[1]})
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
        if path.startswith("/api/entity-files/"):
            parts = [unquote(p) for p in path[len("/api/entity-files/"):].split("/")]
            if len(parts) != 3 or not all(re.fullmatch(r"[A-Za-z0-9_.:-]{1,200}", p) for p in parts):
                raise ValueError("Invalid entity file path")
            entity_type, entity_id, file_id = parts
            payload, headers = app.client(token)._request(
                "GET", f"/api/v1/entities/{quote(entity_type, safe='')}/{quote(entity_id, safe='')}/files/{quote(file_id, safe='')}",
                read=True, raw=True)
            content_type = headers.get("Content-Type") or "application/octet-stream"
            if not content_type.split(";")[0].strip().startswith(("image/", "video/")):
                raise HlError(415, "unsupported_media", "Only image and video attachments are served")
            self._send(200, payload, content_type)
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

    def save_layer_records(self, token: str, state: StateStore, investigation_id: str,
                           item: dict[str, Any], request: dict[str, Any]) -> dict[str, Any]:
        """Save a layer to an i360 investigation: every record it presents is attached to the investigation
        (25 per HL API call); the layer's own view is kept too when the app's memory type is set up."""
        layer = request.get("layer") if isinstance(request.get("layer"), dict) else {}
        wanted = [str(i) for i in layer.get("record_ids") or [] if isinstance(i, (str, int)) and str(i).strip()]
        data = self.app.dataset(token, "he")
        by_id: dict[str, str] = {}
        for row in data.events:
            if row.get("i360_item_id"):
                for key in (row.get("record_id"), row.get("event_id"), row.get("i360_item_id")):
                    if key:
                        by_id.setdefault(str(key), str(row["i360_item_id"]))
        # A record the chat showed may be outside the snapshot: its id is then the i360 item id itself.
        item_ids = list(dict.fromkeys(by_id.get(i, i) for i in wanted))
        if not item_ids:
            raise ValueError("This layer shows no records to save")
        records = state.attach_items(investigation_id, item_ids)
        try:
            saved = state.add_memory_item(investigation_id, "layers", item, request.get("name"))
        except MemoryTypeMissing:
            saved = {"id": f"records:{item['id']}", "label": item.get("label")}
        return {"saved": {**saved, "records": records}, "memory": state.load_memory(investigation_id)}

    def record_files(self, token: str, record_id: str) -> dict[str, Any]:
        """Files of one record, with signed URLs the browser can load directly from HL API."""
        data = self.app.dataset(token, "he")
        row = next((r for r in data.events if record_id in {r.get("event_id"), r.get("record_id"), r.get("i360_item_id")}), None)
        # A record the chat showed may be outside the snapshot: its id is then the i360 item id itself.
        item_id = (row.get("i360_item_id") if row else None) or record_id
        response = self.app.client(token).item_files(item_id, signed_urls=True)
        if isinstance(response, dict):
            response["files"] = normalize_record_files(response.get("files"), self.app.settings.hl_api_public_origin)
        return response

    # -- chat ------------------------------------------------------------------------
    def chat_ask(self, token: str, request: dict[str, Any]) -> None:
        settings = self.app.settings
        if not settings.chat_service_url:
            self.send_json(501, {"error": "chat_off", "message": "The chat is not configured on this deployment (CHAT_SERVICE_URL)."})
            return
        context = TurnContext.from_request(request)
        context.investigation_type = settings.external_investigation_type or settings.investigation_type
        locale = normalize_locale(str(request.get("locale") or "en"))
        self.log_message("chat turn: scope %s, %d previous citations, viewer %s, i360 conversation %s, message %s",
                         context.scope, len(context.previous_citations), context.viewer_item_id or "-",
                         context.i360_conversation_id or "-", json.dumps(context.message[:300], ensure_ascii=False))
        self.start_stream()

        def emit(event: str, data: Any) -> None:
            self.log_chat_event(event, data)
            self.stream_event(event, data)

        llm = LlmClient(self.app.client(token), settings.llm_model, timeout=settings.llm_timeout_seconds) \
            if settings.llm_enabled else None
        # The /i question a clarification was asked about: the next message (with or without /i)
        # answers it, unless it is another command.
        pending = str(request.get("internal_pending") or "")[:2000]
        if re.match(INTERNAL_COMMAND, context.message) or (pending and not context.message.lstrip().startswith("/")):
            # /i: answered from the records the app loaded, not by the i360 chat.
            try:
                self.internal_turn(token, locale, llm, emit, context, pending)
            except ClientGone:
                self.log_message("chat: the browser closed the stream")
            except AuthExpired:
                self.try_stream_event("error", {"error": "signed_out", "message": "Sign in again."})
            except Exception as exc:  # noqa: BLE001 - the stream is already open; report in it
                self.log_message("chat /i: unhandled error %r", exc)
                self.try_stream_event("error", {"error": "internal_error", "message": "The /i assistant failed."})
            return
        chat = ChatServiceClient(settings.chat_service_url, token, settings.chat_idle_timeout_seconds)
        turn = ChatTurn(llm, chat, AppToolHost(self.app, token, locale), emit, context, settings.chat_model)
        turn.raw_test = os.environ.get("CHAT_RAW_TEST") == "1"  # never set on LAMBDA
        try:
            turn.run()
        except ClientGone:
            self.log_message("chat: the browser closed the stream")
        except AuthExpired:
            self.try_stream_event("error", {"error": "signed_out", "message": "Sign in again."})
        except HlError as exc:
            self.log_message("chat error: %s %s %s", exc.status, exc.code, exc)
            self.try_stream_event("error", {"error": exc.code, "message": str(exc)})
        except Exception as exc:  # noqa: BLE001 - the stream is already open; report in it
            self.log_message("chat: unhandled error %r", exc)
            self.try_stream_event("error", {"error": "internal_error", "message": "The chat failed."})

    def internal_turn(self, token: str, locale: str, llm: Any, emit: Callable[[str, Any], None],
                      context: TurnContext, pending: str = "") -> None:
        """/i <question>: the model turns the question into a query over the loaded records (our layer and
        field names), our code runs it, the model answers from the result, and the records are shown."""
        snap = self.app.snapshot(token)
        rows = self.app.rows(snap, locale)
        catalogue = snap.memo(f"internal:{locale}", lambda: self.internal_catalogue(snap, rows))
        by_id = {str(r.get("record_id") or r.get("i360_item_id") or ""): r for r in rows}

        people = {str(e.get("entity_id") or ""): e for e in snap.entities or [] if isinstance(e, dict)}

        def show(ids: list[str], view: str, label: str) -> int:
            persons = [i for i in ids if i in people]
            if persons:
                # People open in the person viewer, one at a time: the first (the answer names the others).
                entity = people[persons[0]]
                emit("action", {"kind": "open_entity", "entity_id": persons[0], "entity": entity})
                emit("step", {"text": f"Opened {entity.get('canonical_name') or persons[0]}"})
                ids = [i for i in ids if i not in people]
                if not ids:
                    return 0
            if view == "open" and len(ids) == 1 and by_id.get(ids[0]):
                row = by_id[ids[0]]  # "open the record": the record viewer, as open_item does
                emit("action", {"kind": "open_item", "row": row, "group": str(row.get("source_type") or "")})
                return 1
            groups: dict[str, list[dict[str, Any]]] = {}
            for record_id in ids:
                row = by_id.get(record_id)
                if row:
                    groups.setdefault(str(row.get("source_type") or "records"), []).append(row)
            if groups:
                emit("action", {"kind": "show_items", "label": label, "view": view if view in ("map", "table", "timeline") else "table",
                                "groups": [{"label": name, "rows": group} for name, group in groups.items()]})
            return sum(len(g) for g in groups.values())

        question = re.sub(INTERNAL_COMMAND, "", context.message, count=1).strip()
        previous = [c["id"] for c in context.previous_citations]
        result = InternalTurn(llm, catalogue, emit, show, previous, pending).run(question)
        # The records found go back to the browser as the answer's citations, so a following /i question
        # can say "them" (and the i360 chat sees them as the previous answer's records, as with its own).
        found = result.get("ids") if "ids" in result else previous
        emit("done", {"i360_conversation_id": context.i360_conversation_id, "i360_scope": context.i360_scope,
                      "summary": f"internal · {result.get('count', 0)} records", "i360_last_turns": context.i360_last_turns,
                      "citations": [{"id": i, "type": "", "time": "", "text": ""} for i in (found or [])[:500]],
                      "entities": [], "internal_pending": result.get("clarify", "")})

    def internal_catalogue(self, snap: Any, rows: list[dict[str, Any]]) -> Catalogue:
        layers: dict[str, list[dict[str, Any]]] = {}
        for row in rows:
            layers.setdefault(str(row.get("source_type") or ""), []).append(row)
        labels = {layer: self.app.layer_field_labels(layer) for layer in layers}
        entities: dict[str, str] = {}
        persons = []
        for entity in snap.entities or []:
            if isinstance(entity, dict):
                entity_id = str(entity.get("entity_id") or entity.get("id") or "")
                name = entity.get("canonical_name") or entity.get("name") or entity.get("display_name")
                if entity_id and name:
                    entities[entity_id] = str(name)
                if entity_id:
                    persons.append(self.internal_person(entity_id, entity))
        if persons:
            layers["Persons"] = persons  # the people the app loaded, as a layer the questions can name
        return Catalogue({k: v for k, v in layers.items() if k}, labels, entities)

    @staticmethod
    def internal_person(entity_id: str, entity: dict[str, Any]) -> dict[str, Any]:
        """A person as a row of /i's "Persons" layer. i360's telecom knowledge on the person (MSISDN /
        IMSI it derived from the linked records) carries a review status: "recommended" waits for the analyst's
        approval, "approved" is accepted."""
        telecom = entity.get("telecom") if isinstance(entity.get("telecom"), dict) else {}
        review = telecom.get("i360_review") or {}
        claim = ((telecom.get("subscriber_identity_derivation") or {}).get("claim") or {}).get("value") or {}
        approved = telecom.get("approved_subscriber_identity") or {}
        statuses = {str(s) for s in review.values() if s}
        row = {"source_type": "Persons", "record_id": entity_id,
               "name": entity.get("canonical_name") or "", "given_name": entity.get("given_name") or "",
               "gender": entity.get("gender") or "", "nationality": entity.get("nationality") or "",
               "identifiers": entity.get("identifiers") or "", "person_type": entity.get("i360_entity_type") or "",
               "imei": telecom.get("imei") or "",
               "msisdn": claim.get("msisdn") or approved.get("msisdn") or telecom.get("msisdn") or "",
               "imsi": claim.get("imsi") or approved.get("imsi") or telecom.get("imsi") or "",
               "msisdn_status": review.get("msisdn") or "", "imsi_status": review.get("imsi") or "",
               "knowledge_status": "recommended" if "recommended" in statuses else
                                   ("approved" if statuses == {"approved"} else "")}
        return {k: (str(v) if not isinstance(v, str) else v) for k, v in row.items()}

    def log_chat_event(self, event: str, data: Any) -> None:
        """One log line per step, action and closing note of a chat turn (ids and counts, not the records),
        plus the start of each i360 answer's text, to see what i360 said before our model summarised it."""
        data = data if isinstance(data, dict) else {}
        if event == "step":
            line = f"step{' (error)' if data.get('error') else ''}: {str(data.get('text') or '')[:200]}"
            if data.get("detail"):
                line += f" [{str(data['detail'])[:300]}]"
            if data.get("trace"):
                line += f" [{str(data['trace'])[:300]}]"
            if data.get("tool") == "ask_i360" and "question" in data:
                line += f" [focus {data.get('focus') or '-'}, scope {data.get('scope') or '-'}, question {json.dumps(data.get('question'))}]"
            if data.get("trace"):
                line += f" [{str(data['trace'])[:800]}]"
        elif event == "action":
            row = data.get("row") or {}
            detail = {"show_items": lambda: f"{sum(len(g.get('rows') or []) for g in data.get('groups') or [])} rows, view {data.get('view')}",
                      "open_item": lambda: f"record {row.get('record_id') or row.get('event_id') or ''} item {row.get('i360_item_id') or ''}",
                      "open_layer": lambda: f"{data.get('layer_id')} view {data.get('view')}",
                      "open_entity": lambda: f"entity {data.get('entity_id')}"}.get(str(data.get("kind")), lambda: "")()
            line = f"action {data.get('kind')}: {detail}"
        elif event in {"note", "error"}:
            line = f"{event}: {str(data.get('text') or data.get('message') or '')[:200]}"
        elif event == "i360" and data.get("event") == "understood":
            # What i360 read in the question: field_words shows which of our words it took as a field.
            line = f"i360 understood: {json.dumps(data.get('data'), ensure_ascii=False)[:800]}"
            if data.get("layer"):
                line += f", layer {data['layer']}"
        elif event == "i360" and data.get("event") in {"answer", "error"}:
            inner = data.get("data") or {}
            cards = inner.get("cards") if isinstance(inner.get("cards"), dict) else {}
            line = (f"i360 answer: {len(inner.get('citations') or [])} citations, {len(answer_entities(inner))} entities, "
                    f"leg {inner.get('leg')}, keys {sorted(inner)[:20]}, cards {sorted(cards)[:20]}"
                    if data.get("event") == "answer" else f"i360 error: {inner.get('code')} {inner.get('message')}")
            if data.get("layer"):
                line += f", layer {data['layer']}"
            if data.get("event") == "answer":
                line += f"\n    i360 text: {json.dumps(str(inner.get('content') or '')[:600], ensure_ascii=False)}"
            if data.get("event") == "answer" and inner.get("leg") in {"lookup", "entity", "entities"}:
                # Entity answers' shapes are still being mapped: log their structure (ids and names, no record text).
                sample = {k: inner.get(k) for k in ("cards", "people", "outside_entities", "lookup", "subject", "entities") if inner.get(k)}
                line += f"\n    entity payload: {json.dumps(sample, ensure_ascii=True)[:3000]}"
        else:
            return
        self.log_message("chat %s", line)

    def chat_action(self, token: str, request: dict[str, Any]) -> Any:
        """A tag or note the i360 answer proposed, confirmed by the user: the chat service writes it."""
        settings = self.app.settings
        if not settings.chat_service_url:
            raise HlError(501, "chat_off", "The chat is not configured on this deployment.")
        action = request.get("action") if isinstance(request.get("action"), dict) else {}
        kind = {"tag": "tag", "note": "annotate", "annotate": "annotate"}.get(str(action.get("kind")))
        ids = action.get("ids")
        if not kind or not isinstance(ids, list) or not 0 < len(ids) <= 50:
            raise ValueError("Invalid action")
        # The chat service's POST /chat/actions: {kind: tag|annotate, ids (at most 50), type, value}.
        body = {"kind": kind, "ids": [str(i) for i in ids], "type": action.get("type"),
                "value": action.get("value") if action.get("value") is not None else action.get("text"),
                "text": action.get("text")}
        body["conversation_id"] = str(request.get("conversation_id") or "") or None
        return ChatServiceClient(settings.chat_service_url, token, settings.request_timeout_seconds).call("POST", "/actions", body)

    def start_stream(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Accel-Buffering", "no")  # the ingress must not hold the stream back
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Connection", "close")
        self.end_headers()
        self.close_connection = True

    def stream_event(self, event: str, data: Any) -> None:
        payload = f"event: {event}\ndata: {json.dumps(data, ensure_ascii=False)}\n\n".encode("utf-8")
        try:
            self.wfile.write(payload)
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError, OSError):
            raise ClientGone() from None

    def try_stream_event(self, event: str, data: Any) -> None:
        try:
            self.stream_event(event, data)
        except ClientGone:
            pass

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
        if path == "/api/chat/ask":
            self.chat_ask(token, self.read_json(400_000))
            return
        if path == "/api/chat/items":
            request = self.read_json(100_000)
            ids = [str(i) for i in request.get("ids") or [] if isinstance(i, str) and i.strip()][:100]
            if not ids:
                raise ValueError("Missing ids")
            locale = normalize_locale(str(request.get("locale") or "en"))
            self.send_json(200, {"groups": app.item_layers(token, ids, locale)})
            return
        if path == "/api/chat/action":
            self.send_json(200, self.chat_action(token, self.read_json(100_000)))
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
                if state.external_investigation_type and (request.get("layer") or {}).get("record_ids"):
                    self.send_json(201, self.save_layer_records(token, state, investigation_id, item, request))
                    return
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
        if path in {"/api/report/facts", "/api/report/block"}:
            request = self.read_json(10_000)
            investigation_id = require_investigation_id(request.get("investigation_id"))
            subject_id = analysis.compact_text(request.get("subject_id"), 240)
            if path.endswith("/facts"):
                self.send_json(200, app.report_facts(token, investigation_id, subject_id))
            else:
                self.send_json(200, app.report_block(token, investigation_id, str(request.get("block") or ""), subject_id))
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
            current = data.entities.get(entity_id) or {}
            if (current.get("telecom") or {}).get("i360_review") and action == "approve":
                # i360 derived these identifiers and keeps their status on the person: approving sets it.
                app.approve_i360_telecom(token, str(current.get("i360_entity_type") or ""), entity_id)
                entity = app.dataset(token, "en").entities.get(entity_id)
                self.send_json(201, {"saved": {"method": "i360_status", "status": "approved"}, "entity": entity})
                return
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


class AppToolHost:
    """What the chat's app tools read, with the user's token."""

    def __init__(self, app: App, token: str, locale: str):
        self.app, self.token, self.locale = app, token, locale

    def catalog_layers(self) -> list[dict[str, Any]]:
        return analysis.list_layers(self.app.dataset(self.token, self.locale), self.app.known_sources(self.locale))

    def item_layers(self, item_ids: list[str]) -> list[dict[str, Any]]:
        return self.app.item_layers(self.token, item_ids, self.locale)

    def entity(self, entity_type: str, entity_id: str) -> dict[str, Any] | None:
        """One entity i360 returned, read by id with the user's token, as the person viewer draws it."""
        return self.app.entity_record(self.token, entity_type, entity_id)

    item_field_ids_cache: set[str] | None = None  # per server: the estate's fields change with a deployment
    profile_labels_cache: dict[str, list[str]] | None = None
    # Words the chat would read as a field in every question ("ip", "model"): never sent as labels.
    LABEL_STOP_WORDS = {"ip", "os", "model", "brand", "time", "date", "type", "source", "location", "name", "id",
                        "latitude", "longitude", "lat", "lon", "record id", "record_id"}

    def index_field(self, path: str) -> str:
        """A profile field path (``user_agents_data.device_brand``, ``i360.ip.ip_sessions.source_ip``) as i360's
        index field (``device_brand``, ``source_ip``): the path itself, the layer's ``search_fields`` entry, or its
        trailing segments. '' when the index has no such field (it cannot be searched)."""
        known = self.item_field_ids()
        path = re.sub(r"\[\d+\]", "", str(path or "").removeprefix("i360."))
        for query in (self.app.profile.get("items_query") or {}).get("queries") or []:
            override = ((query or {}).get("search_fields") or {}).get(path)
            if override:
                return override if not known or override in known else ""
        if not known or path in known:
            return path
        parts = path.split(".")
        return next((".".join(parts[i:]) for i in range(1, len(parts)) if ".".join(parts[i:]) in known), "")

    def profile_labels(self) -> dict[str, list[str]]:
        """The profile's names for its layers' fields as the i360 chat's ``labels`` (index field -> words), built
        once: they are the same on every question."""
        if AppToolHost.profile_labels_cache is None:
            # The profile's own words for fields no layer column shows (a record's links: related_objects.id).
            labels: dict[str, list[str]] = {str(f): [str(w) for w in words] for f, words in
                                            (self.app.profile.get("chat_labels") or {}).items()
                                            if not str(f).startswith("_") and self.index_field(f)}
            for query in (self.app.profile.get("items_query") or {}).get("queries") or []:
                for path, name in ((query or {}).get("labels") or {}).items():
                    field = self.index_field(path) if not str(path).startswith("_") else ""
                    if not field:
                        continue
                    for word in (str(name).replace("_", " ").strip(), str(name).strip()):
                        if 3 < len(word) <= 40 and word.lower() not in self.LABEL_STOP_WORDS and word != field:
                            words = labels.setdefault(field, [])
                            if word.lower() not in {w.lower() for w in words}:
                                words.append(word)
            AppToolHost.profile_labels_cache = labels
        return AppToolHost.profile_labels_cache

    def item_field_ids(self) -> set[str]:
        """The ids of the index's item fields (HL ``GET /api/v1/meta/item-fields``): the keys the i360 chat's
        ``labels`` accept. Empty when the list cannot be read."""
        if AppToolHost.item_field_ids_cache is None:
            try:
                listing = self.app.client(self.token).get("/api/v1/meta/item-fields")
            except HlError as exc:
                print(f"item-fields not read: {exc}", file=sys.stderr, flush=True)
                return set()
            ids: set[str] = set()

            def collect(value: Any) -> None:
                if isinstance(value, list):
                    for entry in value:
                        collect(entry)
                elif isinstance(value, dict):
                    if isinstance(value.get("id"), str):
                        ids.add(value["id"])
                    for key in ("fields", "items", "data"):
                        collect(value.get(key))
            collect(listing)
            print(f"item-fields: {len(ids)} ids", file=sys.stderr, flush=True)
            AppToolHost.item_field_ids_cache = ids
        return AppToolHost.item_field_ids_cache

    def layers_scope(self) -> dict[str, Any] | None:
        """Our layers as the i360 chat's ``scope``: the profile's queries merged into one search."""
        request, exact = layers_search(self.app.profile.get("items_query") or {})
        if request is None:
            return None
        ids = [str(item.get("item_id")) for item in self.app.snapshot(self.token).items if item.get("item_id")]
        return {"kind": "results", "name": "Our layers", "query": "the app's layers", "ids": [],
                "total": len(ids), "request": request, "exact": exact}

    def constant_scope(self) -> dict[str, Any] | None:
        """All our layers as the i360 chat's ``scope``, the same on every question: their records, by i360 item id.
        A field/value scope cannot hold them in one request (the Cellular layers' coverage facet cannot sit inside
        an OR); the chat keeps a scope request up to 200,000 characters (about 5,000 ids)."""
        ids = sorted({str(i["item_id"]) for i in self.app.snapshot(self.token).items if i.get("item_id")})
        if not ids:
            return None
        return {"kind": "results", "name": "Our layers", "query": "the app's layers", "ids": [], "total": len(ids),
                "request": {"filters": [{"field": "item_id", "values": ids}]}}

    def layer_sets(self) -> dict[str, dict[str, Any]]:
        """Our layers as the i360 chat's ``sets``, from the profile: each layer's name (and ``words``) for its item
        types, sources, facets and filters. A question that names a layer is answered inside it."""
        sets: dict[str, dict[str, Any]] = {}
        for query in (self.app.profile.get("items_query") or {}).get("queries") or []:
            name = str((query or {}).get("layer") or "")
            request, _ = layers_search({"queries": [query]})
            if not name or request is None:
                continue
            entry = {k: request[k] for k in ("item_types", "source_applications", "facet_filters", "filters")
                     if request.get(k)}
            words = [str(w) for w in (query.get("words") or []) if str(w).strip()]
            sets[name] = {**({"words": [name] + words[:4]} if words else {}), **entry}
        return sets


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

"""Read the scenario's records, entities and locations from i360 for one signed-in user.

v1 approach: a per-user *snapshot*. The app pages through ``POST /items/search`` for the
scenario (with ``include: ["text"]``), completes each page with one ``POST /items/get``
(tags and parties are only on ``get``), maps every item to a UI row, and keeps the result in
memory for ``APP_SNAPSHOT_TTL`` seconds. The existing layer, link and derivation logic then
runs unchanged on those rows.

The snapshot is only a cache: it is keyed by the user's token, so it holds exactly what that
user may see, and any replica can rebuild it. It suits the demo datasets (hundreds to tens of
thousands of records). Pushing filters down to HL API is the next step for larger estates.
"""
from __future__ import annotations

import hashlib
import json
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Any, Callable

from .client import HlClient, HlError, NotOnThisEstate, list_hits, total_pages
from .mapping import Mapping

PAGE_SIZE = 100
EARLIEST = "1970-01-01T00:00:00Z"

ALL_FIELDS_PREFIX = "i360."
_SKIP_KEYS = {"urls", "found", "parent_ids"}


def _cell(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def item_fields(item: dict[str, Any]) -> dict[str, str]:
    """Every populated field of an i360 item as ``i360.<path>`` -> text, for "show all fields" layers.

    Nested objects become dotted paths; a list of scalars is joined; a list of annotations (dicts with
    ``value``) becomes "type: value" lines; tags become "type=value"; anything else is compact JSON.
    """
    out: dict[str, str] = {}

    def walk(value: Any, path: str, depth: int) -> None:
        if value in (None, "", [], {}):
            return
        if isinstance(value, dict):
            if depth >= 3:
                out[path] = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
                return
            for key, child in value.items():
                if key not in _SKIP_KEYS and not str(key).startswith("_"):
                    walk(child, f"{path}.{key}" if path else str(key), depth + 1)
            return
        if isinstance(value, list):
            if all(not isinstance(v, (dict, list)) for v in value):
                out[path] = "; ".join(_cell(v) for v in value if v not in (None, ""))
            elif all(isinstance(v, dict) and "value" in v for v in value):
                key = "value"
                if path.endswith("tags"):
                    out[path] = "; ".join(f"{v.get('type')}={_cell(v.get(key))}" for v in value)
                else:
                    out[path] = "\n".join(f"{v.get('type')}: {_cell(v.get(key))}" if v.get("type") else _cell(v.get(key))
                                           for v in value)
            else:
                out[path] = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            return
        out[path] = _cell(value)

    walk(item, "", 0)
    return {ALL_FIELDS_PREFIX + key: value for key, value in out.items() if value}



@dataclass
class Snapshot:
    """Raw i360 content for one user. Rows and assembled datasets are derived per locale on demand."""
    items: list[dict[str, Any]]
    entities: list[dict[str, Any]]
    locations: dict[str, dict[str, Any]]
    reviews: dict[str, dict[str, Any]]
    fetched_at: float
    truncated: bool = False
    warnings: list[str] = field(default_factory=list)
    derived: dict[str, Any] = field(default_factory=dict)
    lock: threading.RLock = field(default_factory=threading.RLock)

    def memo(self, key: str, build: Callable[[], Any]) -> Any:
        with self.lock:
            if key not in self.derived:
                self.derived[key] = build()
            return self.derived[key]


def _iso(value: datetime) -> str:
    return value.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _merge(hit: dict[str, Any], full: dict[str, Any] | None) -> dict[str, Any]:
    if not full or full.get("found") is False:
        return hit
    merged = dict(hit)
    for key, value in full.items():
        if key == "text" and isinstance(value, dict):
            text = dict(hit.get("text") or {})
            text.update({k: v for k, v in value.items() if v not in (None, "")})
            merged["text"] = text
        elif key == "location" and isinstance(value, dict):
            location = dict(hit.get("location") or {})
            location.update({k: v for k, v in value.items() if v not in (None, "")})
            merged["location"] = location
        elif value not in (None, [], {}, ""):
            merged[key] = value
    return merged


class ItemReader:
    def __init__(self, client: HlClient, mapping: Mapping, base_query: dict[str, Any], max_rows: int,
                 items_per_query: int = 0):
        self.client = client
        self.mapping = mapping
        query = dict(base_query or {})
        # A profile may list several queries ("queries"); each one is read on its own and may name the
        # layer its items appear in ("layer"). A plain items_query is one query, as before.
        self.specs = [self._spec(q) for q in (query.pop("queries", None) or [query])]
        # APP_ITEMS_PER_TYPE overrides every query's "limit" (one query per item type in a profile).
        if items_per_query > 0:
            self.specs = [(days, items_per_query, base, layer, everything)
                          for days, _, base, layer, everything in self.specs]
        self.recent_days, self.limit, self.base_query, self.layer, self.all_fields = self.specs[0]
        self.max_rows = max_rows
        self.warnings: list[str] = []
        # One entry per profile query: what was asked, what HL API reported and what came back.
        self.query_stats: list[dict[str, Any]] = []
        self.truncated = False

    @staticmethod
    def _spec(query: dict[str, Any]) -> tuple[int, int, dict[str, Any], str, bool]:
        query = dict(query or {})
        # "recent_days" is ours, not HL API's: it narrows the scan to the last N days of event time.
        recent_days = int(query.pop("recent_days", 0) or 0)
        # "limit" is ours too: keep only the newest N items, for small test datasets.
        limit = max(0, int(query.pop("limit", 0) or 0))
        # "layer" is ours too: the layer (source_type) these items are shown in.
        layer = str(query.pop("layer", "") or "")
        # "all_fields" is ours too: rows carry every populated item field as i360.<path>.
        everything = bool(query.pop("all_fields", False))
        return recent_days, limit, {k: v for k, v in query.items() if v not in (None, [], {})}, layer, everything

    def _query(self, window: tuple[str, str], page: int, page_size: int = PAGE_SIZE) -> dict[str, Any]:
        body = dict(self.base_query)
        body["time"] = {**(body.get("time") or {}), "from": window[0], "to": window[1], "field": "event"}
        body.update({"page_number": page, "page_size": page_size, "include": ["text"], "sort": "time", "order": "asc"})
        return self.client.search_items(body)

    def _collect_window(self, window: tuple[str, str], out: list[dict[str, Any]], depth: int = 0) -> None:
        if len(out) >= self.max_rows:
            self.truncated = True
            return
        first = self._query(window, 1)
        total = int(first.get("total") or 0)
        fetchable = int(first.get("total_pages") or 1) * PAGE_SIZE
        # Halving ~60 years reaches 1 ms after ~41 levels; the guard below ends it there.
        if total > fetchable and depth < 64:
            start, end = _parse(window[0]), _parse(window[1])
            middle = start + (end - start) / 2
            if middle - start > timedelta(seconds=1):
                self._collect_window((window[0], _iso(middle)), out, depth + 1)
                self._collect_window((_iso(middle + timedelta(milliseconds=1)), window[1]), out, depth + 1)
                return
            self.warnings.append(f"more than {fetchable} items share one instant; some were skipped")
        out.extend(first.get("items") or [])
        pages = int(first.get("total_pages") or 1)
        for page in range(2, pages + 1):
            if len(out) >= self.max_rows:
                self.truncated = True
                return
            out.extend(self._query(window, page).get("items") or [])

    def items(self) -> list[dict[str, Any]]:
        hits: list[dict[str, Any]] = []
        now = datetime.now(timezone.utc)
        end = _iso(now + timedelta(days=3650))
        for self.recent_days, self.limit, self.base_query, self.layer, self.all_fields in self.specs:
            start = _iso(now - timedelta(days=self.recent_days)) if self.recent_days > 0 else EARLIEST
            found: list[dict[str, Any]] = []
            reported_total = None
            if self.limit:
                # Newest first, a page at a time, until the limit or the end of the results.
                page = 1
                while len(found) < self.limit:
                    body = dict(self.base_query)
                    body["time"] = {**(body.get("time") or {}), "from": start, "to": end, "field": "event"}
                    body.update({"page_number": page, "page_size": min(PAGE_SIZE, self.limit),
                                 "include": ["text"], "sort": "time", "order": "desc"})
                    response = self.client.search_items(body)
                    if page == 1:
                        reported_total = response.get("total")
                        self.warnings.extend(f"{self.layer or 'query'}: {w}" for w in response.get("warnings") or [])
                    batch = response.get("items") or []
                    found.extend(batch[: self.limit - len(found)])
                    if len(batch) < body["page_size"] or page >= int(response.get("total_pages") or page):
                        break
                    page += 1
            else:
                self._collect_window((start, end), found)
            if self.layer or self.all_fields:
                mark = {"_layer": self.layer} if self.layer else {}
                if self.all_fields:
                    mark["_all_fields"] = True
                found = [{**hit, **mark} for hit in found]
            self.query_stats.append({
                "layer": self.layer, "query": {k: v for k, v in self.base_query.items() if k != "time"},
                "reported_total": reported_total, "returned": len(found),
                "with_location": sum(1 for hit in found if (hit.get("location") or {}).get("point")),
                "sources": sorted({str(hit.get("source_application")) for hit in found if hit.get("source_application")})[:8],
            })
            hits.extend(found)
        seen: set[str] = set()
        unique = []
        for hit in hits:
            item_id = str(hit.get("item_id") or "")
            if item_id and item_id not in seen:
                seen.add(item_id)
                unique.append(hit)
        if len(unique) > self.max_rows:
            unique = unique[: self.max_rows]
            self.truncated = True
        if not self.mapping.needs_get:
            return unique
        complete: list[dict[str, Any]] = []
        for start in range(0, len(unique), PAGE_SIZE):
            batch = unique[start:start + PAGE_SIZE]
            response = self.client.get_items([hit["item_id"] for hit in batch], self.mapping.get_include)
            self.warnings.extend(str(w) for w in response.get("warnings") or [])
            by_id = {str(item.get("item_id")): item for item in response.get("items") or []}
            complete.extend(_merge(hit, by_id.get(str(hit["item_id"]))) for hit in batch)
        return complete

    @staticmethod
    def _with_layer(row: dict[str, str], item: dict[str, Any]) -> dict[str, str]:
        if item.get("_layer"):
            row["source_type"] = str(item["_layer"])
        if item.get("_all_fields"):
            row.update(item_fields(item))
        return row

    def rows(self, locale: str) -> list[dict[str, str]]:
        return [self._with_layer(self.mapping.item_to_row(item, locale), item) for item in self.items()]

    def _instances(self, entity_type: str) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        page = 1
        while True:
            try:
                response = self.client.search_entities(entity_type, {"page_number": page, "page_size": PAGE_SIZE})
            except NotOnThisEstate:
                self.warnings.append(f"entity search is not available on this estate ({entity_type})")
                return out
            except HlError as exc:
                # 403: the type exists but this user may not read it (e.g. demo types on another estate).
                if exc.status in {400, 403, 404, 422}:
                    self.warnings.append(f"entity type {entity_type} is not readable here: {exc.code}")
                    return out
                raise
            out.extend(hit for hit in list_hits(response) if not hit.get("deleted"))
            if page >= total_pages(response) or not list_hits(response):
                return out
            page += 1

    def entities(self) -> list[dict[str, Any]]:
        records = []
        for entity_type in self.mapping.entities.get("types") or []:
            for instance in self._instances(entity_type):
                record = self.mapping.instance_to_entity(instance)
                if record.get("entity_id"):
                    records.append(record)
        return records

    def locations(self) -> dict[str, dict[str, Any]]:
        locations: dict[str, dict[str, Any]] = {}
        for entity_type in self.mapping.locations.get("types") or []:
            for instance in self._instances(entity_type):
                location_id, record = self.mapping.instance_to_location(instance)
                if location_id:
                    locations[location_id] = record
        return locations


class SnapshotCache:
    """Per-user cache. Nothing in it outlives the TTL or the process."""

    def __init__(self, ttl_seconds: int):
        self.ttl = ttl_seconds
        self._items: dict[tuple[str, str], Snapshot] = {}
        self._locks: dict[tuple[str, str], threading.Lock] = {}
        self._guard = threading.Lock()

    @staticmethod
    def key(token: str, scope: str = "") -> tuple[str, str]:
        return hashlib.sha256(token.encode("utf-8")).hexdigest(), scope

    def get(self, token: str, build: Callable[[], Snapshot], refresh: bool = False) -> Snapshot:
        key = self.key(token, "")
        with self._guard:
            lock = self._locks.setdefault(key, threading.Lock())
            self._evict()
        with lock:
            with self._guard:
                cached = self._items.get(key)
            if cached and not refresh and time.time() - cached.fetched_at < self.ttl:
                return cached
            snapshot = build()
            with self._guard:
                self._items[key] = snapshot
            return snapshot

    def drop(self, token: str) -> None:
        digest = hashlib.sha256(token.encode("utf-8")).hexdigest()
        with self._guard:
            for key in [key for key in self._items if key[0] == digest]:
                self._items.pop(key, None)

    def _evict(self) -> None:
        """Called with ``_guard`` held. Locks are removed only when nobody holds them."""
        now = time.time()
        for key in [key for key, snap in self._items.items() if now - snap.fetched_at > self.ttl * 4]:
            self._items.pop(key, None)
        for key in [key for key in self._locks if key not in self._items]:
            if not self._locks[key].locked():
                self._locks.pop(key, None)

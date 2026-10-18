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
import re
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
_SKIP_KEYS = {"urls", "found", "parent_ids", "related_objects"}


def _cell(value: Any) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def entity_presentation(record: dict[str, Any], entity_type: str) -> dict[str, Any]:
    """Mapping helper fields -> what the entity viewer reads.

    ``image_file_id`` becomes ``image_url`` (served through /api/entity-files, which adds the user's
    token); ``telecom_imei`` / ``telecom_msisdn`` become the ``telecom`` block the person viewer shows.
    """
    record = dict(record)
    file_id = record.pop("image_file_id", None)
    if file_id not in (None, "") and record.get("entity_id"):
        record["image_url"] = f"/api/entity-files/{entity_type}/{record['entity_id']}/{file_id}"
    telecom = {key: record.pop(f"telecom_{key}") for key in ("imei", "msisdn", "imsi")
               if record.get(f"telecom_{key}") not in (None, "", [])}
    for key in ("imei", "msisdn", "imsi"):
        record.pop(f"telecom_{key}", None)
    review = telecom_review(telecom)
    if "i360_review" in review:  # the derived values live in the review / approved identity, not as plain ones
        telecom.pop("msisdn", None)
        telecom.pop("imsi", None)
    telecom.update(review)
    if telecom:
        record["telecom"] = {**(record.get("telecom") or {}), **telecom}
    record.setdefault("i360_entity_type", entity_type)
    return record


def _identifier_entries(value: Any, key: str) -> list[dict[str, str]]:
    """i360 subscriber identifiers as [{value, status}]: a plain value, an entry {key, status}, a list of
    entries, or an entry nested once more under its field name ({"device_imsi": {"imsi", "status"}})."""
    if isinstance(value, list):
        return [e for v in value for e in _identifier_entries(v, key)]
    if isinstance(value, dict):
        if key in value:
            return [{"value": str(value.get(key) or ""), "status": str(value.get("status") or "")}] if value.get(key) else []
        nested = [v for v in value.values() if isinstance(v, (dict, list))]
        return [e for v in nested for e in _identifier_entries(v, key)]
    return [{"value": str(value), "status": ""}] if value not in (None, "") else []


TELECOM_RECOMMENDED, TELECOM_APPROVED = "Recommended", "Approved"  # the status values on the person in i360


def review_status(status: Any) -> str:
    """i360's status text as the viewer's state: "Recommended" -> recommended, "Approved" -> approved."""
    return str(status or "").strip().lower()


def telecom_review(telecom: dict[str, Any]) -> dict[str, Any]:
    """MSISDN / IMSI that i360 derived from the cellular location records linked to the person carry a
    status. Recommended ones are the viewer's review card (approval needed); approved ones are its approved
    identity. Plain values without a status stay as they are."""
    entries = {key: _identifier_entries(telecom.get(key), key) for key in ("msisdn", "imsi")}
    if not any(e["status"] for values in entries.values() for e in values):
        return {k: ", ".join(e["value"] for e in v) for k, v in entries.items() if v and k in telecom}
    first = {k: (v[0] if v else {}) for k, v in entries.items()}
    statuses = {k: review_status(e.get("status")) for k, e in first.items() if e}
    identity = {k: e["value"] for k, e in first.items() if e}
    out: dict[str, Any] = {"msisdn": None, "imsi": None, "i360_review": statuses}
    if all(s == "approved" for s in statuses.values()):
        out["approved_subscriber_identity"] = {**identity, "source": "i360"}
    else:
        out["subscriber_identity_derivation"] = {"status": "candidate", "source": "i360",
                                                 "claim": {"value": identity}, "supporting_record_ids": []}
    return {k: v for k, v in out.items() if v is not None}


CALL_LAYERS: set[str] = set()


def call_fields(item: dict[str, Any]) -> dict[str, str]:
    """An i360 call as the app's call viewer reads it: call_id switches the viewer on; side A is the
    target party (target_indication true), side B the other party."""
    out = {"call_id": _cell(item.get("item_id") or ""), "call_started_at_utc": _cell(item.get("event_time") or "")}
    if isinstance(item.get("duration_ms"), (int, float)):
        out["call_duration_seconds"] = _cell(round(item["duration_ms"] / 1000, 1))
    parties = [p for p in item.get("parties") or [] if isinstance(p, dict)]
    target = next((p for p in parties if str(p.get("target_indication")).lower() == "true"), parties[0] if parties else {})
    other = next((p for p in parties if p is not target), {})
    for side, party in (("side_a", target), ("side_b", other)):
        ids = {str(i.get("type")): _cell(i.get("value")) for i in party.get("identifiers") or [] if isinstance(i, dict)}
        if ids.get("msisdn"):
            out[f"{side}_number"] = out[f"{side}_sim"] = ids["msisdn"]
        if ids.get("imei"):
            out[f"{side}_imei"] = ids["imei"]
    out.update(call_conversation(item, out))
    return out


_LINE_TIME = re.compile(r"_?\[(\d{1,2}:\d{2}(?::\d{2})?)\]\s*")


def _timed_lines(text: Any) -> list[tuple[str, str]]:
    """i360 transcript text as (time, line): "_[00:05] text" marks where each line starts."""
    text = str(text or "").strip()
    if not text:
        return []
    marks = list(_LINE_TIME.finditer(text))
    if not marks:
        return [("", text)]
    lines = []
    for index, mark in enumerate(marks):
        end = marks[index + 1].start() if index + 1 < len(marks) else len(text)
        line = text[mark.end():end].strip()
        if line:
            lines.append((mark.group(1), line))
    return lines


def call_conversation(item: dict[str, Any], sides: dict[str, str]) -> dict[str, str]:
    """The call viewer's conversation: call_transcript paragraphs ("speaker: text") and call_transcript_en
    paragraphs at the same positions. The original lines are the transcription insights (side A =
    party_position A) and the English their translation insights; without those, text.transcript and
    text.english. An English line with no original is shown on its own; the English is not the summary."""
    entries: list[dict[str, str]] = []
    insights = [i for i in item.get("insights") or [] if isinstance(i, dict)]
    spoken = [i for i in insights if i.get("type") == "transcription"]
    translated = [i for i in insights if i.get("type") == "translation"]
    if spoken and translated:
        # Per party, the n-th translation is the n-th line said (the times typed on translations do not
        # match the originals'); a line with no time of its own takes its translation's.
        for position in sorted({str(i.get("party_position") or "").upper() for i in spoken + translated}):
            said = [l for i in spoken if str(i.get("party_position") or "").upper() == position for l in _timed_lines(i.get("value"))]
            english = [l for i in translated if str(i.get("party_position") or "").upper() == position for l in _timed_lines(i.get("value"))]
            side = "a" if position == "A" else "b"
            for index in range(max(len(said), len(english))):
                at, line = said[index] if index < len(said) else ("", "")
                en_at, en_line = english[index] if index < len(english) else ("", "")
                if line:
                    entries.append({"time": at or en_at, "side": side, "text": line, "en": en_line})
                else:
                    entries.append({"time": en_at, "side": side, "text": en_line, "en": en_line})
    else:
        if spoken:
            for insight in spoken:
                side = "a" if str(insight.get("party_position") or "").upper() == "A" else "b"
                for at, line in _timed_lines(insight.get("value")):
                    entries.append({"time": at, "side": side, "text": line, "en": ""})
        else:
            for at, line in _timed_lines((item.get("text") or {}).get("transcript")):
                entries.append({"time": at, "side": "", "text": line, "en": ""})
        for at, line in _timed_lines((item.get("text") or {}).get("english")):
            same = next((e for e in entries if e["time"] and e["time"] == at and not e["en"]), None)
            if same:
                same["en"] = line
            else:
                entries.append({"time": at, "side": "", "text": line, "en": line, "translation_only": "1"})
    if not entries:
        return {}
    entries.sort(key=lambda e: [int(n) for n in e["time"].split(":")] if e["time"] else [10**6])

    def speaker(entry: dict[str, str]) -> str:
        at = f" · {entry['time']}" if entry["time"] else ""
        if entry.get("translation_only"):
            return f"English{at}"
        if entry["side"] == "a":  # the viewer draws a speaker starting "IMEI" on side A
            return f"IMEI {sides.get('side_a_imei') or 'side A'}{at}"
        if entry["side"] == "b":
            return f"{sides.get('side_b_number') or 'Side B'}{at}"
        return f"Speaker{at}"

    original = [f"{speaker(e)}: {e['text']}" for e in entries]
    english = [f"{speaker(e)}: {e['en'] or e['text']}" for e in entries]
    return {"call_transcript": "\n\n".join(original), "call_transcript_en": "\n\n".join(english),
            "event_summary": ""}


def i360_links(item: dict[str, Any]) -> list[dict[str, str]]:
    """What i360 links this item to (its related_objects): entities, and other items (type ITEM) with the
    value the link was made on (matching_value) and how (relation_source, e.g. automatic)."""
    out = []
    for obj in item.get("related_objects") or []:
        if isinstance(obj, dict) and obj.get("id"):
            out.append({"id": str(obj["id"]), "type": str(obj.get("type") or ""), "relation": str(obj.get("relation_type") or ""),
                        "source": str(obj.get("relation_source") or ""),
                        "values": [str(v) for v in obj.get("matching_value") or [] if v not in (None, "")]})
    return out


def i360_identifiers(item: dict[str, Any]) -> list[list[str]]:
    """The item's identifier values as [field, value]: asset_identifier and each party's identifiers."""
    out = []
    if item.get("asset_identifier") not in (None, ""):
        out.append(["asset_identifier", str(item["asset_identifier"])])
    for party in item.get("parties") or []:
        if not isinstance(party, dict):
            continue
        flag = str(party.get("target_indication")).strip().lower()
        role = "target" if flag == "true" else "other" if flag == "false" else str(party.get("role") or "party")
        for ident in party.get("identifiers") or []:
            if isinstance(ident, dict) and ident.get("type") and ident.get("value") not in (None, ""):
                out.append([f"parties.{role}.{ident['type']}", str(ident["value"])])
    return out


def item_fields(item: dict[str, Any]) -> dict[str, str]:
    """Every populated field of an i360 item as ``i360.<path>`` -> text, for "show all fields" layers.

    Nested objects become dotted paths; a list of scalars is joined; a list of annotations (dicts with
    ``type`` and ``value``) becomes "type: value" lines; tags become "type=value"; a one-entry list of objects
    (additional_info, user_agents_data, ip.ip_sessions) is flattened like an object; anything else is compact JSON.
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
            elif all(isinstance(v, dict) and "value" in v and "type" in v for v in value):
                key = "value"
                if path.endswith("tags"):
                    out[path] = "; ".join(f"{v.get('type')}={_cell(v.get(key))}" for v in value)
                else:
                    out[path] = "\n".join(f"{v.get('type')}: {_cell(v.get(key))}" if v.get("type") else _cell(v.get(key))
                                           for v in value)
            elif all(isinstance(v, dict) for v in value) and len(value) == 1:
                walk(value[0], path, depth)  # e.g. additional_info, user_agents_data, ip.ip_sessions
            elif all(isinstance(v, dict) for v in value) and len(value) <= 5 and depth < 3:
                for index, entry in enumerate(value):
                    walk(entry, f"{path}[{index}]", depth + 1)
            else:
                out[path] = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
            return
        if path.endswith("_time") and isinstance(value, (int, float)) and value > 10**11:  # epoch ms -> ISO UTC
            value = datetime.fromtimestamp(value / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        out[path] = _cell(value)

    flat = {k: v for k, v in item.items() if k not in ("parties", "insights", "locations")}
    if isinstance(flat.get("sms"), dict):
        flat["sms"] = {k: v for k, v in flat["sms"].items() if k != "parts"}
    walk(flat, "", 0)
    # SMS parts in their order, as one text.
    parts = (item.get("sms") or {}).get("parts") if isinstance(item.get("sms"), dict) else None
    if parts:
        ordered = sorted((p for p in parts if isinstance(p, dict)), key=lambda p: str(p.get("key") or ""))
        out["sms.parts"] = "\n".join(_cell(p.get("value")) for p in ordered if p.get("value") not in (None, ""))
    # The cell the record was served by: the value of its cell entries (etsi_cgi, etsi_ecgi, ...); the point is in location.
    cells = [str(e["value"]) for e in item.get("locations") or []
             if isinstance(e, dict) and str(e.get("type") or "").startswith("etsi") and e.get("value") not in (None, "")]
    if cells:
        out["locations.cell_id"] = "; ".join(dict.fromkeys(cells))
    # Insights by type (insights.post_comment, insights.transcription, ...): each can carry its own name.
    for insight in item.get("insights") or []:
        if isinstance(insight, dict) and insight.get("value") not in (None, ""):
            key = f"insights.{insight.get('type') or 'note'}"
            out[key] = "\n".join(filter(None, [out.get(key), _cell(insight["value"])]))
    # Call/message parties by role: parties.from.msisdn, parties.to.imei, ... (not raw JSON).
    for party in item.get("parties") or []:
        if not isinstance(party, dict):
            continue
        # The target party (target_indication true) and the other party (false), as in the raw TARGET/OP columns;
        # without the flag, by role (from/to).
        flag = str(party.get("target_indication")).strip().lower()
        role = "target" if flag == "true" else "other" if flag == "false" else str(party.get("role") or party.get("position") or "party")
        for ident in party.get("identifiers") or []:
            if isinstance(ident, dict) and ident.get("type") and ident.get("value") not in (None, ""):
                key = f"parties.{role}.{ident['type']}"
                out[key] = "; ".join(filter(None, [out.get(key), _cell(ident["value"])]))
        if party.get("name"):
            out[f"parties.{role}.name"] = _cell(party["name"])
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


def layers_search(items_query: dict[str, Any], now: datetime | None = None) -> tuple[dict[str, Any] | None, bool]:
    """The profile's layer queries as one HL API ``items/search`` body, for the i360 chat's ``scope``.

    A list filter (``item_types``, ``source_applications``, ...) becomes the union of its values when every
    query has it and is dropped when some query does not; any other filter is kept only when all queries
    agree. So the body covers at least every layer's items. ``limit`` (newest N) cannot be said in a search
    and is left out. Returns ``(body, exact)``: ``exact`` is false when the body may match more than the
    layers' queries (before their limits).
    """
    specs = [ItemReader._spec(q) for q in ((items_query or {}).get("queries") or [items_query or {}])]
    filters = [base for _, _, base, _, _ in specs]
    days = [d for d, _, _, _, _ in specs]
    body: dict[str, Any] = {}
    for key in sorted({k for f in filters for k in f}):
        values = [f.get(key) for f in filters]
        if any(v is None for v in values):
            continue
        if all(isinstance(v, list) for v in values):
            body[key] = []
            for v in values:
                body[key] += [x for x in v if x not in body[key]]
        elif all(v == values[0] for v in values):
            body[key] = values[0]
    if all(d > 0 for d in days):
        now = now or datetime.now(timezone.utc)
        body["time"] = {**(body.get("time") or {}), "from": _iso(now - timedelta(days=max(days))),
                        "to": _iso(now + timedelta(days=3650)), "field": "event"}
    # Exact when the queries differ in at most one filter (a union of one list is the same as the OR of
    # the queries) and share the same window.
    differing = {k for f in filters for k in f if any(g.get(k) != f.get(k) for g in filters)}
    exact = len(differing) <= 1 and all(k in body for k in differing) and len(set(days)) == 1
    return body, exact


class ItemReader:
    def __init__(self, client: HlClient, mapping: Mapping, base_query: dict[str, Any], max_rows: int,
                 items_per_query: int = 0):
        self.client = client
        self.mapping = mapping
        query = dict(base_query or {})
        # "i360_links" (profile-wide): record-to-entity links are i360's own (related_objects), not the app's
        # field-match rules.
        self.i360_links = bool(query.pop("i360_links", False))
        # A profile may list several queries ("queries"); each one is read on its own and may name the
        # layer its items appear in ("layer"). A plain items_query is one query, as before.
        self.specs = [self._spec(q) for q in (query.pop("queries", None) or [query])]
        # APP_ITEMS_PER_TYPE is the default "limit" for queries that do not set their own.
        if items_per_query > 0:
            self.specs = [(days, limit or items_per_query, base, layer, everything)
                          for days, limit, base, layer, everything in self.specs]
        self.recent_days, self.limit, self.base_query, self.layer, self.all_fields = self.specs[0]
        self.max_rows = max_rows
        self.warnings: list[str] = []
        # One entry per profile query: what was asked, what HL API reported and what came back.
        self.query_stats: list[dict[str, Any]] = []
        self.truncated = False

    @staticmethod
    def _spec(query: dict[str, Any]) -> tuple[int, int, dict[str, Any], str, Any]:
        query = dict(query or {})
        # "recent_days" is ours, not HL API's: it narrows the scan to the last N days of event time.
        recent_days = int(query.pop("recent_days", 0) or 0)
        # "limit" is ours too: keep only the newest N items, for small test datasets.
        limit = max(0, int(query.pop("limit", 0) or 0))
        # "layer" is ours too: the layer (source_type) these items are shown in.
        layer = str(query.pop("layer", "") or "")
        query.pop("labels", None)  # display names for the layer's fields; read by the server, not sent
        query.pop("labels_by_id", None)  # the same for rows read by id (items/get alone); read by the server
        if query.pop("call_record", False) and layer:
            CALL_LAYERS.add(layer)  # rows get the fields the app's call viewer reads (see call_fields)
        # "all_fields" is ours too: rows carry every populated item field as i360.<path>;
        # "fields" (a list of paths such as ["item_id", "location"]) keeps only those fields.
        everything = query.pop("all_fields", False)
        only = query.pop("fields", None)
        if only:
            everything = [str(path) for path in only]
        everything = everything if isinstance(everything, list) else bool(everything)
        # Keys starting with "_" are notes in the profile (e.g. "_comment"); HL API refuses unknown fields.
        base = {k: v for k, v in query.items() if v not in (None, [], {}) and not str(k).startswith("_")}
        return recent_days, limit, base, layer, everything

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
            if self.layer or self.all_fields or self.i360_links:
                mark = {"_layer": self.layer} if self.layer else {}
                if self.i360_links:
                    mark["_i360_links"] = True
                if self.layer in CALL_LAYERS:
                    mark["_call_record"] = True
                if self.all_fields:
                    mark["_all_fields"] = self.all_fields
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
        if item.get("_i360_links"):
            row["i360_links"] = json.dumps(i360_links(item), ensure_ascii=False)
            row["i360_identifiers"] = json.dumps(i360_identifiers(item), ensure_ascii=False)
        if item.get("_layer"):
            row["source_type"] = str(item["_layer"])
        if item.get("_call_record"):
            row.update(call_fields(item))
        if item.get("_all_fields"):
            fields = item_fields(item)
            only = item["_all_fields"] if isinstance(item["_all_fields"], list) else None
            if only:
                keep = tuple(ALL_FIELDS_PREFIX + path for path in only)
                fields = {k: v for k, v in fields.items() if any(k == p or k.startswith(p + ".") for p in keep)}
            row.update(fields)
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
                record = entity_presentation(self.mapping.instance_to_entity(instance), entity_type)
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

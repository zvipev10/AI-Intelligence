"""Convert i360 items and entity instances into the row shapes the UI already draws.

The UI (``app.js``) and the layer logic work on flat rows shaped like the old demo CSV:
``event_id``, ``timestamp_utc``, ``source_type``, ``location_id``, ``event_summary`` and the
source-specific columns (``target_imei``, ``ip_public``, ``call_transcript`` ...).

Where each column comes from in i360 is configuration, not code: ``mapping/*.json``.
A column is a *path expression* evaluated against the HL API JSON:

    event_time                              a top-level key
    location.point.lat                      nested keys
    tags[type=imei].value                   first list element whose ``type`` is ``imei``
    parties[0].identifiers[type=msisdn].value
    tags[type=event_id].value | item_id     alternatives: the first non-empty value wins
    'Cellular Calls'                        a literal

A column may also be ``{"he": expr, "en": expr}`` to pick per locale.
When the ingestion team publishes its field list, only the JSON changes.
"""
from __future__ import annotations

import json
import re
from functools import lru_cache
from pathlib import Path
from typing import Any

_SEGMENT = re.compile(r"^(?P<name>[^\[\]]+)?(?P<selectors>(\[[^\]]*\])*)$")
_SELECTOR = re.compile(r"\[([^\]]*)\]")


def _select(value: Any, selector: str) -> Any:
    if not isinstance(value, list):
        return None
    selector = selector.strip()
    if selector.isdigit():
        index = int(selector)
        return value[index] if index < len(value) else None
    if "=" in selector:
        key, expected = (part.strip() for part in selector.split("=", 1))
        expected = expected.strip("'\"")
        for element in value:
            if isinstance(element, dict) and str(element.get(key)) == expected:
                return element
        return None
    return None


def _walk(data: Any, path: str) -> Any:
    current = data
    for raw_segment in _split_dots(path):
        match = _SEGMENT.match(raw_segment)
        if not match:
            return None
        name = match.group("name")
        if name:
            if not isinstance(current, dict):
                return None
            current = current.get(name)
        for selector in _SELECTOR.findall(match.group("selectors") or ""):
            current = _select(current, selector)
        if current is None:
            return None
    return current


def _split_dots(path: str) -> list[str]:
    parts, depth, buffer = [], 0, ""
    for char in path:
        if char == "[":
            depth += 1
        elif char == "]":
            depth -= 1
        if char == "." and depth == 0:
            parts.append(buffer)
            buffer = ""
        else:
            buffer += char
    parts.append(buffer)
    return [part.strip() for part in parts if part.strip()]


def _empty(value: Any) -> bool:
    return value is None or value == "" or value == [] or value == {}


def evaluate(data: Any, expression: str) -> Any:
    for alternative in str(expression).split("|"):
        alternative = alternative.strip()
        if not alternative:
            continue
        if len(alternative) >= 2 and alternative[0] == alternative[-1] and alternative[0] in "'\"":
            return alternative[1:-1]
        value = _walk(data, alternative)
        if not _empty(value):
            return value
    return None


def as_cell(value: Any) -> str:
    """Rows are strings, as the CSV was."""
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float):
        return str(int(value)) if value.is_integer() and abs(value) < 1e15 else repr(value)
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


class Mapping:
    def __init__(self, spec: dict[str, Any]):
        self.spec = spec
        items = spec.get("items") or {}
        self.record_id = items.get("record_id") or "item_id"
        self.fields: dict[str, Any] = items.get("fields") or {}
        self.tag_passthrough: bool = bool(items.get("tag_passthrough", True))
        self.get_include: list[str] = list(items.get("get_include") or [])
        self.needs_get: bool = bool(items.get("needs_get", True))
        self.value_labels: dict[str, dict[str, str]] = spec.get("value_labels") or {}
        self.label_fields: list[str] = list(spec.get("label_fields") or [])
        self.entities: dict[str, Any] = spec.get("entities") or {}
        self.locations: dict[str, Any] = spec.get("locations") or {}

    # -- items -------------------------------------------------------------------------
    def item_to_row(self, item: dict[str, Any], locale: str = "he") -> dict[str, str]:
        row: dict[str, str] = {}
        if self.tag_passthrough:
            for tag in item.get("tags") or []:
                if isinstance(tag, dict) and tag.get("type") and not _empty(tag.get("value")):
                    row.setdefault(str(tag["type"]), as_cell(tag["value"]))
        for column, expression in self.fields.items():
            if isinstance(expression, dict):
                expression = expression.get(locale) or expression.get("he") or next(iter(expression.values()), "")
            value = evaluate(item, expression)
            if not _empty(value):
                row[column] = as_cell(value)
            else:
                row.setdefault(column, "")
        record_id = as_cell(evaluate(item, self.record_id)) or as_cell(item.get("item_id"))
        row["event_id"] = row.get("event_id") or record_id
        row["record_id"] = row.get("record_id") or row["event_id"]
        row["i360_item_id"] = as_cell(item.get("item_id"))
        if locale == "en":
            labels = self.value_labels.get("en") or {}
            for column in self.label_fields:
                if row.get(column) in labels:
                    row[column] = labels[row[column]]
        return row

    # -- reference entities and locations ---------------------------------------------
    @staticmethod
    def _record(instance: dict[str, Any], spec: dict[str, Any]) -> dict[str, Any]:
        record: dict[str, Any] = {}
        json_path = spec.get("record_json")
        if json_path:
            raw = evaluate(instance, json_path)
            if isinstance(raw, str):
                try:
                    raw = json.loads(raw)
                except json.JSONDecodeError:
                    raw = None
            if isinstance(raw, dict):
                record.update(raw)
        for key, expression in (spec.get("fields") or {}).items():
            value = evaluate(instance, expression)
            if not _empty(value):
                record.setdefault(key, value)
        return record

    def instance_to_entity(self, instance: dict[str, Any]) -> dict[str, Any]:
        return self._record(instance, self.entities)

    def instance_to_location(self, instance: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        record = self._record(instance, self.locations)
        location_id = str(record.pop("location_id", "") or instance.get("entity_id") or "")
        for key in ("latitude", "longitude"):
            if record.get(key) not in (None, ""):
                try:
                    record[key] = float(record[key])
                except (TypeError, ValueError):
                    pass
        return location_id, record


@lru_cache(maxsize=4)
def load_mapping(path: str) -> Mapping:
    return Mapping(json.loads(Path(path).read_text(encoding="utf-8")))

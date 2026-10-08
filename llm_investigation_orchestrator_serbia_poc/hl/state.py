"""The user's saved work, stored as i360 entity records.

Three types (names carry ``APP_TYPE_PREFIX``, default ``AII_``), all with one section ``main``:

- ``AII_INVESTIGATION``     one per investigation
- ``AII_MEMORY_ITEM``       one per saved item (layer, object, area, collection request, ...)
- ``AII_TELECOM_APPROVAL``  one per reviewed subscriber-identity derivation

Rules from the HL API docs that shape this module:
- HL API requires the caller to supply ``entity_id`` on create (``general.entity_id`` is mandatory);
  we send a fresh UUID, keep our own key in a field and search by it;
- ``actors`` is left out on create, so HL API grants the record to the signed-in user and it
  appears in that user's searches;
- every saved item is its own record, so two writers never overwrite each other and
  deleting an item is a soft delete of that record (there is no delete-link operation);
- a create is read back before we report success; writes are never retried blindly.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from typing import Any

from .client import HlClient, HlError, list_hits, total_pages

SECTION = "main"
PAGE_SIZE = 100

MEMORY_GROUPS = ("chat_summaries", "layers", "artifacts", "collection_requests", "entity_enrichments")


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def fields_of(instance: dict[str, Any]) -> dict[str, Any]:
    sections = instance.get("sections")
    if isinstance(sections, dict) and isinstance(sections.get(SECTION), dict):
        return sections[SECTION]
    return instance


def entity_id_of(response: dict[str, Any]) -> str:
    for key in ("entity_id", "id", "entityId"):
        if response.get(key):
            return str(response[key])
    return ""


def _payload(instance: dict[str, Any]) -> dict[str, Any]:
    raw = fields_of(instance).get("payload")
    if isinstance(raw, dict):
        return raw
    try:
        value = json.loads(raw or "{}")
    except (TypeError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


# The model provisioned by tools/provision_types.py (CreateEntityTypeRequest shape, contract 252).
def _first(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return None


def _iso_time(value: Any) -> Any:
    if isinstance(value, (int, float)) and value > 10**11:  # epoch milliseconds
        return datetime.fromtimestamp(value / 1000, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    return value


def external_investigation_header(instance: dict[str, Any]) -> dict[str, Any]:
    """An investigation record that i360 owns (e.g. INTELLIGENCE_INVESTIGATION), in the app's shape."""
    sections = instance.get("sections") if isinstance(instance.get("sections"), dict) else {}
    general = _first(sections.get("general"), instance.get("general")) or {}
    details = _first(sections.get("investigation_details"), instance.get("investigation_details")) or {}
    metadata = instance.get("metadata") if isinstance(instance.get("metadata"), dict) else {}
    creator = general.get("creator") if isinstance(general.get("creator"), dict) else {}
    entity_id = entity_id_of(instance) or str(general.get("entity_id") or "")
    created = _iso_time(_first(general.get("creation_time"), instance.get("creation_time"), metadata.get("creation_time")))
    updated = _iso_time(_first(general.get("user_modification_time"), general.get("last_modification_time"),
                               instance.get("last_modification_time"), metadata.get("user_modification_time"))) or created
    return {
        "investigation_id": entity_id,
        "name": str(_first(instance.get("entity_name"), general.get("entity_name"), instance.get("name"), entity_id) or "Investigation"),
        "created_at_utc": created,
        "updated_at_utc": updated,
        "i360_entity_id": entity_id,
        "status": _first(details.get("status"), general.get("entity_status")),
        "activity_level": details.get("activity_level"),
        "research_question": details.get("research_question"),
        "next_milestone": _first(details.get("next_milstone"), details.get("next_milestone")),
        "created_by": _first(instance.get("creator_user_display"), creator.get("name")),
    }


def type_definitions(prefix: str) -> list[dict[str, Any]]:
    def text(name: str, searchable: bool = False) -> dict[str, Any]:
        field = {"name": name, "type": "TEXT"}
        if searchable:
            field["searchable"] = True
        return field

    return [
        {
            "type": f"{prefix}INVESTIGATION",
            "display_name": "AI-Intelligence investigation",
            "title_path": f"{SECTION}.name",
            "sections": [{"name": SECTION, "fields": [
                text("investigation_key", True), text("name", True), text("scenario", True),
                text("created_at_utc"), text("updated_at_utc"),
            ]}],
        },
        {
            "type": f"{prefix}MEMORY_ITEM",
            "display_name": "AI-Intelligence saved item",
            "title_path": f"{SECTION}.label",
            "sections": [{"name": SECTION, "fields": [
                text("investigation_key", True), text("item_key", True), text("group", True),
                text("kind"), text("label", True), text("comment"), text("saved_at_utc"),
                {"name": "payload", "type": "RICH_TEXT"},
            ]}],
        },
        {
            "type": f"{prefix}TELECOM_APPROVAL",
            "display_name": "AI-Intelligence telecom identity review",
            "title_path": f"{SECTION}.derivation_id",
            "sections": [{"name": SECTION, "fields": [
                text("derivation_id", True), text("entity_ref", True), text("scenario", True),
                text("review_state"), text("msisdn"), text("imsi"), text("reviewed_at_utc"),
                text("reviewed_by"), {"name": "payload", "type": "RICH_TEXT"},
            ]}],
        },
    ]


class StateStore:
    def __init__(self, client: HlClient, *, investigation_type: str, memory_item_type: str,
                 approval_type: str, scenario: str, external_investigation_type: str = ""):
        self.client = client
        self.investigation_type = investigation_type
        self.external_investigation_type = external_investigation_type
        self.memory_item_type = memory_item_type
        self.approval_type = approval_type
        self.scenario = scenario

    # -- generic helpers ---------------------------------------------------------------
    def _search_all(self, entity_type: str, conditions: list[dict[str, Any]]) -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        page = 1
        while True:
            body: dict[str, Any] = {"page_number": page, "page_size": PAGE_SIZE}
            if conditions:
                body["fields"] = conditions
            try:
                response = self.client.search_entities(entity_type, body)
            except HlError as exc:
                # Before tools/provision_types.py has run, the app's types do not exist: nothing saved yet.
                # Writes still fail loudly, so a missing type cannot hide lost work.
                if exc.status == 404 or (exc.status == 400 and "invalid entity type" in str(exc).lower()):
                    return out
                raise
            hits = list_hits(response)
            out.extend(hit for hit in hits if not hit.get("deleted"))
            if not hits or page >= total_pages(response):
                return out
            page += 1

    def _create(self, entity_type: str, name: str, fields: dict[str, Any]) -> dict[str, Any]:
        response = self.client.create_entity(entity_type, {
            "entity_id": str(uuid.uuid4()),
            "entity_name": name[:240] or entity_type,
            "sections": {SECTION: {key: value for key, value in fields.items() if value is not None}},
        })
        entity_id = entity_id_of(response)
        if not entity_id:
            raise HlError(502, "create_without_id", f"HL API accepted the {entity_type} write but returned no entity_id")
        # A 2xx means accepted, not readable yet: read it back before reporting success.
        return self.client.get_entity(entity_type, entity_id)

    # -- investigations -----------------------------------------------------------------
    def _investigation_instance(self, investigation_key: str) -> dict[str, Any] | None:
        if self.external_investigation_type:
            # External investigations are keyed by their i360 entity_id.
            try:
                return self.client.get_entity(self.external_investigation_type, investigation_key)
            except HlError as exc:
                if exc.status in {400, 404}:
                    return None
                raise
        hits = self._search_all(self.investigation_type, [
            {"field": f"{SECTION}.investigation_key", "values": [investigation_key]},
        ])
        return hits[0] if hits else None

    def _investigation_header(self, instance: dict[str, Any]) -> dict[str, Any]:
        if self.external_investigation_type:
            return external_investigation_header(instance)
        fields = fields_of(instance)
        return {
            "investigation_id": fields.get("investigation_key") or "",
            "name": fields.get("name") or fields.get("investigation_key") or "Investigation",
            "created_at_utc": fields.get("created_at_utc"),
            "updated_at_utc": fields.get("updated_at_utc") or fields.get("created_at_utc"),
            "i360_entity_id": entity_id_of(instance),
        }

    def list_investigations(self) -> list[dict[str, Any]]:
        if self.external_investigation_type:
            instances = self._search_all(self.external_investigation_type, [])
        else:
            instances = self._search_all(self.investigation_type, [
                {"field": f"{SECTION}.scenario", "values": [self.scenario]},
            ])
        items = [self._investigation_header(instance) for instance in instances]
        counts: dict[str, dict[str, int]] = {}
        for item in self._search_all(self.memory_item_type, []):
            fields = fields_of(item)
            per = counts.setdefault(str(fields.get("investigation_key") or ""), {})
            per[str(fields.get("group") or "")] = per.get(str(fields.get("group") or ""), 0) + 1
        for item in items:
            per = counts.get(item["investigation_id"], {})
            item.update({
                "chat_summary_count": per.get("chat_summaries", 0),
                "layer_count": per.get("layers", 0),
                "artifact_count": per.get("artifacts", 0),
                "collection_request_count": per.get("collection_requests", 0),
                "entity_enrichment_count": per.get("entity_enrichments", 0),
            })
        return sorted(items, key=lambda x: str(x.get("updated_at_utc") or ""), reverse=True)

    def register_investigation(self, investigation_key: str, name: str) -> dict[str, Any]:
        if self.external_investigation_type:
            return self._register_external_investigation(investigation_key, name)
        existing = self._investigation_instance(investigation_key)
        now = utc_now_iso()
        if existing:
            self.client.patch_entity(self.investigation_type, entity_id_of(existing), {
                "entity_name": name, "sections": {SECTION: {"name": name, "updated_at_utc": now}},
            })
            return {**self._investigation_header(existing), "name": name, "updated_at_utc": now}
        created = self._create(self.investigation_type, name, {
            "investigation_key": investigation_key, "name": name, "scenario": self.scenario,
            "created_at_utc": now, "updated_at_utc": now,
        })
        return self._investigation_header(created)

    def _register_external_investigation(self, investigation_key: str, name: str) -> dict[str, Any]:
        entity_type = self.external_investigation_type
        existing = self._investigation_instance(investigation_key)
        if existing:
            if external_investigation_header(existing)["name"] != name:
                self.client.patch_entity(entity_type, entity_id_of(existing), {"entity_name": name})
            return {**external_investigation_header(existing), "name": name}
        # HL API wants the caller's entity_id; the browser's own id keeps the investigation's key stable.
        response = self.client.create_entity(entity_type, {"entity_id": investigation_key, "entity_name": name[:240]})
        entity_id = entity_id_of(response) or investigation_key
        if not entity_id:
            raise HlError(502, "create_without_id", f"HL API accepted the {entity_type} write but returned no entity_id")
        return external_investigation_header(self.client.get_entity(entity_type, entity_id))

    def touch_investigation(self, investigation_key: str, name: str | None = None) -> None:
        existing = self._investigation_instance(investigation_key)
        if existing is None:
            self.register_investigation(investigation_key, name or investigation_key)
            return
        if self.external_investigation_type:
            return  # i360 keeps its own modification time; the app does not rewrite those records
        self.client.patch_entity(self.investigation_type, entity_id_of(existing), {
            "sections": {SECTION: {"updated_at_utc": utc_now_iso()}},
        })


    # -- items attached to an external investigation (HL API related objects) ------------
    # With an i360 investigation type, a record saved to memory is attached to the investigation
    # entity itself (POST /api/v1/items/related-objects), so i360 and every other client see it;
    # the memory lists what i360 reports as related (related_to search) and removing detaches it.
    RELATED_PREFIX = "i360:"

    def _attaches_items(self, group: str, item: dict[str, Any]) -> bool:
        return bool(self.external_investigation_type) and group == "artifacts" \
            and item.get("kind") == "object" and item.get("object_kind") == "record"

    def _attach_item(self, investigation_key: str, item: dict[str, Any]) -> dict[str, Any]:
        item_id = str(item.get("i360_item_id") or item.get("object_id") or "")
        if not item_id:
            raise ValueError("Missing record id")
        response = self.client.add_related_objects(self.external_investigation_type, investigation_key, [item_id])
        outcome = next((r.get("outcome") for r in response.get("results") or [] if r.get("item_id") == item_id), None)
        if outcome not in {"linked", "already_linked"}:
            detail = next((r.get("error") for r in response.get("results") or [] if r.get("error")), "") or outcome
            raise HlError(502, "attach_not_applied", f"i360 did not attach the item to the investigation ({detail})")
        return {**item, "id": self.RELATED_PREFIX + item_id, "object_id": item_id, "source": "i360_related_object"}

    def _attached_items(self, investigation_key: str) -> list[dict[str, Any]]:
        response = self.client.search_items({
            "related_to": {"ids": [investigation_key]},
            "time": {"from": "1970-01-01T00:00:00Z", "to": "2100-01-01T00:00:00Z", "field": "event"},
            "page_number": 1, "page_size": 100, "include": ["text"], "sort": "time", "order": "desc",
        })
        out = []
        for hit in list_hits(response):
            item_id = str(hit.get("item_id") or "")
            if not item_id:
                continue
            text = hit.get("text") if isinstance(hit.get("text"), dict) else {}
            summary = next((str(text[k]) for k in ("english", "summary", "synopsis", "original", "transcript") if text.get(k)), "")
            out.append({
                "id": self.RELATED_PREFIX + item_id, "kind": "object", "object_kind": "record", "object_id": item_id,
                "label": str(hit.get("name") or f"{hit.get('item_type') or 'item'} {hit.get('event_time') or item_id}"),
                "source_type": str(hit.get("source_application") or ""), "summary": summary[:1800],
                "saved_at_utc": hit.get("event_time"), "source": "i360_related_object",
            })
        return out

    def attached_items(self, investigation_key: str, include: list[str] | None = None) -> list[dict[str, Any]]:
        """The items attached to an external investigation, in full (items/get), newest first."""
        if not self.external_investigation_type:
            return []
        hits = list_hits(self.client.search_items({
            "related_to": {"ids": [investigation_key]},
            "time": {"from": "1970-01-01T00:00:00Z", "to": "2100-01-01T00:00:00Z", "field": "event"},
            "page_number": 1, "page_size": 100, "include": ["text"], "sort": "time", "order": "desc",
        }))
        ids = [str(hit["item_id"]) for hit in hits if hit.get("item_id")]
        if not ids:
            return []
        full = {str(item.get("item_id")): item for item in self.client.get_items(ids, include or []).get("items") or []}
        out = []
        for hit in hits:
            item = full.get(str(hit.get("item_id")))
            out.append({**hit, **item} if item and item.get("found") is not False else hit)
        return out

    def _detach_item(self, investigation_key: str, item_key: str) -> bool:
        item_id = item_key[len(self.RELATED_PREFIX):]
        response = self.client.remove_related_objects(self.external_investigation_type, investigation_key, [item_id])
        outcome = next((r.get("outcome") for r in response.get("results") or [] if r.get("item_id") == item_id), None)
        return outcome in {"unlinked", "not_linked"}

    def load_memory(self, investigation_key: str) -> dict[str, Any]:
        header_instance = self._investigation_instance(investigation_key)
        header = self._investigation_header(header_instance) if header_instance else {
            "investigation_id": investigation_key, "name": investigation_key,
            "created_at_utc": None, "updated_at_utc": None,
        }
        memory: dict[str, list[dict[str, Any]]] = {group: [] for group in MEMORY_GROUPS}
        items = self._search_all(self.memory_item_type, [
            {"field": f"{SECTION}.investigation_key", "values": [investigation_key]},
        ])
        for instance in items:
            fields = fields_of(instance)
            group = str(fields.get("group") or "")
            if group in memory:
                payload = _payload(instance)
                payload.setdefault("id", fields.get("item_key"))
                memory[group].append(payload)
        if self.external_investigation_type:
            memory["artifacts"].extend(self._attached_items(investigation_key))
        for group in memory:
            memory[group].sort(key=lambda item: str(item.get("saved_at_utc") or ""))
        return {
            "schema_version": 1,
            "investigation_id": investigation_key,
            "name": header.get("name") or investigation_key,
            "created_at_utc": header.get("created_at_utc"),
            "updated_at_utc": header.get("updated_at_utc"),
            "memory": memory,
        }

    def add_memory_item(self, investigation_key: str, group: str, item: dict[str, Any], name: str | None = None) -> dict[str, Any]:
        if group not in MEMORY_GROUPS:
            raise ValueError("Invalid memory group")
        if self._attaches_items(group, item):
            if self._investigation_instance(investigation_key) is None:
                raise ValueError("Investigation not found in i360")
            return self._attach_item(investigation_key, item)
        if self._investigation_instance(investigation_key) is None:
            self.register_investigation(investigation_key, name or investigation_key)
        self._create(self.memory_item_type, str(item.get("label") or item.get("kind") or group), {
            "investigation_key": investigation_key,
            "item_key": str(item.get("id") or ""),
            "group": group,
            "kind": str(item.get("kind") or ""),
            "label": str(item.get("label") or "")[:240],
            "comment": str(item.get("analyst_comment") or ""),
            "saved_at_utc": str(item.get("saved_at_utc") or utc_now_iso()),
            "payload": json.dumps(item, ensure_ascii=False),
        })
        self.touch_investigation(investigation_key)
        return item

    def delete_memory_item(self, investigation_key: str, group: str, item_key: str) -> bool:
        if self.external_investigation_type and group == "artifacts" and item_key.startswith(self.RELATED_PREFIX):
            return self._detach_item(investigation_key, item_key)
        hits = self._search_all(self.memory_item_type, [
            {"field": f"{SECTION}.investigation_key", "values": [investigation_key]},
            {"field": f"{SECTION}.item_key", "values": [item_key]},
        ])
        hits = [hit for hit in hits if fields_of(hit).get("group") == group]
        for hit in hits:
            self.client.delete_entity(self.memory_item_type, entity_id_of(hit))
        if hits:
            self.touch_investigation(investigation_key)
        return bool(hits)

    # -- telecom identity reviews --------------------------------------------------------
    def load_reviews(self) -> dict[str, dict[str, Any]]:
        reviews: dict[str, dict[str, Any]] = {}
        instances = self._search_all(self.approval_type, [
            {"field": f"{SECTION}.scenario", "values": [self.scenario]},
        ])
        instances.sort(key=lambda inst: str(fields_of(inst).get("reviewed_at_utc") or ""))
        for instance in instances:
            fields = fields_of(instance)
            derivation_id = str(fields.get("derivation_id") or "")
            if derivation_id:
                reviews[derivation_id] = {**_payload(instance), "_entity_id": entity_id_of(instance)}
        return reviews

    def save_review(self, review: dict[str, Any], reviewer: str) -> dict[str, Any]:
        derivation_id = str(review.get("derivation_id") or "")
        entity_ref = str((review.get("subject") or {}).get("object_id") or review.get("entity_id") or "")
        value = (review.get("claim") or {}).get("value") or {}
        fields = {
            "derivation_id": derivation_id,
            "entity_ref": entity_ref,
            "scenario": self.scenario,
            "review_state": review.get("review_state"),
            "msisdn": value.get("msisdn"),
            "imsi": value.get("imsi"),
            "reviewed_at_utc": review.get("reviewed_at_utc") or utc_now_iso(),
            "reviewed_by": reviewer,
            "payload": json.dumps(review, ensure_ascii=False),
        }
        existing = self._search_all(self.approval_type, [
            {"field": f"{SECTION}.derivation_id", "values": [derivation_id]},
        ])
        if existing:
            self.client.patch_entity(self.approval_type, entity_id_of(existing[0]), {"sections": {SECTION: fields}})
        else:
            self._create(self.approval_type, f"{entity_ref} {review.get('review_state')}", fields)
        return review

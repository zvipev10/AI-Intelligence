"""/i (/internal): an assistant over the records the app has already loaded for its layers.

The i360 chat is not asked. One message is one turn:

1. The model behind HL API gets the layers, each layer's fields (our names, a type, the values when few) and the link
   kinds, and turns the question into ONE structured query (tool ``run_query``). It never sees the rows.
2. Our code checks the query against that catalogue (an unknown layer, field or value is said back, never guessed)
   and runs it over the loaded rows: field conditions, i360's own links (``i360_links``: records and entities),
   counts by a field.
   When a layer, field, value or entity named in the question does not exist, the analyst is asked which one is
   meant (the model writes the question, with the closest names), and the reply completes the question.
3. The model writes the answer from the query's result (the count, the counts by field, a sample of the records).
4. The records are shown with the chat's presentation tools (the same ``show_items`` action as i360's answers).

Only the loaded layers are searched (each layer's newest records, as the app shows them), and only i360's own links
are followed.
"""
from __future__ import annotations

import difflib
import json
import re
import time
from dataclasses import dataclass, field
from typing import Any, Callable

from hl.client import AuthExpired, HlError, NotOnThisEstate, Unreachable

MAX_VALUES = 30      # a field with at most this many distinct values lists them for the model
SAMPLE_ROWS = 20     # records of the result the model reads to write its answer
MAX_SHOWN = 200      # records put on screen

# Errors that name something the question asked for and the data does not have: the analyst is asked which is meant.
_UNCLEAR = re.compile(r"^(no layer named|no field named|.* has no field|no record has|no linked entity named)")

# Row keys that are the app's bookkeeping, not record fields.
_SKIP = {"i360_links", "i360_identifiers", "record_id", "i360_item_id", "event_id", "source_type", "event",
         "duplication_counter", "flag", "has_secrecy_holder_processed", "event_summary", "call_transcript",
         "side_a_imei", "side_a_number", "side_b_imei", "side_b_number", "latitude", "longitude", "timestamp_utc"}
_TIME = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}")


def _garbled(query: dict[str, Any]) -> bool:
    """The model's arguments came out broken: the rest of the query spilled into the layer names."""
    return any(re.search(r"[{}\[\]<>|]|\w+:", str(layer)) for layer in query.get("layers") or [])


def _number(value: str) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@dataclass
class Record:
    layer: str
    id: str
    fields: dict[str, str]                      # our field name -> value (text, as the table shows it)
    links: list[dict[str, Any]]                 # i360's links: {id, type, relation, source, values}
    row: dict[str, Any]


@dataclass
class Field:
    name: str
    kind: str = "text"                          # text | number | time
    values: dict[str, int] = field(default_factory=dict)
    layers: set[str] = field(default_factory=set)


class Catalogue:
    """The loaded records with our field names, and what the model is told about them."""

    def __init__(self, layers: dict[str, list[dict[str, Any]]], labels: dict[str, dict[str, str]],
                 entities: dict[str, str] | None = None):
        self.records: list[Record] = []
        self.fields: dict[str, Field] = {}
        self.layers: dict[str, int] = {}
        self.entity_names = dict(entities or {})
        for layer, rows in layers.items():
            names = labels.get(layer) or {}
            self.layers[layer] = len(rows)
            for row in rows:
                values: dict[str, str] = {}
                for key, value in row.items():
                    if key in _SKIP or value in (None, "", "—"):
                        continue
                    name = names.get(key) or (key[len("i360."):] if key.startswith("i360.") else key)
                    values[name] = str(value)
                values.setdefault("time", str(row.get("timestamp_utc") or row.get("i360.event_time") or ""))
                if row.get("latitude") and row.get("longitude"):
                    values["latitude"], values["longitude"] = str(row["latitude"]), str(row["longitude"])
                try:
                    links = json.loads(row.get("i360_links") or "[]")
                except (TypeError, ValueError):
                    links = []
                record = Record(layer, str(row.get("record_id") or row.get("i360_item_id") or ""), values,
                                [l for l in links if isinstance(l, dict)], row)
                self.records.append(record)
                for name, value in values.items():
                    entry = self.fields.setdefault(name, Field(name))
                    entry.layers.add(layer)
                    entry.values[value] = entry.values.get(value, 0) + 1
        for entry in self.fields.values():
            sample = [v for v in list(entry.values)[:50] if v]
            if sample and all(_TIME.match(v) for v in sample):
                entry.kind = "time"
            elif sample and all(_number(v) is not None for v in sample):
                entry.kind = "number"
        self.by_id = {r.id: r for r in self.records}

    def describe(self) -> str:
        """The catalogue as the model reads it."""
        lines = ["Layers (records loaded): " + ", ".join(f"{name} ({n})" for name, n in self.layers.items()), "",
                 "Fields (name | type | layers | values):"]
        for entry in sorted(self.fields.values(), key=lambda f: f.name):
            if entry.name in ("latitude", "longitude"):
                continue
            values = list(entry.values)
            shown = (", ".join(values) if len(values) <= MAX_VALUES and entry.kind == "text"
                     else f"{len(values)} distinct, e.g. " + ", ".join(values[:3]))
            lines.append(f"- {entry.name} | {entry.kind} | {', '.join(sorted(entry.layers))} | {shown[:400]}")
        kinds = sorted({l.get("type") for r in self.records for l in r.links if l.get("type")})
        lines += ["", "Link types on records (i360's links): " + ", ".join(kinds) + ". ITEM = another record."]
        if self.entity_names:
            names = list(self.entity_names.items())[:40]
            lines.append("Linked entities (id: name): " + "; ".join(f"{i}: {n}" for i, n in names))
        return "\n".join(lines)

    # -- running a query ------------------------------------------------------------------------
    def run(self, query: dict[str, Any], previous: list[str] | None = None) -> dict[str, Any]:
        """The query's records and counts, or {"error": ...} naming what does not exist."""
        layers = [str(l) for l in query.get("layers") or []]
        unknown = [l for l in layers if l not in self.layers]
        if unknown:
            return {"error": f"no layer named {', '.join(unknown)}; the layers are {', '.join(self.layers)}"}
        records = [r for r in self.records if not layers or r.layer in layers]
        if query.get("within_previous"):
            previous = set(previous or [])
            if not previous:
                return {"error": "there is no previous result to look in; ask the whole question"}
            records = [r for r in records if r.id in previous]
        problem = self._check(query.get("where") or [], layers)
        if problem:
            return {"error": problem}
        mode = "any" if query.get("match") == "any" else "all"
        conditions = query.get("where") or []
        if conditions:
            test = any if mode == "any" else all
            records = [r for r in records if test(self._holds(r, c) for c in conditions)]
        linked = query.get("linked")
        if linked and linked.get("layer") and linked.get("where"):
            # "IPDR records linked to ADINT records that have an IMEI": a condition on a field the linked layer does
            # not have but the asked layers do belongs to the asked records.
            own = [c for c in linked["where"] if not self._has(str(linked["layer"]), str(c.get("field")))
                   and any(self._has(l, str(c.get("field"))) for l in (layers or self.layers))]
            if own:
                linked = {**linked, "where": [c for c in linked["where"] if c not in own]}
                records = [r for r in records if all(self._holds(r, c) for c in own)]
        if linked:
            # linked.previous alone = linked to the previous answer's records; with a layer, record or entity the
            # link target is that, and the previous answer can only narrow the asked records (within_previous).
            by_previous = linked.get("previous") and not any(linked.get(k) for k in (
                "record_id", "layer", "entity_id", "entity_name", "entity_type"))
            targets = set(previous or []) if by_previous else self._link_targets(linked)
            if by_previous and not targets:
                return {"error": "there is no previous result to link to; ask the whole question"}
            if isinstance(targets, str):
                return {"error": targets}
            records = [r for r in records if self._linked(r, targets, linked)]
        result: dict[str, Any] = {"count": len(records), "records": records}
        group = str(query.get("group_by") or "")
        if group:
            if group not in self.fields and group != "layer":
                return {"error": f"no field named {group}"}
            counts: dict[str, int] = {}
            for r in records:
                key = r.layer if group == "layer" else r.fields.get(group, "(empty)")
                counts[key] = counts.get(key, 0) + 1
            result["groups"] = dict(sorted(counts.items(), key=lambda kv: -kv[1])[:50])
        order = query.get("sort") or {}
        if order.get("field"):
            name, reverse = str(order["field"]), order.get("order") == "desc"
            key = (lambda r: _number(r.fields.get(name, "")) or 0) if self.fields.get(name, Field(name)).kind == "number" \
                else (lambda r: r.fields.get(name, ""))
            result["records"] = sorted(records, key=key, reverse=reverse)
        if query.get("limit"):
            result["records"] = result["records"][:max(1, int(query["limit"]))]
        return result

    def _has(self, layer: str, name: str) -> bool:
        entry = self.fields.get(name)
        return bool(entry and layer in entry.layers)

    def _check(self, conditions: list[dict[str, Any]], layers: list[str]) -> str:
        for c in conditions:
            name = str(c.get("field") or "")
            entry = self.fields.get(name)
            if not entry:
                close = [f for f in self.fields if name.lower().replace(" ", "_") in f.lower()]
                close += [f for f in difflib.get_close_matches(name.lower().replace(" ", "_"), list(self.fields), 3, 0.6)
                          if f not in close]
                if close:
                    return f"no field named '{name}'; did you mean {', '.join(close[:5])}?"
                fields = sorted(f.name for f in self.fields.values() if not layers or f.layers & set(layers))
                return f"no field named '{name}'; the fields are {', '.join(fields[:40])}"
            if layers and not entry.layers & set(layers):
                return f"{', '.join(layers)} has no field '{name}' (it is in {', '.join(sorted(entry.layers))})"
            op = c.get("op")
            if op in ("is", "in") and entry.kind == "text" and len(entry.values) <= MAX_VALUES:
                wanted = c.get("value") if isinstance(c.get("value"), list) else [c.get("value")]
                known = {v.lower() for v in entry.values}
                missing = [str(w) for w in wanted if str(w).lower() not in known]
                if missing and len(missing) == len(wanted):
                    return f"no record has {name} {', '.join(missing)}; its values are {', '.join(entry.values)}"
        return ""

    def _holds(self, record: Record, c: dict[str, Any]) -> bool:
        name, op, value = str(c.get("field")), c.get("op") or "is", c.get("value")
        have = record.fields.get(name)
        if op == "exists":
            return bool(have)
        if op == "missing":
            return not have
        if have is None:
            return False  # "not X" means a value other than X: a record without one is not counted
        text = have.lower()
        if op in ("is", "is_not"):
            hit = text == str(value).lower()
            return hit if op == "is" else not hit
        if op in ("in", "not_in"):
            hit = text in {str(v).lower() for v in (value if isinstance(value, list) else [value])}
            return hit if op == "in" else not hit
        if op == "contains":
            return str(value).lower() in text
        if op in ("gt", "lt", "between"):
            low, high = (value if isinstance(value, list) else [value, value])[:2] if op == "between" else (value, value)
            number = _number(have)
            if number is not None and _number(low) is not None:
                if op == "gt":
                    return number > _number(low)
                if op == "lt":
                    return number < _number(high)
                return _number(low) <= number <= _number(high)
            if op == "gt":
                return have > str(low)
            if op == "lt":
                return have < str(high)
            return str(low) <= have <= str(high)
        return False

    def _link_targets(self, linked: dict[str, Any]) -> set[str] | str:
        """The ids a record must link to: a record, the records of a layer (optionally with conditions), or an
        entity (by id or by name)."""
        if linked.get("record_id"):
            return {str(linked["record_id"])}
        if linked.get("layer"):
            sub = self.run({"layers": [linked["layer"]], "where": linked.get("where") or []})
            if sub.get("error"):
                return sub["error"]
            return {r.id for r in sub["records"]}
        if linked.get("entity_id"):
            return {str(linked["entity_id"])}
        if linked.get("entity_name"):
            wanted = str(linked["entity_name"]).lower()
            ids = {i for i, n in self.entity_names.items() if wanted in str(n).lower()}
            return ids or f"no linked entity named '{linked['entity_name']}'"
        if linked.get("entity_type"):
            return {"*" + str(linked["entity_type"])}
        return "a link needs a record, a layer or an entity"

    def _linked(self, record: Record, targets: set[str], linked: dict[str, Any]) -> bool:
        """i360's links count in both directions: this record names the target, or the target names it."""
        for l in record.links:
            if str(l.get("id")) in targets or ("*" + str(l.get("type"))) in targets:
                return True
        for target in targets:
            other = self.by_id.get(target)
            if other and any(str(l.get("id")) == record.id for l in other.links):
                return True
        return False


# --------------------------------------------------------------------------------------------
# The turn
# --------------------------------------------------------------------------------------------
CONDITION = {"type": "object", "additionalProperties": False, "required": ["field", "op"], "properties": {
    "field": {"type": "string", "description": "A field name from the list, exactly as written"},
    "op": {"type": "string", "enum": ["is", "is_not", "in", "not_in", "contains", "exists", "missing", "gt", "lt",
                                      "between"]},
    "value": {"description": "A value as the list writes it; a list for in / not_in / between"}}}

QUERY_TOOL = {"type": "function", "function": {
    "name": "run_query", "description": "Run one query over the app's loaded records.",
    "parameters": {"type": "object", "additionalProperties": False, "properties": {
        "layers": {"type": "array", "items": {"type": "string"},
                   "description": "Layers to search, by name; empty for all"},
        "where": {"type": "array", "items": CONDITION, "description": "Conditions on fields"},
        "match": {"type": "string", "enum": ["all", "any"], "description": "all (AND, default) or any (OR)"},
        "linked": {"type": "object", "additionalProperties": False, "description":
                   "Keep only records i360 links to: one record, the records of a layer (with conditions), or an "
                   "entity", "properties": {
                       "previous": {"type": "boolean", "description": "Linked to the previous answer's records"},
                       "record_id": {"type": "string"}, "layer": {"type": "string"},
                       "where": {"type": "array", "items": CONDITION},
                       "entity_id": {"type": "string"}, "entity_name": {"type": "string"},
                       "entity_type": {"type": "string"}}},
        "within_previous": {"type": "boolean", "description": "Search only the records of the previous answer "
                                                              "(the question says them / these / of them / which of them)"},
        "group_by": {"type": "string", "description": "A field name, or 'layer', to count the records by"},
        "sort": {"type": "object", "properties": {"field": {"type": "string"},
                                                  "order": {"type": "string", "enum": ["asc", "desc"]}}},
        "limit": {"type": "integer"},
        "show": {"type": "string", "enum": ["map", "table", "timeline", "open", "none"],
                 "description": "How to show the records: map for places, timeline for calls, table otherwise; "
                                "open to open one record in the record viewer (\"open the record\"); none when the "
                                "question asks only for a number"}}}}}

QUERY_PROMPT = """You turn an analyst's question about the records loaded in an intelligence map application into
ONE query, by calling run_query. You do not see the records and you do not answer.
- layers: exactly the layers the question names, no others; empty when it names none.
- Use the layer and field names exactly as listed. Map the analyst's words to them ("keyboard language" ->
  keyboard_language, "incoming" -> the value the field lists, e.g. in).
- A condition's value must be written as the field's values are written in the list.
- A word naming a kind of record ("calls", "SMS", "sessions", "images") is a condition on the field that holds the
  record kind, with its listed value (e.g. "calls" -> SESSION TYPE is voice_call), not just the layer.
- A condition belongs to the records it describes: in "IPDR records linked to ADINT records that have an IMEI", the
  IMEI is the IPDR records' (IPDR has imei), so it goes in where, not in linked.where.
- "linked to record X" -> linked.record_id; "linked to ADINT records (where ...)" -> linked.layer (+ linked.where);
  "linked to <person>" -> linked.entity_name; "has a <field>" -> op exists.
- "how many ... by <field>" -> group_by. A question that asks only for a number -> show none.
- "them", "these", "of them", "which of them", "among these" refer to the previous answer's records:
  set within_previous (keep the layers of those records).
- "the related / linked / connected <layer> record(s)" after an answer are OTHER records, linked to the previous
  answer's records: layers [<layer>], linked.previous = true (not within_previous).
- "open ..." -> show open.
- The Persons layer holds the people (persons of interest). "Recommended knowledge" / "new knowledge to approve"
  is i360's telecom identity (MSISDN / IMSI) waiting for approval: Persons where knowledge_status is recommended.
- Map a word to a listed layer or field only when it clearly means it. A layer, field or value the question names
  that is not in the list (and is not clearly one of them) is written as the analyst wrote it: never dropped and never
  swapped for a different one. The analyst is then asked which one is meant.
- Nothing invented."""

CLARIFY_PROMPT = """An analyst asked a question about the records loaded in an intelligence map application, and a
name in it does not match the loaded data (the problem below says which, with the names that do exist). Ask the
analyst ONE short question, in English, that first says which word was not found and then offers the closest names
(at most five) as options to choose from, e.g. "There is no layer called RADAR. Did you mean Satellite or Cellular
Locations?". Do not answer the question and do not mention queries, JSON or tools."""

ANSWER_PROMPT = """You answer an analyst's question from the result of a query over the records loaded in the
application's layers. Answer in one to three short sentences, in English. Use only the result below: the count, the
counts by field, and the sample records. Say the number of records found. Do not describe records you were not
given, do not guess, and do not mention queries, JSON or tools. Records are shown to the analyst next to your
answer."""


class InternalTurn:
    """One /i message: question -> query (model) -> result (our code) -> answer (model) -> shown."""

    def __init__(self, llm: Any, catalogue: Catalogue, emit: Callable[[str, Any], None],
                 show: Callable[[list[str], str, str], int], previous: list[str] | None = None,
                 pending: str = ""):
        self.llm, self.catalogue, self.emit, self.show = llm, catalogue, emit, show
        self.pending = pending  # the question a clarification was asked about, which this message answers
        self.previous = [str(i) for i in previous or [] if str(i) in catalogue.by_id]
        self.started = time.monotonic()

    def run(self, question: str) -> dict[str, Any]:
        if self.llm is None:
            self.emit("note", {"text": "/i needs the assistant model, which is not configured here."})
            return {}
        self.emit("step", {"text": "Reading the question against the loaded layers", "live": True})
        if self.pending:
            question = f"{self.pending}\n(Asked which name was meant, the analyst answered: {question})"
        query = self.ask_query(question)
        if query is None:
            return {}
        result = self.catalogue.run(query, self.previous)
        if result.get("error") and _UNCLEAR.match(result["error"]):
            # A name the data does not have: ask which is meant instead of answering. The reply completes the question
            # (the analyst's own question, again when the reply named something that does not exist either).
            self.emit("step", {"text": "Asked which name is meant", "detail": result["error"]})
            self.emit("note", {"text": self.ask_clarification(question, result["error"])})
            return {"query": query, "error": result["error"], "clarify": self.pending or question}
        if result.get("error"):
            self.emit("step", {"text": "The question does not fit the loaded data", "detail": result["error"]})
            self.emit("note", {"text": result["error"][0].upper() + result["error"][1:] + "."})
            return {"query": query, "error": result["error"]}
        ids = [r.id for r in result["records"]]
        self.emit("step", {"text": f"Searched the loaded layers · {result['count']} record"
                                   f"{'' if result['count'] == 1 else 's'}",
                           "detail": json.dumps(query, ensure_ascii=False), "tool": "internal_query"})
        self.emit("note", {"text": self.ask_answer(question, query, result)})
        view = query.get("show") if query.get("show") in ("map", "table", "timeline", "open", "none") else "table"
        if re.match(r"\s*(open|show me the record)\b", question, re.I) and len(ids) == 1:
            view = "open"  # "open the related IPDR record": the record viewer
        if view == "none" and not query.get("group_by"):
            view = "table"  # records found are shown, so a follow-up's "them" is on screen
        if ids and view != "none":
            shown = self.show(ids[:MAX_SHOWN], view, question[:60])
            if shown:
                self.emit("step", {"text": "Opened the record viewer" if view == "open" and shown == 1 else
                                   f"Showed {shown} record{'' if shown == 1 else 's'} on the "
                                   f"{'table' if view == 'open' else view}"})
        return {"query": query, "count": result["count"], "ids": ids}

    def ask_query(self, question: str) -> dict[str, Any] | None:
        previous = ""
        if self.previous:
            layers = sorted({self.catalogue.by_id[i].layer for i in self.previous})
            previous = f"\n\nPrevious answer: {len(self.previous)} records ({', '.join(layers)})."
        messages = [{"role": "system", "content": QUERY_PROMPT + "\n\n" + self.catalogue.describe() + previous},
                    {"role": "user", "content": question}]
        for attempt in range(2):
            try:
                reply = self.llm.complete(messages, [QUERY_TOOL])
            except AuthExpired:
                raise
            except (NotOnThisEstate, Unreachable, HlError) as exc:
                self.emit("note", {"text": f"The assistant model did not answer ({exc})."})
                return None
            call = next((c for c in reply.get("tool_calls") or [] if c.get("name") == "run_query"), None)
            arguments = (call or {}).get("arguments") or {}
            if call and not _garbled(arguments):
                return arguments
            messages.append({"role": "assistant", "content": reply.get("content") or ""})
            messages.append({"role": "user", "content": "Call run_query with the query." if not call else
                             "The run_query arguments were not valid JSON (a layer name held the rest of the query). "
                             "Call run_query again, each part in its own property."})
        self.emit("note", {"text": "The assistant model gave no query for this question."})
        return None

    def ask_clarification(self, question: str, problem: str) -> str:
        messages = [{"role": "system", "content": CLARIFY_PROMPT},
                    {"role": "user", "content": f"Question: {question}\n\nProblem: {problem}"}]
        try:
            reply = self.llm.complete(messages, [])
        except AuthExpired:
            raise
        except (NotOnThisEstate, Unreachable, HlError):
            reply = {}
        text = str((reply or {}).get("content") or "").strip()
        return text or problem[0].upper() + problem[1:] + ". Which did you mean?"

    def ask_answer(self, question: str, query: dict[str, Any], result: dict[str, Any]) -> str:
        sample = [{"layer": r.layer, "id": r.id, **{k: v for k, v in list(r.fields.items())[:14]}}
                  for r in result["records"][:SAMPLE_ROWS]]
        facts = {"count": result["count"], "groups": result.get("groups"), "sample_records": sample}
        messages = [{"role": "system", "content": ANSWER_PROMPT},
                    {"role": "user", "content": f"Question: {question}\n\nResult:\n"
                                                + json.dumps(facts, ensure_ascii=False)[:12000]}]
        try:
            reply = self.llm.complete(messages, [])
        except AuthExpired:
            raise
        except (NotOnThisEstate, Unreachable, HlError):
            reply = {}
        text = str((reply or {}).get("content") or "").strip()
        if not text:  # the model wrote nothing: the count is still the answer
            text = f"{result['count']} record{'' if result['count'] == 1 else 's'} found in the loaded layers."
        return text

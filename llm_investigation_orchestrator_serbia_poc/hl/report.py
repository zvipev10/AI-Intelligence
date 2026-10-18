"""Investigation report from memory (docs/report-plan.md, layout A "Document").

Facts come straight from the records and people saved to the investigation and their i360 links; no model
touches a fact. Analysis blocks (interpretation only) are written by HL API's language model
(POST /api/v1/llm/chat), one call per block, answering JSON with the short refs (R1, R2, ...) of the records
it rests on after each sentence. The server maps refs back to record ids, drops refs it did not give, and
marks sentences left without support.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from typing import Any, Callable

MAX_CARDS = 150          # records given to the model per block; the newest are kept
CARD_TEXT = 400          # characters of transcript / note per card
CARD_FIELDS = 12         # named fields per card

# The correlation chain: each layer's role, in the order the sample report tells the story.
CHAIN = [("Satellite", "Detection"), ("ADINT", "Device set"), ("IPDR", "Attribution"), ("person", "Identification"),
         ("Cellular Calls", "Intercept"), ("CCTV", "Confirmation")]
LAYER_ORDER = ["Satellite", "ADINT", "IPDR", "Cellular Calls", "Cellular Locations", "CCTV"]

RULES = ("You are an intelligence analyst writing one block of a multi-source fusion report on one subject. Use ONLY "
         "the records given; never invent people, places, times or facts. After each sentence give the refs of the "
         "records it rests on (R1, R2, ... as given after 'ref='); refs go in the 'refs' list, never in the text. "
         "If the records do not cover something, say so instead of guessing. English, plain and concise.")

SENTENCES = {"type": "object", "properties": {"sentences": {"type": "array", "items": {
    "type": "object", "properties": {"text": {"type": "string"}, "refs": {"type": "array", "items": {"type": "string"}}},
    "required": ["text", "refs"]}}}, "required": ["sentences"]}

ASSESSMENT = {"type": "object", "properties": {
    "claims": {"type": "array", "items": {"type": "object", "properties": {
        "claim": {"type": "string"}, "level": {"type": "string", "enum": ["HIGH", "MODERATE", "LOW"]},
        "refs": {"type": "array", "items": {"type": "string"}}}, "required": ["claim", "level", "refs"]}},
    "open_questions": {"type": "array", "items": {"type": "string"}}}, "required": ["claims", "open_questions"]}

LAYER_TASK = {
    "Satellite": "what the imagery shows (objects, places, times) and what it means for the subject",
    "ADINT": "which devices, keyboards and IPs were observed and how they tie to the subject",
    "IPDR": "what the network sessions show: private and public IPs, carrier, IMEI, and the link to the device set",
    "Cellular Calls": "what the calls show: who, when, from where, and what was said",
    "Cellular Locations": "the subject's movement: route, times and places",
    "CCTV": "what the camera footage confirms, where and when",
}


def _short(value: Any, limit: int) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def record_id_of(row: dict[str, Any]) -> str:
    return str(row.get("i360_item_id") or row.get("record_id") or row.get("event_id") or "")


def _point(row: dict[str, Any]) -> tuple[float, float] | None:
    try:
        lat, lon = float(row.get("latitude")), float(row.get("longitude"))
    except (TypeError, ValueError):
        return None
    return (lat, lon) if str(row.get("latitude") or "").strip() and abs(lat) <= 90 and abs(lon) <= 180 else None


def _km(a: tuple[float, float], b: tuple[float, float]) -> float:
    lat1, lon1, lat2, lon2 = map(math.radians, (*a, *b))
    h = math.sin((lat2 - lat1) / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin((lon2 - lon1) / 2) ** 2
    return 6371 * 2 * math.asin(math.sqrt(h))


def record_card(row: dict[str, Any], labels: dict[str, str], entity_names: dict[str, str], ref: str = "") -> str:
    """One record as a few lines the model can cite by its short ref: layer, time, place, named fields, text, links."""
    head = ([f"ref={ref}"] if ref else [f"id={record_id_of(row)}"]) + [f"layer={row.get('source_type') or '-'}", f"time={row.get('timestamp_utc') or '-'}"]
    point = _point(row)
    if point:
        head.append(f"place={point[0]:.5f},{point[1]:.5f}")
    lines = [" | ".join(head)]
    named = [(labels[key], row.get(key)) for key in labels if row.get(key) not in (None, "")]
    if named:
        lines.append("fields: " + "; ".join(f"{name}={_short(value, 80)}" for name, value in named[:CARD_FIELDS]))
    text = row.get("call_transcript_en") or row.get("i360.text.english") or row.get("i360.insights.post_comment") \
        or row.get("event_summary") or row.get("i360.text.transcript") or ""
    if text:
        lines.append("text: " + _short(text, CARD_TEXT))
    links = []
    for link in row.get("observed_entity_links") or []:
        name = entity_names.get(str(link.get("entity_id")), link.get("entity_name") or link.get("entity_id"))
        links.append(f"person {name}" + (f" (shared {link.get('matched_value')})" if link.get("matched_value") else ""))
    for link in row.get("observed_record_links") or []:
        links.append(f"another record ({link.get('record_id')})" + (f", matched value {link.get('matched_value')}" if link.get("matched_value") else ""))
    if links:
        lines.append("links: " + "; ".join(links))
    return "\n".join(lines)


def person_card(entity: dict[str, Any], linked: dict[str, int]) -> str:
    identity = identifiers_of(entity)
    parts = [f"person (the subject) | name={entity.get('canonical_name') or entity.get('entity_id')}"]
    ids = [f"{key.upper()} {value}" + (f" ({status})" if status else "") for key, (value, status) in identity.items() if value]
    if ids:
        parts.append("identifiers: " + "; ".join(ids))
    if linked:
        parts.append("linked records: " + "; ".join(f"{layer} {count}" for layer, count in sorted(linked.items())))
    return "\n".join(parts)


def identifiers_of(entity: dict[str, Any]) -> dict[str, tuple[str, str]]:
    """IMEI, MSISDN, IMSI of a person with their status: approved / recommended, not yet approved / ''."""
    telecom = entity.get("telecom") if isinstance(entity.get("telecom"), dict) else {}
    approved = telecom.get("approved_subscriber_identity") or {}
    review = ((telecom.get("subscriber_identity_derivation") or {}).get("claim") or {}).get("value") or {}
    out = {"imei": (str(telecom.get("imei") or ""), "")}
    for key in ("msisdn", "imsi"):
        if approved.get(key):
            out[key] = (str(approved[key]), "approved")
        elif review.get(key):
            out[key] = (str(review[key]), "recommended, not yet approved")
        else:
            out[key] = (str(telecom.get(key) or ""), "")
    return out


def _linked_counts(rows: list[dict[str, Any]]) -> dict[str, dict[str, int]]:
    counts: dict[str, dict[str, int]] = {}
    for row in rows:
        for link in row.get("observed_entity_links") or []:
            per = counts.setdefault(str(link.get("entity_id")), {})
            layer = str(row.get("source_type") or "-")
            per[layer] = per.get(layer, 0) + 1
    return counts


def default_subject(persons: list[dict[str, Any]], rows: list[dict[str, Any]]) -> str:
    """The person with the most linked memory records."""
    counts = _linked_counts(rows)
    ranked = sorted(persons, key=lambda p: -sum(counts.get(str(p.get("entity_id")), {}).values()))
    return str(ranked[0].get("entity_id")) if ranked else ""


def _top(rows: list[dict[str, Any]], key: str, n: int = 3) -> list[str]:
    values = Counter(v.strip() for r in rows for v in str(r.get(key) or "").split(";") if v.strip())
    return [v for v, _ in values.most_common(n)]


def compute_facts(name: str, rows: list[dict[str, Any]], persons: list[dict[str, Any]], subject_id: str,
                  labels_of: Callable[[dict[str, Any]], dict[str, str]]) -> dict[str, Any]:
    """Everything the report states as fact, from the memory records, persons and i360 links.
    labels_of(row) gives a row's field display names (they depend on how the row was read)."""
    ordered = sorted(rows, key=lambda r: str(r.get("timestamp_utc") or ""))
    times = [str(r.get("timestamp_utc")) for r in ordered if r.get("timestamp_utc")]
    points = [p for p in (_point(r) for r in ordered) if p]
    by_layer: dict[str, list[dict[str, Any]]] = {}
    for row in ordered:
        by_layer.setdefault(str(row.get("source_type") or "Other"), []).append(row)
    layers = sorted(by_layer, key=lambda l: LAYER_ORDER.index(l) if l in LAYER_ORDER else len(LAYER_ORDER))
    subject = next((p for p in persons if str(p.get("entity_id")) == subject_id), None)
    identity = identifiers_of(subject) if subject else {}
    linked = _linked_counts(ordered)

    def layer_facts(layer: str) -> dict[str, Any]:
        lrows = by_layer[layer]
        counts: dict[str, Counter] = {}
        for row in lrows:
            for key, label in labels_of(row).items():
                counts.setdefault(label, Counter()).update(
                    v.strip() for v in str(row.get(key) or "").split(";") if v.strip())
        fields = [{"label": label, "values": [v for v, _ in c.most_common(3)]} for label, c in counts.items() if c]
        lt = [str(r.get("timestamp_utc")) for r in lrows if r.get("timestamp_utc")]
        out = {"layer": layer, "count": len(lrows), "first": lt[0] if lt else "", "last": lt[-1] if lt else "",
               "fields": fields[:8], "records": [{"id": record_id_of(r), "time": r.get("timestamp_utc") or "",
                                                   "label": _short(r.get("i360.insights.post_comment") or r.get("call_transcript_en")
                                                                   or r.get("i360.item_type") or layer, 80)} for r in lrows]}
        pts = [p for p in (_point(r) for r in lrows) if p]
        if layer == "Cellular Locations" and len(pts) > 1:
            out["route_km"] = round(sum(_km(a, b) for a, b in zip(pts, pts[1:])), 1)
            out["route_points"] = len(pts)
        if layer == "Cellular Calls":
            out["quotes"] = call_lines(lrows)
        links = [(record_id_of(r), l) for r in lrows for l in r.get("observed_record_links") or []]
        if links:
            out["record_links"] = [{"id": rid, "other": l.get("record_id"), "value": l.get("matched_value"),
                                    "fields": f"{l.get('record_field')} / {l.get('linked_record_field')}"} for rid, l in links]
        return out

    def has_record_link(a: str, b: str) -> bool:
        ids_b = {record_id_of(r) for r in by_layer.get(b, [])}
        return any(l.get("record_id") in ids_b for r in by_layer.get(a, []) for l in r.get("observed_record_links") or [])

    def has_person_link(layer: str) -> bool:
        return bool(subject) and any(str(l.get("entity_id")) == subject_id
                                     for r in by_layer.get(layer, []) for l in r.get("observed_entity_links") or [])

    chain, previous = [], None
    for layer, role in CHAIN:
        present = (layer == "person" and subject is not None) or layer in by_layer
        if not present:
            continue
        if previous is None:
            linked_step = None
        elif layer == "person":
            linked_step = has_person_link(previous)
        elif previous == "person":
            linked_step = has_person_link(layer)
        else:
            linked_step = has_record_link(previous, layer) or has_record_link(layer, previous)
        chain.append({"layer": layer, "role": role, "linked": linked_step})
        previous = layer

    contacts = Counter(str(r.get("side_b_number") or r.get("i360.parties.other.msisdn") or "")
                       for r in by_layer.get("Cellular Calls", []) + by_layer.get("Cellular Locations", []))
    contacts.pop("", None)
    adint, ipdr = by_layer.get("ADINT", []), by_layer.get("IPDR", [])
    table = [{"label": key.upper(), "value": value, "status": status} for key, (value, status) in identity.items() if value]
    table += [{"label": "Device", "value": ", ".join(filter(None, _top(adint, "i360.user_agents_data.device_brand", 2) + _top(adint, "i360.user_agents_data.device_model", 2)))},
              {"label": "Public IP (ADINT)", "value": ", ".join(_top(adint, "i360.ip.ip_sessions.source_ip"))},
              {"label": "Private IP (IPDR)", "value": ", ".join(_top(ipdr, "i360.additional_info.ip_source") or _top(ipdr, "i360.additional_info.ip_private"))},
              {"label": "Carrier (IPDR)", "value": ", ".join(_top(ipdr, "i360.source_application"))},
              {"label": "Top B-party contacts", "value": ", ".join(f"{n} ({c})" for n, c in contacts.most_common(3))}]
    return {
        "title": name,
        "subtitle": f"Fusion of {', '.join(l for l in layers if l != 'Other')} records on one subject." if layers else "",
        "records_total": len(ordered),
        "period": {"first": times[0] if times else "", "last": times[-1] if times else ""},
        "area": ({"south": min(p[0] for p in points), "west": min(p[1] for p in points),
                  "north": max(p[0] for p in points), "east": max(p[1] for p in points)} if points else None),
        "persons": [{"id": str(p.get("entity_id")), "name": p.get("canonical_name") or p.get("entity_id"),
                     "linked": sum(linked.get(str(p.get("entity_id")), {}).values())} for p in persons],
        "subject": ({"id": subject_id, "name": subject.get("canonical_name") or subject_id, "image_url": subject.get("image_url") or "",
                     "identifiers": [{"label": k.upper(), "value": v, "status": s} for k, (v, s) in identity.items() if v],
                     "linked": linked.get(subject_id, {})} if subject else None),
        "chain": chain,
        "layers": [layer_facts(l) for l in layers],
        "identifiers_table": [row for row in table if row["value"]],
    }


def call_lines(rows: list[dict[str, Any]]) -> list[dict[str, str]]:
    """Every translated call line, numbered, with its record, speaker and time: the model picks one to quote,
    the app prints it verbatim."""
    out = []
    for row in rows:
        for paragraph in str(row.get("call_transcript_en") or "").split("\n\n"):
            speaker, _, text = paragraph.partition(": ")
            if text.strip():
                out.append({"n": str(len(out) + 1), "id": record_id_of(row), "speaker": speaker.strip(), "text": text.strip(),
                            "time": row.get("timestamp_utc") or ""})
    return out


def block_task(block: str, facts: dict[str, Any]) -> tuple[str, dict[str, Any], str]:
    """(instruction, schema, layer) for one analysis block: summary, chain, layer:<name>, assessment."""
    if block == "summary":
        return "Write the executive summary: 4-6 sentences on what these records establish about the subject, from detection to identification.", SENTENCES, ""
    if block == "chain":
        steps = " -> ".join(f"{s['role']} ({s['layer']}{'' if s['linked'] in (None, True) else ', no i360 link'})" for s in facts.get("chain") or [])
        return f"In 1-2 sentences, explain how the sources connect along this chain: {steps}.", SENTENCES, ""
    if block.startswith("layer:"):
        layer = block[len("layer:"):]
        task = LAYER_TASK.get(layer, f"what these {layer} records show about the subject")
        schema = SENTENCES
        if layer == "Cellular Calls":
            schema = {**SENTENCES, "properties": {**SENTENCES["properties"], "quote_line": {"type": "string"}}}
            task += ". Also choose the single most telling translated line and give its number in 'quote_line' (from the CALL LINES list)"
        return f"Write 2-3 sentences on {task}. Use and cite only the refs given. Say what is missing.", schema, layer
    if block == "assessment":
        return ("Give the assessment: 3-6 claims about the subject, each with a confidence level HIGH, MODERATE or LOW and the refs it "
                "rests on; then the open questions these records leave."), ASSESSMENT, ""
    raise ValueError("Unknown report block")


def parse_json(content: str) -> dict[str, Any]:
    text = str(content or "").strip()
    fenced = re.search(r"```(?:json)?\s*(\{.*\})\s*```", text, re.S)
    if fenced:
        text = fenced.group(1)
    start, end = text.find("{"), text.rfind("}")
    if start < 0 or end <= start:
        raise ValueError("the model did not answer with JSON")
    try:
        return json.loads(text[start:end + 1])
    except json.JSONDecodeError as exc:
        raise ValueError(f"the model's JSON is incomplete ({exc.msg})") from None


_INLINE_REFS = re.compile(r"\s*[\[(](?:(?:ref|id)=)?(?:R\d+|[0-9a-f-]{8,})(?:\s*,\s*(?:(?:ref|id)=)?(?:R\d+|[0-9a-f-]{8,}))*[\])]")


def _resolve(cited: list[Any], refs: dict[str, str]) -> tuple[list[str], int]:
    ids = set(refs.values())
    keys = [re.sub(r"^(?:ref|id)=", "", str(i).strip().strip("[]()")) for i in cited or []]
    resolved = [refs.get(k.upper(), k if k in ids else "") for k in keys]
    return list(dict.fromkeys(i for i in resolved if i)), sum(1 for i in resolved if not i)


def checked_block(answer: dict[str, Any], refs: dict[str, str]) -> dict[str, Any]:
    """Map refs back to record ids, drop the ones not given, mark text left without support."""
    removed, out = 0, {}
    sentences = []
    for sentence in answer.get("sentences") or []:
        if isinstance(sentence, dict) and str(sentence.get("text") or "").strip():
            ids, lost = _resolve(sentence.get("refs"), refs)
            removed += lost
            sentences.append({"text": _INLINE_REFS.sub("", str(sentence["text"])).strip(), "record_ids": ids, "unsupported": not ids})
    if sentences or "sentences" in answer:
        out["sentences"] = sentences
    claims = []
    for claim in answer.get("claims") or []:
        if isinstance(claim, dict) and str(claim.get("claim") or "").strip():
            ids, lost = _resolve(claim.get("refs"), refs)
            removed += lost
            level = str(claim.get("level") or "").upper()
            claims.append({"claim": _INLINE_REFS.sub("", str(claim["claim"])).strip(), "level": level if level in ("HIGH", "MODERATE", "LOW") else "LOW",
                           "record_ids": ids, "unsupported": not ids})
    if claims or "claims" in answer:
        out["claims"] = claims
        out["open_questions"] = [str(q).strip() for q in answer.get("open_questions") or [] if str(q).strip()]
    if answer.get("quote_line"):
        out["quote_line"] = str(answer["quote_line"]).strip().lstrip("#")
    out["removed_ids"] = removed
    return out


def run_block(complete_json: Callable[[list[dict[str, str]], dict[str, Any]], dict[str, Any]], block: str,
              facts: dict[str, Any], rows: list[dict[str, Any]], labels_of: Callable[[dict[str, Any]], dict[str, str]],
              persons: list[dict[str, Any]], subject_id: str, entity_names: dict[str, str]) -> dict[str, Any]:
    """One analysis block over the memory records (those of one layer for a layer block)."""
    instruction, schema, layer = block_task(block, facts)
    ordered = sorted(rows, key=lambda r: str(r.get("timestamp_utc") or ""))
    if layer:
        ordered = [r for r in ordered if str(r.get("source_type") or "") == layer]
    used = ordered[-MAX_CARDS:]
    refs = {f"R{n}": record_id_of(r) for n, r in enumerate(used, 1)}
    cards = [record_card(r, labels_of(r), entity_names, f"R{n}") for n, r in enumerate(used, 1)]
    subject = next((p for p in persons if str(p.get("entity_id")) == subject_id), None)
    body = [f"BLOCK: {block}", f"TASK: {instruction}"]
    if len(used) < len(ordered):
        body.append(f"NOTE: only the newest {len(used)} of {len(ordered)} records are given.")
    if subject:
        body.append("SUBJECT:\n" + person_card(subject, _linked_counts(rows).get(subject_id, {})))
    if layer == "Cellular Calls":
        ref_of = {v: k for k, v in refs.items()}
        body.append("CALL LINES:\n" + "\n".join(f"{q['n']}. [{ref_of.get(q['id'], '-')}] {q['speaker']} at {q['time']}: {q['text']}"
                                                for q in call_lines(used)))
    body.append(f"RECORDS ({len(cards)}):\n" + "\n\n".join(cards))
    messages = [{"role": "system", "content": RULES}, {"role": "user", "content": "\n\n".join(body)}]
    response = complete_json(messages, schema)
    try:
        answer = parse_json(response.get("content") or "")
    except ValueError:
        # Usually an answer cut off at the token limit: ask once more for a shorter one.
        retry = messages[:-1] + [{"role": "user", "content": messages[-1]["content"] + "\n\nKeep it short."}]
        response = complete_json(retry, schema)
        answer = parse_json(response.get("content") or "")
    result = checked_block(answer, refs)
    result.update({"block": block, "records_used": len(used), "records_total": len(ordered), "model": response.get("model") or ""})
    return result

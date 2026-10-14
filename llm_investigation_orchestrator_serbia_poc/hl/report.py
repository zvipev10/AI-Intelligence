"""Investigation report: the records saved to an investigation, analysed section by section by HL API's
language model (POST /api/v1/llm/chat).

The app reads the memory records itself and gives the model one short "record card" per record; the model
answers each section as JSON (paragraphs with the record ids they rest on, plus gaps). Every cited id is
checked against the cards: an id the model invents is dropped, and a paragraph left without one is marked
unsupported. The result is analysis by the model, not i360 data, and is labelled so.
"""

from __future__ import annotations

import json
import re
from typing import Any, Callable

MAX_CARDS = 150          # records given to the model per section; the newest are kept
CARD_TEXT = 400          # characters of transcript / note per card
CARD_FIELDS = 12         # named fields per card

SECTIONS: list[dict[str, str]] = [
    {"id": "summary", "title": "Summary",
     "instruction": "Write a 4-6 sentence overview of what these records show: what kinds of records, the period, "
                    "the places, the people and devices, and what stands out."},
    {"id": "timeline", "title": "Timeline",
     "instruction": "Describe the sequence of events in time order, one paragraph per phase or day, with dates and times. "
                    "The records are already sorted by time."},
    {"id": "places", "title": "Places",
     "instruction": "Describe where the activity happens: which places or areas recur, what happens at each, and how "
                    "places connect over time."},
    {"id": "people", "title": "People and devices",
     "instruction": "Describe the people and devices: who they are, which identifiers (IMEI, MSISDN, IMSI) belong to whom "
                    "and with which approval status, and which records involve each of them."},
    {"id": "communications", "title": "Communications",
     "instruction": "Describe the calls and messages: who contacted whom, when, from where, and what was said "
                    "(use the transcripts and translations)."},
    {"id": "links", "title": "Links",
     "instruction": "Describe the links between records and between records and people, with the value each link was "
                    "made on, and what the links suggest."},
    {"id": "gaps", "title": "Gaps and open questions",
     "instruction": "List what these records do not answer, what is uncertain or contradictory, and what further "
                    "collection would help."},
]

RULES = ("You are an intelligence analyst writing one section of a report on an investigation. Use ONLY the records "
         "given below; never invent people, places, times or facts. Every paragraph must cite the refs of the records it "
         "rests on (R1, R2, ... as given after 'ref='); put them in record_ids, not in the text. If the records do not cover something, say so in 'gaps' "
         "instead of guessing. Write in English, plainly and concisely.")

SCHEMA = {
    "type": "object",
    "properties": {
        "paragraphs": {"type": "array", "items": {
            "type": "object",
            "properties": {"text": {"type": "string"}, "record_ids": {"type": "array", "items": {"type": "string"}}},
            "required": ["text", "record_ids"]}},
        "gaps": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["paragraphs", "gaps"],
}


def _short(value: Any, limit: int) -> str:
    text = re.sub(r"\s+", " ", str(value or "")).strip()
    return text if len(text) <= limit else text[: limit - 1] + "…"


def record_id_of(row: dict[str, Any]) -> str:
    return str(row.get("i360_item_id") or row.get("record_id") or row.get("event_id") or "")


def record_card(row: dict[str, Any], labels: dict[str, str], entity_names: dict[str, str], ref: str = "") -> str:
    """One record as a few lines the model can cite by its short ref (R1, R2, ...): layer, time, place,
    named fields, text, links. Short refs are copied reliably; long ids are not."""
    head = ([f"ref={ref}"] if ref else [f"id={record_id_of(row)}"]) + [f"layer={row.get('source_type') or '-'}", f"time={row.get('timestamp_utc') or '-'}"]
    if str(row.get("latitude") or "").strip() and str(row.get("longitude") or "").strip():
        head.append(f"place={row.get('latitude')},{row.get('longitude')}")
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
    """A saved person: name, id, telecom identifiers with their status, linked records per layer."""
    telecom = entity.get("telecom") if isinstance(entity.get("telecom"), dict) else {}
    parts = [f"person id={entity.get('entity_id')} | name={entity.get('canonical_name') or entity.get('entity_id')}"]
    ids = [f"IMEI {telecom['imei']}"] if telecom.get("imei") else []
    approved = telecom.get("approved_subscriber_identity") or {}
    review = ((telecom.get("subscriber_identity_derivation") or {}).get("claim") or {}).get("value") or {}
    for key in ("msisdn", "imsi"):
        if approved.get(key):
            ids.append(f"{key.upper()} {approved[key]} (approved)")
        elif review.get(key):
            ids.append(f"{key.upper()} {review[key]} (recommended, not approved)")
        elif telecom.get(key):
            ids.append(f"{key.upper()} {telecom[key]}")
    if ids:
        parts.append("identifiers: " + "; ".join(ids))
    if linked:
        parts.append("linked records: " + "; ".join(f"{layer} {count}" for layer, count in sorted(linked.items())))
    return "\n".join(parts)


def section_messages(section: dict[str, str], record_cards: list[str], person_cards: list[str], note: str) -> list[dict[str, str]]:
    body = [f"SECTION: {section['title']}", f"TASK: {section['instruction']}"]
    if note:
        body.append(f"NOTE: {note}")
    if person_cards:
        body.append("PEOPLE SAVED TO THE INVESTIGATION:\n" + "\n\n".join(person_cards))
    body.append(f"RECORDS ({len(record_cards)}):\n" + "\n\n".join(record_cards))
    body.append('Answer as JSON: {"paragraphs": [{"text": "...", "record_ids": ["R1", "R2"]}], "gaps": ["..."]}')
    return [{"role": "system", "content": RULES}, {"role": "user", "content": "\n\n".join(body)}]


def parse_json(content: str) -> dict[str, Any]:
    """The model's JSON answer; tolerates a fenced block or text around the object."""
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


def checked_section(answer: dict[str, Any], refs: dict[str, str]) -> dict[str, Any]:
    """Map cited refs (R1, ...) back to record ids, dropping any not among the records given; mark paragraphs
    left without support. A full record id the model copied correctly is accepted too."""
    ids = set(refs.values())
    paragraphs, removed = [], 0
    for paragraph in answer.get("paragraphs") or []:
        if not isinstance(paragraph, dict) or not str(paragraph.get("text") or "").strip():
            continue
        cited = [re.sub(r"^(?:ref|id)=", "", str(i).strip().strip("[]()")) for i in paragraph.get("record_ids") or []]
        resolved = [refs.get(i.upper(), i if i in ids else "") for i in cited]
        kept = list(dict.fromkeys(i for i in resolved if i))
        removed += sum(1 for i in resolved if not i)
        text = re.sub(r"\s*[\[(](?:(?:ref|id)=)?(?:R\d+|[0-9a-f-]{8,})(?:\s*,\s*(?:(?:ref|id)=)?(?:R\d+|[0-9a-f-]{8,}))*[\])]", "",
                      str(paragraph["text"])).strip()  # citations are listed apart
        paragraphs.append({"text": text, "record_ids": kept, "unsupported": not kept})
    gaps = [str(g).strip() for g in answer.get("gaps") or [] if str(g).strip()]
    return {"paragraphs": paragraphs, "gaps": gaps, "removed_ids": removed}


def run_section(complete_json: Callable[[list[dict[str, str]], dict[str, Any]], dict[str, Any]],
                section: dict[str, str], rows: list[dict[str, Any]], labels_of: Callable[[str], dict[str, str]],
                persons: list[dict[str, Any]], entity_names: dict[str, str]) -> dict[str, Any]:
    """One report section: cards for the newest MAX_CARDS records (in time order) and the saved persons,
    one model call, then the citation check."""
    ordered = sorted(rows, key=lambda r: str(r.get("timestamp_utc") or ""))
    used = ordered[-MAX_CARDS:]
    note = f"Only the newest {len(used)} of {len(ordered)} saved records are given." if len(used) < len(ordered) else ""
    refs = {f"R{n}": record_id_of(r) for n, r in enumerate(used, 1)}
    record_cards = [record_card(r, labels_of(str(r.get("source_type") or "")), entity_names, f"R{n}") for n, r in enumerate(used, 1)]
    linked: dict[str, dict[str, int]] = {}
    for row in ordered:
        for link in row.get("observed_entity_links") or []:
            per = linked.setdefault(str(link.get("entity_id")), {})
            layer = str(row.get("source_type") or "-")
            per[layer] = per.get(layer, 0) + 1
    person_cards = [person_card(p, linked.get(str(p.get("entity_id")), {})) for p in persons]
    messages = section_messages(section, record_cards, person_cards, note)
    response = complete_json(messages, SCHEMA)
    try:
        answer = parse_json(response.get("content") or "")
    except ValueError:
        # Usually an answer cut off at the token limit: ask once more for a shorter one.
        retry = messages[:-1] + [{"role": "user", "content": messages[-1]["content"]
                                  + "\n\nKeep it short: at most 5 paragraphs of 2-3 sentences."}]
        response = complete_json(retry, SCHEMA)
        answer = parse_json(response.get("content") or "")
    result = checked_section(answer, refs)
    result.update({"id": section["id"], "title": section["title"], "records_used": len(used),
                   "records_total": len(ordered), "model": response.get("model") or ""})
    return result

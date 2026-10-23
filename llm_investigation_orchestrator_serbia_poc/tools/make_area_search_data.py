#!/usr/bin/env python3
"""Writes demo_data/lambda-area-search.json: the app's own records for the polygon area search demo.

These records are not in i360. They copy the exact item shape of the LAMBDA layers (ADINT, Cellular
Locations, Satellite), sit around the satellite convoy track north-west of Hama and are dated March to
May 2026, weeks to months before the earliest i360 record (2026-07-01).

    python tools/make_area_search_data.py <templates.json>

<templates.json> is a dump of current i360 items by layer ({"ADINT": [item, ...], ...}); one item of
each layer is the template whose shape every synthetic record keeps. The output is deterministic.
"""
from __future__ import annotations

import copy
import json
import sys
import uuid
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "demo_data" / "lambda-area-search.json"
NAMESPACE = uuid.UUID("6f1d4c2e-9a37-4b8e-8f51-2a7c0e3d9b64")


def new_id(name: str) -> str:
    return str(uuid.uuid5(NAMESPACE, name))


def dms(lat: float, lon: float) -> str:
    def part(value: float, width: int) -> str:
        degrees = int(abs(value))
        minutes = int((abs(value) - degrees) * 60)
        seconds = (abs(value) - degrees - minutes / 60) * 3600
        return f"{degrees:0{width}d}{minutes:02d}{seconds:05.2f}"
    return f"N{part(lat, 2)} E{part(lon, 3)}"


def geo(lat: float, lon: float, when: str, party_id: str | None, value: str | None, template: dict) -> dict:
    entry = copy.deepcopy(template)
    entry.update({"point": {"lat": lat, "lon": lon}, "geography": f"POINT ({lon} {lat})", "type": "geo",
                  "accuracy": "gps", "from_time": when, "party_id": party_id, "value": value})
    if "to_time" in entry and entry["to_time"] is not None:
        entry["to_time"] = when
    return entry


def base(template: dict, item_id: str, when: str, lat: float, lon: float) -> dict:
    item = copy.deepcopy(template)
    for key in ("highlight", "score", "_layer", "_all_fields", "_call_record", "_i360_links", "found"):
        item.pop(key, None)
    item.update({"item_id": item_id, "event_time": when, "end_time": when, "related_objects": None,
                 "parent_ids": [], "context": []})
    item["location"] = {**(item.get("location") or {}), "point": {"lat": lat, "lon": lon}, "accuracy": "gps"}
    return item


# --- ADINT: 7 location updates from phones that are not in the current data ------------------------------
ADINT = [
    # time, lat, lon, brand, model, os, language, ip, accuracy_m
    ("2026-03-04T06:12:00Z", 35.0690, 36.3000, "Xiaomi", "Redmi Note 12", "Android", "ar", "198.51.100.14", 20),
    ("2026-03-19T17:40:00Z", 35.0830, 36.2910, "Oppo", "A78", "Android", "ar", "198.51.100.37", 35),
    ("2026-04-07T09:05:00Z", 35.0900, 36.2760, "Samsung", "Galaxy A54", "Android", "fa", "198.51.100.52", 15),
    ("2026-04-22T21:18:00Z", 35.1070, 36.2680, "Tecno", "Spark 10", "Android", "ar", "198.51.100.68", 60),
    ("2026-05-03T05:47:00Z", 35.0910, 36.2960, "Apple", "iPhone 13", "iOS", "en", "198.51.100.91", 10),
    ("2026-05-11T13:26:00Z", 35.0720, 36.2810, "Infinix", "Hot 30", "Android", "fa", "198.51.100.103", 45),
    ("2026-05-18T19:02:00Z", 35.0970, 36.2620, "Nokia", "G21", "Android", "ar", "198.51.100.120", 80),
]

# --- Cellular Locations: 9 calls and SMS of a new target, each with a cell and a GPS point -----------------
TARGET = {"msisdn": "963933412870", "imsi": "417012345098761", "imei": "356938104472615"}
OTHER_IMEI = {"963944118203": "352099001761481", "963966540338": "861536030196001"}  # known handsets of two contacts
CELLULAR = [
    # time, lat, lon, type, direction, other msisdn, other imsi, cell, duration s, sms text
    ("2026-03-02T07:31:00Z", 35.0780, 36.3090, "voice_call", "out", "963944118203", "417016620194387", "3104-21877", 94, None),
    ("2026-03-14T22:05:00Z", 35.0940, 36.2880, "sms", "out", "963955207714", "417019031265540", "3102-21290", 0, "وصلنا عند المفرق"),
    ("2026-03-27T11:48:00Z", 35.0840, 36.2720, "voice_call", "in", "963944118203", "417016620194387", "3105-22410", 212, None),
    ("2026-04-09T18:22:00Z", 35.1040, 36.2830, "sms", "in", "963988301457", "417017744329016", "3102-21291", 0, "الطريق فاضي هلق"),
    ("2026-04-19T04:56:00Z", 35.1110, 36.2640, "voice_call", "out", "963955207714", "417019031265540", "3101-20983", 47, None),
    ("2026-04-28T15:10:00Z", 35.0740, 36.2970, "sms", "out", "963944118203", "417016620194387", "3104-21878", 0, "جيب السيارة التانية"),
    ("2026-05-06T20:37:00Z", 35.0910, 36.2580, "voice_call", "in", "963966540338", "417015580931274", "3107-22715", 138, None),
    ("2026-05-14T08:03:00Z", 35.0650, 36.2920, "sms", "in", "963988301457", "417017744329016", "3104-21876", 0, "بكرا الصبح بكير"),
    ("2026-05-20T23:44:00Z", 35.0990, 36.2760, "voice_call", "out", "963966540338", "417015580931274", "3103-21504", 76, None),
]

# --- Satellite: 4 captures with cars detected, images cropped from the current captures -------------------
SATELLITE = [
    # time, lat, lon, image file, classification, detected objects, recognised objects, analyst note, cloud %, sun, off-nadir
    ("2026-03-09T07:12:00Z", 35.0768, 36.3008, "sat-area-a.png", "Vehicles",
     "2x light vehicle, 3x cargo truck (parked)", ["car", "car", "truck", "truck", "truck"],
     "Vehicles parked on the clearing beside the road; no movement observed.", 3, 38.1, 6.4),
    ("2026-04-02T07:09:00Z", 35.0843, 36.2918, "sat-area-b.png", "Vehicles",
     "1x light vehicle leading 2x cargo truck", ["car", "truck", "truck"],
     "A light vehicle leads two trucks north-west along the road.", 8, 47.6, 3.9),
    ("2026-04-25T07:15:00Z", 35.0918, 36.2828, "sat-area-c.png", "Vehicles",
     "1x light vehicle, 1x cargo truck", ["car", "truck"],
     "A light vehicle follows one truck on the road; spacing about 80 m.", 2, 55.2, 5.1),
    ("2026-05-16T07:21:00Z", 35.0993, 36.2738, "sat-area-d.png", "Vehicles",
     "2x light vehicle, 3x cargo truck in column", ["car", "car", "truck", "truck", "truck"],
     "Short column of five vehicles moving along the ridge road.", 6, 61.8, 4.6),
]


def adint_items(template: dict) -> list[dict]:
    out = []
    for n, (when, lat, lon, brand, model, os_name, language, ip, accuracy) in enumerate(ADINT, 1):
        item = base(template, new_id(f"adint-{n}"), when, lat, lon)
        item["language"] = language
        item["fe_correlation_ids"] = [f"ADINT_OBS-21-{n:03d}"]
        item["additional_info"] = [{"accuracy_m": accuracy}]
        agent = copy.deepcopy((template.get("user_agents_data") or [{}])[0])
        agent.update({"device_name": new_id(f"adint-device-{n}"), "device_brand": brand, "device_model": model,
                      "operating_system_name": os_name, "language_code": language})
        item["user_agents_data"] = [agent]
        session = copy.deepcopy(((template.get("ip") or {}).get("ip_sessions") or [{}])[0])
        session.update({"source_ip": ip})
        item["ip"] = {**(template.get("ip") or {}), "ip_sessions": [session]}
        item["locations"] = [geo(lat, lon, when, None, None, (template.get("locations") or [{}])[0])] if template.get("locations") else []
        out.append(item)
    return out


def cellular_items(sms_template: dict, call_template: dict) -> list[dict]:
    out = []
    for n, (when, lat, lon, kind, direction, msisdn, imsi, cell, seconds, text) in enumerate(CELLULAR, 1):
        template = sms_template if kind == "sms" else call_template
        item = base(template, new_id(f"cellular-{n}"), when, lat, lon)
        target_role, other_role = ("from", "to") if direction == "out" else ("to", "from")
        item["call_direction"] = direction
        item["parties"] = [
            {"id": "1", "role": target_role, "identifiers": [{"type": t, "value": TARGET[t]} for t in ("msisdn", "imsi", "imei")],
             "target_indication": "True"},
            {"id": "2", "role": other_role, "identifiers": [{"type": "msisdn", "value": msisdn}, {"type": "imsi", "value": imsi}]
             + ([{"type": "imei", "value": OTHER_IMEI[msisdn]}] if msisdn in OTHER_IMEI else []), "target_indication": "False"},
        ]
        cgi_template, geo_template = (template.get("locations") or [{}, {}])[:2]
        cgi = copy.deepcopy(cgi_template)
        cgi.update({"from_time": when, "to_time": when, "party_id": "1", "value": cell})
        item["locations"] = [cgi, geo(lat, lon, when, "1", dms(lat, lon), geo_template)]
        item["locations"][1]["to_time"] = when
        item["fe_correlation_ids"] = [uuid.uuid5(NAMESPACE, f"cellular-correlation-{n}").hex.upper() * 2]
        item["asset_identifier"] = "2345671288"
        start = datetime.fromisoformat(when.replace("Z", "+00:00"))
        end = (start + timedelta(seconds=seconds)).strftime("%Y-%m-%dT%H:%M:%SZ")
        telephony = dict(template.get("telephony") or {})
        telephony.update({"cc_start_time": when, "cc_end_time": end, "iri_start_time": when, "iri_end_time": end,
                          "cc_duration": float(seconds * 1000), "iri_duration": float(seconds * 1000)})
        item["telephony"] = telephony
        item["end_time"] = end
        if kind == "sms":
            item["messages"] = [{"text": text, "type": "message"}]
            item["sms"] = {**(template.get("sms") or {}), "number_of_parts": 1, "parts": [{"key": "1", "value": text}]}
            item["content_size"] = len(json.dumps(item["messages"], ensure_ascii=False).encode("utf-8")) * 20
        else:
            item["duration_ms"] = float(seconds * 1000)
        out.append(item)
    return out


def satellite_items(template: dict) -> list[dict]:
    out = []
    for n, (when, lat, lon, image, classification, detected, objects, note, cloud, sun, nadir) in enumerate(SATELLITE, 1):
        item = base(template, new_id(f"satellite-{n}"), when, lat, lon)
        item["fe_correlation_ids"] = [new_id(f"satellite-correlation-{n}")]
        item["locations"] = [geo(lat, lon, when, None, None, (template.get("locations") or [{}])[0])]
        info = dict((template.get("additional_info") or [{}])[0])
        info.update({"off_nadir_deg": nadir, "sun_elevation_deg": sun, "gsd_m": 0.5, "footprint_radius_km": 0.6,
                     "cloud_cover_pct": cloud, "classification": classification, "detected_objects": detected})
        item["additional_info"] = [info]
        item["tags"] = ([{"type": "event", "value": True, "source": "system"}, {"type": "flag", "value": "HasContent", "source": "system"}]
                        + [{"type": "object_recognition", "value": value, "source": "system"} for value in objects]
                        + [{"type": "duplication_counter", "value": 0, "source": "system"}])
        insight = copy.deepcopy((template.get("insights") or [{}])[0])
        insight.update({"value": note, "annotation_id": 90000000 + n})
        item["insights"] = [insight]
        file_id = f"90010000000{n:02d}"
        item["media"] = {**(template.get("media") or {}), "kind": "image", "has_thumbnail": True, "primary_file_id": file_id,
                         "thumbnail_file_id": file_id, "file_count": 1, "primary_file_name": image,
                         "primary_file_content_type": "image/png"}
        item["content_size"] = (ROOT / "demo_data" / "area-search" / image).stat().st_size
        out.append(item)
    return out


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print(__doc__)
        return 2
    templates = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    cellular = templates["Cellular Locations"]
    sms = next(i for i in cellular if i.get("item_type") == "sms")
    call = next(i for i in cellular if i.get("item_type") == "voice_call")
    data = {
        "_comment": "The app's own records (not in i360) for the polygon area search demo; written by tools/make_area_search_data.py.",
        "layers": {
            "ADINT": adint_items(templates["ADINT"][0]),
            "Cellular Locations": cellular_items(sms, call),
            "Satellite": satellite_items(templates["Satellite"][0]),
        },
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8", newline="\n")
    print(f"wrote {OUT} ({sum(len(v) for v in data['layers'].values())} records)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

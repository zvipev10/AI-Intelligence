#!/usr/bin/env python3
"""Writes demo_data/lambda-area-search.json: the app's own records for the polygon area search demo.

These records are not in i360. They copy the exact item shape of the LAMBDA layers (ADINT, Cellular
Locations, Satellite), are scattered in and around the town of Masyaf and are dated March to
May 2026, weeks to months before the earliest i360 record (2026-07-01).

    python tools/make_area_search_data.py <templates.json>

<templates.json> is a dump of current i360 items by layer ({"ADINT": [item, ...], ...}); one item of
each layer is the template whose shape every synthetic record keeps. The output is deterministic.
"""
from __future__ import annotations

import copy
import json
import random
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


# Every record has its own spot in and around Masyaf (centre about 35.065, 36.342).

# --- ADINT: 7 location updates from phones that are not in the current data ------------------------------
ADINT = [
    # time, lat, lon, brand, model, os, language, ip, accuracy_m
    ("2026-03-04T06:12:00Z", 35.0712, 36.3385, "Xiaomi", "Redmi Note 12", "Android", "ar", "198.51.100.14", 20),
    ("2026-03-19T17:40:00Z", 35.0598, 36.3501, "Oppo", "A78", "Android", "ar", "198.51.100.37", 35),
    ("2026-04-07T09:05:00Z", 35.0821, 36.3302, "Samsung", "Galaxy A54", "Android", "fa", "198.51.100.52", 15),
    ("2026-04-22T21:18:00Z", 35.0505, 36.3367, "Tecno", "Spark 10", "Android", "ar", "198.51.100.68", 60),
    ("2026-05-03T05:47:00Z", 35.0689, 36.3618, "Apple", "iPhone 13", "iOS", "en", "198.51.100.91", 10),
    ("2026-05-11T13:26:00Z", 35.0444, 36.3540, "Infinix", "Hot 30", "Android", "fa", "198.51.100.103", 45),
    ("2026-05-18T19:02:00Z", 35.0866, 36.3489, "Nokia", "G21", "Android", "ar", "198.51.100.120", 80),
]

# --- Cellular Locations: 9 calls and SMS of a new target, each with a cell and a GPS point -----------------
def luhn(digits: str) -> str:
    total = 0
    for i, d in enumerate(reversed(digits)):
        v = int(d) * (2 if i % 2 == 0 else 1)
        total += v - 9 if v > 9 else v
    return digits + str((10 - total % 10) % 10)


def device(rng: random.Random) -> dict[str, str]:
    """A random Syrian subscriber: MSISDN (9639...), IMSI (41701...) and an IMEI with its check digit."""
    tac = rng.choice(["35329470", "35693810", "35209900", "86153603", "35874210", "86719305", "35412608"])
    return {"msisdn": "9639" + "".join(rng.choice("0123456789") for _ in range(8)),
            "imsi": "41701" + "".join(rng.choice("0123456789") for _ in range(10)),
            "imei": luhn(tac + "".join(rng.choice("0123456789") for _ in range(6)))}


CELLULAR = [
    # time, lat, lon, type, direction, cell, duration s, sms text (both devices of every record are random)
    ("2026-03-02T07:31:00Z", 35.0634, 36.3248, "voice_call", "out", "3104-21877", 94, None),
    ("2026-03-14T22:05:00Z", 35.0750, 36.3560, "sms", "out", "3102-21290", 0, "وصلنا عند المفرق"),
    ("2026-03-27T11:48:00Z", 35.0552, 36.3205, "voice_call", "in", "3105-22410", 212, None),
    ("2026-04-09T18:22:00Z", 35.0901, 36.3399, "sms", "in", "3102-21291", 0, "الطريق فاضي هلق"),
    ("2026-04-19T04:56:00Z", 35.0481, 36.3466, "voice_call", "out", "3101-20983", 47, None),
    ("2026-04-28T15:10:00Z", 35.0785, 36.3196, "sms", "out", "3104-21878", 0, "جيب السيارة التانية"),
    ("2026-05-06T20:37:00Z", 35.0607, 36.3655, "voice_call", "in", "3107-22715", 138, None),
    ("2026-05-14T08:03:00Z", 35.0420, 36.3290, "sms", "in", "3104-21876", 0, "بكرا الصبح بكير"),
    ("2026-05-20T23:44:00Z", 35.0839, 36.3634, "voice_call", "out", "3103-21504", 76, None),
]

# --- Satellite: 4 captures of civilian sites with cars detected; synthetic images (tools/draw_area_search_images.py)
SATELLITE = [
    # time, lat, lon, image file, classification, detected objects, recognised objects, analyst note, cloud %, sun, off-nadir
    ("2026-03-09T07:12:00Z", 35.0532, 36.3130, "sat-area-a.png", "Logistics park",
     "2x large warehouse, ~40x car in staff car park, 6x car on access road",
     ["building", "building", "parking lot"] + ["car"] * 8,
     "Two large warehouses with a nearly full staff car park; steady civilian traffic on the access road.", 3, 38.1, 6.4),
    ("2026-04-02T07:09:00Z", 35.0880, 36.3250, "sat-area-b.png", "Construction site",
     "1x large building under construction, 1x tower crane, 2x excavator, 2x dump truck, 1x concrete mixer, 7x car",
     ["building", "crane", "excavator", "excavator", "truck", "truck", "truck"] + ["car"] * 7,
     "Concrete frame of a large building going up; earthworks with two excavators and a mixer on site.", 8, 47.6, 3.9),
    ("2026-04-25T07:15:00Z", 35.0470, 36.3700, "sat-area-c.png", "Factory",
     "1x large factory hall, 4x storage silo, 4x truck in yard, ~20x car parked, 8x car on road",
     ["building", "building", "silo", "truck", "truck", "truck", "truck"] + ["car"] * 8,
     "Factory beside the main road with four silos; trucks loading in the yard and cars passing on the road.", 2, 55.2, 5.1),
    ("2026-05-16T07:21:00Z", 35.0925, 36.3570, "sat-area-d.png", "Plant hire depot",
     "1x hangar, 4x excavator, 3x dump truck, 3x concrete mixer, 6x shipping container, ~25x car",
     ["building", "excavator", "excavator", "excavator", "excavator", "truck", "truck", "truck", "container"] + ["car"] * 8,
     "Plant-hire depot with rows of yellow machinery, containers and a customer car park.", 6, 61.8, 4.6),
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
    for n, (when, lat, lon, kind, direction, cell, seconds, text) in enumerate(CELLULAR, 1):
        rng = random.Random(f"cellular-{n}")
        target, other = device(rng), device(rng)
        template = sms_template if kind == "sms" else call_template
        item = base(template, new_id(f"cellular-{n}"), when, lat, lon)
        target_role, other_role = ("from", "to") if direction == "out" else ("to", "from")
        item["call_direction"] = direction
        item["parties"] = [
            {"id": "1", "role": target_role, "identifiers": [{"type": t, "value": target[t]} for t in ("msisdn", "imsi", "imei")],
             "target_indication": "True"},
            {"id": "2", "role": other_role, "identifiers": [{"type": t, "value": other[t]} for t in ("msisdn", "imsi")]
             + ([{"type": "imei", "value": other["imei"]}] if rng.random() < 0.5 else []), "target_indication": "False"},
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
        info.update({"off_nadir_deg": nadir, "sun_elevation_deg": sun, "gsd_m": 0.3, "footprint_radius_km": 0.12,
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

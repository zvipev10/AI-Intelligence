"""Offline deterministic synthetic fixture builder. Requires Pillow/imageio-ffmpeg.

Dependencies are build-only; the application serves the checked-in media files.
"""
import csv
import hashlib
import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path
from PIL import Image, ImageDraw
import imageio_ffmpeg

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data/syria_convoy_v1"
MEDIA = ROOT / "assets/demo/syria/convoy-v1"


def frame(site, step, timestamp, satellite=False):
    image = Image.new("RGB", (640, 360), "#b4a588")
    draw = ImageDraw.Draw(image)
    for x in range(0, 640, 80):
        draw.rectangle((x + 8, 66, x + 65, 128), fill="#cbbca2", outline="#827762")
        draw.rectangle((x + 12, 255, x + 61, 300), fill="#9b9477", outline="#827762")
    draw.polygon([(0, 160), (640, 145), (640, 238), (0, 252)], fill="#55595c")
    for x in range(0, 640, 65):
        draw.line((x, 203, x + 32, 201), fill="#e9dfbf", width=3)
    for vehicle in range(4):
        x = int((step * 95 + vehicle * 76 + site * 19) % 760) - 60
        draw.rectangle((x, 175, x + 43, 192), fill="#3e575d", outline="#152d31", width=2)
        draw.rectangle((x + 5, 178, x + 14, 189), fill="#9ec0c6")
    draw.rectangle((0, 0, 640, 53), fill="#142833")
    draw.text((15, 10), "SYNTHETIC DEMO - NOT REAL IMAGERY", fill="white")
    draw.text((15, 30), f"{'SATELLITE' if satellite else 'CCTV'} | SITE {site} | {timestamp}", fill="#83dfed")
    draw.rectangle((0, 325, 640, 360), fill="#142833")
    draw.text((15, 337), "Convoy: 4 simulated vehicles | Fictional observation", fill="white")
    return image


def main():
    DATA.mkdir(parents=True, exist_ok=True); MEDIA.mkdir(parents=True, exist_ok=True)
    locations = {}
    for site, latitude in [(1, 35.0), (2, 35.045)]:
        locations[f"LOC-SYR-{site:03}"] = {"name": f"Demo Site {site}", "latitude": latitude, "longitude": 38.5, "country": "Syria", "region": "Central Syria (synthetic demo)", "type": "demonstration site", "precision": "synthetic", "locality": f"Fictional Site {site}"}
    entities = [{"entity_id": "ENT-SYR-CONVOY", "canonical_name": "Convoy", "aliases": ["convoy", "שיירה"], "entity_type": "vehicle convoy", "description": "Synthetic convoy entity shared by all 12 demonstration observations."}]
    records = []
    for site in [1, 2]:
        for source in ["CCTV", "Satellite"]:
            for number in range(1, 4):
                at = datetime(2026, 9, 22, 8, tzinfo=timezone.utc) + timedelta(hours=number - 1, minutes=(site - 1) * 15)
                stamp = at.isoformat().replace("+00:00", "Z")
                stem = f"site-{site}-{source.lower()}-{number}"
                record = {"event_id": f"REC-SYR-{source.upper()}-{site}-{number}", "timestamp_utc": stamp, "source_type": source, "source_reliability": "high", "source_reliability_label": "Synthetic demo", "certainty_level": "observed", "entity_id": "ENT-SYR-CONVOY", "location_id": f"LOC-SYR-{site:03}", "event_summary": f"SYNTHETIC DEMO: {source} observation {number} shows movement of the Convoy (4 simulated vehicles) at Demo Site {site}. Extracted location and entity are demonstration annotations, not real-world detections.", "collection_family": "synthetic_cctv_video" if source == "CCTV" else "synthetic_satellite_imagery", "observation_id": stem, "mission_id": f"SYR-DEMO-{site}", "object_class": "שיירת כלי רכב", "estimated_object_count": "4", "movement_status": "moving", "movement_direction": "east", "geolocation_confidence": "high", "identification_confidence": "high", "synthetic_media": "true", "video_url": "", "image_series": ""}
                if source == "CCTV":
                    path = MEDIA / (stem + ".mp4")
                    command = [imageio_ffmpeg.get_ffmpeg_exe(), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", "640x360", "-r", "12", "-i", "-", "-an", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-movflags", "+faststart", str(path)]
                    process = subprocess.Popen(command, stdin=subprocess.PIPE)
                    for tick in range(60):
                        process.stdin.write(frame(site, tick / 12 + number, stamp).tobytes())
                    process.stdin.close()
                    if process.wait(): raise RuntimeError("Video encoder failed")
                    record["video_url"] = "/" + path.relative_to(ROOT).as_posix()
                else:
                    series = []
                    for capture in range(3):
                        captured = (at + timedelta(minutes=capture * 5)).isoformat().replace("+00:00", "Z")
                        path = MEDIA / f"{stem}-{capture + 1}.png"
                        frame(site, number + capture / 2, captured, True).save(path)
                        series.append({"image_url": "/" + path.relative_to(ROOT).as_posix(), "timestamp_utc": captured})
                    record["image_series"] = json.dumps(series)
                records.append(record)
    for suffix in ["", ".en"]:
        with (DATA / f"events{suffix}.csv").open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(records[0])); writer.writeheader(); writer.writerows(records)
        for name, content in [("locations", locations), ("entities", entities)]:
            (DATA / f"{name}{suffix}.json").write_bytes(json.dumps(content, indent=2, ensure_ascii=False).encode())
    profile_path = ROOT / "demo_profiles/syria.json"
    profile = json.loads(profile_path.read_text(encoding="utf-8"))
    profile.update(profile_version="2", dataset_version="convoy-v1", empty_dataset=False)
    profile["files"] = {kind: f"data/syria_convoy_v1/{kind}.{'csv' if kind == 'events' else 'json'}" for kind in ["events", "locations", "entities"]}
    for language in ["he", "en"]:
        profile["sources"][language] = [source for source in profile["sources"][language] if source not in ["CCTV", "Satellite"]] + ["CCTV", "Satellite"]
    profile["map"]["center"] = [38.5, 35.0225]; profile["map"]["zoom"] = 12
    profile["checksums"] = {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes().replace(b"\r\n", b"\n")).hexdigest() for path in [*DATA.iterdir(), *MEDIA.iterdir()]}
    profile_path.write_bytes(json.dumps(profile, indent=2, ensure_ascii=False).encode())
    print(f"Created {len(records)} records, {len(locations)} locations, {len(entities)} entity; {len(list(MEDIA.iterdir()))} media files")


if __name__ == "__main__":
    main()

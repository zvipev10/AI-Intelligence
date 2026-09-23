import csv
import json
import math
import unittest
from collections import Counter
from pathlib import Path
from datetime import datetime
from demo_runtime import load_profile

ROOT = Path(__file__).resolve().parent


class SyriaConvoy(unittest.TestCase):
    def test_dataset_relations_and_media(self):
        profile = load_profile(ROOT, "syria", verify=True)
        rows = list(csv.DictReader((ROOT / profile["files"]["events"]).read_text(encoding="utf-8").splitlines()))
        locations = json.loads((ROOT / profile["files"]["locations"]).read_text())
        entities = json.loads((ROOT / profile["files"]["entities"]).read_text(encoding="utf-8"))
        self.assertEqual(len({r["event_id"] for r in rows}), 4)
        self.assertEqual(len(entities), 1)
        self.assertEqual(Counter((r["source_type"], r["location_id"]) for r in rows), {(s, l): 1 for s in ["CCTV", "Satellite"] for l in locations})
        first, second = locations.values()
        distance = 6371 * math.radians(abs(first["latitude"] - second["latitude"]))
        self.assertAlmostEqual(distance, 5, delta=.1)
        for row in rows:
            self.assertEqual(row["entity_id"], entities[0]["entity_id"])
            self.assertEqual(row["synthetic_media"], "true")
            if row["source_type"] == "CCTV":
                self.assertIn(b"ftyp", (ROOT / row["video_url"].lstrip("/")).read_bytes()[:32])
            else:
                captures = json.loads(row["image_series"])
                self.assertEqual(len({c["timestamp_utc"] for c in captures}), 3)
                for capture in captures:
                    self.assertTrue((ROOT / capture["image_url"].lstrip("/")).read_bytes().startswith(b"\x89PNG"))
                    counterpart = next(r for r in rows if r["event_id"] == capture["paired_record_id"])
                    paired = next(c for c in json.loads(counterpart["image_series"]) if c["pair_id"] == capture["pair_id"])
                    self.assertEqual(capture["paired_image_url"], paired["image_url"])
                    self.assertEqual(capture["paired_timestamp_utc"], paired["timestamp_utc"])
                    delta = datetime.fromisoformat(paired["timestamp_utc"]) - datetime.fromisoformat(capture["timestamp_utc"])
                    self.assertEqual(delta.total_seconds(), 900 if row["location_id"].endswith("001") else -900)

    def test_kosovo_has_no_new_sources(self):
        profile = load_profile(ROOT, "kosovo", verify=True)
        self.assertNotIn("CCTV", profile["sources"]["en"])
        self.assertNotIn("Satellite", profile["sources"]["en"])


if __name__ == "__main__":
    unittest.main()

import csv
import json
import math
import unittest
from collections import Counter
from pathlib import Path
from demo_runtime import load_profile

ROOT = Path(__file__).resolve().parent


class SyriaConvoy(unittest.TestCase):
    def test_dataset_relations_and_media(self):
        profile = load_profile(ROOT, "syria", verify=True)
        rows = list(csv.DictReader((ROOT / profile["files"]["events"]).read_text(encoding="utf-8").splitlines()))
        locations = json.loads((ROOT / profile["files"]["locations"]).read_text())
        entities = json.loads((ROOT / profile["files"]["entities"]).read_text(encoding="utf-8"))
        self.assertEqual(len({r["event_id"] for r in rows}), 12)
        self.assertEqual(len(entities), 1)
        self.assertEqual(Counter((r["source_type"], r["location_id"]) for r in rows), {(s, l): 3 for s in ["CCTV", "Satellite"] for l in locations})
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

    def test_kosovo_has_no_new_sources(self):
        profile = load_profile(ROOT, "kosovo", verify=True)
        self.assertNotIn("CCTV", profile["sources"]["en"])
        self.assertNotIn("Satellite", profile["sources"]["en"])


if __name__ == "__main__":
    unittest.main()

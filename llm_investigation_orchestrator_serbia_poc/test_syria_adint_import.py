import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from import_syria_adint import validate
from demo_runtime import load_profile

ROOT = Path(__file__).resolve().parent

class AdintImportTests(unittest.TestCase):
    def test_exact_fields_nulls_and_preserved_sources(self):
        profile = load_profile(ROOT, "syria", verify=True)
        self.assertEqual(profile["dataset_version"], "adint-v1")
        source = json.loads((ROOT / "data/syria_adint_v1/ADINT.json").read_text())
        rows = list(csv.DictReader((ROOT / profile["files"]["events"]).read_text().splitlines()))
        imported = {r["observation_id"]: r for r in rows if r["source_type"] == "ADINT"}
        self.assertEqual(len(rows), 324); self.assertEqual(len(imported), 120)
        locations = json.loads((ROOT / profile["files"]["locations"]).read_text())
        self.assertEqual(len(locations), 86)
        for raw in source:
            row = imported[raw["observation_id"]]
            for key, value in raw.items():
                self.assertEqual(row[key], "" if value is None else str(value))
            if raw["latitude"] is None:
                self.assertEqual(row["location_id"], "")
            else:
                loc = locations[row["location_id"]]
                self.assertEqual((loc["latitude"], loc["longitude"]), (raw["latitude"], raw["longitude"]))
        old = list(csv.DictReader((ROOT / "data/syria_network_v1/events.csv").read_text().splitlines()))
        current = {r["event_id"]: r for r in rows}
        for row in old:
            if row["source_type"] == "ADINT":
                self.assertNotIn(row["event_id"], current)
            else:
                self.assertEqual(row, {k: current[row["event_id"]][k] for k in row})
        self.assertEqual((ROOT / "data/syria_adint_v1/events.csv").read_bytes(), (ROOT / "data/syria_adint_v1/events.en.csv").read_bytes())

    def test_invalid_input_rejected(self):
        rows = json.loads((ROOT / "data/syria_adint_v1/ADINT.json").read_text())
        for key, value in [("latitude", 100), ("longitude", None), ("accuracy_m", -1), ("ip", "invalid")]:
            with self.subTest(key=key), self.assertRaises(ValueError):
                validate([{**rows[0], key: value}])
        with self.assertRaises(ValueError): validate([rows[0], rows[0]])

    def test_public_projection_and_search(self):
        with tempfile.TemporaryDirectory() as state:
            code = """import mcp_server.server as s
assert len(s.EVENTS)==324
rows=[s.public_event(r) for r in s.EVENTS if r['source_type']=='ADINT']
assert sum(r['latitude'] is None for r in rows)==36
assert sum(r['ip'] is None for r in rows)==51
assert sum(r['keyboard_language'] is None for r in rows)==76
assert all(not r['location_id'] for r in rows if r['latitude'] is None)
for keyword in ['OBS-01-001',rows[0]['device_id'],'iPhone 15']:
 assert s.search_events({'source_types':['ADINT'],'keywords':[keyword]})['total']>0
assert all(r['timestamp_utc'] < '2026-09-06' for r in rows)
"""
            r = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env={**os.environ, "INTELLIGENCE_POC_SCENARIO":"syria", "INTELLIGENCE_POC_STATE_ROOT":state}, capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr)

if __name__ == "__main__": unittest.main()

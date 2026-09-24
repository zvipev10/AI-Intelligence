import csv
import json
import math
import os
import subprocess
import sys
import tempfile
import unittest
from collections import Counter
from datetime import datetime
from pathlib import Path
from demo_runtime import load_profile

ROOT = Path(__file__).resolve().parent


class NetworkFixture(unittest.TestCase):
    def test_unique_ip_join_and_nearby_points(self):
        p = {"files": {"events": "data/syria_network_v1/events.csv", "locations": "data/syria_network_v1/locations.json"}}
        rows = list(csv.DictReader((ROOT / p["files"]["events"]).read_text().splitlines()))
        counts = Counter(r["source_type"] for r in rows)
        self.assertEqual(counts, {"CCTV": 2, "Satellite": 2, "ADINT": 4, "IPDR": 200})
        adint = [r for r in rows if r["source_type"] == "ADINT"]
        ipdr = [r for r in rows if r["source_type"] == "IPDR"]
        pairs = [(a, i) for a in adint for i in ipdr if a["ip_address"] == i["ip_address"]]
        self.assertEqual(len(pairs), 1)
        a, i = pairs[0]
        self.assertEqual(a["location_id"], "LOC-SYR-001")
        self.assertTrue(all(not r["imei"] for r in adint))
        self.assertEqual(len(i["imei"]), 15)
        self.assertLessEqual(datetime.fromisoformat(i["session_start_utc"]), datetime.fromisoformat(a["timestamp_utc"]))
        self.assertGreaterEqual(datetime.fromisoformat(i["session_end_utc"]), datetime.fromisoformat(a["timestamp_utc"]))
        loc = json.loads((ROOT / p["files"]["locations"]).read_text())
        origin = loc["LOC-SYR-001"]
        for row in adint[1:]:
            point = loc[row["location_id"]]
            lat1, lat2 = map(math.radians, [origin["latitude"], point["latitude"]])
            dlon = math.radians(point["longitude"] - origin["longitude"])
            distance = 6371000 * 2 * math.asin(math.sqrt(math.sin((lat2-lat1)/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2))
            self.assertAlmostEqual(distance, 500, delta=1)
        previous = list(csv.DictReader((ROOT / "data/syria_convoy_v3/events.csv").read_text().splitlines()))
        for old in previous:
            current = next(r for r in rows if r["event_id"] == old["event_id"])
            self.assertEqual({k: current[k] for k in old}, old)

    def test_replaced_ipdr_does_not_retain_old_synthetic_match(self):
        with tempfile.TemporaryDirectory() as state:
            code = """import mcp_server.server as s
a=s.search_events({'source_types':['ADINT'],'keywords':['OBS-01-001']})['events']
assert len(a)==1 and not a[0]['imei']
assert a[0]['device_id'] and a[0]['ip']=='192.0.2.10'
r=s.search_events({'source_types':['IPDR'],'keywords':[a[0]['ip_address']]})
assert r['total']==0
"""
            result = subprocess.run([sys.executable, "-c", code], cwd=ROOT, env={**os.environ, "INTELLIGENCE_POC_SCENARIO": "syria", "INTELLIGENCE_POC_STATE_ROOT": state}, capture_output=True, timeout=30)
            self.assertEqual(result.returncode, 0, result.stderr.decode())


if __name__ == "__main__":
    unittest.main()

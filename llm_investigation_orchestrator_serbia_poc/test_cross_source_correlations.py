import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class CrossSourceCorrelations(unittest.TestCase):
    def test_syria_catalog_exact_filter_and_device_correlations(self):
        code = r'''
import mcp_server.server as server

catalog = server.describe_active_data({})
assert any(row["name"] == "Cellular Geolocations" and row["record_count"] == 18 for row in catalog["sources"])
assert any(field["name"] == "side_a_imei" and field["role"] == "device_identifier" for field in catalog["fields"])

call = server.search_events({"field_filters": [{"field": "call_id", "equals": "SYR-DEMO-CALL-001"}]})
assert call["total"] == 1 and call["event_ids"] == ["REC-SYR-CALL-001"]

correlations = server.discover_record_correlations({"roles": ["device_identifier"]})["correlations"]
call_links = [item for item in correlations if any(row["event_id"] == "REC-SYR-CALL-001" for row in item["records"])]
assert {item["value"] for item in call_links} == {"353294702931926"}
assert {"שיחות סלולר", "Cellular Geolocations", "IPDR"} <= set(call_links[0]["source_types"])
'''
        with tempfile.TemporaryDirectory() as state:
            result = subprocess.run(
                [sys.executable, "-c", code],
                cwd=ROOT,
                env={**os.environ, "INTELLIGENCE_POC_SCENARIO": "syria", "INTELLIGENCE_POC_STATE_ROOT": state},
                capture_output=True,
                text=True,
                timeout=60,
            )
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()

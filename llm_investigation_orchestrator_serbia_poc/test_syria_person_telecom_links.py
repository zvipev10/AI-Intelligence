import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from demo_runtime import load_profile


ROOT = Path(__file__).resolve().parent


class SyriaPersonTelecomLinks(unittest.TestCase):
    def test_iranian_person_links_to_existing_telecom_records_and_call_parties(self):
        profile = load_profile(ROOT, "syria", verify=True)
        self.assertEqual(profile["dataset_version"], "cellular-records-v5")
        code = r'''
import server

events, entities, _ = server.ui_layer_data("en")
by_id = {event["event_id"]: event for event in events}
person = entities["ENT-SYR-PERSON-002"]
assert person["canonical_name"] == "Arman Rahimi"
assert person["nationality"] == "Iranian"
assert person["image_url"] == "/assets/demo/syria/persons/arman-rahimi-reference-v1.png"
assert person["identity_status"] == "profiled individual"
assert person["identifiers"]["imei"] == "353294702931926"
omar = entities["ENT-SYR-PERSON-001"]
assert omar["identifiers"]["imei"] == "352099001122338"
assert person["event_count"] == 8
assert "ENT-SYR-PERSON-002" in by_id["REC-SYR-IPDR-1683930569233410"]["related_entity_ids"]
assert "ENT-SYR-PERSON-002" in by_id["REC-SYR-CELL-CSV-013"]["related_entity_ids"]
call = by_id["REC-SYR-CALL-001"]
assert (call["side_a_entity_id"], call["side_a_entity_name"]) == ("ENT-SYR-PERSON-002", "Arman Rahimi")
assert (call["side_b_entity_id"], call["side_b_entity_name"]) == ("ENT-SYR-PERSON-001", "Omar Al-Khatib")
assert call["side_a_imei"] == person["identifiers"]["imei"]
assert call["side_b_imei"] == omar["identifiers"]["imei"]
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

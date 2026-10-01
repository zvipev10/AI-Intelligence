import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from demo_runtime import load_profile


ROOT = Path(__file__).resolve().parent


class SyriaPersonTelecomLinks(unittest.TestCase):
    def test_iranian_person_links_to_existing_telecom_records_without_call_party_identity(self):
        profile = load_profile(ROOT, "syria", verify=True)
        self.assertEqual(profile["dataset_version"], "cellular-records-v11")
        code = r'''
import server

events, entities, _ = server.ui_layer_data("en")
by_id = {event["event_id"]: event for event in events}
person = entities["ENT-SYR-PERSON-002"]
assert person["canonical_name"] == "Arman Rahimi"
assert person["nationality"] == "Iranian"
assert person["image_url"] == "/assets/demo/syria/persons/arman-rahimi-reference-v1.png"
assert person["identity_status"] == "profiled individual"
assert person["telecom"]["imei"] == "353294702931926"
assert "msisdn" not in person["telecom"] and "imsi" not in person["telecom"]
derivation = person["telecom"]["subscriber_identity_derivation"]
assert derivation["claim"]["value"]["msisdn"] == "9630943700780"
assert derivation["claim"]["value"]["imsi"] == "417011234567890"
assert derivation["status"] == "candidate"
assert len(person["telecom"]["reference_record_ids"]) == 20
assert [call["event_id"] for call in person["telecom"]["calls"]] == ["REC-SYR-CALL-001", "REC-SYR-CALL-002"]
omar = entities["ENT-SYR-PERSON-001"]
assert omar["telecom"]["imei"] == "352099001122338"
assert person["event_count"] == 22
assert "ENT-SYR-PERSON-002" in by_id["REC-SYR-IPDR-1683930569233410"]["related_entity_ids"]
assert "ENT-SYR-PERSON-002" in by_id["REC-SYR-CELL-CSV-013"]["related_entity_ids"]
ipdr_link = by_id["REC-SYR-IPDR-1683930569233410"]["observed_entity_links"][0]
assert (ipdr_link["entity_id"], ipdr_link["record_field"], ipdr_link["entity_field"]) == ("ENT-SYR-PERSON-002", "imei", "telecom.imei")
cell_link = by_id["REC-SYR-CELL-CSV-013"]["observed_entity_links"][0]
assert (cell_link["entity_id"], cell_link["record_field"], cell_link["entity_field"]) == ("ENT-SYR-PERSON-002", "target_imei", "telecom.imei")
call = by_id["REC-SYR-CALL-001"]
assert (call["side_a_entity_id"], call["side_a_entity_name"]) == ("ENT-SYR-PERSON-002", "Arman Rahimi")
assert (call.get("side_b_entity_id"), call.get("side_b_entity_name")) == (None, None)
assert call["side_a_imei"] == person["telecom"]["imei"]
assert call["side_b_imei"] == ""
call2 = by_id["REC-SYR-CALL-002"]
assert (call2["side_a_entity_id"], call2["side_a_entity_name"]) == ("ENT-SYR-PERSON-002", "Arman Rahimi")
assert (call2.get("side_b_entity_id"), call2.get("side_b_entity_name")) == (None, None)
assert call2["side_b_imei"] == ""
assert call2["audio_url"] == "/assets/demo/syria/call-media-v1/call-2.mp3"
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

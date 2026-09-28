import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class PersonTelecomCorrelationTests(unittest.TestCase):
    def test_imei_linked_identifiers_are_derived_and_persisted_only_after_approval(self):
        with tempfile.TemporaryDirectory() as state:
            code = """
import server
correlation = server.telecom_identifier_correlation('ENT-SYR-PERSON-002')
assert correlation['imei'] == '353294702931926'
assert correlation['msisdn'] == '9630943700780'
assert correlation['imsi'] == '417011234567890'
assert len(correlation['supporting_record_ids']) == 18
saved = server.approve_person_telecom_correlation({'investigation_id': 'telecom-correlation-demo', 'entity_id': 'ENT-SYR-PERSON-002'})
assert saved['saved']['method'] == 'imei_linked_telecom_identity_correlation'
memory = server.load_investigation_memory('telecom-correlation-demo')
assert memory['memory']['entity_enrichments'][0]['msisdn'] == '9630943700780'
try:
    server.telecom_identifier_correlation('ENT-SYR-PERSON-001')
except ValueError as error:
    assert 'No cellular-geolocation' in str(error)
else:
    raise AssertionError('Expected no corroborated identifiers for Omar')
"""
            result = subprocess.run(
                [sys.executable, "-c", code], cwd=Path(__file__).resolve().parent,
                env={**os.environ, "INTELLIGENCE_POC_SCENARIO": "syria", "INTELLIGENCE_POC_STATE_ROOT": state},
                capture_output=True, text=True, timeout=60,
            )
            self.assertEqual(result.returncode, 0, result.stderr)


class PersonTelecomCorrelationUiTests(unittest.TestCase):
    def test_viewer_exposes_identifier_correlation_and_approval(self):
        app = (Path(__file__).resolve().parent / "app.js").read_text(encoding="utf-8")
        bootstrap = (Path(__file__).resolve().parent / "demo_bootstrap.js").read_text(encoding="utf-8")
        self.assertIn("IMEI-linked telecom identity correlation", app)
        self.assertIn("Approve and save to entity", app)
        self.assertIn("/api/investigation-entity/telecom-correlation/approve", app)
        self.assertIn('script.src = "./app.js?v=247";', bootstrap)


if __name__ == "__main__":
    unittest.main()

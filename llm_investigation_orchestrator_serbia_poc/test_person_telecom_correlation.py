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
rejected = server.review_subscriber_identity_derivation({'entity_id': 'ENT-SYR-PERSON-002', 'action': 'reject'})
assert rejected['saved']['review_state'] == 'rejected'
assert 'msisdn' not in server.load_ui_entity_db('en')['ENT-SYR-PERSON-002']['telecom']
saved = server.approve_entity_telecom_correlation({'entity_id': 'ENT-SYR-PERSON-002'})
assert saved['saved']['method'] == 'subscriber_identity_from_imei_linked_records_v1'
entity_telecom = server.load_ui_entity_db('en')['ENT-SYR-PERSON-002']['telecom']
assert entity_telecom['msisdn'] == '9630943700780'
assert entity_telecom['imsi'] == '417011234567890'
assert entity_telecom['approved_subscriber_identity']['imsi'] == '417011234567890'
assert 'extracted_subscriber_identity' not in entity_telecom
assert server.ENTITY_APPROVALS_PATH.exists()
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
        self.assertIn("function personTelecomDetailsHtml(item)", app)
        self.assertIn("function recordLinkedEntitiesHtml(item)", app)
        self.assertIn("function recordLinkIndicator(item)", app)
        self.assertIn('class="record-link-indicator"', app)
        self.assertIn("Linked entities", app)
        self.assertIn("function approveExtractedTelecomIdentity(entityId, button)", app)
        self.assertIn("Extracted subscriber identity", app)
        self.assertIn("data-approve-telecom-entity", app)
        self.assertIn('"/api/derivations/review"', app)
        self.assertIn('"Approve"', app)
        self.assertIn("Reference records", app)
        self.assertIn("Calls", app)
        self.assertIn('script.src = "./app.js?v=267";', bootstrap)


if __name__ == "__main__":
    unittest.main()

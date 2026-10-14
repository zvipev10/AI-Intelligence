import json
import unittest

from hl import report


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"i360_item_id": "call-2", "source_type": "Cellular Calls", "timestamp_utc": "2026-09-02T14:01:00Z",
             "call_transcript_en": "Open the gates.", "latitude": "35.07", "longitude": "36.30",
             "observed_entity_links": [{"entity_id": "p-1", "matched_value": "353294702931926"}]},
            {"i360_item_id": "ipdr-1", "source_type": "IPDR", "timestamp_utc": "2026-10-11T09:15:14Z",
             "i360.ip.ip_sessions.source_ip": "203.0.113.107",
             "observed_record_links": [{"record_id": "adint-1", "matched_value": "203.0.113.107"}]},
        ]
        self.labels = {"IPDR": {"i360.ip.ip_sessions.source_ip": "ip_public"}}
        self.person = {"entity_id": "p-1", "canonical_name": "Arman Rahimi",
                       "telecom": {"imei": "353294702931926",
                                   "subscriber_identity_derivation": {"claim": {"value": {"msisdn": "963094370078"}}}}}

    def test_cards_carry_refs_fields_text_and_links(self):
        card = report.record_card(self.rows[1], self.labels["IPDR"], {}, "R2")
        self.assertIn("ref=R2 | layer=IPDR", card)
        self.assertIn("ip_public=203.0.113.107", card)
        self.assertIn("matched value 203.0.113.107", card)
        call = report.record_card(self.rows[0], {}, {"p-1": "Arman Rahimi"}, "R1")
        self.assertIn("text: Open the gates.", call)
        self.assertIn("person Arman Rahimi", call)
        self.assertIn("MSISDN 963094370078 (recommended, not approved)", report.person_card(self.person, {}))

    def test_refs_map_back_to_records_and_invented_ones_are_dropped(self):
        asked = []

        def complete_json(messages, schema):
            asked.append(messages)
            return {"model": "m", "content": json.dumps({"paragraphs": [
                {"text": "A call on 2 Sep (R1).", "record_ids": ["R1"]},
                {"text": "Made up.", "record_ids": ["R9"]}], "gaps": ["No names for side B."]})}

        result = report.run_section(complete_json, report.SECTIONS[0], self.rows, lambda layer: self.labels.get(layer, {}),
                                    [self.person], {"p-1": "Arman Rahimi"})
        self.assertEqual(["call-2"], result["paragraphs"][0]["record_ids"])
        self.assertEqual("A call on 2 Sep.", result["paragraphs"][0]["text"])  # the inline ref is removed
        self.assertTrue(result["paragraphs"][1]["unsupported"])
        self.assertEqual(1, result["removed_ids"])
        self.assertEqual((2, 2, "m"), (result["records_used"], result["records_total"], result["model"]))
        self.assertIn("ref=R1 | layer=Cellular Calls", asked[0][1]["content"])  # in time order

    def test_a_cut_off_answer_is_asked_once_more(self):
        answers = iter(['{"paragraphs": [{"text": "cut', '{"paragraphs": [], "gaps": ["none"]}'])
        result = report.run_section(lambda m, s: {"content": next(answers)}, report.SECTIONS[0], self.rows,
                                    lambda layer: {}, [], {})
        self.assertEqual(["none"], result["gaps"])


if __name__ == "__main__":
    unittest.main()

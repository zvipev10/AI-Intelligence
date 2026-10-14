import json
import unittest

from hl import report


class ReportTests(unittest.TestCase):
    def setUp(self):
        self.rows = [
            {"i360_item_id": "sat-1", "source_type": "Satellite", "timestamp_utc": "2026-08-31T07:18:00Z",
             "latitude": "35.0731", "longitude": "36.3053", "i360.insights.post_comment": "Convoy, 3 trucks"},
            {"i360_item_id": "adint-1", "source_type": "ADINT", "timestamp_utc": "2026-08-31T08:00:00Z",
             "i360.ip.ip_sessions.source_ip": "203.0.113.107", "i360.user_agents_data.device_brand": "Apple",
             "observed_record_links": [{"record_id": "ipdr-1", "matched_value": "203.0.113.107",
                                        "record_field": "ip.ip_sessions.source_ip", "linked_record_field": "ip.ip_sessions.source_ip"}]},
            {"i360_item_id": "ipdr-1", "source_type": "IPDR", "timestamp_utc": "2026-09-02T09:10:00Z",
             "i360.ip.ip_sessions.source_ip": "203.0.113.107", "i360.additional_info.ip_source": "10.30.4.117",
             "observed_entity_links": [{"entity_id": "p-1", "matched_value": "353294702931926"}],
             "observed_record_links": [{"record_id": "adint-1", "matched_value": "203.0.113.107"}]},
            {"i360_item_id": "call-1", "source_type": "Cellular Calls", "timestamp_utc": "2026-09-02T14:01:00Z",
             "latitude": "35.07", "longitude": "36.30", "side_b_number": "963940952424",
             "call_transcript_en": "IMEI 353 · 00:02: Hello\n\n963940952424 · 00:05: Open the gates; we have fifteen units of petrol.",
             "observed_entity_links": [{"entity_id": "p-1", "matched_value": "353294702931926"}]},
        ]
        self.labels = {"IPDR": {"i360.ip.ip_sessions.source_ip": "ip_public"}, "ADINT": {"i360.ip.ip_sessions.source_ip": "ip"}}
        self.person = {"entity_id": "p-1", "canonical_name": "Arman Rahimi",
                       "telecom": {"imei": "353294702931926",
                                   "subscriber_identity_derivation": {"claim": {"value": {"msisdn": "963094370078"}}}}}

    def labels_of(self, layer):
        return self.labels.get(layer, {})

    def test_facts_come_from_the_records_and_links(self):
        facts = report.compute_facts("Op Praha", self.rows, [self.person], "p-1", self.labels_of)
        self.assertEqual(4, facts["records_total"])
        self.assertEqual("2026-08-31T07:18:00Z", facts["period"]["first"])
        self.assertIn("Fusion of Satellite, ADINT, IPDR, Cellular Calls", facts["subtitle"])
        chain = [(s["layer"], s["linked"]) for s in facts["chain"]]
        self.assertEqual([("Satellite", None), ("ADINT", False), ("IPDR", True), ("person", True), ("Cellular Calls", True)], chain)
        ipdr = next(layer for layer in facts["layers"] if layer["layer"] == "IPDR")
        self.assertEqual([{"label": "ip_public", "values": ["203.0.113.107"]}], ipdr["fields"])
        calls = next(layer for layer in facts["layers"] if layer["layer"] == "Cellular Calls")
        self.assertEqual("Open the gates; we have fifteen units of petrol.", calls["quotes"][1]["text"])
        table = {row["label"]: row for row in facts["identifiers_table"]}
        self.assertEqual("recommended, not yet approved", table["MSISDN"]["status"])
        self.assertEqual("10.30.4.117", table["Private IP (IPDR)"]["value"])
        self.assertEqual("963940952424 (1)", table["Top B-party contacts"]["value"])
        self.assertEqual("p-1", report.default_subject([{"entity_id": "p-0"}, self.person], self.rows))

    def test_a_layer_block_cites_refs_that_map_back_and_drops_invented_ones(self):
        asked = []

        def complete_json(messages, schema):
            asked.append(messages[1]["content"])
            return {"model": "m", "content": json.dumps({"sentences": [
                {"text": "The call announces fuel (R1).", "refs": ["R1"]},
                {"text": "Made up.", "refs": ["R7"]}], "quote_line": "2"})}

        facts = report.compute_facts("Op Praha", self.rows, [self.person], "p-1", self.labels_of)
        result = report.run_block(complete_json, "layer:Cellular Calls", facts, self.rows, self.labels_of, [self.person], "p-1", {})
        self.assertEqual(["call-1"], result["sentences"][0]["record_ids"])
        self.assertEqual("The call announces fuel.", result["sentences"][0]["text"])
        self.assertTrue(result["sentences"][1]["unsupported"])
        self.assertEqual((1, "2", 1), (result["removed_ids"], result["quote_line"], result["records_used"]))
        self.assertIn("CALL LINES:", asked[0])
        self.assertNotIn("layer=IPDR", asked[0])  # a layer block sees only that layer's records

    def test_assessment_claims_get_levels_and_a_cut_off_answer_is_asked_again(self):
        answers = iter(['{"claims": [{"claim": "cut', json.dumps({"claims": [{"claim": "Subject drives a fuel convoy.", "level": "moderate", "refs": ["R4"]}],
                                                                  "open_questions": ["Who is side B?"]})])
        facts = report.compute_facts("Op Praha", self.rows, [self.person], "p-1", self.labels_of)
        result = report.run_block(lambda m, s: {"content": next(answers)}, "assessment", facts, self.rows, self.labels_of, [self.person], "p-1", {})
        self.assertEqual([("MODERATE", ["call-1"])], [(c["level"], c["record_ids"]) for c in result["claims"]])
        self.assertEqual(["Who is side B?"], result["open_questions"])


if __name__ == "__main__":
    unittest.main()

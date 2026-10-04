import unittest

from link_graph import build_links, derive_subscriber_identity


class LinkGraphTests(unittest.TestCase):
    def setUp(self):
        self.entities = {
            "ENT-PERSON": {"entity_type": "person", "telecom": {"imei": "353294702931926"}},
            "ENT-DEVICE": {"entity_type": "device", "canonical_name": "device-1", "aliases": []},
        }
        self.locations = {"LOC-1": {"name": "Point"}}

    def test_links_remain_field_backed_and_subscriber_identity_is_derived(self):
        events = [
            {"event_id": "REC-1", "source_type": "Cellular Geolocations", "target_imei": "353294702931926", "target_msisdn": "9630943700780", "target_imsi": "417011234567890", "location_id": "LOC-1"},
            {"event_id": "REC-2", "source_type": "Cellular Geolocations", "target_imei": "353294702931926", "target_msisdn": "9630943700780", "target_imsi": "417011234567890"},
        ]
        links = build_links(events, self.entities, self.locations)
        self.assertEqual(2, len([item for item in links if item["rule_id"] == "entity_imei_to_cellular_target_imei_v1"]))
        self.assertFalse(any(item["to"]["field"] in {"telecom.imsi", "telecom.msisdn"} for item in links))
        derivation = derive_subscriber_identity(events, links, "ENT-PERSON")
        self.assertEqual("candidate", derivation["status"])
        self.assertEqual("9630943700780", derivation["claim"]["value"]["msisdn"])

    def test_tied_or_singleton_pairs_do_not_create_a_claim(self):
        singleton = [{"event_id": "REC-1", "target_imei": "353294702931926", "target_msisdn": "1", "target_imsi": "2"}]
        self.assertIsNone(derive_subscriber_identity(singleton, build_links(singleton, self.entities, self.locations), "ENT-PERSON"))
        tie = singleton + [{"event_id": "REC-2", "target_imei": "353294702931926", "target_msisdn": "3", "target_imsi": "4"}]
        self.assertIsNone(derive_subscriber_identity(tie, build_links(tie, self.entities, self.locations), "ENT-PERSON"))

    def test_blank_side_b_never_creates_a_person_link(self):
        events = [{"event_id": "REC-CALL", "source_type": "Cellular Calls", "side_a_imei": "353294702931926", "side_b_imei": ""}]
        links = build_links(events, self.entities, self.locations)
        self.assertEqual(["entity_imei_to_call_party_v1"], [item["rule_id"] for item in links])

    def test_adint_ip_links_only_to_a_containing_ipdr_target_session(self):
        events = [
            {"event_id": "REC-ADINT", "source_type": "ADINT", "ip": "203.0.113.91", "timestamp_utc": "2026-09-04T10:00:00Z"},
            {"event_id": "REC-IPDR-MATCH", "source_type": "IPDR", "ip_target": "203.0.113.91", "session_start_utc": "2026-09-04T09:59:00Z", "session_end_utc": "2026-09-04T10:01:00Z"},
            {"event_id": "REC-IPDR-OUTSIDE", "source_type": "IPDR", "ip_target": "203.0.113.91", "session_start_utc": "2026-09-04T10:02:00Z", "session_end_utc": "2026-09-04T10:03:00Z"},
            {"event_id": "REC-IPDR-REVERSED", "source_type": "IPDR", "ip_target": "203.0.113.91", "session_start_utc": "2026-09-04T10:01:00Z", "session_end_utc": "2026-09-04T09:59:00Z"},
            {"event_id": "REC-IPDR-UNDOCUMENTED", "source_type": "IPDR", "ip_out": "203.0.113.91", "session_start_utc": "2026-09-04T09:59:00Z", "session_end_utc": "2026-09-04T10:01:00Z"},
        ]
        links = [item for item in build_links(events, self.entities, self.locations) if item["rule_id"] == "adint_ip_to_ipdr_target_ip_temporal_v1"]
        self.assertEqual(1, len(links))
        self.assertEqual("REC-ADINT", links[0]["from"]["object_id"])
        self.assertEqual("REC-IPDR-MATCH", links[0]["to"]["object_id"])
        self.assertEqual(["REC-ADINT", "REC-IPDR-MATCH"], links[0]["provenance_record_ids"])


if __name__ == "__main__":
    unittest.main()

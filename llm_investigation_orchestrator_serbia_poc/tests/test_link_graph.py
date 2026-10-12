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

    def test_i360_records_carry_i360_links_only(self):
        # On i360 the links are the record's related_objects; the shared IMEI only says what matched.
        import json
        events = [
            {"event_id": "IPDR-1", "source_type": "IPDR", "imei": "353294702931926",
             "i360_links": json.dumps([{"id": "ENT-PERSON", "type": "PERSON_OF_INTEREST"}, {"id": "INV-1", "type": "INTELLIGENCE_INVESTIGATION"}]),
             "i360_identifiers": json.dumps([["asset_identifier", "353294702931926"]])},
            {"event_id": "CALL-1", "source_type": "Cellular Calls", "side_a_imei": "353294702931926",
             "i360_links": json.dumps([{"id": "ENT-PERSON"}]), "i360_identifiers": "[]"},
            {"event_id": "LOC-1", "source_type": "Cellular Geolocations", "target_imei": "353294702931926",
             "i360_links": "[]", "i360_identifiers": "[]"},  # same IMEI, not linked in i360: no link
            {"event_id": "IPDR-2", "source_type": "IPDR", "i360_links": json.dumps([{"id": "ENT-PERSON"}]), "i360_identifiers": "[]"},
        ]
        links = build_links(events, self.entities, self.locations)
        got = {(l["from"]["object_id"], l["from"]["field"], l["matched_value"]) for l in links}
        self.assertEqual({("IPDR-1", "asset_identifier", "353294702931926"), ("CALL-1", "side_a_imei", "353294702931926"),
                          ("IPDR-2", "related_objects", "")}, got)
        self.assertEqual({"i360_related_object_v1"}, {l["rule_id"] for l in links})

    def test_i360_item_links_join_two_records_on_their_value(self):
        import json
        from analysis import apply_graph_entity_links
        events = [
            {"event_id": "IPDR-1", "source_type": "IPDR", "i360.ip.ip_sessions.destination_ip": "203.0.113.107",
             "i360_links": json.dumps([{"id": "ADINT-1", "type": "ITEM", "source": "automatic", "values": ["203.0.113.107"]}]),
             "i360_identifiers": "[]"},
            {"event_id": "ADINT-1", "source_type": "ADINT", "i360.ip.ip_sessions.source_ip": "203.0.113.107",
             "i360_links": json.dumps([{"id": "IPDR-1", "type": "ITEM", "source": "automatic", "values": ["203.0.113.107"]}]),
             "i360_identifiers": "[]"},
        ]
        links = build_links(events, self.entities, self.locations)
        self.assertEqual(1, len(links))  # both records carry the link; it is made once
        self.assertEqual(("i360_related_item_v1", "203.0.113.107"), (links[0]["rule_id"], links[0]["matched_value"]))
        apply_graph_entity_links(events, self.entities, self.locations)
        ipdr = events[0]["observed_record_links"][0]
        self.assertEqual(("ADINT-1", "ip.ip_sessions.destination_ip", "ip.ip_sessions.source_ip"),
                         (ipdr["record_id"], ipdr["record_field"], ipdr["linked_record_field"]))
        self.assertEqual("IPDR-1", events[1]["observed_record_links"][0]["record_id"])

    def test_tied_or_singleton_pairs_do_not_create_a_claim(self):
        singleton = [{"event_id": "REC-1", "target_imei": "353294702931926", "target_msisdn": "1", "target_imsi": "2"}]
        self.assertIsNone(derive_subscriber_identity(singleton, build_links(singleton, self.entities, self.locations), "ENT-PERSON"))
        tie = singleton + [{"event_id": "REC-2", "target_imei": "353294702931926", "target_msisdn": "3", "target_imsi": "4"}]
        self.assertIsNone(derive_subscriber_identity(tie, build_links(tie, self.entities, self.locations), "ENT-PERSON"))

    def test_blank_side_b_never_creates_a_person_link(self):
        events = [{"event_id": "REC-CALL", "source_type": "Cellular Calls", "side_a_imei": "353294702931926", "side_b_imei": ""}]
        links = build_links(events, self.entities, self.locations)
        self.assertEqual(["entity_imei_to_call_party_v1"], [item["rule_id"] for item in links])

    def test_adint_ip_links_match_ipdr_public_ip_without_a_time_constraint(self):
        events = [
            {"event_id": "REC-ADINT", "source_type": "ADINT", "ip": "203.0.113.91", "timestamp_utc": "2026-09-04T10:00:00Z"},
            {"event_id": "REC-IPDR-MATCH", "source_type": "IPDR", "ip_public": "203.0.113.91", "session_start_utc": "2026-09-04T09:59:00Z", "session_end_utc": "2026-09-04T10:01:00Z"},
            {"event_id": "REC-IPDR-OUTSIDE", "source_type": "IPDR", "ip_public": "203.0.113.91", "session_start_utc": "2026-09-04T10:02:00Z", "session_end_utc": "2026-09-04T10:03:00Z"},
            {"event_id": "REC-IPDR-REVERSED", "source_type": "IPDR", "ip_public": "203.0.113.91", "session_start_utc": "2026-09-04T10:01:00Z", "session_end_utc": "2026-09-04T09:59:00Z"},
            {"event_id": "REC-IPDR-TARGET", "source_type": "IPDR", "ip_target": "203.0.113.91", "session_start_utc": "2026-09-04T09:59:00Z", "session_end_utc": "2026-09-04T10:01:00Z"},
        ]
        links = [item for item in build_links(events, self.entities, self.locations) if item["rule_id"] == "adint_ip_to_ipdr_public_ip_v1"]
        self.assertEqual({"REC-IPDR-MATCH", "REC-IPDR-OUTSIDE", "REC-IPDR-REVERSED"}, {item["to"]["object_id"] for item in links})
        self.assertTrue(all(item["from"]["object_id"] == "REC-ADINT" for item in links))
        self.assertTrue(all(item["provenance_record_ids"] == sorted(["REC-ADINT", item["to"]["object_id"]]) for item in links))


if __name__ == "__main__":
    unittest.main()

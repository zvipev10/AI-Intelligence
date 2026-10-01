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


if __name__ == "__main__":
    unittest.main()

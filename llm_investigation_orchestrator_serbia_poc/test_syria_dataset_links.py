"""Regression coverage for links projected from the active Syria dataset."""

import unittest

import server
from demo_runtime import load_profile


class SyriaDatasetLinksTests(unittest.TestCase):
    def test_replacement_dataset_projects_raw_and_entity_links(self):
        profile = load_profile(server.ROOT, "syria", verify=True)
        self.assertEqual(profile["dataset_version"], "cellular-records-v12")
        events = server.load_ui_events("en")

        raw_links = [
            (event["event_id"], link["record_id"], link["matched_value"])
            for event in events for link in event.get("observed_record_links") or []
            if link.get("rule_id") == "adint_ip_to_ipdr_target_ip_temporal_v1"
        ]
        self.assertEqual(set(raw_links), {
            ("REC-SYR-ADINT-OBS-04-006", "REC-SYR-IPDR-24735884207980800", "203.0.113.91"),
            ("REC-SYR-IPDR-24735884207980800", "REC-SYR-ADINT-OBS-04-006", "203.0.113.91"),
            ("REC-SYR-ADINT-OBS-11-006", "REC-SYR-IPDR-25229854643096800", "203.0.113.20"),
            ("REC-SYR-IPDR-25229854643096800", "REC-SYR-ADINT-OBS-11-006", "203.0.113.20"),
        })

        ipdr_entity_links = {
            event["event_id"]
            for event in events if event.get("source_type") == "IPDR"
            if any(link.get("rule_id") == "entity_imei_to_ipdr_imei_v1" for link in event.get("observed_entity_links") or [])
        }
        self.assertEqual(ipdr_entity_links, {
            "REC-SYR-IPDR-1683930569233410",
            "REC-SYR-IPDR-1848587380938750",
            "REC-SYR-IPDR-3001185062876120",
            "REC-SYR-IPDR-3495155497992130",
        })


if __name__ == "__main__":
    unittest.main()

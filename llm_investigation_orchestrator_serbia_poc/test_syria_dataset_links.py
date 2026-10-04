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
            if link.get("rule_id") == "adint_ip_to_ipdr_target_ip_v1"
        ]
        self.assertEqual(len(raw_links), 660)
        self.assertTrue(all(link[2] for link in raw_links))
        self.assertEqual({record_id for source_id, record_id, ip in raw_links if source_id == "REC-SYR-ADINT-OBS-01-003"}, {
            "REC-SYR-IPDR-349608730945890",
            "REC-SYR-IPDR-565467576585657",
            "REC-SYR-IPDR-1025303322412050",
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

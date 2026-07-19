import unittest

from fusion_tools import find_duplicate_candidates, prepare_candidate, reconcile_quantity


def event(record_id, summary, *, mission="", count="3", source="X"):
    return {
        "event_id": record_id, "timestamp_utc": "2026-01-01T00:00:00Z", "source_type": source,
        "collection_family": "airborne_isr_video_exploitation" if mission else "public_source",
        "observation_id": "", "mission_id": mission, "event_summary": summary,
        "object_class": "vehicle", "estimated_object_count": count, "entity_id": "ENT-1", "location_id": "LOC-1",
    }


class FusionToolsTests(unittest.TestCase):
    def test_same_uav_mission_is_one_group(self):
        result = prepare_candidate([event("A", "first", mission="M-1"), event("B", "different", mission="M-1")], "high")
        self.assertEqual(result["independent_source_group_count"], 1)
        self.assertFalse(result["persistence_eligible"])

    def test_separate_uav_missions_are_independent(self):
        result = prepare_candidate([event("A", "first", mission="M-1"), event("B", "different", mission="M-2")], "medium")
        self.assertTrue(result["persistence_eligible"])

    def test_visible_reposts_collapse(self):
        first = event("A", "Armored vehicle reported near the northern crossing by local observers")
        second = event("B", "Local observers reported an armored vehicle near the northern crossing", source="Telegram")
        result = prepare_candidate([first, second], "high")
        self.assertEqual(result["independent_source_group_count"], 1)

    def test_distinct_reports_are_independent(self):
        result = prepare_candidate([event("A", "vehicle seen at checkpoint"), event("B", "aerial image confirms convoy")], "medium")
        self.assertTrue(result["persistence_eligible"])

    def test_low_confidence_is_report_only(self):
        result = prepare_candidate([event("A", "one"), event("B", "two")], "low")
        self.assertFalse(result["persistence_eligible"])
        self.assertIn("report only", result["persistence_block_reasons"][0])

    def test_quantity_shapes(self):
        self.assertEqual(reconcile_quantity([event("A", "one", count="")])["count_assessment"], "unresolved")
        self.assertEqual(reconcile_quantity([event("A", "one")])["count_assessment"], "approximate")
        self.assertEqual(reconcile_quantity([event("A", "one"), event("B", "two")])["count_assessment"], "exact")
        result = reconcile_quantity([event("A", "one", count="2"), event("B", "two", count="6")])
        self.assertEqual((result["count_min"], result["count_max"], result["count_estimate"], result["count_assessment"]), (2, 6, 4, "range"))

    def test_duplicate_lookup(self):
        candidate = {"target_id": "T-1", "object_class": "vehicle", "location_id": "LOC-1", "entity_id": "ENT-1", "evidence": [{"record_id": "A"}]}
        result = find_duplicate_candidates([candidate], ["A", "B"], object_class="vehicle", location_id="LOC-1", entity_id="ENT-1")
        self.assertTrue(result["duplicate_found"])
        self.assertEqual(result["matches"][0]["match_type"], "same-evidence")


if __name__ == "__main__":
    unittest.main()

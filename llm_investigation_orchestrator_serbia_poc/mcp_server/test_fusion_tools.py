import unittest

from fusion_tools import discover_corroborating_evidence, find_duplicate_candidates, prepare_candidate, reconcile_quantity


def event(record_id, summary, *, mission="", count="3", source="X"):
    return {
        "event_id": record_id, "timestamp_utc": "2026-01-01T00:00:00Z", "source_type": source,
        "collection_family": "airborne_isr_video_exploitation" if mission else "public_source",
        "observation_id": "", "mission_id": mission, "event_summary": summary,
        "object_class": "vehicle", "estimated_object_count": count, "entity_id": "ENT-1", "location_id": "LOC-1",
    }


class FusionToolsTests(unittest.TestCase):
    def test_discovers_and_ranks_independent_corroboration(self):
        anchor = event("A", "UAV observation", mission="M-1", count="4", source="UAV")
        anchor["collection_family"] = "airborne_isr_video_exploitation"
        anchor["object_class"] = "משאית לוגיסטית"
        anchor["timestamp_utc"] = "2026-01-01T10:00:00Z"
        first = event("B", "תושבים דיווחו על משאית אספקה; נראו כ-4 פריטים", source="חדשות")
        second = event("C", "תיעוד מציג רכב תובלה לוגיסטי ובין 2 ל-6 פריטים", source="טלגרם")
        distractor = event("D", "דיווח על משאית אספקה אך אין סימן המקשר לאותו כוח", source="X")
        for item, hour in ((first, 11), (second, 12), (distractor, 10)):
            item["timestamp_utc"] = f"2026-01-01T{hour:02d}:00:00Z"
            item["collection_family"] = "public_source"
            item["object_class"] = ""
        result = discover_corroborating_evidence([anchor], [first, second, distractor])
        self.assertEqual(result["selected_event_ids"], ["A", "B", "C"])
        self.assertFalse(result["ambiguous"])
        self.assertNotIn("D", [item["record_id"] for item in result["retrieved"]])

    def test_rejects_pair_that_does_not_clearly_beat_competing_anchor(self):
        anchor = event("A", "UAV observation", mission="M-1", count="4", source="UAV")
        competitor = event("Z", "Other UAV observation", mission="M-2", count="4", source="UAV")
        for item, minute in ((anchor, 0), (competitor, 5)):
            item.update({
                "collection_family": "airborne_isr_video_exploitation", "object_class": "משאית לוגיסטית",
                "timestamp_utc": f"2026-01-01T10:{minute:02d}:00Z",
            })
        first = event("B", "משאית אספקה; נראו כ-4 פריטים", source="חדשות")
        second = event("C", "רכב תובלה לוגיסטי ובין 2 ל-6 פריטים", source="טלגרם")
        for item, minute in ((first, 6), (second, 7)):
            item.update({"collection_family": "public_source", "object_class": "", "timestamp_utc": f"2026-01-01T10:{minute:02d}:00Z"})
        result = discover_corroborating_evidence([anchor], [anchor, competitor, first, second])
        self.assertEqual(result["selected_event_ids"], ["A"])

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

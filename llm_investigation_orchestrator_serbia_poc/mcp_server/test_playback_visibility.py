import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import server


class PlaybackVisibilityTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = tempfile.TemporaryDirectory()
        self.policy_path = Path(self.temp_root.name) / "active_visibility.json"
        self.patch = patch.object(server, "PLAYBACK_VISIBILITY_PATH", self.policy_path)
        self.patch.start()
        self.events = server.EVENTS
        self.assertGreaterEqual(len(self.events), 3)

    def tearDown(self):
        self.patch.stop()
        self.temp_root.cleanup()

    def write_policy(self, start, end, layers=None, dataset=None, active=True):
        self.policy_path.write_text(json.dumps({
            "schema_version": 1,
            "active": active,
            "run_id": "run_test",
            "scenario_id": "scenario-test",
            "scenario_version": 1,
            "dataset": dataset or server.DATASET_VERSION,
            "layers": layers or [],
            "visible_timeframe": {
                "from": start.isoformat().replace("+00:00", "Z"),
                "to": end.isoformat().replace("+00:00", "Z"),
                "from_inclusive": True,
                "to_exclusive": True,
            },
            "revision": 1,
        }), encoding="utf-8")

    def test_inactive_playback_preserves_full_event_access(self):
        event = self.events[-1]
        self.assertEqual(event, server.visible_event(event["event_id"]))
        self.write_policy(self.events[0]["timestamp"], self.events[1]["timestamp"], active=False)
        self.assertEqual(event, server.visible_event(event["event_id"]))

    def test_timeframe_is_inclusive_at_start_and_exclusive_at_end(self):
        first, second = self.events[0], self.events[1]
        self.write_policy(first["timestamp"], second["timestamp"])
        self.assertIsNotNone(server.visible_event(first["event_id"]))
        self.assertIsNone(server.visible_event(second["event_id"]))
        result = server.search_events({"event_ids": [first["event_id"], second["event_id"]]})
        self.assertEqual([first["event_id"]], result["event_ids"])

    def test_layer_scope_filters_sources(self):
        first = self.events[0]
        same_time_or_later = next(
            event for event in self.events[1:] if event["source_type"] != first["source_type"]
        )
        self.write_policy(
            self.events[0]["timestamp"],
            self.events[-1]["timestamp"].replace(year=self.events[-1]["timestamp"].year + 1),
            [f"events:{first['source_type']}"],
        )
        self.assertIsNotNone(server.visible_event(first["event_id"]))
        self.assertIsNone(server.visible_event(same_time_or_later["event_id"]))

    def test_direct_object_aggregate_and_presentation_cannot_leak_future_event(self):
        first, future = self.events[0], self.events[-1]
        self.write_policy(first["timestamp"], self.events[1]["timestamp"])
        objects = server.get_objects({
            "object_type": "event",
            "event_ids": [first["event_id"], future["event_id"]],
        })
        self.assertEqual([first["event_id"]], [item["event_id"] for item in objects["events"]])
        self.assertIn(future["event_id"], objects["missing_event_ids"])
        aggregate = server.aggregate_events({"group_by": "date"})
        self.assertEqual(1, aggregate["total_events"])
        with self.assertRaisesRegex(ValueError, "unknown event IDs"):
            server.present_requested_results({"layers": [{
                "kind": "events",
                "ids": [future["event_id"]],
                "label": "Future",
                "view": "timeline",
            }]})

    def test_related_sequence_linkage_and_fusion_reject_future_events(self):
        first, future = self.events[0], self.events[-1]
        self.write_policy(first["timestamp"], self.events[1]["timestamp"])
        sequence = server.build_event_sequence({"event_ids": [first["event_id"], future["event_id"]]})
        self.assertEqual([first["event_id"]], sequence["ordered_event_ids"])
        linkage = server.explain_linkage({
            "first_event_id": first["event_id"],
            "second_event_id": future["event_id"],
        })
        self.assertIn(future["event_id"], linkage["missing_event_ids"])
        with self.assertRaisesRegex(ValueError, "unknown event_id"):
            server.prepare_target_candidate({
                "event_ids": [future["event_id"]],
                "discover_corroboration": False,
            })

    def test_semantic_candidates_are_post_filtered(self):
        first, future = self.events[0], self.events[-1]
        self.write_policy(first["timestamp"], self.events[1]["timestamp"])
        fake = [
            {"event_id": future["event_id"], "semantic_score": 0.99},
            {"event_id": first["event_id"], "semantic_score": 0.80},
        ]
        with patch.object(server, "get_semantic_index") as index:
            index.return_value.search.return_value = fake
            result = server.semantic_candidates("query", {}, 10)
        self.assertEqual([first["event_id"]], [item["event_id"] for item in result])

    def test_invalid_or_mismatched_policy_fails_closed(self):
        self.policy_path.write_text("{", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unreadable"):
            server.search_events({})
        self.write_policy(
            self.events[0]["timestamp"], self.events[1]["timestamp"], dataset="other"
        )
        with self.assertRaisesRegex(ValueError, "does not match"):
            server.search_events({})

    def test_stored_target_bank_is_hidden_during_playback(self):
        self.write_policy(self.events[0]["timestamp"], self.events[1]["timestamp"])
        with self.assertRaisesRegex(ValueError, "unavailable"):
            server.search_target_candidates({})


if __name__ == "__main__":
    unittest.main()

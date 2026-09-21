import csv
import wave
import unittest
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EVENTS = ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_events_projection_v2_1.csv"
AUDIO_ROOT = ROOT / "assets" / "audio" / "cellular_calls"


class CellularCallDatasetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with EVENTS.open(encoding="utf-8-sig", newline="") as handle:
            cls.events = list(csv.DictReader(handle))
        cls.calls = [row for row in cls.events if row.get("source_type") == "שיחות סלולר"]

    def test_layer_contains_twenty_four_calls(self):
        self.assertEqual(len(self.calls), 24)
        self.assertEqual(len({row["call_id"] for row in self.calls}), 24)
        self.assertEqual(len({row["event_id"] for row in self.calls}), 24)

    def test_calls_are_attributed_to_unidentified_actors(self):
        self.assertEqual({row["entity_id"] for row in self.calls}, {"ENT-UNIDENTIFIED-ACTORS"})

    def test_repeated_side_a_crosses_the_three_scenario_locations(self):
        linked = [row for row in self.calls if row["side_a_imei"] == "356789104321567"]
        self.assertEqual(len(linked), 9)
        self.assertEqual({row["side_a_number"] for row in linked}, {"+38349555001"})
        self.assertEqual(Counter(row["side_a_location_id"] for row in linked), {
            "LOC-V2-013": 3,
            "LOC-V2-009": 3,
            "LOC-V2-010": 3,
        })

    def test_other_party_is_distinct_and_elsewhere(self):
        self.assertTrue(all(row["side_a_imei"] != row["side_b_imei"] for row in self.calls))
        self.assertTrue(all(row["side_a_number"] != row["side_b_number"] for row in self.calls))
        self.assertTrue(all(row["side_a_location_id"] != row["side_b_location_id"] for row in self.calls))
        linked = [row for row in self.calls if row["side_a_imei"] == "356789104321567"]
        self.assertEqual(len({row["side_b_imei"] for row in linked}), 9)
        self.assertEqual(len({row["side_b_number"] for row in linked}), 9)

    def test_every_call_has_valid_simulated_audio(self):
        for row in self.calls:
            path = ROOT / row["audio_url"].removeprefix("./")
            self.assertTrue(path.is_file(), row["call_id"])
            with wave.open(str(path), "rb") as recording:
                self.assertEqual(recording.getnchannels(), 1)
                self.assertEqual(recording.getframerate(), 8_000)
                self.assertGreater(recording.getnframes(), 0)
            self.assertEqual(row["synthetic_media"], "true")
            self.assertTrue(row["call_transcript"])
            self.assertTrue(row["call_transcript_en"])

    def test_english_source_name_is_defined(self):
        translations = (ROOT / "generate_english_projection.py").read_text(encoding="utf-8")
        self.assertIn('"שיחות סלולר": "Cellular Calls"', translations)

    def test_public_tool_contract_exposes_call_fields(self):
        server_source = (ROOT / "mcp_server" / "server.py").read_text(encoding="utf-8")
        for field in (
            "call_id", "call_started_at_utc", "call_duration_seconds",
            "side_a_imei", "side_a_number", "side_a_location_id",
            "side_b_imei", "side_b_number", "side_b_location_id", "audio_url",
        ):
            self.assertIn(f'"{field}": event.get("{field}", "")', server_source)

    def test_map_presents_both_call_endpoints_and_shared_record(self):
        app_source = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn('function addCellularCallMapPresentation(event, layer, index, bounds)', app_source)
        self.assertIn('geometry: { type: "LineString"', app_source)
        self.assertIn('[["a", sideA], ["b", sideB]]', app_source)
        self.assertIn('element.dataset.viewerKind = "record"', app_source)
        self.assertIn('element.dataset.viewerId = recordId', app_source)
        self.assertIn('openObjectViewer("record", recordId', app_source)
        self.assertIn('addCellularCallMapPresentation(event, layer, index, bounds)', app_source)

    def test_raw_table_exposes_both_endpoint_location_ids(self):
        app_source = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn('activeLocaleText("מיקום צד א׳", "Side A location")', app_source)
        self.assertIn('activeLocaleText("מיקום צד ב׳", "Side B location")', app_source)
        self.assertIn('event.side_a_location_id || "-"', app_source)
        self.assertIn('event.side_b_location_id || "-"', app_source)


if __name__ == "__main__":
    unittest.main()

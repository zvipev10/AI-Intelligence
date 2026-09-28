import csv
import unittest
from datetime import datetime, timezone
from pathlib import Path

import scenario_playback
from demo_runtime import load_profile


ROOT = Path(__file__).resolve().parent


def utc(value):
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)


class SyriaPlaybackManifestTests(unittest.TestCase):
    def setUp(self):
        self.profile = load_profile(ROOT, "syria", verify=True)
        self.manifest = scenario_playback.get_manifest(
            ROOT / "scenario_manifests", "syria-collection-flow", 1
        )
        with (ROOT / self.profile["files"]["events"]).open(encoding="utf-8-sig", newline="") as handle:
            self.events = list(csv.DictReader(handle))

    def test_syria_enables_the_existing_playback_engine(self):
        self.assertTrue(self.profile["features"]["playback"])
        self.assertEqual("cellular-records-v5", self.manifest["scope"]["dataset"])

    def test_manifest_splits_the_existing_source_timeline_into_demo_returns(self):
        self.assertEqual(
            ["satellite-lead", "sigint-data-return", "cellular-call-return", "cctv-return"],
            [stage["id"] for stage in self.manifest["stages"]],
        )
        cumulative_counts = []
        for stage_index in range(len(self.manifest["stages"])):
            timeframe = scenario_playback.visible_timeframe(self.manifest, stage_index)
            start, end = utc(timeframe["from"]), utc(timeframe["to"])
            cumulative_counts.append(sum(
                start <= utc(row["timestamp_utc"]) < end
                for row in self.events
            ))
        self.assertEqual([2, 722, 723, 725], cumulative_counts)


if __name__ == "__main__":
    unittest.main()

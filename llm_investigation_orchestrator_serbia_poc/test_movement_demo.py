import csv
import unittest
from pathlib import Path

from evidence_catalog import build_catalog


ROOT = Path(__file__).resolve().parent
EVENTS = ROOT / "data" / "serbian_intelligence_v2_1" / "serbia_kosovo_events_projection_v2_1.csv"
SCENARIO_RECORDS = {
    "LOC-V2-013": {"REC-V2-014801", "REC-V2-014802", "REC-V2-014803"},
    "LOC-V2-009": {"REC-V2-014804", "REC-V2-014805", "REC-V2-014806"},
    "LOC-V2-010": {"REC-V2-014807", "REC-V2-014808", "REC-V2-014809"},
}


class MovementDemoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with EVENTS.open(encoding="utf-8-sig", newline="") as handle:
            cls.events = list(csv.DictReader(handle))
        cls.by_id = {row["event_id"]: row for row in cls.events}

    def test_scenario_is_a_time_ordered_force_pattern(self):
        uav_ids = ["REC-V2-014801", "REC-V2-014804", "REC-V2-014807"]
        rows = [self.by_id[record_id] for record_id in uav_ids]
        self.assertEqual([row["location_id"] for row in rows], ["LOC-V2-013", "LOC-V2-009", "LOC-V2-010"])
        self.assertEqual([row["timestamp_utc"] for row in rows], sorted(row["timestamp_utc"] for row in rows))
        self.assertEqual({row["entity_id"] for row in rows}, {"ENT-KSF"})
        self.assertEqual({row["object_class"] for row in rows}, {"שיירת כלי רכב"})
        self.assertTrue(all(row["movement_status"] == "בתנועה" for row in rows))

    def test_each_route_point_has_fused_evidence(self):
        catalog = build_catalog(self.events, dataset_version="v2.1")
        fused = [row for row in catalog["rows"] if row["evidence_status"] == "fused"]
        for location_id, required_ids in SCENARIO_RECORDS.items():
            candidates = [
                row for row in fused
                if row["location_ids"] == [location_id]
                and row["subject_entity_ids"] == ["ENT-KSF"]
                and row["object_class"] == "שיירת כלי רכב"
            ]
            self.assertTrue(
                any(required_ids.issubset(set(row["source_record_ids"])) for row in candidates),
                f"missing fused scenario evidence for {location_id}",
            )


if __name__ == "__main__":
    unittest.main()

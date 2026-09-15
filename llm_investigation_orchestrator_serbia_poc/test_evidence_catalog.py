import unittest

from evidence_catalog import build_catalog


def event(record_id, hour, mission, *, source="uav", object_class="מסוק", summary="זוהה מסוק"):
    return {
        "event_id": record_id,
        "timestamp_utc": f"2026-09-14T{hour}:00:00Z",
        "source_type": source,
        "source_reliability_label": "confirmed",
        "certainty_level": "גבוהה",
        "entity_id": "ENT-KFOR",
        "location_id": "LOC-V2-010",
        "event_summary": summary,
        "collection_family": "airborne_isr_video_exploitation" if mission else "public_source",
        "mission_id": mission,
        "object_class": object_class,
        "estimated_object_count": "2",
        "identification_confidence": "גבוהה",
    }


class EvidenceCatalogTests(unittest.TestCase):
    def test_projects_every_record_and_fuses_independent_groups(self):
        rows = [event("REC-1", "01", "UAV-1"), event("REC-2", "02", "UAV-2")]
        catalog = build_catalog(rows, dataset_version="v2.1")
        self.assertEqual(catalog["counts"]["projected"], 2)
        self.assertEqual(catalog["counts"]["fused"], 1)
        fused = next(row for row in catalog["rows"] if row["evidence_status"] == "fused")
        self.assertEqual(fused["source_record_ids"], ["REC-1", "REC-2"])

    def test_different_time_buckets_are_not_fused(self):
        rows = [event("REC-1", "01", "UAV-1"), event("REC-2", "08", "UAV-2")]
        self.assertEqual(build_catalog(rows, dataset_version="v2.1")["counts"]["fused"], 0)

    def test_unstructured_public_report_remains_reported(self):
        rows = [
            event("REC-1", "01", "UAV-1"),
            event("REC-2", "02", "", source="public", object_class="", summary="דיווח כללי על פעילות באזור"),
        ]
        catalog = build_catalog(rows, dataset_version="v2.1")
        self.assertEqual(catalog["counts"]["fused"], 0)
        self.assertEqual(catalog["counts"]["projected"], 2)
        self.assertEqual([row["evidence_status"] for row in catalog["rows"]], ["observed"])

    def test_build_is_reproducible(self):
        rows = [event("REC-1", "01", "UAV-1"), event("REC-2", "02", "UAV-2")]
        first = build_catalog(rows, dataset_version="v2.1")
        second = build_catalog(list(reversed(rows)), dataset_version="v2.1")
        self.assertEqual(first["source_fingerprint"], second["source_fingerprint"])
        self.assertEqual({row["evidence_id"] for row in first["rows"]}, {row["evidence_id"] for row in second["rows"]})


if __name__ == "__main__":
    unittest.main()

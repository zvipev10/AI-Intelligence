import json
import unittest
from pathlib import Path

import analysis
from analysis import Dataset
from hl.items import ItemReader
from hl.mapping import load_mapping

ROOT = Path(__file__).resolve().parent.parent
PROFILE = json.loads((ROOT / "demo_profiles" / "lambda.json").read_text(encoding="utf-8"))
LOCAL = json.loads((ROOT / PROFILE["local_items"]).read_text(encoding="utf-8"))
# The area of the real ADINT data around and west of Masyaf, where the local records are.
AREA = [[36.250, 35.022], [36.365, 35.022], [36.372, 35.070], [36.365, 35.124], [36.250, 35.124], [36.245, 35.070], [36.286, 35.060]]


def local_rows():
    reader = ItemReader(None, load_mapping(str(ROOT / "mapping" / "default.json")), PROFILE["items_query"], 1000)
    mapping = reader.mapping
    return [ItemReader._with_layer(mapping.item_to_row(item, "en"), item) for item in reader.local_items(LOCAL)]


def i360_row(event_id, layer, when, lat, lon):
    return {"event_id": event_id, "record_id": event_id, "source_type": layer, "timestamp_utc": when,
            "latitude": str(lat), "longitude": str(lon)}


class LocalDataTests(unittest.TestCase):
    def test_the_local_records_are_seven_adint_nine_cellular_and_four_satellite(self):
        counts = {layer: len(items) for layer, items in LOCAL["layers"].items()}
        self.assertEqual({"ADINT": 7, "Cellular Locations": 9, "Satellite": 4}, counts)

    def test_each_local_record_has_its_layer_fields(self):
        rows = local_rows()
        core = {"ADINT": ["timestamp_utc", "latitude", "observation_id", "ip", "brand", "model", "os", "device_id", "accuracy_m"],
                "Cellular Locations": ["EVENT TIME", "SESSION TYPE", "DIRECTION", "TARGET MSISDN", "TARGET IMEI", "OP MSISDN", "LATITUDE"],
                "Satellite": ["acquisition_datetime_utc", "sensor_platform", "center_lat", "gsd_m", "footprint_radius_km", "cloud_cover_pct"]}
        for spec in PROFILE["items_query"]["queries"]:
            paths = {name: path for path, name in spec["labels"].items()}
            for row in (r for r in rows if r["source_type"] == spec["layer"]):
                missing = [name for name in core.get(spec["layer"], []) if not row.get(f"i360.{paths[name]}")]
                self.assertEqual([], missing, f"{spec['layer']} {row['event_id']}")

    def test_local_records_are_older_than_every_i360_record_and_marked_local(self):
        rows = local_rows()
        self.assertTrue(all(row["record_origin"] == "local" for row in rows))
        self.assertTrue(all("2026-03-01" <= row["timestamp_utc"] < "2026-06-01" for row in rows))

    def test_every_local_record_lies_inside_the_area_at_its_own_place(self):
        rows = local_rows()
        points = {(row["latitude"], row["longitude"]) for row in rows}
        self.assertEqual(len(rows), len(points))
        self.assertTrue(all(analysis.point_in_polygon(float(r["longitude"]), float(r["latitude"]), AREA) for r in rows))

    def test_satellite_images_exist(self):
        for item in LOCAL["layers"]["Satellite"]:
            self.assertTrue((ROOT / "demo_data" / "area-search" / item["media"]["primary_file_name"]).is_file())
            self.assertIn("car", [t["value"] for t in item["tags"] if t["type"] == "object_recognition"])


class AreaSearchTests(unittest.TestCase):
    def dataset(self):
        rows = local_rows() + [
            i360_row("i360-inside", "ADINT", "2026-09-01T09:00:00Z", 35.08, 36.29),
            i360_row("i360-outside", "ADINT", "2026-04-01T09:00:00Z", 34.50, 36.00),
        ]
        return Dataset(rows, {}, {}, {}, "en")

    def test_the_default_window_finds_only_the_local_records(self):
        window = PROFILE["area_search"]
        found = analysis.area_search(self.dataset(), AREA, window["start_time"], window["end_time"])
        self.assertEqual({"events:ADINT": 7, "events:Cellular Locations": 9, "events:Satellite": 4},
                         {layer["layer_id"]: layer["count"] for layer in found})
        self.assertNotIn("i360-inside", [i for layer in found for i in layer["event_ids"]])

    def test_a_wider_window_brings_the_i360_records_in_the_area(self):
        found = analysis.area_search(self.dataset(), AREA, "2026-01-01T00:00:00Z", "2026-12-31T23:59:59Z")
        ids = [i for layer in found for i in layer["event_ids"]]
        self.assertIn("i360-inside", ids)
        self.assertNotIn("i360-outside", ids)

    def test_the_found_ids_open_through_the_layer_filters(self):
        data = self.dataset()
        layer = next(l for l in analysis.area_search(data, AREA, "2026-03-01T00:00:00Z") if l["layer_id"] == "events:Satellite")
        _, rows = analysis.layer_rows(data, layer["layer_id"], {"event_ids": layer["event_ids"]})
        self.assertEqual(4, len(rows))

    def test_an_area_needs_three_points(self):
        with self.assertRaises(ValueError):
            analysis.area_search(self.dataset(), [[36.0, 35.0], [36.1, 35.1]])


if __name__ == "__main__":
    unittest.main()

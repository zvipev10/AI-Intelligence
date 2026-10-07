import unittest

from hl.mapping import Mapping, as_cell, evaluate

ITEM = {
    "item_id": "u-1",
    "event_time": "2026-09-01T05:24:00Z",
    "source_application": "IPDR",
    "text": {"original": "מקור", "english": "source"},
    "location": {"point": {"lat": 35.5, "lon": 36.25}},
    "tags": [{"type": "event_id", "value": "REC-1"}, {"type": "imei", "value": "353294702931926"},
             {"type": "empty", "value": ""}],
    "parties": [{"id": "a", "identifiers": [{"type": "msisdn", "value": "9630"}, {"type": "imei", "value": "111"}]}],
}


class PathExpressionTests(unittest.TestCase):
    def test_nested_keys_selectors_and_indexes(self):
        self.assertEqual(35.5, evaluate(ITEM, "location.point.lat"))
        self.assertEqual("353294702931926", evaluate(ITEM, "tags[type=imei].value"))
        self.assertEqual("9630", evaluate(ITEM, "parties[0].identifiers[type=msisdn].value"))

    def test_first_non_empty_alternative_wins(self):
        self.assertEqual("REC-1", evaluate(ITEM, "tags[type=missing].value | tags[type=event_id].value | item_id"))
        self.assertEqual("u-1", evaluate(ITEM, "tags[type=empty].value | item_id"))
        self.assertIsNone(evaluate(ITEM, "nothing.here | tags[type=nope].value"))

    def test_literal(self):
        self.assertEqual("Cellular Calls", evaluate(ITEM, "'Cellular Calls'"))

    def test_cells_are_strings(self):
        self.assertEqual("35", as_cell(35.0))
        self.assertEqual("35.5", as_cell(35.5))
        self.assertEqual("true", as_cell(True))
        self.assertEqual("", as_cell(None))


class MappingTests(unittest.TestCase):
    def setUp(self):
        self.mapping = Mapping({
            "items": {
                "record_id": "tags[type=event_id].value | item_id",
                "tag_passthrough": True,
                "fields": {
                    "timestamp_utc": "event_time",
                    "source_type": "source_application",
                    "event_summary": {"he": "text.original", "en": "text.english"},
                    "latitude": "location.point.lat",
                },
            },
            "label_fields": ["source_type"],
            "value_labels": {"en": {"IPDR": "IP sessions"}},
        })

    def test_row_shape_and_ids(self):
        row = self.mapping.item_to_row(ITEM, "he")
        self.assertEqual("REC-1", row["event_id"])
        self.assertEqual("REC-1", row["record_id"])
        self.assertEqual("u-1", row["i360_item_id"])
        self.assertEqual("353294702931926", row["imei"])  # tag passthrough
        self.assertNotIn("empty", row)
        self.assertEqual("35.5", row["latitude"])
        self.assertEqual("מקור", row["event_summary"])

    def test_locale_specific_fields_and_labels(self):
        row = self.mapping.item_to_row(ITEM, "en")
        self.assertEqual("source", row["event_summary"])
        self.assertEqual("IP sessions", row["source_type"])

    def test_record_id_falls_back_to_item_id(self):
        row = self.mapping.item_to_row({"item_id": "u-2", "tags": []}, "he")
        self.assertEqual("u-2", row["event_id"])

    def test_entities_and_locations_from_instances(self):
        mapping = Mapping({
            "entities": {"record_json": "sections.raw.json", "fields": {"entity_id": "sections.main.ref_id"}},
            "locations": {"fields": {"location_id": "sections.main.ref_id", "name": "entity_name",
                                     "latitude": "sections.main.position.geoPoint.lat"}},
        })
        entity = mapping.instance_to_entity({"sections": {"main": {"ref_id": "ENT-1"},
                                                          "raw": {"json": '{"canonical_name": "A", "telecom": {"imei": "1"}}'}}})
        self.assertEqual({"entity_id": "ENT-1", "canonical_name": "A", "telecom": {"imei": "1"}}, entity)
        location_id, location = mapping.instance_to_location({
            "entity_id": "x", "entity_name": "Site", "sections": {"main": {"ref_id": "LOC-1", "position": {"geoPoint": {"lat": "35.1"}}}}})
        self.assertEqual("LOC-1", location_id)
        self.assertEqual({"name": "Site", "latitude": 35.1}, location)


if __name__ == "__main__":
    unittest.main()

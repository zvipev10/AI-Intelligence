import unittest
from datetime import datetime, timedelta, timezone

from hl.client import HlError
from hl.items import EARLIEST, ItemReader, _parse
from hl.mapping import Mapping


class RecordingClient:
    def __init__(self):
        self.bodies = []

    def search_items(self, body):
        self.bodies.append(body)
        return {"total": 0, "total_pages": 1, "items": []}


def mapping():
    return Mapping({"version": 1, "items": {"record_id": "item_id", "needs_get": False, "fields": {}}})


class RecentDaysTests(unittest.TestCase):
    def test_recent_days_narrows_the_window_and_is_not_sent(self):
        client = RecordingClient()
        ItemReader(client, mapping(), {"item_types": ["location_update"], "recent_days": 30}, 100).items()
        body = client.bodies[0]
        self.assertNotIn("recent_days", body)
        self.assertEqual(["location_update"], body["item_types"])
        start = _parse(body["time"]["from"])
        self.assertLess(abs(start - (datetime.now(timezone.utc) - timedelta(days=30))), timedelta(minutes=1))

    def test_without_recent_days_the_scan_starts_at_the_beginning(self):
        client = RecordingClient()
        ItemReader(client, mapping(), {"filters": [{"field": "scenario", "values": ["syria"]}]}, 100).items()
        self.assertEqual(EARLIEST, client.bodies[0]["time"]["from"])

    def test_limit_asks_for_one_page_of_the_newest_items(self):
        client = RecordingClient()
        ItemReader(client, mapping(), {"item_types": ["location_update"], "limit": 50}, 30000).items()
        self.assertEqual(1, len(client.bodies))
        body = client.bodies[0]
        self.assertNotIn("limit", body)
        self.assertEqual((50, "desc", 1), (body["page_size"], body["order"], body["page_number"]))


class ForbiddenEntitiesClient(RecordingClient):
    def search_entities(self, entity_type, body):
        raise HlError(403, "ems", "Action not allowed")


class UnreadableEntityTypeTests(unittest.TestCase):
    def test_a_forbidden_entity_type_is_a_warning_not_a_failure(self):
        reader = ItemReader(ForbiddenEntitiesClient(), Mapping({"version": 1, "items": {"fields": {}},
                                                               "entities": {"types": ["DEMO_ENTITY"], "fields": {}}}), {}, 100)
        self.assertEqual([], reader.entities())
        self.assertTrue(any("DEMO_ENTITY" in warning for warning in reader.warnings))


if __name__ == "__main__":
    unittest.main()

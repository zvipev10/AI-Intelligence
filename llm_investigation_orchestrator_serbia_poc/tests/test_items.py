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

    def test_each_query_is_read_and_can_name_its_layer(self):
        class Client(RecordingClient):
            def search_items(self, body):
                self.bodies.append(body)
                kind = body["item_types"][0]
                return {"total": 1, "total_pages": 1, "items": [
                    {"item_id": f"{kind}-1", "item_type": kind, "source_application": "Telegram"}]}

        client = Client()
        reader = ItemReader(client, Mapping({"version": 1, "items": {"record_id": "item_id", "needs_get": False,
                                                                     "fields": {"source_type": "source_application"}}}),
                            {"queries": [{"item_types": ["location_update"], "limit": 5},
                                         {"item_types": ["image"], "limit": 5, "layer": "image"}]}, 100)
        rows = reader.rows("en")
        self.assertEqual([["location_update"], ["image"]], [body["item_types"] for body in client.bodies])
        self.assertTrue(all("layer" not in body and "queries" not in body for body in client.bodies))
        self.assertEqual(["Telegram", "image"], [row["source_type"] for row in rows])


class ForbiddenEntitiesClient(RecordingClient):
    def search_entities(self, entity_type, body):
        raise HlError(403, "ems", "Action not allowed")


class UnreadableEntityTypeTests(unittest.TestCase):
    def test_a_forbidden_entity_type_is_a_warning_not_a_failure(self):
        reader = ItemReader(ForbiddenEntitiesClient(), Mapping({"version": 1, "items": {"fields": {}},
                                                               "entities": {"types": ["DEMO_ENTITY"], "fields": {}}}), {}, 100)
        self.assertEqual([], reader.entities())
        self.assertTrue(any("DEMO_ENTITY" in warning for warning in reader.warnings))


class UnprovisionedTypesClient:
    def search_entities(self, entity_type, body):
        raise HlError(400, "ems_error", f"ems -> HTTP 400: Invalid entity type: /entities/entities/{entity_type}/search")


class UnprovisionedStateTests(unittest.TestCase):
    def test_reads_before_provisioning_return_nothing(self):
        from hl.state import StateStore
        store = StateStore(UnprovisionedTypesClient(), investigation_type="AII_INVESTIGATION",
                           memory_item_type="AII_MEMORY_ITEM", approval_type="AII_TELECOM_APPROVAL", scenario="lambda")
        self.assertEqual([], store._search_all("AII_TELECOM_APPROVAL", []))

    def test_other_bad_requests_still_fail(self):
        from hl.state import StateStore

        class BadRequest:
            def search_entities(self, entity_type, body):
                raise HlError(400, "bad_request", "page_size too large")

        store = StateStore(BadRequest(), investigation_type="A", memory_item_type="B", approval_type="C", scenario="x")
        with self.assertRaises(HlError):
            store._search_all("C", [])


if __name__ == "__main__":
    unittest.main()

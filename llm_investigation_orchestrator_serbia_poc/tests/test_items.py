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

    def test_a_limit_above_one_page_reads_further_pages(self):
        class Client(RecordingClient):
            def search_items(self, body):
                self.bodies.append(body)
                start = (body["page_number"] - 1) * body["page_size"]
                return {"total": 1000, "total_pages": 10,
                        "items": [{"item_id": f"i{n}"} for n in range(start, start + body["page_size"])]}

        client = Client()
        items = ItemReader(client, mapping(), {"item_types": ["image"]}, 30000, items_per_query=200).items()
        self.assertEqual(200, len(items))
        self.assertEqual([1, 2], [body["page_number"] for body in client.bodies])

    def test_a_querys_own_limit_wins_over_the_default(self):
        client = RecordingClient()
        ItemReader(client, mapping(), {"item_types": ["video"], "limit": 200}, 30000, items_per_query=300).items()
        self.assertEqual(100, client.bodies[0]["page_size"])  # paged: 200 = 2 pages of 100

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


class ServerRowsTests(unittest.TestCase):
    def test_the_server_keeps_the_layer_name_of_cached_items(self):
        from types import SimpleNamespace

        from hl.items import Snapshot
        from server import App

        app = SimpleNamespace(mapping=Mapping({"version": 1, "items": {"record_id": "item_id",
                                                                       "fields": {"source_type": "source_application"}}}))
        snap = Snapshot(items=[{"item_id": "a", "source_application": "Telegram"},
                               {"item_id": "b", "source_application": "Telegram", "_layer": "image"}],
                        entities=[], locations={}, reviews={}, fetched_at=0.0)
        self.assertEqual(["Telegram", "image"], [row["source_type"] for row in App.rows(app, snap, "en")])


class RecordFilesTests(unittest.TestCase):
    def test_signed_links_become_absolute_and_media_comes_first(self):
        from server import normalize_record_files

        files = normalize_record_files([
            {"file_id": "1", "role": "source_grab", "raw_type": "rawdata", "content_type": "application/json",
             "urls": {"primary": "/api/v1/items/x/files/1?variant=primary&token=a"}},
            {"file_id": "2", "role": "media", "raw_type": "image", "content_type": "image/png",
             "urls": {"primary": "/api/v1/items/x/files/2?variant=primary&token=b",
                      "thumbnail": "/api/v1/items/x/files/2?variant=thumbnail&token=c"}},
        ], "https://hl.example")
        self.assertEqual(["2", "1"], [f["file_id"] for f in files])
        self.assertEqual("https://hl.example/api/v1/items/x/files/2?variant=primary&token=b", files[0]["url"])
        self.assertTrue(files[0]["thumbnail_url"].startswith("https://hl.example/"))


class AllFieldsTests(unittest.TestCase):
    def test_item_fields_flattens_everything_populated(self):
        from hl.items import item_fields

        fields = item_fields({
            "item_id": "x", "item_type": "image", "name": None, "location": {"point": {"lat": 35.08, "lon": 36.29}},
            "text": {"transcript": "3x cargo truck", "english": None},
            "insights": [{"type": "transcription", "value": "a"}, {"type": "post_comment", "value": "b"}],
            "tags": [{"type": "object_recognition", "value": "weapon"}], "flags": ["HasContent"],
            "media": {"kind": "image", "file_count": 1}, "parties": [], "_layer": "Satellite",
        })
        self.assertEqual("image", fields["i360.item_type"])
        self.assertEqual("35.08", fields["i360.location.point.lat"])
        self.assertEqual("3x cargo truck", fields["i360.text.transcript"])
        self.assertEqual("a", fields["i360.insights.transcription"])
        self.assertEqual("b", fields["i360.insights.post_comment"])
        self.assertEqual("object_recognition=weapon", fields["i360.tags"])
        self.assertEqual("HasContent", fields["i360.flags"])
        self.assertEqual("image", fields["i360.media.kind"])
        self.assertNotIn("i360.name", fields)
        self.assertNotIn("i360.parties", fields)
        self.assertNotIn("i360._layer", fields)

    def test_contract_260_parts_are_flattened(self):
        from hl.items import item_fields

        fields = item_fields({
            "additional_info": [{"gsd_m": 0.5, "image_id": "RT-1"}],
            "user_agents_data": [{"device_brand": "Apple", "operating_system_name": "iOS", "value": None, "name": None}],
            "ip": {"ip_sessions": [{"source_ip": "203.0.113.107", "user_agent": None}]},
            "fe_correlation_ids": ["ADINT_OBS-01-002"],
            "context": [{"type": "COVERAGE", "value": "c-1"}]})
        self.assertEqual("0.5", fields["i360.additional_info.gsd_m"])
        self.assertEqual("RT-1", fields["i360.additional_info.image_id"])
        self.assertEqual("Apple", fields["i360.user_agents_data.device_brand"])
        self.assertEqual("203.0.113.107", fields["i360.ip.ip_sessions.source_ip"])
        self.assertEqual("ADINT_OBS-01-002", fields["i360.fe_correlation_ids"])
        self.assertEqual("COVERAGE: c-1", fields["i360.context"])
        self.assertNotIn("i360.user_agents_data", fields)

    def test_epoch_millisecond_times_become_iso(self):
        from hl.items import item_fields

        fields = item_fields({"ip": {"ip_sessions": [{"start_time": 1788650807000, "destination_port": 443}]}})
        self.assertEqual("2026-09-05T23:26:47Z", fields["i360.ip.ip_sessions.start_time"])
        self.assertEqual("443", fields["i360.ip.ip_sessions.destination_port"])

    def test_parties_with_a_target_flag_are_target_and_other(self):
        from hl.items import item_fields

        fields = item_fields({"parties": [
            {"role": "to", "target_indication": "True", "identifiers": [{"type": "msisdn", "value": "963094370078"}]},
            {"role": "from", "target_indication": "False", "identifiers": [{"type": "imei", "value": "869123048645329"}]}],
            "messages": [{"text": "hello", "status": None}]})
        self.assertEqual("963094370078", fields["i360.parties.target.msisdn"])
        self.assertEqual("869123048645329", fields["i360.parties.other.imei"])
        self.assertEqual("hello", fields["i360.messages.text"])

    def test_parties_are_flattened_by_role(self):
        from hl.items import item_fields

        fields = item_fields({"item_id": "c", "parties": [
            {"role": "from", "identifiers": [{"type": "msisdn", "value": "963094370078"}, {"type": "imei", "value": "353294702931926"}]},
            {"role": "to", "identifiers": [{"type": "msisdn", "value": "963943636427"}]}]})
        self.assertEqual("963094370078", fields["i360.parties.from.msisdn"])
        self.assertEqual("353294702931926", fields["i360.parties.from.imei"])
        self.assertEqual("963943636427", fields["i360.parties.to.msisdn"])
        self.assertNotIn("i360.parties", fields)

    def test_profile_notes_are_not_sent(self):
        client = RecordingClient()
        ItemReader(client, mapping(), {"item_types": ["x"], "_comment": "a note", "labels": {"event_time": "t"},
                                       "limit": 5}, 100).items()
        self.assertNotIn("_comment", client.bodies[0])
        self.assertNotIn("labels", client.bodies[0])

    def test_coverage_facet_filters_reach_hl_api(self):
        client = RecordingClient()
        coverage = [{"group": "coverage", "values": ["f1a50da7"]}]
        ItemReader(client, mapping(), {"item_types": ["voice_call"], "facet_filters": coverage, "limit": 5,
                                       "layer": "Cellular Locations", "fields": ["item_id"]}, 100).items()
        self.assertEqual(coverage, client.bodies[0]["facet_filters"])

    def test_fields_keeps_only_the_named_paths(self):
        class Client(RecordingClient):
            def search_items(self, body):
                self.bodies.append(body)
                return {"total": 1, "total_pages": 1, "items": [{
                    "item_id": "a", "item_type": "location_update", "source_application": "ADINT",
                    "location": {"point": {"lat": 1.5, "lon": 2.5}, "accuracy": "gps"}, "item_idx": "no"}]}

        client = Client()
        rows = ItemReader(client, mapping(), {"source_applications": ["ADINT"], "limit": 5, "layer": "ADINT",
                                              "fields": ["item_id", "location"]}, 100).rows("en")
        i360 = sorted(k for k in rows[0] if k.startswith("i360."))
        self.assertEqual(["i360.item_id", "i360.location.accuracy", "i360.location.point.lat", "i360.location.point.lon"], i360)
        self.assertNotIn("fields", client.bodies[0])
        self.assertEqual("ADINT", rows[0]["source_type"])

    def test_a_query_with_all_fields_puts_them_on_its_rows(self):
        class Client(RecordingClient):
            def search_items(self, body):
                self.bodies.append(body)
                return {"total": 1, "total_pages": 1, "items": [{"item_id": "a", "item_type": "image", "sub_type": "file_image"}]}

        client = Client()
        rows = ItemReader(client, mapping(), {"item_types": ["image"], "limit": 5, "all_fields": True}, 100).rows("en")
        self.assertNotIn("all_fields", client.bodies[0])
        self.assertEqual("file_image", rows[0]["i360.sub_type"])


class PersonMappingTests(unittest.TestCase):
    def test_a_person_of_interest_becomes_a_person_with_photo_and_imei(self):
        import json as _json
        from pathlib import Path

        profile = _json.loads((Path(__file__).resolve().parent.parent / "demo_profiles" / "lambda.json").read_text(encoding="utf-8"))
        hit = {"entity_type": "PERSON_OF_INTEREST", "entity_id": "p-1", "entity_name": "Arman Rahimi", "entity": {
            "details": {"full_name": "Arman Rahimi", "first_name": "Rahimi", "device_imei": "353294702931926"},
            "identifier": {"poi_id": "89bt", "official_picture": {"id": 1444056121000, "extension": "png"}},
            "general": {"entity_id": "p-1", "entity_name": "Arman Rahimi"}}}

        class Client:
            def search_entities(self, entity_type, body):
                return {"items": [hit], "total_pages": 1}

        m = Mapping({"version": 1, "items": {"fields": {}}, "entities": profile["entity_mapping"]})
        person = ItemReader(Client(), m, {}, 100).entities()[0]
        self.assertEqual(("p-1", "Arman Rahimi", "person"), (person["entity_id"], person["canonical_name"], person["entity_type"]))
        self.assertEqual("Rahimi", person["given_name"])
        self.assertEqual("/api/entity-files/PERSON_OF_INTEREST/p-1/1444056121000", person["image_url"])
        self.assertEqual({"imei": "353294702931926"}, person["telecom"])
        self.assertEqual("89bt", person["identifiers"])
        self.assertNotIn("image_file_id", person)


class VideoFileTests(unittest.TestCase):
    def test_videos_use_the_browser_friendly_web_preview(self):
        from server import normalize_record_files

        files = normalize_record_files([
            {"file_id": "v", "role": "media", "raw_type": "video", "content_type": "video/mp4",
             "urls": {"primary": "/f/v?variant=primary", "web_preview": "/f/v?variant=web_preview"}}], "https://hl.example")
        self.assertEqual("https://hl.example/f/v?variant=web_preview", files[0]["url"])
        self.assertEqual("https://hl.example/f/v?variant=primary", files[0]["original_url"])


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

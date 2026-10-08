"""The LAMBDA test profile: the newest tracker location updates, one layer per source, drawn as map points."""
import json
import os
import tempfile
import unittest
from pathlib import Path

from devtools.fake_hlapi import FakeEstate, make_server
from hl.state import type_definitions
from tests.test_api import Browser, start


def item(item_id, item_type, when, lat=None, lon=None, text=None, source="TrackLocation"):
    record = {"item_id": item_id, "item_type": item_type, "event_time": when, "source_application": source}
    if lat is not None:
        record["location"] = {"point": {"lat": lat, "lon": lon}, "city": None, "country": None,
                              "address": None, "accuracy": "gps"}
    if text:
        record["text"] = {"english": text}
    return record


ITEMS = [
    item("LU-1", "location_update", "2026-08-02T10:00:00Z", 32.08, 34.78),
    item("LU-2", "location_update", "2026-08-03T11:30:00Z", 32.06, 34.80),
    item("LU-3", "location_update", "2026-08-04T09:15:00Z", 32.10, 34.85, source="ankle_bracelet"),
    item("VC-1", "voice_call", "2026-08-04T09:15:00Z", 25.20, 55.27, "call about a meeting"),  # another item type
]


class LambdaProfileTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.saved_env = dict(os.environ)
        fixture = Path(tempfile.mkdtemp()) / "lambda.json"
        fixture.write_text(json.dumps({"scenario": "lambda", "items": ITEMS, "entities": {}}), encoding="utf-8")
        estate = FakeEstate({"analyst": "analyst"}, result_window=200)
        estate.load_fixture(fixture)
        estate.provision(type_definitions("AII_"))
        cls.fake = start(make_server("127.0.0.1", 0, estate))
        os.environ.pop("APP_MAPPING", None)
        os.environ.update({"HL_API_URL": f"http://127.0.0.1:{cls.fake.server_address[1]}",
                           "APP_COOKIE_SECURE": "false", "APP_SCENARIO": "lambda", "APP_SNAPSHOT_TTL": "300"})
        import server as app_server
        from http.server import ThreadingHTTPServer
        cls.previous_app = getattr(app_server.Handler, "app", None)
        app_server.Handler.app = app_server.App(app_server.load_settings())
        app_server.Handler.quiet = True
        cls.app_server = app_server
        cls.app = start(ThreadingHTTPServer(("127.0.0.1", 0), app_server.Handler))
        cls.base = f"http://127.0.0.1:{cls.app.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.app.shutdown()
        cls.fake.shutdown()
        cls.app_server.Handler.app = cls.previous_app
        os.environ.clear()
        os.environ.update(cls.saved_env)

    def browser(self):
        browser = Browser(self.base)
        self.assertEqual(200, browser.login("analyst", "analyst")[0])
        return browser

    def test_profile_mapping_is_used(self):
        status, body = Browser(self.base).call("GET", "/api/status")
        self.assertEqual((200, "lambda"), (status, body["scenario_id"]))

    def test_one_event_layer_per_source(self):
        status, body = self.browser().call("GET", "/api/layers?lang=en")
        self.assertEqual(200, status, body)
        counts = {layer["id"]: layer["count"] for layer in body["layers"]}
        self.assertEqual(2, counts["events:TrackLocation"])
        self.assertEqual(1, counts["events:ankle_bracelet"])
        self.assertNotIn("events:voice_call", counts)

    def test_rows_carry_coordinates(self):
        status, body = self.browser().call("GET", "/api/layers/events:TrackLocation/rows?lang=en")
        self.assertEqual(200, status, body)
        points = {row["event_id"]: (float(row["latitude"]), float(row["longitude"])) for row in body["rows"]}
        self.assertEqual({"LU-1": (32.08, 34.78), "LU-2": (32.06, 34.80)}, points)


if __name__ == "__main__":
    unittest.main()

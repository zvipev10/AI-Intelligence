"""The LAMBDA test profile: satellite (EO optical) images, drawn as map points from their own location."""
import json
import os
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path

from devtools.fake_hlapi import FakeEstate, make_server
from hl.state import type_definitions
from tests.test_api import Browser, start


def item(item_id, item_type, days_ago, lat=None, lon=None, source="EO optical (fictional)"):
    when = (datetime.now(timezone.utc) - timedelta(days=days_ago)).strftime("%Y-%m-%dT%H:%M:%SZ")
    record = {"item_id": item_id, "item_type": item_type, "event_time": when, "source_application": source,
              "text": {"transcript": "3x cargo truck"}}
    if lat is not None:
        record["location"] = {"point": {"lat": lat, "lon": lon}, "accuracy": "gps"}
    return record


ITEMS = [
    item("SAT-1", "image", 30, 35.0806, 36.2963),
    item("SAT-2", "image", 31, 35.07, 36.30),
    item("TG-1", "image", 1, source="Telegram"),  # another source: not in the layer
    item("LU-1", "location_update", 2, 32.08, 34.78, source="TrackLocation"),  # another item type
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

    def test_only_the_satellite_layer(self):
        status, body = self.browser().call("GET", "/api/layers?lang=en")
        self.assertEqual(200, status, body)
        events = {layer["id"]: layer["count"] for layer in body["layers"] if layer["id"].startswith("events:")}
        self.assertEqual({"events:Satellite": 2}, events)

    def test_rows_carry_coordinates(self):
        status, body = self.browser().call("GET", "/api/layers/events:Satellite/rows?lang=en")
        self.assertEqual(200, status, body)
        points = {row["event_id"]: (float(row["latitude"]), float(row["longitude"])) for row in body["rows"]}
        self.assertEqual({"SAT-1": (35.0806, 36.2963), "SAT-2": (35.07, 36.30)}, points)


if __name__ == "__main__":
    unittest.main()

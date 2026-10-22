"""The LAMBDA test profile: satellite (EO optical) images and ADINT items, drawn as map points from their own location."""
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
    item("AD-1", "location_update", 3, 35.10, 36.25, source="ADINT"),
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

    def test_satellite_and_adint_layers(self):
        status, body = self.browser().call("GET", "/api/layers?lang=en")
        self.assertEqual(200, status, body)
        events = {layer["id"]: layer["count"] for layer in body["layers"] if layer["id"].startswith("events:")}
        # The cellular and IPDR layers have no data in this fixture; they are listed with 0.
        self.assertEqual({"events:Satellite": 2, "events:ADINT": 1, "events:Cellular Locations": 0,
                          "events:Cellular Calls": 0, "events:IPDR": 0, "events:CCTV": 0}, events)

    def test_layers_carry_the_mapping_display_names(self):
        status, body = self.browser().call("GET", "/api/layers?lang=en")
        self.assertEqual(200, status, body)
        labels = {layer["id"]: layer.get("field_labels") or {} for layer in body["layers"]}
        self.assertEqual("acquisition_datetime_utc", labels["events:Satellite"]["i360.event_time"])
        self.assertEqual("analyst_note", labels["events:Satellite"]["i360.insights.post_comment"])
        self.assertEqual("observation_id", labels["events:ADINT"]["i360.fe_correlation_ids"])
        self.assertEqual("ip_public", labels["events:IPDR"]["i360.ip.ip_sessions.source_ip"])

    def test_adint_language_has_one_mapping_for_search_and_one_for_get_by_id(self):
        # HL API's items/get does not return "language" (search does), so rows read by id name language_code.
        status, body = self.browser().call("GET", "/api/layers?lang=en")
        self.assertEqual(200, status, body)
        adint = next(layer for layer in body["layers"] if layer["id"] == "events:ADINT")
        self.assertEqual("keyboard_language", adint["field_labels"]["i360.language"])
        self.assertNotIn("i360.user_agents_data.language_code", adint["field_labels"])
        self.assertEqual("keyboard_language", adint["field_labels_by_id"]["i360.user_agents_data.language_code"])
        self.assertNotIn("i360.language", adint["field_labels_by_id"])
        self.assertEqual("observation_id", adint["field_labels_by_id"]["i360.fe_correlation_ids"])
        status, body = self.browser().call("POST", "/api/chat/items", {"ids": ["AD-1"], "locale": "en"})
        self.assertEqual(200, status, body)
        group = body["groups"][0]
        self.assertEqual(("ADINT", "by_id"), (group["label"], group["rows"][0]["i360_read"]))
        self.assertEqual("keyboard_language", group["field_labels"]["i360.user_agents_data.language_code"])

    def test_launcher_page_and_its_applications(self):
        browser = self.browser()
        status, body = browser.call("GET", "/api/launcher")
        self.assertEqual(200, status, body)
        self.assertEqual("Military Intelligence", body["title"])
        self.assertEqual(["ADINT", "Cellular Geolocations", "Cellular Calls", "Satellite", "CCTV"], [e["name"] for e in body["applications"]])
        self.assertEqual("./?layer=ADINT", body["applications"][0]["url"])
        self.assertEqual(["i360", "Administrator", "Dashboards", "i360 Studio"], [e["name"] for e in body["workspace"]])
        self.assertNotIn("url", body["workspace"][2])  # Dashboards: not on LAMBDA yet, shown as unavailable
        import urllib.request
        with urllib.request.urlopen(self.base + "/home") as response:
            page = response.read().decode("utf-8")
        self.assertIn("/api/launcher", page)
        self.assertIn("Expert applications", page)

    def test_layer_rows_carry_the_display_names_too(self):
        status, body = self.browser().call("GET", "/api/layers/events:Satellite/rows?lang=en")
        self.assertEqual(200, status, body)
        self.assertEqual("acquisition_datetime_utc", body["layer"]["field_labels"]["i360.event_time"])

    def test_rows_carry_coordinates(self):
        status, body = self.browser().call("GET", "/api/layers/events:Satellite/rows?lang=en")
        self.assertEqual(200, status, body)
        points = {row["event_id"]: (float(row["latitude"]), float(row["longitude"])) for row in body["rows"]}
        self.assertEqual({"SAT-1": (35.0806, 36.2963), "SAT-2": (35.07, 36.30)}, points)


if __name__ == "__main__":
    unittest.main()

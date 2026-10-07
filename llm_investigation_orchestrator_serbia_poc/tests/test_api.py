"""End-to-end: the app server against the fake HL API, both in-process on free ports."""
import csv
import io
import json
import os
import threading
import time
import unittest
import urllib.error
import urllib.request
from http.cookiejar import CookieJar
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "devtools" / "fixtures" / "syria.json.gz"

from devtools.fake_hlapi import FakeEstate, make_server  # noqa: E402
from hl.state import type_definitions  # noqa: E402


def start(server):
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server


class Browser:
    """A cookie-keeping client, like the browser."""

    def __init__(self, base):
        self.base = base
        self.jar = CookieJar()
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.jar))

    def call(self, method, path, body=None, raw=False):
        data = json.dumps(body).encode() if body is not None else None
        request = urllib.request.Request(self.base + path, data=data, method=method,
                                         headers={"Content-Type": "application/json"} if data else {})
        try:
            with self.opener.open(request, timeout=30) as response:
                payload = response.read()
                return response.status, (payload if raw else json.loads(payload or b"{}"))
        except urllib.error.HTTPError as exc:
            payload = exc.read()
            return exc.code, (payload if raw else json.loads(payload or b"{}"))

    def login(self, username="analyst", password="analyst"):
        return self.call("POST", "/api/login", {"username": username, "password": password})


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.estate = FakeEstate({"analyst": "analyst", "other": "other"}, result_window=200)
        cls.estate.load_fixture(FIXTURE)
        cls.estate.provision(type_definitions("AII_"))
        cls.fake = start(make_server("127.0.0.1", 0, cls.estate))
        os.environ.update({
            "HL_API_URL": f"http://127.0.0.1:{cls.fake.server_address[1]}",
            "APP_COOKIE_SECURE": "false", "APP_SCENARIO": "syria", "APP_SNAPSHOT_TTL": "300",
        })
        import server as app_server
        from http.server import ThreadingHTTPServer
        app_server.Handler.app = app_server.App(app_server.load_settings())
        app_server.Handler.quiet = True
        cls.app = start(ThreadingHTTPServer(("127.0.0.1", 0), app_server.Handler))
        cls.base = f"http://127.0.0.1:{cls.app.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.app.shutdown()
        cls.fake.shutdown()

    def signed_in(self, user="analyst"):
        browser = Browser(self.base)
        status, body = browser.login(user, user)
        self.assertEqual(200, status, body)
        return browser

    # -- health, static, auth -----------------------------------------------------------
    def test_health_needs_no_backend_call(self):
        before = len(self.estate.calls)
        status, body = Browser(self.base).call("GET", "/healthz")
        self.assertEqual((200, "ok"), (status, body["status"]))
        self.assertEqual(before, len(self.estate.calls))

    def test_static_files_are_allowlisted(self):
        browser = Browser(self.base)
        self.assertEqual(200, browser.call("GET", "/", raw=True)[0])
        self.assertEqual(200, browser.call("GET", "/vendor/maplibre-gl.js", raw=True)[0])
        for path in ("/server.py", "/hl/client.py", "/mapping/default.json", "/devtools/fixtures/syria.json.gz",
                     "/vendor/../server.py", "/assets/%2e%2e/server.py", "/vendor/%2e%2e/hl/config.py"):
            self.assertEqual(404, browser.call("GET", path, raw=True)[0], path)

    def test_signed_out_status_and_guard(self):
        browser = Browser(self.base)
        status, body = browser.call("GET", "/api/status")
        self.assertEqual(200, status)
        self.assertFalse(body["authenticated"])
        self.assertEqual("syria", body["scenario_id"])
        self.assertEqual(401, browser.call("GET", "/api/layers")[0])
        self.assertEqual(401, browser.call("POST", "/api/investigations", {"investigation_id": "x", "name": "x"})[0])

    def test_wrong_password_is_401_without_cookie(self):
        browser = Browser(self.base)
        status, body = browser.login("analyst", "nope")
        self.assertEqual((401, "invalid_credentials"), (status, body["error"]))
        self.assertEqual(0, len(browser.jar))

    def test_cookie_is_httponly_and_holds_only_the_token(self):
        browser = self.signed_in()
        cookie = next(iter(browser.jar))
        self.assertEqual("aii_session", cookie.name)
        self.assertTrue(cookie.has_nonstandard_attr("HttpOnly"))
        self.assertIn(cookie.value, self.estate.tokens)

    def test_expired_token_signs_out(self):
        browser = self.signed_in()
        token = next(iter(browser.jar)).value
        user, _ = self.estate.tokens[token]
        self.estate.tokens[token] = (user, time.time() - 1)
        status, body = browser.call("GET", "/api/status")
        self.assertFalse(body["authenticated"])
        self.assertEqual(401, browser.call("GET", "/api/investigations")[0])

    def test_logout(self):
        browser = self.signed_in()
        self.assertEqual(200, browser.call("POST", "/api/logout")[0])
        self.assertEqual(401, browser.call("GET", "/api/layers")[0])

    # -- data ---------------------------------------------------------------------------
    def test_layers_match_the_dataset(self):
        status, body = self.signed_in().call("GET", "/api/layers")
        self.assertEqual(200, status)
        counts = {layer["id"]: layer["count"] for layer in body["layers"]}
        self.assertEqual(15, counts["entity-metadata:all"])
        self.assertEqual(404, counts["location-metadata:all"])
        self.assertEqual(300, counts["events:IPDR"])
        self.assertEqual(300, counts["events:Cellular Geolocations"])
        self.assertEqual(120, counts["events:ADINT"])
        self.assertEqual(2, counts["events:שיחות סלולר"])
        self.assertNotIn("evidence:all", counts)

    def test_paging_past_the_result_window_reads_every_item(self):
        # The fake's result_window is 200, below the 726 items: the reader must split by time.
        status, body = self.signed_in().call("GET", "/api/dataset/info")
        self.assertEqual((200, 726, False), (status, body["rows"], body["truncated"]))

    def test_dataset_csv_carries_the_original_columns(self):
        status, payload = self.signed_in().call("GET", "/api/dataset/events?lang=he", raw=True)
        rows = {row["event_id"]: row for row in csv.DictReader(io.StringIO(payload.decode("utf-8")))}
        self.assertEqual(726, len(rows))
        call = rows["REC-SYR-CALL-1"] if "REC-SYR-CALL-1" in rows else next(r for r in rows.values() if r.get("call_id"))
        self.assertTrue(call["side_a_imei"])
        self.assertTrue(call["timestamp_utc"].endswith("Z"))
        ipdr = next(r for r in rows.values() if r["source_type"] == "IPDR")
        self.assertTrue(ipdr["ip_public"])
        self.assertFalse(any(r.get("audio_url") or r.get("video_url") for r in rows.values()))

    def test_rows_filters_and_links(self):
        browser = self.signed_in()
        filters = json.dumps({"source_record_ids": []})
        status, body = browser.call("GET", "/api/layers/events:IPDR/rows")
        self.assertEqual((200, 300), (status, len(body["rows"])))
        status, body = browser.call("GET", "/api/links")
        self.assertEqual(200, status)
        self.assertTrue(any(link["rule_id"] == "entity_imei_to_cellular_target_imei_v1" for link in body["links"]))
        self.assertEqual(404, browser.call("GET", "/api/layers/evidence:all/rows")[0])
        del filters

    def test_english_locale_translates_labels(self):
        status, body = self.signed_in().call("GET", "/api/layers?lang=en")
        ids = {layer["id"] for layer in body["layers"]}
        self.assertIn("events:Cellular Calls", ids)

    # -- saved work ---------------------------------------------------------------------
    def test_investigation_memory_round_trip_and_isolation(self):
        browser = self.signed_in()
        status, body = browser.call("POST", "/api/investigations", {"investigation_id": "inv_rt", "name": "Round trip"})
        self.assertEqual(200, status, body)
        status, body = browser.call("POST", "/api/investigation-memory/layer", {
            "investigation_id": "inv_rt", "comment": "keep",
            "layer": {"id": "l", "label": "IPDR", "kind": "events", "catalog_layer_id": "events:IPDR",
                      "reconstruction": {"type": "typed_ids", "layer_kind": "events",
                                         "record_ids": ["REC-SYR-CELL-CSV-001", "NOPE"], "locale": "he"}}})
        self.assertEqual(201, status, body)
        layer_id = body["saved"]["id"]
        status, body = browser.call("POST", "/api/investigation-memory/artifact", {
            "investigation_id": "inv_rt", "artifact": {"kind": "polygon", "label": "area", "geometry": {
                "type": "Polygon", "coordinates": [[[36.2, 35.0], [36.3, 35.0], [36.3, 35.1], [36.2, 35.0]]]}}})
        self.assertEqual(201, status, body)
        status, body = browser.call("POST", "/api/collection-request", {
            "investigation_id": "inv_rt", "role": "sigint", "collection_type": "cellular_calls",
            "target": {"type": "imei", "imei": "353294702931926"}})
        self.assertEqual(201, status, body)
        self.assertEqual("analyst", body["saved"]["requested_by"])

        status, memory = browser.call("GET", "/api/investigation-memory?id=inv_rt")
        self.assertEqual({"layers": 1, "artifacts": 1, "collection_requests": 1},
                         {k: len(v) for k, v in memory["memory"].items() if v})
        status, presentation = browser.call(
            "GET", f"/api/investigation-memory/layers/{layer_id}/presentation?investigation_id=inv_rt&locale=he")
        self.assertEqual(("partially_restored", ["NOPE"]), (presentation["restore_status"], presentation["missing_ids"]))

        listing = browser.call("GET", "/api/investigations")[1]["investigations"]
        entry = next(i for i in listing if i["investigation_id"] == "inv_rt")
        self.assertEqual((1, 1, 1), (entry["layer_count"], entry["artifact_count"], entry["collection_request_count"]))

        other = self.signed_in("other")
        self.assertFalse(any(i["investigation_id"] == "inv_rt" for i in other.call("GET", "/api/investigations")[1]["investigations"]))
        self.assertEqual({}, {k: v for k, v in other.call("GET", "/api/investigation-memory?id=inv_rt")[1]["memory"].items() if v})

        status, body = browser.call("POST", "/api/investigation-memory/delete",
                                    {"investigation_id": "inv_rt", "group": "layers", "item_id": layer_id})
        self.assertEqual(200, status, body)
        self.assertEqual([], body["memory"]["memory"]["layers"])
        self.assertEqual(400, browser.call("POST", "/api/investigation-memory/delete",
                                           {"investigation_id": "inv_rt", "group": "layers", "item_id": layer_id})[0])

    def test_validation_errors_are_400(self):
        browser = self.signed_in()
        self.assertEqual(400, browser.call("POST", "/api/investigations", {"investigation_id": "bad id!", "name": "x"})[0])
        self.assertEqual(400, browser.call("POST", "/api/investigation-memory/artifact",
                                           {"investigation_id": "inv_v", "artifact": {"kind": "polygon", "geometry": {}}})[0])
        self.assertEqual(400, browser.call("POST", "/api/collection-request", {
            "investigation_id": "inv_v", "role": "visint", "collection_type": "cellular_calls",
            "target": {"type": "imei", "imei": "353294702931926"}})[0])

    def test_subscriber_identity_review_is_saved_in_i360(self):
        browser = self.signed_in()
        status, body = browser.call("GET", "/api/derivations?entity_id=ENT-SYR-PERSON-002")
        self.assertEqual(1, len(body["derivations"]))
        status, body = browser.call("POST", "/api/derivations/review", {"entity_id": "ENT-SYR-PERSON-002", "action": "approve"})
        self.assertEqual(201, status, body)
        self.assertEqual("approved", body["saved"]["review_state"])
        self.assertEqual("analyst", body["saved"]["reviewed_by"])
        approvals = [r for r in self.estate.instances["AII_TELECOM_APPROVAL"].values() if not r.get("deleted")]
        self.assertTrue(any(r["sections"]["main"]["entity_ref"] == "ENT-SYR-PERSON-002" for r in approvals))
        rows = browser.call("GET", "/api/layers/entity-metadata:all/rows")[1]["rows"]
        person = next(r for r in rows if r["entity_id"] == "ENT-SYR-PERSON-002")
        self.assertEqual("9630943700780", person["telecom"]["approved_subscriber_identity"]["msisdn"])
        self.assertEqual(400, browser.call("POST", "/api/derivations/review", {"entity_id": "ENT-NOPE"})[0])


if __name__ == "__main__":
    unittest.main()

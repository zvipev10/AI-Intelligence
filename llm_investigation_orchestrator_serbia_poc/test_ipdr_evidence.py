import copy
import csv
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from ipdr_evidence import attach_package, interval_validation
from demo_runtime import load_profile

ROOT = Path(__file__).resolve().parent
DATA = ROOT / load_profile(ROOT, "syria", verify=True)["files"]["events"]
DATA = DATA.parent


class IpdrEvidence(unittest.TestCase):
    def rows(self):
        with (DATA / "events.csv").open(newline="", encoding="utf-8-sig") as handle:
            return list(csv.DictReader(handle))

    def test_parity_identity_and_idempotence(self):
        rows = self.rows()
        before = copy.deepcopy(rows)
        package = attach_package(rows, DATA / "events.csv")
        self.assertEqual(package["record_count"], 300)
        self.assertEqual(sum(package["session_validation_counts"].values()), 300)
        for old, new in zip(before, rows):
            self.assertEqual(old, {key: new[key] for key in old})
            if old["source_type"] != "IPDR":
                self.assertEqual(old, new)
        self.assertEqual(attach_package(rows, DATA / "events.csv"), package)
        ipdr = [r for r in rows if r["source_type"] == "IPDR"]
        self.assertEqual(sum(bool(r["imei"]) for r in ipdr), 4)
        self.assertEqual({r["source_reference"]["data_row"] for r in ipdr}, set(range(1, 301)))

    def test_source_and_membership_fail_closed(self):
        for mutation in ("checksum", "value", "duplicate", "count"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                path = Path(tmp)
                for filename in ("ipdr-package.json", "IPDR-expanded.csv"):
                    (path / filename).write_bytes((DATA / filename).read_bytes())
                rows = self.rows()
                ipdr = [r for r in rows if r["source_type"] == "IPDR"]
                if mutation == "checksum":
                    with (path / "IPDR-expanded.csv").open("ab") as handle:
                        handle.write(b"\n")
                elif mutation == "value":
                    ipdr[0]["imei"] = "invented"
                elif mutation == "duplicate":
                    ipdr[0]["source_record_id"] = ipdr[1]["source_record_id"]
                else:
                    rows.remove(ipdr[0])
                with self.assertRaises(ValueError):
                    attach_package(rows, path / "events.csv")
                self.assertFalse(any("package_id" in row for row in rows))

    def test_intervals(self):
        start = "2026-09-01T00:00:00Z"
        self.assertEqual(interval_validation(start, start)["duration_seconds"], 0)
        self.assertEqual(interval_validation(start, "2026-08-31T23:59:00Z")["state"], "invalid")
        self.assertEqual(interval_validation(start, "")["state"], "unknown")
        self.assertEqual(interval_validation("bad", start)["state"], "invalid")
        self.assertEqual(interval_validation("2026-09-01T00:00:00", start)["state"], "invalid")

    def test_ui_mcp_and_visibility(self):
        code = '''import json
import server as ui
import mcp_server.server as mcp
for locale in ("he", "en"):
    layers = ui.list_ui_layers(locale)
    assert not any(layer["id"].startswith("ipdr-package:") for layer in layers)
    evidence_layer = next(layer for layer in layers if layer["id"] == ui.EVIDENCE_CATALOG_LAYER_ID)
    metadata, rows = ui.get_ui_layer_rows(evidence_layer["id"], locale)
    assert len(rows) == 1 and evidence_layer["count"] == 1
    assert metadata["kind"] == "evidence"
    assert rows[0]["evidence_type"] == "ipdr_package" and rows[0]["record_count"] == 300
    raw = ui.get_ui_layer_rows("events:IPDR", locale)[1]
    assert len(raw) == 300 and sum(bool(r["imei"]) for r in raw) == 4
    selected = raw[0]["event_id"]
    assert len(ui.get_ui_layer_rows("events:IPDR", locale, {"event_ids": [selected]})[1]) == 1
    evidence = ui.load_evidence_catalog(locale)
    assert len(evidence) == 1 and evidence[0]["evidence_type"] == "ipdr_package"
    assert not any(r.get("source_type") == "IPDR" for r in evidence)
    assert mcp.get_evidence({"evidence_id": selected})["evidence"] is None
    obj = mcp.get_evidence({"evidence_id": rows[0]["package_id"]})["evidence"]
    assert len(obj["source_record_ids"]) == 300
    mcp.load_ui_catalog = lambda requested_locale: ui.list_ui_layers(requested_locale)
    action = mcp.open_object_viewer({"object_kind": "evidence", "object_id": rows[0]["package_id"], "locale": locale})["object_viewer_actions"]
    validated, errors = ui.validate_object_viewer_actions(action, locale)
    assert not errors and validated[0]["object_kind"] == "ipdr_package" and validated[0]["catalog_layer_id"] == ui.EVIDENCE_CATALOG_LAYER_ID
    json.dumps(obj)
ui.active_playback_timeframe = lambda: {"_from": ui.parse_utc("2026-09-01T00:00:00Z"), "_to": ui.parse_utc("2026-09-01T12:00:00Z")}
assert len(ui.load_evidence_catalog("en")) == 1
raw = ui.get_ui_layer_rows("events:IPDR", "en")[1]
assert 0 < len(raw) < 300
'''
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, "-c", code], cwd=ROOT,
                env={**os.environ, "INTELLIGENCE_POC_SCENARIO": "syria", "INTELLIGENCE_POC_STATE_ROOT": tmp},
                capture_output=True, text=True, timeout=90)
        self.assertEqual(result.returncode, 0, result.stderr)


if __name__ == "__main__":
    unittest.main()

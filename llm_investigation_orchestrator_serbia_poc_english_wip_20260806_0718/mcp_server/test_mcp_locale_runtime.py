import json
import re
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import server


HEBREW_RE = re.compile(r"[\u0590-\u05ff]")


def call_tool(name, locale, **arguments):
    response = server.handle_message({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {"name": name, "arguments": {**arguments, "locale": locale}},
    })
    return response["result"]["structuredContent"]


class McpLocaleRuntimeTests(unittest.TestCase):
    def test_runtime_manifests_are_complete_and_id_aligned(self):
        he = server.RUNTIMES["he"]
        en = server.RUNTIMES["en"]
        self.assertEqual(set(he.manifest), {"events", "locations", "entities"})
        self.assertEqual(set(he.events_by_id), set(en.events_by_id))
        self.assertEqual(set(he.locations), set(en.locations))
        self.assertEqual(set(he.entities), set(en.entities))
        self.assertNotEqual(he.semantic_index_dir, en.semantic_index_dir)

    def test_english_health_and_representative_payloads_are_clean(self):
        health = call_tool("get_runtime_health", "en")
        events = call_tool("search_events", "en", source_types=["TikTok"], limit=5)
        entities = call_tool("get_objects", "en", object_type="entity", limit=5)
        location = call_tool("resolve_location", "en", query="North Kosovo")
        aggregation = call_tool("aggregate_events", "en", group_by="location", limit=5)
        intent = call_tool("classify_question_intent", "en", question="Show a timeline of vehicle movements")
        next_step = call_tool(
            "plan_next_investigation_step", "en", objective="Trace convoy",
            candidate_chain_event_ids=[], pending_recommended_seeds=[], expanded_seed_event_ids=[],
            new_clues_to_trace=[], linkage_checks_done=[], semantic_calls_used=0,
            related_calls_used=0, tool_budget_remaining=0,
        )
        payload = json.dumps(
            [health, events, entities, location, aggregation, intent, next_step],
            ensure_ascii=False,
        )
        self.assertIsNone(HEBREW_RE.search(payload))
        self.assertEqual(health["locale"], "en")
        self.assertTrue(health["semantic_cache_namespace"].endswith("/en") or health["semantic_cache_namespace"].endswith("\\en"))

    def test_alternating_calls_restore_locale_without_contamination(self):
        en_first = call_tool("get_runtime_health", "en")
        he = call_tool("get_runtime_health", "he")
        en_second = call_tool("get_runtime_health", "en")
        self.assertEqual(en_first["sources"], en_second["sources"])
        self.assertNotEqual(en_first["sources"]["events"]["sha256"], he["sources"]["events"]["sha256"])
        self.assertEqual(server.ACTIVE_LOCALE.get(), "he")

    def test_missing_english_asset_fails_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            base = root / "events.csv"
            base.write_text("event_id\nREC-1\n", encoding="utf-8")
            with patch.object(server, "DATA_PATH", base), patch.object(server, "LOCATIONS_PATH", root / "locations.json"), patch.object(server, "ENTITIES_PATH", root / "entities.json"):
                with self.assertRaisesRegex(ValueError, "en MCP runtime assets unavailable"):
                    server.load_runtime("en")

    def test_unavailable_english_runtime_does_not_fall_back_to_hebrew(self):
        english = server.RUNTIMES.pop("en")
        previous_error = server.RUNTIME_ERRORS.get("en")
        server.RUNTIME_ERRORS["en"] = "test asset failure"
        try:
            result = call_tool("get_runtime_health", "en")
            hebrew = call_tool("get_runtime_health", "he")
        finally:
            server.RUNTIMES["en"] = english
            if previous_error is None:
                server.RUNTIME_ERRORS.pop("en", None)
            else:
                server.RUNTIME_ERRORS["en"] = previous_error
        self.assertIn("en MCP runtime is unavailable", result["error"])
        self.assertEqual(hebrew["locale"], "he")


if __name__ == "__main__":
    unittest.main()

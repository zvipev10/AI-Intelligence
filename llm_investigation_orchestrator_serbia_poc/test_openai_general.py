import unittest
from unittest.mock import MagicMock

from openai_general import GENERAL_TOOL_NAMES, configuration_error, load_settings


class OpenAIGeneralSettingsTests(unittest.TestCase):
    def test_is_disabled_by_default(self):
        settings = load_settings({})
        self.assertFalse(settings.enabled)
        self.assertIn("not enabled", configuration_error(settings))

    def test_enabled_route_requires_key_without_revealing_any_value(self):
        settings = load_settings({"INTELLIGENCE_POC_OPENAI_GENERAL_ENABLED": "true"})
        self.assertTrue(settings.enabled)
        self.assertIn("OPENAI_API_KEY", configuration_error(settings))

    def test_enabled_route_uses_server_configuration(self):
        settings = load_settings({
            "INTELLIGENCE_POC_OPENAI_GENERAL_ENABLED": "1",
            "OPENAI_API_KEY": "not-a-real-key",
            "INTELLIGENCE_POC_OPENAI_GENERAL_MODEL": "gpt-5.6-terra",
        })
        self.assertIsNone(configuration_error(settings))
        self.assertEqual(settings.model, "gpt-5.6-terra")

    def test_general_creation_and_presentation_tools_match_hermes_general(self):
        self.assertIn("persist_fused_evidence", GENERAL_TOOL_NAMES)
        self.assertTrue({
            "present_requested_results", "present_saved_memory_layers", "open_catalog_layers",
        }.issubset(GENERAL_TOOL_NAMES))

    def test_shared_bridge_capture_keeps_tool_audits_separate(self):
        from openai_general import MCPToolBridge
        bridge = MCPToolBridge(__file__)
        bridge.request = MagicMock(return_value={"content": [{"text": "{}"}]})
        with bridge.capture_calls() as first:
            bridge.call("search_events", {"query": "first"})
        with bridge.capture_calls() as second:
            bridge.call("search_events", {"query": "second"})
        self.assertEqual("first", first[0]["arguments"]["query"])
        self.assertEqual("second", second[0]["arguments"]["query"])


if __name__ == "__main__":
    unittest.main()

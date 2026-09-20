import unittest

from openai_general import configuration_error, load_settings


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


if __name__ == "__main__":
    unittest.main()

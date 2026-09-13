import unittest

from moshe_profile.configure_multiplex import configure_default, configure_env, configure_ui


class MosheMultiplexTests(unittest.TestCase):
    def test_default_gateway_serves_only_moshe_as_named_profile(self):
        result = configure_default(
            {"gateway": {"trust_recent_files": True}, "mcp_servers": {"general": {}}},
            {"command": "/usr/bin/python3"},
        )
        self.assertTrue(result["gateway"]["multiplex_profiles"])
        self.assertEqual(result["gateway"]["multiplex_profile_allowlist"], ["moshe"])
        self.assertEqual(set(result["mcp_servers"]), {"general", "serbia-events-poc-moshe"})
        self.assertNotIn("serbia-events-poc-moshe", result.get("platform_toolsets", {}).get("api_server", []))

    def test_profile_env_uses_distinct_api_key_and_disables_own_transports(self):
        result = configure_env("WHATSAPP_ENABLED=true\nKEEP=value\nAPI_SERVER_KEY=old\n", "new-secret")
        self.assertNotIn("WHATSAPP_ENABLED", result)
        self.assertIn("KEEP=value", result)
        self.assertIn("API_SERVER_KEY=new-secret", result)
        self.assertIn("HERMES_PARALLEL_TOOL_CALLS=false", result)

    def test_ui_routes_moshe_to_shared_listener_prefix(self):
        result = configure_ui({"remote_port": 8642, "agents": {"general_persistent": {"remote_port": 8644}}}, "moshe-secret")
        self.assertEqual(result["agents"]["moshe"], {
            "remote_port": 8642,
            "api_key": "moshe-secret",
            "api_path_prefix": "/p/moshe",
            "mcp_tool_prefix": "mcp_serbia_events_poc_moshe_",
            "audit_path": "/opt/serbia-poc/mcp_audit_moshe.jsonl",
        })
        self.assertEqual(result["agents"]["general_persistent"]["remote_port"], 8644)


if __name__ == "__main__":
    unittest.main()

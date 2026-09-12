import unittest

from mcp_server.migrate_api_toolset_names import migrated_config


class McpToolsetMigrationTests(unittest.TestCase):
    def test_legacy_aliases_are_replaced_with_server_keys(self):
        result = migrated_config({
            "mcp_servers": {
                "intelligence-events-poc": {},
                "serbia-events-poc": {},
            },
            "platform_toolsets": {
                "api_server": ["mcp-intelligence-events-poc", "mcp-serbia-events-poc"],
            },
        })
        self.assertEqual(
            result["platform_toolsets"]["api_server"],
            ["intelligence-events-poc", "serbia-events-poc"],
        )

    def test_unknown_toolset_fails_before_config_is_written(self):
        with self.assertRaisesRegex(ValueError, "missing-server"):
            migrated_config({
                "mcp_servers": {"serbia-events-poc": {}},
                "platform_toolsets": {"api_server": ["missing-server"]},
            })


if __name__ == "__main__":
    unittest.main()

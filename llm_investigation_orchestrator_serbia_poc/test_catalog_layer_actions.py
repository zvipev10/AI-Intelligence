import importlib.util
import unittest
from pathlib import Path

from agent_result_pipeline import catalog_layer_actions_from_audit


ROOT = Path(__file__).resolve().parent


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class CatalogLayerActionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.gateway = load_module("catalog_gateway", ROOT / "server.py")
        cls.mcp = load_module("catalog_mcp", ROOT / "mcp_server" / "server.py")

    def test_mcp_builds_deterministic_open_action(self):
        result = self.mcp.open_catalog_layers({
            "catalog_layer_ids": ["events:טלגרם"],
            "view": "map",
        })
        self.assertEqual(result["catalog_layer_actions"][0], {
            "action": "open",
            "catalog_layer_id": "events:טלגרם",
            "view": "map",
        })

    def test_empty_catalog_request_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "at least one catalog_layer_id"):
            self.mcp.open_catalog_layers({"catalog_layer_ids": [], "view": "map"})

    def test_gateway_accepts_real_layer_and_rejects_unknown_id(self):
        actions, errors = self.gateway.validate_catalog_layer_actions([
            {"action": "open", "catalog_layer_id": "events:טלגרם", "view": "map"},
            {"action": "open", "catalog_layer_id": "טלגרם", "view": "map"},
        ], "he")
        self.assertEqual([item["catalog_layer_id"] for item in actions], ["events:טלגרם"])
        self.assertEqual(errors, [{"catalog_layer_id": "טלגרם", "error": "unknown_catalog_layer_id"}])

    def test_pipeline_uses_latest_successful_catalog_action(self):
        audit = [
            {"tool": "open_catalog_layers", "result": {"catalog_layer_actions": [{"catalog_layer_id": "old"}]}},
            {"tool": "open_catalog_layers", "is_error": True, "result": {}},
            {"tool": "open_catalog_layers", "result": {"catalog_layer_actions": [{"catalog_layer_id": "new"}]}},
        ]
        self.assertEqual(catalog_layer_actions_from_audit(audit), [{"catalog_layer_id": "new"}])

    def test_tool_is_exposed_and_browser_consumes_it(self):
        tool_names = {item["name"] for item in self.mcp.TOOLS}
        self.assertIn("open_catalog_layers", tool_names)
        self.assertIn("open_catalog_layers", self.mcp.TOOL_HANDLERS)
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("await openCatalogLayer(action.catalog_layer_id", app)
        self.assertIn("catalog_layer_action_errors", app)


if __name__ == "__main__":
    unittest.main()

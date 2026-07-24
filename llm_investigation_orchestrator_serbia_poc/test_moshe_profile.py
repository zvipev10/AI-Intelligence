import unittest
from pathlib import Path
from unittest.mock import patch

import server
from agent_routing import AgentRouteRegistry
from moshe_profile.provision_profile import MOSHE_AUDIT_PATH, MOSHE_PORT, MOSHE_TOOLS, restricted_config


ROOT = Path(__file__).resolve().parent


class MosheProfileTests(unittest.TestCase):
    def source_config(self):
        return {
            "platforms": {"api_server": {"enabled": True, "host": "127.0.0.1", "port": 8642, "key": "secret"}},
            "platform_toolsets": {"api_server": ["mcp-intelligence-events-poc", "mcp-serbia-events-poc"]},
            "mcp_servers": {
                "intelligence-events-poc": {"enabled": True},
                "serbia-events-poc": {
                    "command": "/usr/bin/python3", "args": ["/opt/serbia-poc/mcp_server/server.py"],
                    "env": {"INTELLIGENCE_POC_DATASET_VERSION": "v2.1", "INTELLIGENCE_POC_AUDIT": "/old/audit"},
                    "enabled": True, "tools": {"include": ["search_events"]},
                },
            },
        }

    def test_profile_is_restricted_and_isolated(self):
        config = restricted_config(self.source_config())
        self.assertEqual(config["platforms"]["api_server"]["port"], MOSHE_PORT)
        self.assertEqual(config["platform_toolsets"]["api_server"], ["mcp-serbia-events-poc"])
        self.assertEqual(set(config["mcp_servers"]), {"serbia-events-poc"})
        serbia = config["mcp_servers"]["serbia-events-poc"]
        self.assertEqual(serbia["tools"]["include"], MOSHE_TOOLS)
        self.assertEqual(serbia["env"]["INTELLIGENCE_POC_AUDIT"], MOSHE_AUDIT_PATH)
        self.assertIn("create_target_candidate", MOSHE_TOOLS)
        self.assertIn("present_requested_results", MOSHE_TOOLS)
        self.assertNotIn("execute_sql", MOSHE_TOOLS)

    def test_profile_selects_structured_evidence_references(self):
        soul = (ROOT / "moshe_profile" / "SOUL.md").read_text(encoding="utf-8")
        self.assertIn("evidence_layers", soul)
        self.assertIn("אל תכתוב שורת טקסט חופשי `מזהי ראיות:`", soul)

    def test_backend_merges_only_selected_agent_endpoint(self):
        base = {
            "remote_host": "127.0.0.1", "remote_port": 8642, "api_key": "secret",
            "audit_path": "/general/audit", "agents": {"moshe": {"remote_port": 8643, "audit_path": MOSHE_AUDIT_PATH}},
        }
        with patch.object(server, "load_hermes_config", return_value=base):
            general = server.load_agent_hermes_config("general")
            moshe = server.load_agent_hermes_config("moshe")
        self.assertEqual(general["remote_port"], 8642)
        self.assertEqual(general["audit_path"], "/general/audit")
        self.assertEqual(moshe["remote_port"], 8643)
        self.assertEqual(moshe["audit_path"], MOSHE_AUDIT_PATH)
        self.assertNotIn("agents", moshe)

    def test_service_uses_named_profile_and_resource_guard(self):
        unit = (ROOT / "moshe_profile" / "hermes-moshe-gateway.service").read_text(encoding="utf-8")
        self.assertIn("bin/hermes gateway run", unit)
        self.assertIn('Environment="HERMES_HOME=/home/ubuntu/.hermes/profiles/moshe"', unit)
        self.assertIn('Environment="API_SERVER_PORT=8643"', unit)
        self.assertIn("MemoryHigh=400M", unit)
        self.assertIn("MemoryMax=600M", unit)

    def test_frontend_sends_unmodified_current_message_for_routing(self):
        frontend = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("routing_prompt: clean", frontend)
        self.assertIn("routing_prompt: instruction", frontend)
        self.assertIn("/api/live-steps?agent=moshe", frontend)

    def test_backend_ignores_mentions_in_enriched_agent_prompt(self):
        previous = server.AGENT_ROUTES
        server.AGENT_ROUTES = AgentRouteRegistry()
        try:
            general = server.route_agent_request({
                "investigation_id": "chat-1",
                "routing_prompt": "שאלה כללית",
                "prompt": "שאלה כללית\nהוראת מערכת עם הדוגמה @משה",
            })
            moshe = server.route_agent_request({
                "investigation_id": "chat-1",
                "routing_prompt": "@משה בדוק יעד",
                "prompt": "@משה בדוק יעד\nהקשר נוסף",
            })
            continued = server.route_agent_request({
                "investigation_id": "chat-1", "routing_prompt": "@משה המשך", "prompt": "enriched",
            })
        finally:
            server.AGENT_ROUTES = previous
        self.assertEqual(general.responding_agent, "general")
        self.assertEqual(moshe.responding_agent, "moshe")
        self.assertEqual(continued.mission_run_id, moshe.mission_run_id)
        self.assertTrue(moshe.mission_started)
        self.assertFalse(continued.mission_started)


if __name__ == "__main__":
    unittest.main()

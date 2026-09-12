import unittest
import json
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import server
from general_persistent_profile.provision_profile import (
    GENERAL_PERSISTENT_AUDIT_PATH,
    GENERAL_PERSISTENT_PORT,
    configured_profile,
)
from general_persistent_profile.configure_ui_gateway import main as configure_ui_gateway


ROOT = Path(__file__).resolve().parent


class GeneralPersistentProfileTests(unittest.TestCase):
    def test_instruction_mode_is_explicit_and_defaults_to_inline(self):
        self.assertEqual(server.normalize_instruction_mode(None), "inline")
        self.assertEqual(server.normalize_instruction_mode("unexpected"), "inline")
        self.assertEqual(server.normalize_instruction_mode("persistent"), "persistent")

    def test_profile_uses_separate_port_and_audit_log(self):
        source = {
            "platforms": {
                "api_server": {"enabled": True, "host": "127.0.0.1", "port": 8642},
                "telegram": {"enabled": True},
            },
            "platform_toolsets": {"api_server": ["mcp-serbia-events-poc"], "telegram": ["all"]},
            "mcp_servers": {
                "serbia-events-poc": {
                    "env": {"INTELLIGENCE_POC_AUDIT": "/opt/serbia-poc/mcp_audit.jsonl"}
                }
            },
        }
        result = configured_profile(source)
        self.assertEqual(result["platforms"]["api_server"]["port"], GENERAL_PERSISTENT_PORT)
        self.assertEqual(set(result["platforms"]), {"api_server"})
        self.assertEqual(result["platform_toolsets"], {"api_server": ["mcp-serbia-events-poc"]})
        self.assertEqual(
            result["mcp_servers"]["serbia-events-poc"]["env"]["INTELLIGENCE_POC_AUDIT"],
            GENERAL_PERSISTENT_AUDIT_PATH,
        )

    def test_backend_merges_persistent_general_endpoint(self):
        base = {
            "remote_port": 8642,
            "api_key": "secret",
            "audit_path": "/general/audit",
            "agents": {
                "general_persistent": {
                    "remote_port": GENERAL_PERSISTENT_PORT,
                    "audit_path": GENERAL_PERSISTENT_AUDIT_PATH,
                }
            },
        }
        with patch.object(server, "load_hermes_config", return_value=base):
            candidate = server.load_agent_hermes_config("general_persistent")
        self.assertEqual(candidate["remote_port"], GENERAL_PERSISTENT_PORT)
        self.assertEqual(candidate["audit_path"], GENERAL_PERSISTENT_AUDIT_PATH)

    def test_soul_contains_core_general_contract(self):
        soul = (ROOT / "general_persistent_profile" / "SOUL.md").read_text(encoding="utf-8")
        for marker in (
            "classify_question_intent",
            "present_requested_results",
            "evidence_layers",
            "challenge_hypothesis",
            "@משה",
        ):
            self.assertIn(marker, soul)

    def test_service_uses_isolated_profile(self):
        unit = (ROOT / "general_persistent_profile" / "hermes-general-persistent-gateway.service").read_text(
            encoding="utf-8"
        )
        self.assertIn("profiles/generalpersistent", unit)
        self.assertIn('Environment="API_SERVER_PORT=8644"', unit)
        self.assertIn('Environment="TELEGRAM_ENABLED=false"', unit)
        self.assertIn('Environment="WHATSAPP_ENABLED=false"', unit)
        self.assertIn("MemoryMax=600M", unit)

    def test_ui_gateway_configuration_preserves_secret_and_other_agents(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / ".hermes-api.json"
            path.write_text(
                json.dumps({"api_key": "secret", "agents": {"moshe": {"remote_port": 8643}}}),
                encoding="utf-8",
            )
            with patch("sys.argv", ["configure_ui_gateway.py", "--config", str(path)]):
                self.assertEqual(configure_ui_gateway(), 0)
            result = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(result["api_key"], "secret")
        self.assertEqual(result["agents"]["moshe"]["remote_port"], 8643)
        self.assertEqual(result["agents"]["general_persistent"]["remote_port"], 8644)


if __name__ == "__main__":
    unittest.main()

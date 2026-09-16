import unittest
from pathlib import Path

from talia_profile.provision_profile import (
    ASSESSMENT_STORE_PATH,
    TALIA_MCP_SERVER_NAME,
    TALIA_TOOLS,
    restricted_config,
)


ROOT = Path(__file__).resolve().parent


class TaliaProfileTests(unittest.TestCase):
    def source_config(self):
        return {
            "platforms": {"api_server": {"enabled": True}},
            "mcp_servers": {
                "serbia-events-poc": {
                    "command": "/usr/bin/python3",
                    "args": ["/opt/serbia-poc/mcp_server/server.py"],
                    "env": {},
                    "tools": {"include": ["search_events"]},
                }
            },
        }

    def test_profile_exposes_assessment_tools_but_not_target_or_workstream_tools(self):
        config = restricted_config(self.source_config())
        self.assertEqual({TALIA_MCP_SERVER_NAME}, set(config["mcp_servers"]))
        server = config["mcp_servers"][TALIA_MCP_SERVER_NAME]
        self.assertEqual(TALIA_TOOLS, server["tools"]["include"])
        self.assertEqual(ASSESSMENT_STORE_PATH, server["env"]["INTELLIGENCE_POC_ASSESSMENT_STORE"])
        self.assertIn("create_enemy_assessment", TALIA_TOOLS)
        self.assertIn("present_requested_results", TALIA_TOOLS)
        self.assertFalse(any("target" in name or "workstream" in name for name in TALIA_TOOLS))

    def test_soul_preserves_evidence_assessment_target_boundary(self):
        soul = (ROOT / "talia_profile" / "SOUL.md").read_text(encoding="utf-8")
        for marker in ("EVD-*", "ASM-*", "אינה ראיה", "kind=assessments", "אל תיצרי או תעדכני מטרות"):
            self.assertIn(marker, soul)

    def test_frontend_exposes_talia_routing_and_assessment_presentation(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("/api/live-steps?agent=talia", app)
        self.assertIn('result.responding_agent === "talia"', app)
        self.assertIn('activeLayer.kind === "assessments"', app)
        self.assertIn('layer.kind === "assessments"', app)


if __name__ == "__main__":
    unittest.main()

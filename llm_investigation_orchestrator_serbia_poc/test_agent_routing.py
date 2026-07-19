import unittest
from unittest.mock import patch

from agent_routing import AgentRouteRegistry, GENERAL_AGENT_ID, MOSHE_AGENT_ID, mentions_moshe


class AgentRoutingTests(unittest.TestCase):
    def test_exact_current_message_mention_routes_to_moshe(self):
        self.assertTrue(mentions_moshe("@משה בדוק את המטרה"))
        self.assertTrue(mentions_moshe("בבקשה, @משה"))
        self.assertFalse(mentions_moshe("משה בדוק"))
        self.assertFalse(mentions_moshe("@משהו בדוק"))
        self.assertFalse(mentions_moshe("mail@משה.example"))

    @patch("agent_routing.secrets.token_hex", side_effect=["first", "second"])
    def test_consecutive_mentions_share_mission_and_nonmention_closes_it(self, _token):
        registry = AgentRouteRegistry()
        first = registry.route("chat-1", "@משה התחל")
        registry.bind_hermes_session("chat-1", first.mission_run_id, "hermes-session-1")
        second = registry.route("chat-1", "@משה המשך")
        general = registry.route("chat-1", "עכשיו שאלה כללית")
        later = registry.route("chat-1", "@משה משימה חדשה")
        self.assertEqual(first.responding_agent, MOSHE_AGENT_ID)
        self.assertTrue(first.mission_started)
        self.assertEqual(second.mission_run_id, first.mission_run_id)
        self.assertEqual(second.hermes_session_id, "hermes-session-1")
        self.assertEqual(general.responding_agent, GENERAL_AGENT_ID)
        self.assertTrue(general.mission_closed)
        self.assertNotEqual(later.mission_run_id, first.mission_run_id)
        self.assertIsNone(later.hermes_session_id)

    def test_history_cannot_trigger_moshe(self):
        registry = AgentRouteRegistry()
        decision = registry.route("chat-1", "המשך בבקשה")
        self.assertEqual(decision.responding_agent, GENERAL_AGENT_ID)

    def test_conversations_are_isolated(self):
        registry = AgentRouteRegistry()
        first = registry.route("chat-a", "@משה א")
        second = registry.route("chat-b", "@משה ב")
        self.assertNotEqual(first.mission_run_id, second.mission_run_id)

    def test_stale_session_binding_is_rejected(self):
        registry = AgentRouteRegistry()
        first = registry.route("chat-1", "@משה התחל")
        registry.route("chat-1", "עבור לכללי")
        with self.assertRaisesRegex(ValueError, "no longer active"):
            registry.bind_hermes_session("chat-1", first.mission_run_id, "stale")


if __name__ == "__main__":
    unittest.main()

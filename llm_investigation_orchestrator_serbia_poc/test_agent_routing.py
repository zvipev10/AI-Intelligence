import unittest
from unittest.mock import patch

from agent_routing import (
    AgentRouteRegistry,
    GENERAL_AGENT_ID,
    MOSHE_AGENT_ID,
    OPENAI_GENERAL_AGENT_ID,
    TALIA_AGENT_ID,
    mentions_moshe,
    mentions_openai_general,
    mentions_talia,
)


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

    def test_openai_general_is_explicit_and_does_not_replace_general(self):
        self.assertTrue(mentions_openai_general("@OpenAI בדוק את האירועים"))
        self.assertTrue(mentions_openai_general("@אופן איי בדוק את האירועים"))
        self.assertFalse(mentions_openai_general("OpenAI בדוק את האירועים"))
        self.assertFalse(mentions_openai_general("@OpenAIs בדוק את האירועים"))

        registry = AgentRouteRegistry()
        experimental = registry.route("chat-openai", "@OpenAI בדוק את האירועים")
        existing = registry.route("chat-existing", "בדוק את האירועים")

        self.assertEqual(experimental.responding_agent, OPENAI_GENERAL_AGENT_ID)
        self.assertFalse(experimental.mission_started)
        self.assertIsNone(experimental.mission_run_id)
        self.assertEqual(existing.responding_agent, GENERAL_AGENT_ID)

    def test_exact_talia_mention_routes_to_isolated_mission(self):
        self.assertTrue(mentions_talia("@טליה צרי הערכה"))
        self.assertTrue(mentions_talia("please ask @Talia"))
        self.assertFalse(mentions_talia("טליה צרי הערכה"))
        registry = AgentRouteRegistry()
        decision = registry.route("chat-t", "@טליה צרי הערכה")
        self.assertEqual(TALIA_AGENT_ID, decision.responding_agent)
        self.assertRegex(decision.mission_run_id, r"^talia-[0-9a-f]{16}-[0-9a-f]{12}$")

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

    def test_mission_id_stays_within_prompt_cache_key_limit(self):
        registry = AgentRouteRegistry()
        decision = registry.route("investigation-" + "x" * 500, "@משה בדוק")
        self.assertLessEqual(len(decision.mission_run_id), 64)
        self.assertRegex(decision.mission_run_id, r"^moshe-[0-9a-f]{16}-[0-9a-f]{12}$")


if __name__ == "__main__":
    unittest.main()

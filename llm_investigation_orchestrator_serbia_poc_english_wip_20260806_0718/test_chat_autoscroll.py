import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class ChatAutoScrollTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8")
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_new_user_messages_always_follow_the_bottom(self):
        self.assertIn(
            'const shouldFollow = role === "user" || conversationIsNearBottom();',
            self.app,
        )
        self.assertIn("followConversationAfterUpdate(shouldFollow);", self.app)

    def test_assistant_updates_follow_only_when_near_bottom(self):
        self.assertIn("const CONVERSATION_BOTTOM_THRESHOLD_PX = 96;", self.app)
        self.assertIn("function conversationIsNearBottom()", self.app)
        self.assertIn(
            "conversation.scrollHeight - conversation.scrollTop - conversation.clientHeight <= CONVERSATION_BOTTOM_THRESHOLD_PX",
            self.app,
        )
        self.assertIn("const shouldFollow = conversationIsNearBottom();", self.app)

    def test_live_step_rebuild_uses_one_scroll_decision(self):
        self.assertIn("manageConversationScroll: false", self.app)
        self.assertIn(
            "options.manageConversationScroll !== false && conversationIsNearBottom()",
            self.app,
        )

    def test_asset_version_is_bumped(self):
        self.assertIn('app.js?v=153', self.index)


if __name__ == "__main__":
    unittest.main()

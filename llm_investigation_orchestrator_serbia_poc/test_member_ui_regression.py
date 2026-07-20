import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class MemberUiRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8")
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_member_container_and_renderer_are_both_present(self):
        self.assertIn('id="michlolTeam"', self.index)
        self.assertIn("function renderMichlolTeam()", self.app)
        self.assertIn("renderMichlolTeam();", self.app)

    def test_member_roster_includes_moshe(self):
        self.assertIn('displayName: "משה"', self.app)
        self.assertIn('id: "moshe-targets-officer"', self.app)

    def test_at_mention_autocomplete_is_wired(self):
        self.assertIn("function activeMentionRange(textarea)", self.app)
        self.assertIn("function matchingTeamMembers(query)", self.app)
        self.assertIn("function chooseTeamMention(index = teamMentionState.activeIndex)", self.app)
        self.assertIn('menu.setAttribute("aria-label", "בחירת חבר מכלול")', self.app)

    def test_mentions_stop_before_punctuation_and_remain_highlighted_after_send(self):
        self.assertIn(r'const mentionPattern = /@([\p{L}\p{N}_-]+)/gu;', self.app)
        self.assertIn('appendMessage("user", `<p>${highlightedPromptHtml(clean)}</p>`);', self.app)

    def test_moshe_member_opening_comes_from_agent(self):
        self.assertIn("async function appendAgentMemberOpeningMessage(member)", self.app)
        self.assertIn('routing_prompt: "@משה"', self.app)
        self.assertIn("if (member.id === MOSHE_MEMBER_ID) appendAgentMemberOpeningMessage(member);", self.app)

    def test_shared_agent_result_entry_point_is_retained(self):
        self.assertIn("function applyAgentResult(result, prompt, options = {})", self.app)
        self.assertNotIn("function applyHermesResult(", self.app)

    def test_attack_targets_use_the_shared_layer_pipeline(self):
        self.assertIn("function buildTypedResultLayers(result = {})", self.app)
        self.assertIn('layer.kind === "attack_targets"', self.app)
        self.assertNotIn("function renderMoshe", self.app)
        self.assertNotIn("function applyMoshe", self.app)
        self.assertIn("target-raw-references", self.app)
        self.assertIn("target.raw_data_references || []", self.app)


if __name__ == "__main__":
    unittest.main()

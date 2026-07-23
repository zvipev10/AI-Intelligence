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

    def test_moshe_answers_use_targets_officer_title(self):
        self.assertIn('const MOSHE_MESSAGE_LABEL = "משה - קצין מטרות";', self.app)
        self.assertIn('result.responding_agent === "moshe" ? MOSHE_MESSAGE_LABEL', self.app)
        self.assertIn('label.textContent = resultMessageLabel(options.result);', self.app)

    def test_shared_agent_result_entry_point_is_retained(self):
        self.assertIn("function applyAgentResult(result, prompt, options = {})", self.app)
        self.assertNotIn("function applyHermesResult(", self.app)

    def test_csv_parser_only_opens_quotes_at_the_start_of_a_field(self):
        self.assertIn("let atFieldStart = true;", self.app)
        self.assertIn("else if (char === '\"' && atFieldStart)", self.app)
        self.assertNotIn("else if (char === '\"') quoted = !quoted;", self.app)

    def test_attack_targets_use_the_shared_layer_pipeline(self):
        self.assertIn("function buildTypedResultLayers(result = {})", self.app)
        self.assertIn('layer.kind === "attack_targets"', self.app)
        self.assertNotIn("function renderMoshe", self.app)
        self.assertNotIn("function applyMoshe", self.app)
        self.assertIn("target-raw-references", self.app)
        self.assertIn("target.raw_data_references || []", self.app)

    def test_persisted_attack_targets_are_a_refreshable_catalog_layer(self):
        self.assertIn('const ATTACK_TARGET_CATALOG_LAYER_ID = "attack-targets:all";', self.app)
        self.assertIn("async function refreshOpenAttackTargetCatalogLayer()", self.app)
        self.assertIn('typedLayers.some(layer => layer.kind === "attack_targets")', self.app)

    def test_target_table_shows_source_types_and_plain_raw_record_count(self):
        self.assertIn("<th>סוגי מקור</th><th>רשומות גולמיות</th>", self.app)
        self.assertNotIn("<th>מקורות עצמאיים</th>", self.app)
        self.assertIn("item.source_types || []", self.app)
        self.assertIn("item.evidence_count || (item.raw_data_references || []).length", self.app)
        self.assertNotIn("function targetEvidenceHtml", self.app)
        self.assertNotIn("הסבר מיזוג:", self.app)

    def test_moshe_tools_use_readable_shared_activity_labels(self):
        self.assertIn('prepare_target_candidate: "הכנת מועמד מטרה"', self.app)
        self.assertIn('create_target_candidate: "יצירת מועמד מטרה"', self.app)
        self.assertIn('attach_target_evidence: "צירוף ראיות למטרה"', self.app)


if __name__ == "__main__":
    unittest.main()

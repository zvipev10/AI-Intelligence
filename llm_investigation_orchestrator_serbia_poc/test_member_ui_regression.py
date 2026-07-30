import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class MemberUiRegressionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8")
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.styles = (ROOT / "styles.css").read_text(encoding="utf-8")

    def test_member_container_and_renderer_are_both_present(self):
        self.assertIn('id="michlolTeam"', self.index)
        self.assertIn("function renderMichlolTeam()", self.app)
        self.assertIn("renderMichlolTeam();", self.app)

    def test_member_icons_have_separated_click_targets(self):
        self.assertIn(".michlol-team {", self.styles)
        self.assertIn("gap: 9px", self.styles.split(".michlol-team {", 1)[1].split("}", 1)[0])
        member_rule = self.styles.split(".michlol-member {", 1)[1].split("}", 1)[0]
        self.assertIn("min-width: 34px", member_rule)
        self.assertIn("min-height: 34px", member_rule)
        more_rule = self.styles.split(".michlol-more summary {", 1)[1].split("}", 1)[0]
        self.assertIn("width: 34px", more_rule)
        self.assertIn("height: 34px", more_rule)

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

    def test_selected_member_is_implicitly_addressed_without_changing_visible_message(self):
        self.assertIn("function addressedPromptForSelectedMember(prompt)", self.app)
        self.assertIn("return member ? `@${member.displayName} ${clean}` : clean;", self.app)
        self.assertIn("const addressedPrompt = addressedPromptForSelectedMember(clean);", self.app)
        self.assertIn("routing_prompt: addressedPrompt", self.app)
        self.assertIn('appendMessage("user", `<p>${highlightedPromptHtml(clean)}</p>`);', self.app)

    def test_pressing_selected_member_again_returns_to_general_chat(self):
        self.assertIn("if (state.activeConversationMemberId === member.id)", self.app)
        self.assertIn("state.activeConversationMemberId = null;", self.app)
        self.assertIn('conversation.querySelectorAll(".member-welcome-message").forEach(message => message.remove());', self.app)
        self.assertIn("if (state.workstreamComposerMode) setWorkstreamComposerMode(false);", self.app)

    def test_explicit_mentions_take_precedence_over_selected_member(self):
        self.assertIn("if (!clean || teamMentionsForPrompt(clean).length) return clean;", self.app)

    def test_moshe_member_opening_is_immediate_and_hardcoded(self):
        self.assertIn("const MOSHE_WELCOME =", self.app)
        self.assertIn(
            "member.id === MOSHE_MEMBER_ID ? MOSHE_WELCOME : MICHLOL_MEMBER_WELCOME",
            self.app,
        )
        self.assertIn("appendMemberWelcomeMessage(member);", self.app)
        self.assertNotIn("appendAgentMemberOpeningMessage", self.app)

    def test_member_welcome_uses_general_assistant_background(self):
        rule = self.styles.split(".member-welcome-message {", 1)[1].split("}", 1)[0]
        self.assertNotIn("background:", rule)
        self.assertIn(".assistant-message {", self.styles)

    def test_moshe_answers_use_targets_officer_title(self):
        self.assertIn('const MOSHE_MESSAGE_LABEL = "משה - קצין מטרות";', self.app)
        self.assertIn('result.responding_agent === "moshe" ? MOSHE_MESSAGE_LABEL', self.app)
        self.assertIn('label.textContent = resultMessageLabel(options.result);', self.app)

    def test_shared_agent_result_entry_point_is_retained(self):
        self.assertIn("function applyAgentResult(result, prompt, options = {})", self.app)
        self.assertNotIn("function applyHermesResult(", self.app)

    def test_show_results_uses_only_explicit_requested_result_layers(self):
        self.assertIn("return (result.requested_result_layers || [])", self.app)
        self.assertNotIn("return (result.layers || [])", self.app)
        self.assertIn("const hasRequestedResults = buildTypedResultLayers(options.result).length > 0;", self.app)
        self.assertIn('${hasRequestedResults ? `<button type="button" class="final-answer-show-btn', self.app)

    def test_final_requested_results_wait_for_explicit_button_press(self):
        apply_body = self.app.split("function applyAgentResult(result, prompt, options = {})", 1)[1].split("async function runSavedQuestion", 1)[0]
        self.assertEqual(apply_body.count("addResultLayers({"), 1)
        self.assertIn("if (options.restoreOnly)", apply_body)
        self.assertIn("layers: typedLayers", apply_body)
        self.assertNotIn("activateView(requestedView, { automatic: true", apply_body)
        self.assertIn("toggleFinalAnswerVisibility(options.result", self.app)

    def test_evidence_references_are_structured_separate_and_manual(self):
        self.assertIn("function buildEvidenceReferenceLayers(result = {})", self.app)
        self.assertIn("return (result.evidence_reference_layers || [])", self.app)
        self.assertIn("function buildEvidenceReferencesSection(result)", self.app)
        self.assertIn("מזהי ראיות · ${layers.length.toLocaleString", self.app)
        self.assertIn("identifiers.slice(0, 14)", self.app)
        self.assertIn("function toggleEvidenceReferenceLayer(result, layer, btn)", self.app)
        self.assertIn("layers: [layer]", self.app)
        self.assertIn("if (evidenceReferences && evidenceToggle)", self.app)
        self.assertNotIn("buildResultLayers({\n      events:", self.app)

    def test_evidence_section_and_layers_start_collapsed(self):
        self.assertIn('const section = document.createElement("details");', self.app)
        self.assertIn('class="evidence-references-summary"', self.app)
        self.assertIn('<details class="evidence-reference-details">', self.app)
        self.assertNotIn('<details open class="evidence-reference-details">', self.app)

    def test_evidence_layer_visibility_is_independent_from_requested_results(self):
        self.assertIn("evidenceLayerSourceId(result, layer)", self.app)
        self.assertIn("evidence:${finalSourceId(result)}:${layer.dataId}", self.app)
        self.assertIn("updateEvidenceReferenceButtons();", self.app)
        self.assertIn('layer.preferredView === "timeline" ? "ציר זמן" : "מפה"', self.app)
        self.assertIn("state.rawOverlayMinimized = false;", self.app)
        self.assertIn("activateView(layer.preferredView", self.app)
        self.assertIn("renderAllViews();", self.app)

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
        self.assertIn('buildTypedResultLayers(result).some(layer => layer.kind === "attack_targets")', self.app)

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

    def test_recording_save_button_uses_explicit_label(self):
        self.assertIn('options.result.saved_question_id ? "נשמר" : "שמור הקלטה"', self.app)
        self.assertIn('button.textContent = "שמור הקלטה";', self.app)

    def test_agent_waiting_message_is_temporary_animated_thinking_indicator(self):
        styles = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn("function thinkingIndicatorHtml()", self.app)
        self.assertIn('aria-label="חושב"', self.app)
        self.assertIn("thinking-dot 1.05s infinite", styles)
        self.assertIn("@media (prefers-reduced-motion: reduce)", styles)
        self.assertNotIn("Hermes מנתח את הבקשה ומפעיל כלי חקירה", self.app)
        self.assertNotIn("Hermes ממשיך את החקירה", self.app)
        self.assertNotIn("משה מתחבר לשיחה", self.app)
        self.assertNotIn("member-opening-status", self.app)
        self.assertNotIn("state.activeActivityEmpty.hidden = true;", self.app)
        self.assertLess(
            self.app.index('<ol class="activity-list"></ol>'),
            self.app.index('<div class="activity-empty">${message ? escapeHtml(message) : thinkingIndicatorHtml()}</div>')
        )
        self.assertIn("if (research) research.replaceWith(details);", self.app)


if __name__ == "__main__":
    unittest.main()

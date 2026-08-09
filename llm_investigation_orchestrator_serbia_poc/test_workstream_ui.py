import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class WorkstreamUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8")
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.styles = (ROOT / "styles.css").read_text(encoding="utf-8")

    def test_plus_menu_enters_tracking_mode(self):
        self.assertIn('data-prompt-option="workstream">מעקב</button>', self.index)
        self.assertIn('promptOption.dataset.promptOption === "workstream"', self.app)
        self.assertIn("startWorkstreamComposerMode()", self.app)

    def test_tracking_does_not_require_or_attach_a_layer(self):
        self.assertNotIn("כדי ליצור מעקב יש לצרף שכבה אחת במפורש.", self.app)
        self.assertNotIn("starting_source: workstreamLayerReference(layer)", self.app)
        self.assertNotIn("if (state.promptSelectedLayerIds.size !== 1) openQueryLayersModal()", self.app)
        self.assertNotIn("starting_source", self.app)
        self.assertNotIn("data-workstream-open-layer", self.app)

    def test_creation_is_a_moshe_conversation_without_inline_confirmation(self):
        self.assertIn("workstream_creation_requested: workstreamCreationRequested", self.app)
        self.assertIn("routing_prompt: addressedPrompt", self.app)
        self.assertIn("result.workstream_created", self.app)
        self.assertNotIn("pendingWorkstreamDraft", self.app)
        self.assertNotIn("data-workstream-confirm", self.app)
        self.assertNotIn("data-workstream-cancel", self.app)

    def test_internal_workstream_tools_are_not_rendered_as_investigation_steps(self):
        self.assertIn("internalWorkstreamTools", self.app)
        self.assertIn(
            "(steps || []).filter(step => !internalWorkstreamTools.has(step.tool))",
            self.app,
        )

    def test_workstreams_have_a_dedicated_workspace_rail(self):
        self.assertIn('id="workstreamRail"', self.index)
        self.assertIn('id="workstreamRailList"', self.index)
        self.assertIn('id="workstreamRailToggle"', self.index)
        self.assertNotIn('id="workstreamIndicator"', self.index)
        self.assertNotIn('id="workstreamMenu"', self.index)
        self.assertIn("appendWorkstreamUpdate", self.app)
        self.assertIn("workstream-rail-visible", self.app)

    def test_multiple_workstreams_are_visible_at_a_glance(self):
        self.assertIn("data-workstream-show", self.app)
        self.assertIn("workstreamRailList.innerHTML", self.app)
        self.assertIn("workstream-rail-card", self.app)
        self.assertNotIn("על איזה מהם להציג עדכון?", self.app)

    def test_workstream_rail_tracks_unseen_changes(self):
        self.assertIn("serbia-poc-workstream-seen-v1", self.app)
        self.assertIn("function workstreamHasNewItems(workstream)", self.app)
        self.assertIn("function markWorkstreamSeen(workstream)", self.app)
        self.assertIn("updated_at_utc", self.app)
        self.assertIn("workstream-new-badge", self.app)

    def test_workstream_rail_is_only_visible_in_real_time(self):
        self.assertIn('state.investigationPlayback?.mode === "real_time"', self.app)
        self.assertIn("workstreamRail.hidden = !visible", self.app)

    def test_tracking_option_is_only_visible_for_moshe(self):
        self.assertIn("option.hidden = state.activeConversationMemberId !== MOSHE_MEMBER_ID", self.app)
        self.assertIn("if (state.activeConversationMemberId !== MOSHE_MEMBER_ID) return;", self.app)

    def test_reopening_replaces_the_previous_copy(self):
        self.assertIn("data-workstream-update-id", self.app)
        self.assertIn("message.dataset.workstreamUpdateId = workstream.workstream_id", self.app)

    def test_reopened_summary_deduplicates_title_objective_and_responsibility(self):
        self.assertIn("function normalizedWorkstreamSummaryText(value)", self.app)
        self.assertIn("const renderedValues = new Set([normalizedWorkstreamSummaryText(title)]);", self.app)
        self.assertIn("if (!normalized || renderedValues.has(normalized)) return", self.app)
        self.assertIn("${objectiveHtml}", self.app)
        self.assertIn("${responsibilityHtml}", self.app)

    def test_workstream_update_has_no_workstream_specific_playback_control(self):
        self.assertIn("workstream.objective", self.app)
        self.assertIn("workstream.assignments", self.app)
        self.assertNotIn("data-playback-next", self.app)
        self.assertNotIn("advanceWorkstreamPlayback", self.app)
        self.assertNotIn("/api/workstreams/${encodeURIComponent(workstreamId)}/playback", self.app)
        self.assertNotIn(".playback-next-button", self.styles)
        self.assertIn("data-workstream-archive", self.app)

    def test_workstream_update_can_show_filtered_results(self):
        self.assertIn("data-workstream-results", self.app)
        self.assertIn("toggleWorkstreamResultVisibility", self.app)
        self.assertIn("/presentation", self.app)
        self.assertIn("workstreamResultSourceId", self.app)
        self.assertIn("final-answer-show-btn layers-hidden", self.app)
        self.assertIn('<span class="final-answer-show-label">הצג תוצאות</span>', self.app)
        self.assertIn("Array.isArray(workstream.target_ids)", self.app)
        self.assertIn("targetIds.some", self.app)
        self.assertIn("artifact.content?.indications", self.app)

    def test_investigation_playback_control_is_visible_in_upper_bar(self):
        self.assertIn('id="playbackNextButton"', self.index)
        self.assertIn('class="playback-header-button"', self.index)
        self.assertIn('id="intelligenceModeSelect"', self.index)
        self.assertIn('value="historical">מידע היסטורי', self.index)
        self.assertIn('value="real_time">זמן אמת', self.index)
        self.assertIn('id="intelligencePeriod"', self.index)
        self.assertIn("/api/playback/next", self.app)
        self.assertIn("/api/playback/mode", self.app)
        self.assertIn("investigation_id: state.investigationId", self.app)
        self.assertIn("advanceInvestigationPlayback", self.app)
        self.assertIn("changeIntelligenceMode", self.app)
        self.assertNotIn("initializeHistoricalPlayback", self.app)
        self.assertIn('state.investigationPlayback?.mode !== "real_time"', self.app)
        self.assertIn("reevaluation?.assessment?.answer", self.app)
        self.assertIn("appendMoshePlaybackAssessment", self.app)
        self.assertIn("buildTypedResultLayers(result)", self.app)
        self.assertIn("toggleFinalAnswerVisibility(result, \"\", button)", self.app)
        self.assertIn(".playback-header-button", self.styles)

    def test_boot_does_not_reset_playback_or_change_investigation_identity(self):
        boot_start = self.app.index("async function boot()")
        boot = self.app[boot_start:]
        self.assertNotIn("initializeHistoricalPlayback", boot)
        self.assertIn("await loadWorkstreams();", boot)
        self.assertNotIn("allowLatestFallback", boot)

    def test_reopened_workstream_shows_active_artifact_details(self):
        self.assertIn("function workstreamArtifactHtml(workstream)", self.app)
        self.assertIn("content.lead_statement", self.app)
        self.assertIn("content.indications", self.app)
        self.assertIn("content.gaps", self.app)
        self.assertIn("artifact.revision", self.app)
        self.assertIn("WORKSTREAM_ARTIFACT_STATUS_LABELS", self.app)

    def test_archive_runs_immediately_without_chat_confirmation(self):
        self.assertIn(
            "void archiveWorkstreamFromChat(archiveWorkstream.dataset.workstreamArchive);",
            self.app,
        )
        self.assertNotIn("requestWorkstreamArchive", self.app)
        self.assertNotIn("data-workstream-archive-confirm", self.app)
        self.assertNotIn("data-workstream-archive-cancel", self.app)

    def test_workstreams_reload_with_investigation(self):
        self.assertIn("async function loadWorkstreams()", self.app)
        self.assertIn("loadWorkstreams();", self.app)
        self.assertIn("renderWorkstreamIndicator();", self.app)

    def test_workstreams_cannot_replace_selected_investigation(self):
        self.assertNotIn("adoptCanonicalWorkstreamInvestigation", self.app)
        self.assertNotIn("fallback=latest", self.app)
        self.assertNotIn("allowLatestFallback", self.app)
        self.assertIn(
            "fetch(`/api/workstreams?investigation_id=${encodeURIComponent(investigationId)}`",
            self.app,
        )

    def test_explicit_investigation_selection_loads_only_selected_context(self):
        self.assertIn("void loadSelectedInvestigation(investigation.id);", self.app)
        self.assertIn("async function loadSelectedInvestigation(investigationId)", self.app)
        self.assertIn("if (state.investigationId !== investigationId) return;", self.app)
        self.assertIn(
            "token !== state.workstreamLoadToken || investigationId !== state.investigationId",
            self.app,
        )

    def test_investigation_list_is_independent_from_active_name(self):
        self.assertIn('investigationSearchQuery: ""', self.app)
        self.assertIn("matchingInvestigations(state.investigationSearchQuery)", self.app)
        self.assertIn("state.investigationSearchQuery = investigationInput.value;", self.app)
        self.assertNotIn("matchingInvestigations(investigationInput.value)", self.app)

    def test_old_investigation_registry_is_removed(self):
        self.assertIn(
            'const INVESTIGATIONS_STORAGE_KEY = "serbia-poc-investigations-v2";',
            self.app,
        )
        self.assertIn(
            'const LEGACY_INVESTIGATIONS_STORAGE_KEYS = ["serbia-poc-investigations-v1"];',
            self.app,
        )
        self.assertIn(
            "LEGACY_INVESTIGATIONS_STORAGE_KEYS.forEach(key => localStorage.removeItem(key));",
            self.app,
        )

    def test_tracking_and_workstream_messages_have_visible_states(self):
        self.assertIn(".prompt-form.tracking-mode", self.styles)
        self.assertIn(".workstream-message", self.styles)
        self.assertIn(".workstream-rail[hidden]", self.styles)
        self.assertIn(".workstream-rail-card.has-new", self.styles)

    def test_workstream_rail_is_responsive_and_collapsible(self):
        self.assertIn(".workspace.workstream-rail-visible", self.styles)
        self.assertIn(".workstream-rail.collapsed", self.styles)
        self.assertIn(".workstream-rail { order: -1; width: 100%;", self.styles)

    def test_moshe_proposal_is_staged_in_general_chat_state(self):
        self.assertIn("pendingMosheWorkstreamProposal", self.app)
        self.assertIn("workstreamContextForChat(currentTurnMessageId)", self.app)
        self.assertIn("applyWorkstreamChatResult(result)", self.app)
        self.assertIn("result.workstream_artifact", self.app)
        self.assertNotIn("data-workstream-proposal-confirm", self.app)

    def test_thinking_indicator_is_preserved(self):
        self.assertIn("function thinkingIndicatorHtml()", self.app)
        self.assertIn('aria-label="חושב"', self.app)
        self.assertIn("thinkingIndicatorHtml()", self.app)
        self.assertIn(".thinking-indicator", self.styles)
        self.assertIn("@keyframes thinking-dot", self.styles)


if __name__ == "__main__":
    unittest.main()

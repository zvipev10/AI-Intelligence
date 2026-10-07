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

    def test_result_header_places_tabs_left_and_layer_search_right(self):
        tabs = self.index.split('<nav class="view-tabs"', 1)[1].split("</nav>", 1)[0]
        self.assertLess(tabs.index('class="view-tab-list"'), tabs.index('class="layer-selector"'))
        actions = tabs.split('class="view-tabs-actions"', 1)[1]
        self.assertIn('id="memoryButton" class="view-tab memory-presentation-button"', actions)
        self.assertLess(actions.index('id="memoryButton"'), actions.index('class="layer-selector"'))
        self.assertNotIn('id="memoryButton"', self.index.split('<nav class="view-tabs"', 1)[0])
        view_tabs_rule = self.styles.split(".view-tabs {", 1)[1].split("}", 1)[0]
        self.assertIn("justify-content: space-between", view_tabs_rule)
        self.assertIn("direction: ltr", view_tabs_rule)
        self.assertIn(".view-tabs-actions {", self.styles)
        layer_selector_rule = self.styles.split(".layer-selector {", 1)[1].split("}", 1)[0]
        self.assertIn("position: relative", layer_selector_rule)
        self.assertNotIn("position: absolute", layer_selector_rule)
        self.assertIn(
            ".result-panel { border: 0; border-radius: 0; background: transparent; }",
            self.styles,
        )

    def test_mobile_results_table_keeps_intrinsic_column_widths(self):
        mobile = self.styles.split("@media (max-width: 760px)", 1)[1]
        self.assertIn(
            ".raw-events-table table { width: max-content; min-width: max-content; table-layout: auto; }",
            mobile,
        )
        self.assertNotIn(".raw-events-table table { width: 880px; min-width: 880px; table-layout: fixed; }", mobile)

    def test_member_roster_includes_moshe(self):
        self.assertIn('displayName: "משה"', self.app)
        self.assertIn('id: "moshe-targets-officer"', self.app)

    def test_naama_and_gadi_define_specialist_workspace_defaults(self):
        self.assertIn('roleLabel: "קצינת סיגינט"', self.app)
        self.assertIn('roleLabel: "SIGINT Officer"', self.app)
        self.assertIn('workspaceRole: "sigint"', self.app)
        self.assertIn('roleLabel: "קצין ויזינט"', self.app)
        self.assertIn('roleLabel: "VISINT Officer"', self.app)
        self.assertIn('workspaceRole: "visint"', self.app)
        self.assertIn('defaultCatalogLayerId: "events:Cellular Calls"', self.app)
        self.assertIn('defaultCatalogLayerId: "events:Satellite"', self.app)
        self.assertIn('openDefaultCall: true', self.app)

    def test_specialist_members_are_the_first_two_selection_icons(self):
        for locale in ("he", "en"):
            roster = self.app.split(f"  {locale}: [", 1)[1].split("\n  ],", 1)[0]
            self.assertLess(roster.index('workspaceRole: "sigint"'), roster.index('workspaceRole: "visint"'))
            self.assertLess(roster.index('workspaceRole: "visint"'), roster.index('moshe-targets-officer'))

    def test_specialist_selection_is_limited_to_saved_investigation_workspaces(self):
        self.assertIn('function roleWorkspaceSelectionAvailable()', self.app)
        self.assertIn('return state.pageView === "workspace" && !state.draftSessionActive;', self.app)
        self.assertIn('michlolTeam.hidden = !available;', self.app)
        self.assertIn('if (!roleWorkspaceSelectionAvailable()) return;', self.app)

    def test_specialist_scope_filters_catalog_and_open_result_layers(self):
        self.assertIn('function roleWorkspaceAllowsCatalogLayer(layerId)', self.app)
        self.assertIn('function roleWorkspaceLayers(layers = state.layers)', self.app)
        self.assertIn('return roleWorkspaceLayers().filter(layer => layer.visible', self.app)
        self.assertIn('.filter(layer => roleWorkspaceAllowsCatalogLayer(layer.id))', self.app)
        self.assertIn('if (!options.roleDefault && !options.memoryRestore && !roleWorkspaceAllowsCatalogLayer(layerId)) return null;', self.app)

    def test_pressing_selected_member_again_returns_to_full_workspace(self):
        body = self.app.split("function selectTeamMember(memberId)", 1)[1].split("\n}", 1)[0]
        self.assertIn("if (state.activeTeamMemberId === member.id)", body)
        self.assertIn("state.activeTeamMemberId = null;", body)
        self.assertIn("void applyRoleWorkspace(null);", body)
        self.assertIn('selectTeamMember(michlolMember.dataset.memberId);', self.app)

    def test_role_layers_match_the_localized_calls_layer(self):
        self.assertIn('const CATALOG_LAYER_ALIASES = { "events:שיחות סלולר": "events:Cellular Calls" };', self.app)
        self.assertIn("profile.allowedCatalogLayerIds.has(canonicalCatalogLayerId(layerId))", self.app)
        self.assertIn("openCatalogLayer(resolveCatalogLayerId(profile.defaultCatalogLayerId), { silent: true, roleDefault: true })", self.app)

    def test_removed_chat_and_agent_ui_is_gone(self):
        for marker in ('id="conversationPanel"', 'id="promptForm"', 'id="chatPanelToggle"', 'id="workstreamRail"',
                       'id="playbackNextButton"', 'id="recordedModal"', 'id="stepInjectModal"', 'id="queryModal"',
                       'id="agentStatusIndicator"', 'id="suggestions"'):
            self.assertNotIn(marker, self.index)
        for endpoint in ("/api/investigate", "/api/live-steps", "/api/agent-queue", "/api/performance-client",
                         "/api/saved-question", "/api/recorded-", "/api/workstreams", "/api/playback", "/api/scenario",
                         "chat-summary", "evidence:all", "attack-targets:all", "X-Demo-Generation"):
            self.assertNotIn(endpoint, self.app)
        self.assertNotIn("function runPrompt(", self.app)
        self.assertNotIn("teamMentionsForPrompt", self.app)
        self.assertNotIn(".conversation-panel", self.styles)
        self.assertIn("grid-template-columns: minmax(420px, 1fr)", self.styles.split(".workspace {", 1)[1].split("}", 1)[0])

    def test_csv_parser_only_opens_quotes_at_the_start_of_a_field(self):
        self.assertIn("let atFieldStart = true;", self.app)
        self.assertIn("else if (char === '\"' && atFieldStart)", self.app)
        self.assertNotIn("else if (char === '\"') quoted = !quoted;", self.app)

    def test_every_result_column_supports_filtering_and_sorting(self):
        self.assertIn("function enhanceResultsTable(layer)", self.app)
        self.assertIn('data-result-sort="${column}"', self.app)
        self.assertIn('data-result-filter="${column}"', self.app)
        self.assertIn("function applyResultTableControls(layerId)", self.app)
        self.assertIn("resultTableControls: new Map()", self.app)
        self.assertIn(".result-column-sort", self.styles)
        self.assertIn(".result-column-filter", self.styles)
        self.assertIn(".result-column-filter-toggle", self.styles)
        self.assertIn('data-result-filter-toggle="${column}"', self.app)
        self.assertIn('class="result-column-title"', self.app)
        self.assertIn('class="result-column-actions"', self.app)
        self.assertIn('event.key === "Enter" || event.key === "Escape"', self.app)
        self.assertIn('!event.target.closest(".result-column-filter-popover, .result-column-filter-toggle")', self.app)


if __name__ == "__main__":
    unittest.main()

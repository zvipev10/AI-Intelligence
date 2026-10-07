import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class WelcomePageContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8")
        cls.styles = (ROOT / "styles.css").read_text(encoding="utf-8")

    def test_welcome_is_initial_view_and_workspace_is_preserved(self):
        self.assertIn('id="welcomePage" class="welcome-page"', self.index)
        self.assertIn('<main class="workspace" hidden>', self.index)
        self.assertIn('setPageView("welcome", { focus: false });', self.app)
        self.assertIn('state.map?.resize();', self.app)

    def test_app_is_english_only_without_a_language_switch(self):
        self.assertNotIn('id="localeToggle"', self.index)
        self.assertNotIn("switchLocale", self.app)
        self.assertIn('const INITIAL_LOCALE = "en";', self.app)
        self.assertIn('<html lang="en" dir="ltr"', self.index)
        self.assertIn('renderWelcomePage();', self.app)
        self.assertIn('data-i18n-text-he="החקירות שלי" data-i18n-text-en="My investigations"', self.index)

    def test_real_investigation_and_members_are_rendered_from_state(self):
        self.assertIn("ownedInvestigations.map(ownedInvestigationRibbonHtml)", self.app)
        self.assertIn("currentMembers().slice(0, Math.min(5, participantCount))", self.app)
        self.assertIn('data-open-investigation=', self.app)
        self.assertIn('data-welcome-action="invite"', self.app)
        self.assertIn('activeLocaleText("הזמנה / הוספה", "Invite / add")', self.app)
        ribbon = self.app.split("function ownedInvestigationRibbonHtml(investigation)", 1)[1].split("\nfunction ", 1)[0]
        self.assertIn("investigation.layer_count", ribbon)
        self.assertIn("investigation.collection_request_count", ribbon)
        self.assertNotIn("2 items need attention", ribbon)

    def test_investigation_list_comes_from_the_server(self):
        load = self.app.split("async function loadInvestigations()", 1)[1].split("\n}", 1)[0]
        self.assertIn('fetch(buildLocaleApiUrl("/api/investigations")', load)
        self.assertIn(".map(investigationFromServer)", load)
        self.assertIn("LEGACY_INVESTIGATIONS_STORAGE_KEYS.forEach(key => scenarioStorage.removeItem(key));", load)
        self.assertNotIn("INVESTIGATIONS_STORAGE_KEY,", self.app)
        self.assertNotIn("function saveInvestigationRegistry", self.app)
        create = self.app.split("async function createInvestigation(name, id = createInvestigationId())", 1)[1].split("\n}", 1)[0]
        self.assertIn("await registerInvestigationRecord({ id, name: safeName })", create)
        self.assertIn('fetch("/api/investigations", {', self.app)
        self.assertIn("await loadInvestigations();", self.app)

    def test_welcome_has_no_new_investigation_action(self):
        welcome_markup = self.index.split('<main id="welcomePage"', 1)[1].split('</main>', 1)[0]
        self.assertNotIn('investigationAddButton', welcome_markup)
        self.assertNotIn('New investigation', welcome_markup)

    def test_welcome_action_starts_a_draft_investigation(self):
        welcome_markup = self.index.split('<main id="welcomePage"', 1)[1].split('</main>', 1)[0]
        self.assertIn('id="welcomeDraftButton"', welcome_markup)
        self.assertIn('data-i18n-text-en="Start exploring in a draft investigation"', welcome_markup)
        self.assertNotIn('welcomePromptForm', welcome_markup)
        self.assertIn('function startDraftInvestigation()', self.app)
        self.assertIn('state.draftSessionActive = true;', self.app)
        self.assertIn('state.investigationId = createInvestigationId();', self.app)
        start_draft = self.app.split('function startDraftInvestigation()', 1)[1].split('\n}', 1)[0]
        self.assertNotIn('ensureInvestigationRecord', start_draft)
        self.assertNotIn('registerInvestigationRecord', start_draft)
        self.assertIn('setPageView("workspace", { focus: false });', start_draft)
        self.assertIn('welcomeDraftButton?.addEventListener("click", () => startDraftInvestigation());', self.app)
        self.assertIn('.welcome-draft-button', self.styles)

    def test_welcome_action_sits_in_the_register_header_and_assets_are_versioned(self):
        intro = self.index.split('<section class="welcome-intro"', 1)[1].split('</section>', 1)[0]
        self.assertIn('id="welcomeDraftButton"', intro)
        self.assertIn(".welcome-actions { display: flex; justify-content: flex-end;", self.styles)
        self.assertIn('href="./styles.css?v=182"', self.index)
        self.assertIn('src="./demo_bootstrap.js?v=245"', self.index)

    def test_welcome_register_has_no_generated_ui_ornament(self):
        # Proposals explain themselves in words: no sparkle icon, no purple "AI" accent, no glow.
        self.assertNotIn("auto_awesome", self.app)
        self.assertNotIn("#c58af9", self.styles)
        self.assertNotIn("radial-gradient", self.styles)
        self.assertNotIn("investigation-ribbon::before", self.styles)
        self.assertIn('activeLocaleText("הוצעה כי", "Proposed because")', self.app)

    def test_data_values_use_the_self_hosted_mono_face(self):
        self.assertIn('src: url("./assets/fonts/ibm-plex-mono-latin-400-normal.woff2")', self.styles)
        self.assertTrue((ROOT / "assets/fonts/ibm-plex-mono-latin-400-normal.woff2").is_file())
        self.assertTrue((ROOT / "assets/fonts/ibm-plex-sans-latin-400-normal.woff2").is_file())
        self.assertIn('td[dir="ltr"], td .object-viewer-open[data-viewer-kind="record"]', self.styles)
        self.assertIn("function isDataLikeViewerValue(value)", self.app)
        self.assertNotIn("Noto Sans Hebrew", self.styles)

    def test_draft_creation_modal_and_memory_save_gate(self):
        self.assertIn('id="draftCreateInvestigationButton"', self.index)
        self.assertIn('id="draftCreateModal"', self.index)
        self.assertIn('id="draftInvestigationName"', self.index)
        modal_markup = self.index.split('id="draftCreateModal"', 1)[1].split('</div>\n  </div>', 1)[0]
        self.assertNotIn('id="draftCreateDescription"', modal_markup)
        self.assertNotIn('<label for="draftInvestigationName"', modal_markup)
        self.assertIn('data-i18n-aria-en="Investigation name"', modal_markup)
        self.assertIn('.draft-create-actions button {', self.styles)
        self.assertIn('grid-template-columns: repeat(2, minmax(0, 1fr))', self.styles)
        self.assertNotIn('id="draftCreateParticipants"', self.index)
        self.assertIn('function createInvestigationFromDraft()', self.app)
        self.assertIn('const duplicate = Boolean(findInvestigationByName(name));', self.app)
        self.assertIn('await createInvestigation(name, state.investigationId);', self.app)
        self.assertNotIn('draftCreateParticipants', self.app)
        # Saving a layer, object or polygon, or requesting collection, first asks for an investigation name.
        self.assertEqual(self.app.count('openDraftCreateModal(() => '), 4)
        self.assertIn('const pendingAction = state.pendingDraftMemoryAction;', self.app)
        self.assertIn('if (pendingAction) await pendingAction();', self.app)

    def test_welcome_uses_centered_content_without_blue_kickers_or_open_hint(self):
        welcome_markup = self.index.split('<main id="welcomePage"', 1)[1].split('</main>', 1)[0]
        self.assertNotIn('class="welcome-eyebrow"', welcome_markup)
        self.assertNotIn('מרחב החקירות שלך', welcome_markup)
        self.assertNotIn('אפשרויות לשיתוף פעולה', welcome_markup)
        self.assertNotIn('העבודה שלי', welcome_markup)
        self.assertNotIn('לחצו על הסרט לפתיחה', self.app)
        self.assertNotIn('ribbon-open-hint', self.app)
        self.assertIn('justify-content: center', self.styles)

    def test_similar_investigations_and_demo_actions_are_explicit(self):
        self.assertIn('const SIMILAR_INVESTIGATIONS = demoRuntime?.scenario_id === "syria" ? SYRIA_PROPOSED_INVESTIGATIONS : SERBIA_SIMILAR_INVESTIGATIONS;', self.app)
        similar_data = self.app.split("const SERBIA_SIMILAR_INVESTIGATIONS = [", 1)[1].split("];", 1)[0]
        participant_counts = [line.strip() for line in similar_data.splitlines() if "participants:" in line]
        self.assertEqual(["participants: 2,", "participants: 3,", "participants: 6,"], participant_counts)
        self.assertIn("slice(0, Math.min(5, participantCount))", self.app)
        self.assertIn('id="similarInvestigationsList"', self.index)
        self.assertIn('data-i18n-text-he="הדגמה בלבד"', self.index)
        self.assertIn("No data was changed and no message was sent.", self.app)

    def test_ribbon_interactions_are_not_nested(self):
        self.assertIn('class="ribbon-main-action"', self.app)
        self.assertIn('class="ribbon-actions"', self.app)
        self.assertNotIn('<button class="investigation-ribbon"', self.app)
        self.assertIn('.ribbon-main-action:focus-visible', self.styles)


if __name__ == "__main__":
    unittest.main()

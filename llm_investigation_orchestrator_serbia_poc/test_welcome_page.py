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

    def test_existing_language_switch_is_reused(self):
        self.assertEqual(self.index.count('id="languageToggle"'), 1)
        self.assertIn('languageToggle?.addEventListener("change"', self.app)
        self.assertIn('renderWelcomePage();', self.app)
        self.assertIn('data-i18n-text-he="החקירות שלי" data-i18n-text-en="My investigations"', self.index)

    def test_real_investigation_and_members_are_rendered_from_state(self):
        self.assertIn("investigations.map(ownedInvestigationRibbonHtml)", self.app)
        self.assertIn("currentMembers().slice(0, 5)", self.app)
        self.assertIn('data-open-investigation=', self.app)
        self.assertIn('data-welcome-action="invite"', self.app)

    def test_welcome_has_no_new_investigation_action(self):
        welcome_markup = self.index.split('<main id="welcomePage"', 1)[1].split('</main>', 1)[0]
        self.assertNotIn('investigationAddButton', welcome_markup)
        self.assertNotIn('New investigation', welcome_markup)

    def test_similar_investigations_and_demo_actions_are_explicit(self):
        self.assertIn("const SIMILAR_INVESTIGATIONS = [", self.app)
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

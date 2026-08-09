import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class AgentStepCollapseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8-sig")
        cls.styles = (ROOT / "styles.css").read_text(encoding="utf-8")

    def test_step_uses_closed_native_disclosure_by_default(self):
        self.assertIn('<details class="activity-disclosure">', self.app)
        self.assertNotIn('<details class="activity-disclosure" open>', self.app)
        self.assertIn('<summary class="activity-card-summary"', self.app)

    def test_summary_contains_only_step_identity_and_disclosure_icon(self):
        summary = self.app.split('<summary class="activity-card-summary"', 1)[1].split('</summary>', 1)[0]
        self.assertIn('activity-step-number', summary)
        self.assertIn('activity-step-title', summary)
        self.assertIn('activity-expand-icon', summary)
        self.assertNotIn('activity-tool', summary)
        self.assertNotIn('activity-status', summary)

    def test_existing_details_and_actions_remain_inside_expanded_region(self):
        expanded = self.app.split('<div class="activity-expanded">', 1)[1].split('</details>', 1)[0]
        for expected in ('activity-tool', 'activity-status', 'activity-rationale', 'activity-detail', 'activity-result', 'activity-step-actions'):
            self.assertIn(expected, expanded)

    def test_disclosure_has_keyboard_and_open_state_styling(self):
        self.assertIn('.activity-card-summary:focus-visible', self.styles)
        self.assertIn('.activity-disclosure[open] .activity-expand-icon', self.styles)

    def test_unknown_tools_get_specific_readable_titles(self):
        self.assertIn('clean.replace(/[_-]+/g, " ").trim()', self.app)
        self.assertIn('readable.charAt(0).toUpperCase() + readable.slice(1)', self.app)


if __name__ == "__main__":
    unittest.main()

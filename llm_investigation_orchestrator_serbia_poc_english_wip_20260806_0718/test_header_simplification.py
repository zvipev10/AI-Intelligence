import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class HeaderSimplificationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "styles.css").read_text(encoding="utf-8")
        cls.js = (ROOT / "app.js").read_text(encoding="utf-8-sig")

    def test_language_labels_are_inside_existing_switch(self):
        self.assertIn('<span class="language-switch-slider" aria-hidden="true"><span>E</span><span>ע</span></span>', self.html)
        self.assertNotIn('class="language-switch-text"', self.html)
        self.assertIn('id="languageToggle"', self.html)

    def test_compact_status_controls_have_accessible_detail_surfaces(self):
        self.assertIn('id="datasetStatusIndicator"', self.html)
        self.assertIn('id="agentStatusIndicator"', self.html)
        self.assertIn('role="tooltip"', self.html)
        self.assertIn('aria-describedby="datasetStatusTooltip"', self.html)
        self.assertIn('aria-describedby="agentStatusTooltip"', self.html)

    def test_runtime_status_updates_state_and_localized_accessible_name(self):
        self.assertIn('function updateSystemStatus(', self.js)
        self.assertIn('status.indicator.dataset.state = status.state', self.js)
        self.assertIn('status.indicator.setAttribute("aria-label"', self.js)
        self.assertIn('updateSystemStatus("dataset"', self.js)
        self.assertIn('updateSystemStatus("agent"', self.js)

    def test_status_details_are_available_on_hover_and_focus(self):
        self.assertIn('.status-indicator:hover .status-tooltip', self.css)
        self.assertIn('.status-indicator:focus .status-tooltip', self.css)
        self.assertIn('.status-indicator[data-state="ready"]', self.css)
        self.assertIn('.status-indicator[data-state="error"]', self.css)


if __name__ == "__main__":
    unittest.main()

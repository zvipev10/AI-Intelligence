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

    def test_tracking_requires_one_explicit_layer(self):
        self.assertIn('state.workstreamComposerMode ? "radio" : "checkbox"', self.app)
        self.assertIn("layers.length !== 1", self.app)
        self.assertIn("כדי ליצור מעקב יש לצרף שכבה אחת במפורש.", self.app)
        self.assertIn("starting_source: workstreamLayerReference(layer)", self.app)

    def test_creation_requires_inline_confirmation(self):
        self.assertIn("state.pendingWorkstreamDraft = draft", self.app)
        self.assertIn("data-workstream-confirm", self.app)
        self.assertIn("data-workstream-cancel", self.app)
        self.assertIn('fetch("/api/workstreams"', self.app)
        self.assertNotIn("await createWorkstreamFromChat", self.app)

    def test_indicator_is_minimal_and_returns_update_to_chat(self):
        self.assertIn('id="workstreamIndicator"', self.index)
        self.assertIn("function requestWorkstreamUpdate()", self.app)
        self.assertIn("appendWorkstreamUpdate", self.app)
        self.assertNotIn("workstream-popover", self.index)
        self.assertNotIn("workstream-drawer", self.index)

    def test_multiple_workstreams_are_selected_in_chat(self):
        self.assertIn("data-workstream-show", self.app)
        self.assertIn("על איזה מהם להציג עדכון?", self.app)

    def test_update_is_deterministic_and_discloses_manual_trigger(self):
        self.assertIn("workstream.objective", self.app)
        self.assertIn("workstream.starting_source", self.app)
        self.assertIn("workstream.assignments", self.app)
        self.assertIn("העדכון מוצג לפי בקשתך ולא נוצר אוטומטית", self.app)

    def test_archive_requires_chat_confirmation(self):
        self.assertIn("requestWorkstreamArchive", self.app)
        self.assertIn("data-workstream-archive-confirm", self.app)
        self.assertIn("data-workstream-archive-cancel", self.app)

    def test_workstreams_reload_with_investigation(self):
        self.assertIn("async function loadWorkstreams()", self.app)
        self.assertIn("loadWorkstreams();", self.app)
        self.assertIn("renderWorkstreamIndicator();", self.app)

    def test_tracking_and_workstream_messages_have_visible_states(self):
        self.assertIn(".prompt-form.tracking-mode", self.styles)
        self.assertIn(".workstream-message", self.styles)
        self.assertIn(".workstream-indicator[hidden]", self.styles)


if __name__ == "__main__":
    unittest.main()

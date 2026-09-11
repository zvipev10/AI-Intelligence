import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class ObjectViewerContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8")
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.styles = (ROOT / "styles.css").read_text(encoding="utf-8")

    def test_accessible_shared_dialog_exists(self):
        self.assertIn('id="objectViewer"', self.index)
        self.assertIn('role="dialog"', self.index)
        self.assertIn('aria-modal="true"', self.index)
        self.assertIn('aria-labelledby="objectViewerTitle"', self.index)

    def test_only_records_and_organizations_are_supported(self):
        self.assertIn("if (!['record', 'organization'].includes(kind)) return false;", self.app)
        self.assertNotIn('data-viewer-kind="target"', self.app)

    def test_grid_and_assistant_open_controls_exist(self):
        self.assertIn('data-viewer-kind="record"', self.app)
        self.assertIn('data-viewer-kind="organization"', self.app)
        self.assertIn("appendAssistantObjectLinks(article)", self.app)

    def test_map_opens_only_a_single_item(self):
        self.assertIn("viewerRefs.length === 1 && item.viewerEligible", self.app)
        self.assertIn("else existing.viewerEligible = false", self.app)

    def test_media_is_not_autoplayed_and_has_fallback(self):
        self.assertIn('<video controls preload="metadata"', self.app)
        self.assertIn('<audio controls preload="metadata"', self.app)
        self.assertNotIn('<video autoplay', self.app)
        self.assertIn('Raw video is not connected', self.app)
        self.assertIn("function safeMediaUrl", self.app)

    def test_uav_media_is_presented_as_shared_source_material(self):
        self.assertIn('Raw UAV video', self.app)
        self.assertIn('The same source footage may therefore support several records.', self.app)
        self.assertIn('item.mission_id', self.app)
        self.assertIn('item.video_segment_id', self.app)
        self.assertIn('function viewerFieldLabel', self.app)

    def test_dialog_is_a_locale_aware_edge_drawer(self):
        self.assertIn(".object-viewer-backdrop", self.styles)
        self.assertIn(".object-viewer-fields", self.styles)
        self.assertIn("margin-inline-start: auto", self.styles)
        self.assertIn('[dir="rtl"] .object-viewer', self.styles)
        self.assertIn("height: 100dvh", self.styles)


if __name__ == "__main__":
    unittest.main()

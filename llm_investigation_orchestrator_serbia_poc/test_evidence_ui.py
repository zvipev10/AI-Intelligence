import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class EvidenceUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8")
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_evidence_layer_has_map_table_timeline_and_viewer_paths(self):
        self.assertIn('layer.kind === "evidence"', self.app)
        self.assertIn('milStdEvidenceDescriptor', self.app)
        self.assertIn('data-viewer-kind="evidence"', self.app)
        self.assertIn('evidenceTimelineItems', self.app)
        self.assertIn('activeLayer.kind === "evidence"', self.app)

    def test_frontend_asset_version_is_bumped(self):
        self.assertIn('app.js?v=181', self.index)


if __name__ == "__main__":
    unittest.main()

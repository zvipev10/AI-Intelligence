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
        self.assertIn('app.js?v=187', self.index)

    def test_html_escaping_tolerates_missing_catalog_fields(self):
        self.assertIn('String(value ?? "").replace', self.app)

    def test_catalog_actions_receive_regular_result_visibility_control(self):
        self.assertIn('function hasCatalogLayerActions', self.app)
        self.assertIn('|| hasCatalogLayerActions(options.result)', self.app)
        self.assertIn('(layer.presentationSourceIds || []).includes(sourceId)', self.app)

    def test_evidence_symbology_is_bounded_before_map_rendering(self):
        self.assertIn("function coalesceEvidenceDescriptors", self.app)
        self.assertIn("coalesceEvidenceDescriptors(milStdDescriptors)", self.app)
        self.assertIn("maximum = 400", self.app)

    def test_evidence_is_a_catalog_family(self):
        self.assertIn('evidence: "Evidence"', self.app)
        self.assertIn('evidence: "ראיות"', self.app)


if __name__ == "__main__":
    unittest.main()

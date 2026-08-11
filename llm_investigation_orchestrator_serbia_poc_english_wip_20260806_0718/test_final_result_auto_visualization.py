import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent


class FinalResultAutoVisualizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8-sig")
        cls.index = (ROOT / "index.html").read_text(encoding="utf-8")

    def test_shared_presenter_is_used_for_normal_and_restore_results(self):
        self.assertIn("function presentFinalAgentResult(result, prompt, options = {})", self.app)
        self.assertIn("presentFinalAgentResult(result, prompt, { showSummary: true });", self.app)
        self.assertIn("finalizeAssistantMessage(result.answer, { result, prompt });\n  presentFinalAgentResult(result, prompt);", self.app)

    def test_agent_map_and_timeline_decisions_are_honored(self):
        resolver = self.app.split("function resolveFinalResultView", 1)[1].split("function presentFinalAgentResult", 1)[0]
        self.assertIn('["map", "timeline"].includes(requestedView)', resolver)
        self.assertIn('["map", "timeline"].includes(result.recommended_view)', resolver)
        self.assertLess(
            resolver.index('["map", "timeline"].includes(result.recommended_view)'),
            resolver.index("layers.find"),
        )
        self.assertIn('layer.capabilities?.map', resolver)
        self.assertIn('layer.capabilities?.timeline', resolver)
        self.assertIn('return "map";', resolver)

    def test_presentation_adds_final_layers_and_activates_automatic_view(self):
        presenter = self.app.split("function presentFinalAgentResult", 1)[1].split("function buildStepQueryContext", 1)[0]
        self.assertIn("layers: typedLayers", presenter)
        self.assertIn("activateView(requestedView", presenter)
        self.assertIn("automatic: true", presenter)
        self.assertIn("renderAllViews();", presenter)

    def test_evidence_reference_layers_remain_outside_auto_presentation(self):
        presenter = self.app.split("function presentFinalAgentResult", 1)[1].split("function buildStepQueryContext", 1)[0]
        self.assertNotIn("buildEvidenceReferenceLayers", presenter)

    def test_asset_cache_key_is_bumped(self):
        self.assertIn('app.js?v=154', self.index)


if __name__ == "__main__":
    unittest.main()

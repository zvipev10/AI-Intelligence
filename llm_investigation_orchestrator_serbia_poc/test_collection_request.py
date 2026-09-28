import tempfile
import unittest
from pathlib import Path

import server


ROOT = Path(__file__).resolve().parent


class CollectionRequestTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.original_dir = server.INVESTIGATIONS_DIR
        server.INVESTIGATIONS_DIR = Path(self.temp.name)

    def tearDown(self):
        server.INVESTIGATIONS_DIR = self.original_dir
        self.temp.cleanup()

    def test_visint_polygon_request_is_persisted(self):
        saved = server.create_collection_request({
            "investigation_id": "investigation-collection-demo",
            "name": "Collection demo",
            "role": "visint",
            "collection_type": "satellite",
            "target": {"type": "polygon", "geometry": {"type": "Polygon", "coordinates": [[[36.1, 33.1], [36.2, 33.1], [36.2, 33.2], [36.1, 33.1]]]}},
            "extraction_objects": ["convoy", "vehicles"],
            "instructions": "Check for movement",
        })
        request = saved["saved"]
        self.assertEqual(request["role"], "visint")
        self.assertEqual(request["collection_type"], "satellite")
        self.assertEqual(request["extraction_objects"], ["convoy", "vehicles"])
        memory = server.load_investigation_memory("investigation-collection-demo")
        self.assertEqual(memory["memory"]["collection_requests"][0]["id"], request["id"])

    def test_sigint_cannot_request_visint_collection(self):
        with self.assertRaisesRegex(ValueError, "not available"):
            server.create_collection_request({
                "investigation_id": "investigation-collection-demo",
                "role": "sigint",
                "collection_type": "satellite",
                "target": {"type": "imei", "imei": "123456789012345"},
            })


class CollectionRequestUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = (ROOT / "app.js").read_text(encoding="utf-8")
        cls.bootstrap = (ROOT / "demo_bootstrap.js").read_text(encoding="utf-8")

    def test_submitting_collection_opens_the_matching_layer_in_its_preferred_view(self):
        self.assertIn("const COLLECTION_LAYER_PRESENTATIONS = {", self.app)
        self.assertIn('cellular_calls: { layerId: "events:Cellular Calls", view: "timeline" }', self.app)
        self.assertIn('ipdr: { layerId: "events:IPDR", view: "table" }', self.app)
        self.assertIn('await openRequestedCollectionLayer(type);', self.app)
        self.assertIn('activateView(presentation.view', self.app)
        self.assertIn('script.src = "./app.js?v=243";', self.bootstrap)


if __name__ == "__main__":
    unittest.main()

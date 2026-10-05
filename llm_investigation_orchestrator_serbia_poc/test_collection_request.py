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

    def test_ipdr_is_not_requestable(self):
        with self.assertRaisesRegex(ValueError, "not available"):
            server.create_collection_request({
                "investigation_id": "investigation-collection-demo",
                "role": "general",
                "collection_type": "ipdr",
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
        self.assertNotIn('{ id: "ipdr",', self.app)
        self.assertNotIn('ipdr: { layerId: "events:IPDR", view: "table" }', self.app)
        self.assertIn('chatPanelCollapsed: demoRuntime?.scenario_id === "syria"', self.app)
        self.assertIn('await openRequestedCollectionLayer(type);', self.app)
        self.assertIn('activateView(presentation.view', self.app)
        self.assertIn('script.src = "./app.js?v=269";', self.bootstrap)

    def test_specialized_demo_task_screens_follow_source_selection(self):
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        styles = (ROOT / "styles.css").read_text(encoding="utf-8")
        self.assertIn('id="adintTaskModal"', index)
        self.assertIn('NEW COLLECTION TASK · ADINT', index)
        self.assertIn('id="sigintTaskModal"', index)
        self.assertIn('NEW COLLECTION TASK · SIGINT', index)
        self.assertIn('id="cellularCallsTaskModal"', index)
        self.assertIn('NEW COLLECTION TASK · CELLULAR CALLS', index)
        self.assertIn('id="cctvTaskModal"', index)
        self.assertIn('NEW COLLECTION TASK · CCTV', index)
        self.assertIn('id="adintDateFrom" type="date"', index)
        self.assertIn('id="adintTimeFrom" type="time"', index)
        self.assertIn('id="adintLocationMap"', index)
        self.assertNotIn('adint-location-preview.png', index)
        self.assertIn('id="collectionRequestModal"', index)
        self.assertNotIn('id="collectionRequestNote"', index)
        self.assertGreater(index.index('<section class="task-section"><h3>Source</h3>'), index.index('<section class="task-section"><h3>Date and time</h3>'))
        self.assertIn('<section class="task-section"><h3>Comments</h3>', index)
        self.assertIn('id="sigintCircles" type="radio"', index)
        self.assertNotIn('<b>1</b>', index)
        self.assertIn('const defaultType = target.type === "imei" ? "cellular_geolocations" : "adint";', self.app)
        self.assertIn('if (target.type === "polygon" && type === "adint")', self.app)
        self.assertIn('if (target.type === "polygon" && type === "cctv")', self.app)
        self.assertIn('if (target.type === "imei" && type === "cellular_geolocations")', self.app)
        self.assertIn('if (target.type === "imei" && type === "cellular_calls")', self.app)
        self.assertIn('function updateCollectionSourceSelectionAction()', self.app)
        self.assertIn('async function completeDemoCollectionTask(modal, fallbackType)', self.app)
        self.assertIn('await completeDemoCollectionTask(adintTaskModal, "adint")', self.app)
        self.assertIn('await completeDemoCollectionTask(sigintTaskModal, "cellular_geolocations")', self.app)
        self.assertIn('await completeDemoCollectionTask(cellularCallsTaskModal, "cellular_calls")', self.app)
        self.assertIn('await completeDemoCollectionTask(cctvTaskModal, "cctv")', self.app)
        self.assertIn('.task-modal {', styles)
        self.assertIn('.task-modal-sigint', styles)
        self.assertIn('.task-location-map', styles)
        self.assertIn('validateAdintTaskForm', self.app)
        self.assertIn('validateSigintIdentifiers', self.app)
        self.assertIn('function renderAdintLocationMap(coordinates)', self.app)
        self.assertIn('drawn-collection-area', self.app)


if __name__ == "__main__":
    unittest.main()

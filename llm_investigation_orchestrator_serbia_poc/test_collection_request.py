import tempfile
import unittest
from pathlib import Path

import server


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


if __name__ == "__main__":
    unittest.main()

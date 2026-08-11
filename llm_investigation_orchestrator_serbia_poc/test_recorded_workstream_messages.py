import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import server


class RecordedWorkstreamMessageTests(unittest.TestCase):
    def setUp(self):
        self.temp_root = tempfile.TemporaryDirectory()
        self.saved_dir = Path(self.temp_root.name) / "saved"
        self.patch = patch.object(server, "SAVED_QUESTIONS_DIR", self.saved_dir)
        self.patch.start()

    def tearDown(self):
        self.patch.stop()
        self.temp_root.cleanup()

    def request(self, kind="detail"):
        return {
            "title": "Recorded workstream",
            "question": "Workstream update",
            "result": {
                "answer": "Workstream update",
                "investigation_steps": [],
                "workstream_recording": {
                    "kind": kind,
                    "workstream": {
                        "workstream_id": "ws_20260811_120000_abcdef12",
                        "title": "Recorded workstream",
                        "objective": "Track the indication",
                    },
                },
            },
        }

    def test_saves_duplicate_workstream_recordings_with_distinct_ids(self):
        first = server.create_saved_question(self.request())
        second = server.create_saved_question(self.request())
        self.assertNotEqual(first["id"], second["id"])
        metadata = server.list_saved_question_metadata()
        self.assertEqual(2, len(metadata))
        self.assertTrue(all(item["recording_type"] == "workstream_message" for item in metadata))

    def test_rejects_invalid_workstream_recording(self):
        request = self.request(kind="unsupported")
        with self.assertRaisesRegex(ValueError, "Invalid workstream recording"):
            server.create_saved_question(request)


if __name__ == "__main__":
    unittest.main()

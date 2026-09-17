import time
import unittest
from pathlib import Path

import server


ROOT = Path(__file__).resolve().parent


class MobileRunRecoveryTests(unittest.TestCase):
    def setUp(self):
        with server._INVESTIGATION_RESULTS_LOCK:
            server._INVESTIGATION_RESULTS.clear()

    def test_completed_result_can_be_recovered_by_client_request_id(self):
        server.set_investigation_result("request-mobile-1", "running")
        self.assertEqual("running", server.get_investigation_result("request-mobile-1")["status"])
        server.set_investigation_result("request-mobile-1", "completed", result={"answer": "done"})
        recovered = server.get_investigation_result("request-mobile-1")
        self.assertEqual("completed", recovered["status"])
        self.assertEqual("done", recovered["result"]["answer"])

    def test_invalid_and_expired_request_ids_are_not_recoverable(self):
        server.set_investigation_result("bad id", "completed", result={"answer": "bad"})
        self.assertIsNone(server.get_investigation_result("bad id"))
        with server._INVESTIGATION_RESULTS_LOCK:
            server._INVESTIGATION_RESULTS["request-old"] = {
                "request_id": "request-old", "status": "completed", "result": {},
                "error": None, "updated_at": time.time() - server.INVESTIGATION_RESULT_TTL_SECONDS - 1,
            }
        self.assertIsNone(server.get_investigation_result("request-old"))

    def test_mobile_client_reconnects_to_existing_run(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        index = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn("client_request_id: clientRequestId", app)
        self.assertIn("/api/investigate-result?id=", app)
        self.assertIn('document.addEventListener("visibilitychange", onVisible)', app)
        self.assertIn("app.js?v=190", index)


if __name__ == "__main__":
    unittest.main()

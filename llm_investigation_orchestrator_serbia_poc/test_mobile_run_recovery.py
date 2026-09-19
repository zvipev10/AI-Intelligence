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
        server.set_investigation_result(
            "request-mobile-1", "running", live_agent="talia", live_started_at="2026-09-18T16:39:08+00:00"
        )
        self.assertEqual("running", server.get_investigation_result("request-mobile-1")["status"])
        server.set_investigation_result("request-mobile-1", "completed", result={"answer": "done"})
        recovered = server.get_investigation_result("request-mobile-1")
        self.assertEqual("completed", recovered["status"])
        self.assertEqual("done", recovered["result"]["answer"])
        self.assertEqual("talia", recovered["live_agent"])

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
        self.assertIn("liveStepsUrl(addressedPrompt, clientRequestId)", app)
        self.assertIn('params.set("request_id", clientRequestId)', app)
        self.assertIn("/api/investigate-result?id=", app)
        self.assertIn('document.addEventListener("visibilitychange", onVisible)', app)
        self.assertNotIn('document.addEventListener("visibilitychange", recoverWhenVisible)', app)
        self.assertNotIn('window.addEventListener("pageshow", recoverWhenVisible)', app)
        self.assertNotIn("Promise.race([directResult, resumedResult])", app)
        self.assertNotIn('addActivity("connection_recovery"', app)
        self.assertIn("if (!recoveryPromise)", app)
        self.assertIn("result = await recoverExistingRun();", app)
        self.assertIn("app.js?v=196", index)
        self.assertNotIn('addActivity("Hermes"', app)
        self.assertNotIn("if (!cleanAssistantAnswer(result?.answer))", app)

    def test_live_step_refresh_preserves_expanded_step(self):
        app = (ROOT / "app.js").read_text(encoding="utf-8")
        self.assertIn("const canAppendLiveSteps = !sourceBase && existingItems.length <= visibleSteps.length;", app)
        self.assertIn("const firstStepIndex = canAppendLiveSteps ? existingItems.length : 0;", app)
        self.assertIn('if (!canAppendLiveSteps) state.activeActivityList.innerHTML = "";', app)
        self.assertIn("visibleSteps.slice(firstStepIndex).forEach", app)
        self.assertIn("const expandedStepNumbers = new Set(", app)
        self.assertIn('querySelectorAll(".activity-item > details[open]")', app)
        self.assertIn("if (expandedStepNumbers.has(stepNumber))", app)
        self.assertIn('setAttribute("open", "")', app)


if __name__ == "__main__":
    unittest.main()

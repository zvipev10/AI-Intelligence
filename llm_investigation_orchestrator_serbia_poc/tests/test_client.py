import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from hl.client import AuthExpired, HlClient, HlError, NotOnThisEstate, Unreachable, list_hits, total_pages


class Scripted(BaseHTTPRequestHandler):
    """Answers each request with the next scripted (status, body)."""
    script: list = []
    seen: list = []

    def log_message(self, *args):
        pass

    def _answer(self):
        length = int(self.headers.get("Content-Length", "0") or 0)
        type(self).seen.append((self.command, self.path, self.headers.get("Authorization"),
                                self.headers.get("Content-Type"), self.rfile.read(length).decode()))
        status, body = type(self).script.pop(0)
        payload = json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    do_GET = do_POST = do_PATCH = do_DELETE = _answer


class ClientTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Scripted)
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()
        cls.base = f"http://127.0.0.1:{cls.server.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()

    def setUp(self):
        Scripted.script, Scripted.seen = [], []

    def test_token_exchange_is_form_encoded_without_bearer(self):
        Scripted.script = [(200, {"access_token": "t", "expires_in": 60})]
        HlClient(self.base).token_exchange("u", "p w")
        method, path, auth, content_type, body = Scripted.seen[0]
        self.assertEqual(("POST", "/api/v1/auth/token", None), (method, path, auth))
        self.assertEqual("application/x-www-form-urlencoded", content_type)
        self.assertEqual("grant_type=password&username=u&password=p+w", body)

    def test_bearer_token_on_calls(self):
        Scripted.script = [(200, {"user_name": "u"})]
        HlClient(self.base, "tok").whoami()
        self.assertEqual("Bearer tok", Scripted.seen[0][2])

    def test_error_envelope_and_classes(self):
        Scripted.script = [(401, {"error": {"code": "invalid_token", "message": "gone", "hint": "sign in"}})]
        with self.assertRaises(AuthExpired) as caught:
            HlClient(self.base, "t").whoami()
        self.assertEqual(("invalid_token", "sign in"), (caught.exception.code, caught.exception.hint))
        Scripted.script = [(501, {"error": {"code": "not_on_this_estate", "message": "", "hint": ""}})]
        with self.assertRaises(NotOnThisEstate):
            HlClient(self.base, "t").estate()
        Scripted.script = [(400, {"error": "invalid_grant"})]
        with self.assertRaises(HlError) as caught:
            HlClient(self.base).token_exchange("u", "p")
        self.assertEqual("invalid_grant", caught.exception.code)

    def test_reads_retry_on_502_but_writes_never(self):
        Scripted.script = [(503, {}), (200, {"items": []})]
        HlClient(self.base, "t").search_items({"text": {"any": "x"}})
        self.assertEqual(2, len(Scripted.seen))
        Scripted.script, Scripted.seen = [(503, {}), (200, {"entity_id": "e"})], []
        with self.assertRaises(HlError):
            HlClient(self.base, "t").create_entity("T", {"sections": {}})
        self.assertEqual(1, len(Scripted.seen))

    def test_unreachable(self):
        with self.assertRaises(Unreachable):
            HlClient("http://127.0.0.1:9", "t", timeout=2).create_entity("T", {})

    def test_entity_search_shapes(self):
        self.assertEqual([{"a": 1}], list_hits({"items": [{"a": 1}]}))
        self.assertEqual([{"a": 1}], list_hits({"results": [{"a": 1}, "x"]}))
        self.assertEqual(3, total_pages({"searchResponseMetadata": {"totalPages": 3}}))
        self.assertEqual(1, total_pages({}))


if __name__ == "__main__":
    unittest.main()

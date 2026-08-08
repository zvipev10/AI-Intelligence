import unittest

import server


class FakeSemanticIndex:
    backend = "hybrid_embedding"
    manifest = {"record_count": 14800}

    def __init__(self):
        self.received_limit = None

    def search(self, query, filters, limit):
        self.received_limit = limit
        return []


class SemanticResultLimitTests(unittest.TestCase):
    def test_semantic_search_caps_oversized_candidate_requests(self):
        runtime = server.current_runtime()
        original = runtime.semantic_index
        fake = FakeSemanticIndex()
        runtime.semantic_index = fake
        try:
            result = server.semantic_search_events({"query": "כלי טיס", "limit": 2000})
        finally:
            runtime.semantic_index = original

        self.assertEqual(result["requested_limit"], 2000)
        self.assertEqual(result["effective_limit"], server.MAX_SEMANTIC_LIMIT)
        self.assertEqual(fake.received_limit, server.MAX_SEMANTIC_LIMIT)


if __name__ == "__main__":
    unittest.main()

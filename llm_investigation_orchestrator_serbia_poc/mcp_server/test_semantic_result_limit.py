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
        original = server.SEMANTIC_INDEX
        fake = FakeSemanticIndex()
        server.SEMANTIC_INDEX = fake
        try:
            result = server.semantic_search_events({"query": "כלי טיס", "limit": 2000})
        finally:
            server.SEMANTIC_INDEX = original

        self.assertEqual(result["requested_limit"], 2000)
        self.assertEqual(result["effective_limit"], server.MAX_SEMANTIC_LIMIT)
        self.assertEqual(fake.received_limit, server.MAX_SEMANTIC_LIMIT)


if __name__ == "__main__":
    unittest.main()

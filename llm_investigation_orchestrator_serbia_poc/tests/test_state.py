import unittest

from hl.client import HlError
from hl.state import StateStore, external_investigation_header

INVESTIGATION = {
    "entity_id": "inv-1",
    "entity_name": "Port activity",
    "sections": {
        "general": {"entity_status": "ACTIVE", "creation_time": 1791384855120},
        "investigation_details": {"research_question": "Who uses the port?", "status": "open",
                                  "activity_level": "high", "next_milstone": "brief"},
    },
}


class FakeClient:
    def __init__(self):
        self.records = {"inv-1": INVESTIGATION}
        self.created = []
        self.patched = []

    def search_entities(self, entity_type, body):
        if entity_type == "INTELLIGENCE_INVESTIGATION":
            return {"items": list(self.records.values()), "total_pages": 1}
        return {"items": [], "total_pages": 1}

    def get_entity(self, entity_type, entity_id):
        if entity_id not in self.records:
            raise HlError(404, "not_found", "no such entity")
        return self.records[entity_id]

    def create_entity(self, entity_type, body):
        self.created.append((entity_type, body))
        self.records["inv-2"] = {"entity_id": "inv-2", "entity_name": body["entity_name"]}
        return {"entity_id": "inv-2"}

    def patch_entity(self, entity_type, entity_id, body):
        self.patched.append((entity_type, entity_id, body))
        return {}


def store(client):
    return StateStore(client, investigation_type="AII_INVESTIGATION", memory_item_type="AII_MEMORY_ITEM",
                      approval_type="AII_TELECOM_APPROVAL", scenario="lambda",
                      external_investigation_type="INTELLIGENCE_INVESTIGATION")


class ExternalInvestigationTests(unittest.TestCase):
    def test_header_reads_i360_fields(self):
        header = external_investigation_header(INVESTIGATION)
        self.assertEqual(("inv-1", "Port activity"), (header["investigation_id"], header["name"]))
        self.assertEqual("open", header["status"])
        self.assertEqual("Who uses the port?", header["research_question"])
        self.assertEqual("brief", header["next_milestone"])
        self.assertTrue(str(header["created_at_utc"]).startswith("2026-"))

    def test_list_comes_from_the_i360_type(self):
        listed = store(FakeClient()).list_investigations()
        self.assertEqual(["inv-1"], [item["investigation_id"] for item in listed])

    def test_create_makes_an_i360_record_and_returns_its_id(self):
        client = FakeClient()
        created = store(client).register_investigation("investigation-local-123", "New case")
        self.assertEqual([("INTELLIGENCE_INVESTIGATION", {"entity_name": "New case"})], client.created)
        self.assertEqual("inv-2", created["investigation_id"])

    def test_renaming_an_existing_one_patches_only_its_name(self):
        client = FakeClient()
        store(client).register_investigation("inv-1", "Port activity, phase 2")
        self.assertEqual([("INTELLIGENCE_INVESTIGATION", "inv-1", {"entity_name": "Port activity, phase 2"})], client.patched)
        self.assertEqual([], client.created)

    def test_touch_does_not_rewrite_i360_records(self):
        client = FakeClient()
        store(client).touch_investigation("inv-1")
        self.assertEqual(([], []), (client.created, client.patched))


if __name__ == "__main__":
    unittest.main()

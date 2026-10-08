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
        self.records[body["entity_id"]] = {"entity_id": body["entity_id"], "entity_name": body["entity_name"]}
        return {"entity_id": body["entity_id"]}

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
        self.assertEqual([("INTELLIGENCE_INVESTIGATION",
                           {"entity_id": "investigation-local-123", "entity_name": "New case"})], client.created)
        self.assertEqual("investigation-local-123", created["investigation_id"])

    def test_renaming_an_existing_one_patches_only_its_name(self):
        client = FakeClient()
        store(client).register_investigation("inv-1", "Port activity, phase 2")
        self.assertEqual([("INTELLIGENCE_INVESTIGATION", "inv-1", {"entity_name": "Port activity, phase 2"})], client.patched)
        self.assertEqual([], client.created)

    def test_touch_does_not_rewrite_i360_records(self):
        client = FakeClient()
        store(client).touch_investigation("inv-1")
        self.assertEqual(([], []), (client.created, client.patched))


class RelatedClient(FakeClient):
    def __init__(self):
        super().__init__()
        self.related = {}
        self.calls = []

    def add_related_objects(self, entity_type, entity_id, item_ids, relation_type="associated"):
        self.calls.append(("add", entity_type, entity_id, tuple(item_ids)))
        results = []
        for item_id in item_ids:
            outcome = "already_linked" if item_id in self.related.get(entity_id, set()) else "linked"
            self.related.setdefault(entity_id, set()).add(item_id)
            results.append({"item_id": item_id, "outcome": outcome})
        return {"results": results}

    def remove_related_objects(self, entity_type, entity_id, item_ids):
        self.calls.append(("remove", entity_type, entity_id, tuple(item_ids)))
        held = self.related.get(entity_id, set())
        results = [{"item_id": i, "outcome": "unlinked" if i in held else "not_linked"} for i in item_ids]
        held.difference_update(item_ids)
        return {"results": results}

    def search_items(self, body):
        ids = (body.get("related_to") or {}).get("ids") or []
        items = [{"item_id": i, "item_type": "image", "source_application": "EO optical (fictional)",
                  "event_time": "2026-08-31T07:18:00Z", "text": {"transcript": "3x cargo truck"}}
                 for entity_id in ids for i in sorted(self.related.get(entity_id, set()))]
        return {"items": items, "total_pages": 1}


class AttachItemsToInvestigationTests(unittest.TestCase):
    RECORD = {"kind": "object", "object_kind": "record", "object_id": "rec-1", "i360_item_id": "item-1",
              "label": "rec-1", "id": "artifact-x"}

    def test_saving_a_record_attaches_the_item_to_the_i360_investigation(self):
        client = RelatedClient()
        saved = store(client).add_memory_item("inv-1", "artifacts", dict(self.RECORD))
        self.assertEqual([("add", "INTELLIGENCE_INVESTIGATION", "inv-1", ("item-1",))], client.calls)
        self.assertEqual("i360:item-1", saved["id"])
        self.assertEqual([], client.created)  # no AII_MEMORY_ITEM record

    def test_memory_lists_what_i360_reports_as_related(self):
        client = RelatedClient()
        s = store(client)
        s.add_memory_item("inv-1", "artifacts", dict(self.RECORD))
        artifacts = s.load_memory("inv-1")["memory"]["artifacts"]
        self.assertEqual(["i360:item-1"], [a["id"] for a in artifacts])
        self.assertEqual(("record", "item-1", "3x cargo truck"),
                         (artifacts[0]["object_kind"], artifacts[0]["object_id"], artifacts[0]["summary"]))

    def test_removing_detaches_it(self):
        client = RelatedClient()
        s = store(client)
        s.add_memory_item("inv-1", "artifacts", dict(self.RECORD))
        self.assertTrue(s.delete_memory_item("inv-1", "artifacts", "i360:item-1"))
        self.assertEqual([], s.load_memory("inv-1")["memory"]["artifacts"])

    def test_a_refused_attach_is_an_error(self):
        class Refusing(RelatedClient):
            def add_related_objects(self, *args, **kwargs):
                return {"results": [{"item_id": "item-1", "outcome": "failed", "error": "write_not_permitted"}]}

        with self.assertRaises(HlError):
            store(Refusing()).add_memory_item("inv-1", "artifacts", dict(self.RECORD))


if __name__ == "__main__":
    unittest.main()

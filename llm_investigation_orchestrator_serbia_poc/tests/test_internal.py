import json
import unittest

from hl.internal import Catalogue, InternalTurn


def row(layer, record_id, links=(), **fields):
    return {"source_type": layer, "record_id": record_id, "timestamp_utc": "2026-09-01T10:00:00Z",
            "i360_links": json.dumps(list(links)), **{f"i360.{k}": v for k, v in fields.items()}}


LAYERS = {
    "ADINT": [row("ADINT", "a-1", [{"id": "p-1", "type": "ITEM"}], **{"user_agents_data.language_code": "fa", "os": "iOS"}),
              row("ADINT", "a-2", **{"user_agents_data.language_code": "ar", "os": "Android"}),
              row("ADINT", "a-3", [{"id": "inv", "type": "INTELLIGENCE_INVESTIGATION"}],
                  **{"user_agents_data.language_code": "fa", "os": "Android"})],
    "IPDR": [row("IPDR", "p-1", **{"asset_identifier": "3532"}), row("IPDR", "p-2"),
             row("IPDR", "p-3", [{"id": "a-2", "type": "ITEM"}], **{"asset_identifier": "9999"})],
}
LABELS = {"ADINT": {"i360.user_agents_data.language_code": "keyboard_language"},
          "IPDR": {"i360.asset_identifier": "imei"}}


class CatalogueTests(unittest.TestCase):
    def setUp(self):
        self.cat = Catalogue(LAYERS, LABELS, {"inv": "Suspicious military convoy"})

    def ids(self, query):
        result = self.cat.run(query)
        self.assertNotIn("error", result, result.get("error"))
        return sorted(r.id for r in result["records"])

    def test_fields_carry_our_names_and_values(self):
        self.assertIn("keyboard_language | text | ADINT | fa, ar", self.cat.describe())
        self.assertEqual(["a-1", "a-3"], self.ids({"layers": ["ADINT"], "where": [
            {"field": "keyboard_language", "op": "is", "value": "FA"}]}))  # values match whatever the case
        self.assertEqual(["a-1"], self.ids({"where": [{"field": "keyboard_language", "op": "is", "value": "fa"},
                                                      {"field": "os", "op": "is", "value": "iOS"}]}))

    def test_links_count_both_ways(self):
        # a-1 names p-1; p-3 names a-2: both are links between ADINT and IPDR.
        self.assertEqual(["p-1"], self.ids({"layers": ["IPDR"], "linked": {"record_id": "a-1"}}))
        self.assertEqual(["p-1", "p-3"], self.ids({"layers": ["IPDR"], "linked": {"layer": "ADINT"}}))
        self.assertEqual(["a-3"], self.ids({"linked": {"entity_name": "convoy"}}))
        self.assertEqual(["a-3"], self.ids({"linked": {"entity_type": "INTELLIGENCE_INVESTIGATION"}}))

    def test_a_condition_on_the_asked_records_is_kept_with_them(self):
        query = {"layers": ["IPDR"], "linked": {"layer": "ADINT", "where": [{"field": "imei", "op": "exists"}]}}
        self.assertEqual(["p-1", "p-3"], self.ids(query))

    def test_unknown_names_and_values_are_said_back(self):
        self.assertIn("no layer named", self.cat.run({"layers": ["Radar"]})["error"])
        self.assertIn("did you mean keyboard_language", self.cat.run(
            {"where": [{"field": "keyboard", "op": "is", "value": "fa"}]})["error"])
        self.assertIn("its values are fa, ar", self.cat.run(
            {"where": [{"field": "keyboard_language", "op": "is", "value": "Farsi"}]})["error"])
        self.assertIn("IPDR has no field 'keyboard_language'", self.cat.run(
            {"layers": ["IPDR"], "where": [{"field": "keyboard_language", "op": "is", "value": "fa"}]})["error"])

    def test_not_skips_records_without_a_value_and_them_is_the_previous_result(self):
        layers = {"ADINT": LAYERS["ADINT"] + [row("ADINT", "a-4")]}  # a-4 has no keyboard language
        cat = Catalogue(layers, LABELS)
        not_arabic = {"layers": ["ADINT"], "where": [{"field": "keyboard_language", "op": "not_in", "value": ["ar"]}]}
        self.assertEqual(["a-1", "a-3"], sorted(r.id for r in cat.run(not_arabic)["records"]))
        them = {"within_previous": True, "where": [{"field": "os", "op": "is", "value": "Android"}]}
        self.assertEqual(["a-3"], [r.id for r in cat.run(them, ["a-1", "a-3"])["records"]])
        self.assertIn("no previous result", cat.run(them)["error"])

    def test_the_related_records_of_the_previous_answer(self):
        related = {"layers": ["IPDR"], "linked": {"previous": True}}
        self.assertEqual(["p-1"], [r.id for r in self.cat.run(related, ["a-1"])["records"]])
        self.assertIn("no previous result", self.cat.run(related)["error"])

    def test_a_person_with_recommended_knowledge(self):
        import server
        person = server.Handler.internal_person("p-9", {"canonical_name": "Arman Rahimi", "telecom": {
            "imei": "3532", "i360_review": {"msisdn": "recommended", "imsi": "recommended"},
            "subscriber_identity_derivation": {"claim": {"value": {"msisdn": "9630", "imsi": "4170"}}}}})
        self.assertEqual(("recommended", "9630", "recommended"), (person["knowledge_status"], person["msisdn"],
                                                                 person["msisdn_status"]))
        cat = Catalogue({"Persons": [person], **LAYERS}, LABELS, {"p-9": "Arman Rahimi"})
        query = {"layers": ["Persons"], "where": [{"field": "knowledge_status", "op": "is", "value": "recommended"}]}
        self.assertEqual(["p-9"], [r.id for r in cat.run(query)["records"]])

    def test_counts_by_field(self):
        result = self.cat.run({"layers": ["ADINT"], "group_by": "keyboard_language"})
        self.assertEqual({"fa": 2, "ar": 1}, result["groups"])


class TurnTests(unittest.TestCase):
    def test_question_query_answer_show(self):
        calls = []

        class Llm:
            def complete(self, messages, tools):
                calls.append(tools)
                if tools:
                    return {"content": "", "tool_calls": [{"id": "q", "name": "run_query", "arguments": {
                        "layers": ["ADINT"], "where": [{"field": "keyboard_language", "op": "is", "value": "fa"}],
                        "show": "map"}}]}
                return {"content": "2 ADINT records have keyboard language fa.", "tool_calls": []}

        events, shown = [], []
        turn = InternalTurn(Llm(), Catalogue(LAYERS, LABELS), lambda e, d: events.append((e, d)),
                            lambda ids, view, label: shown.append((ids, view)) or len(ids))
        result = turn.run("ADINT records where keyboard language is fa")
        self.assertEqual(2, result["count"])
        self.assertEqual([(["a-1", "a-3"], "map")], shown)
        self.assertEqual("2 ADINT records have keyboard language fa.", [d for e, d in events if e == "note"][0]["text"])
        self.assertEqual([], calls[1])  # the answer is written without tools, from the result


if __name__ == "__main__":
    unittest.main()

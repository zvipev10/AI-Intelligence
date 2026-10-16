"""The chat: the app server against the fake HL API (scripted model) and the fake i360 chat service."""
import json
import os
import threading
import unittest
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FIXTURE = ROOT / "devtools" / "fixtures" / "syria.json.gz"

from devtools.fake_chat import make_chat_server  # noqa: E402
from devtools.fake_hlapi import FakeEstate, make_server  # noqa: E402
from hl.chat import ChatTurn, TurnContext, assistant_message, parse_sse  # noqa: E402
from hl.items import layers_search  # noqa: E402
from hl.state import type_definitions  # noqa: E402
from tests.test_api import Browser, start  # noqa: E402


def events_of(raw: bytes):
    return list(parse_sse(iter(raw.splitlines(keepends=True))))


class ChatUnitTests(unittest.TestCase):
    def test_sse_blocks_comments_and_multiline_data(self):
        raw = b": keep-alive\n\nevent: token\ndata: {\"text\": \"a\"}\n\nevent: answer\ndata: {\"content\":\ndata: \"b\"}\n\n"
        self.assertEqual([("token", {"text": "a"}), ("answer", {"content": "b"})], events_of(raw))

    def test_tool_calls_written_as_text_are_lifted(self):
        message = assistant_message({"choices": [{"message": {"content":
            'Sure.<tool_call>{"name": "open_layer", "arguments": {"layer": "CCTV"}}</tool_call>'}}]})
        self.assertEqual("Sure.", message["content"])
        self.assertEqual([("open_layer", {"layer": "CCTV"})], [(c["name"], c["arguments"]) for c in message["tool_calls"]])

    def test_returned_tool_calls_with_json_string_arguments(self):
        message = assistant_message({"choices": [{"message": {"content": None, "tool_calls": [
            {"id": "c1", "type": "function", "function": {"name": "ask_i360", "arguments": "{\"question\": \"q\"}"}}]}}]})
        self.assertEqual([{"id": "c1", "name": "ask_i360", "arguments": {"question": "q"}}], message["tool_calls"])

    def test_hl_api_reduced_answer(self):
        message = assistant_message({"model": "m", "content": None, "finish_reason": "tool_calls", "usage": {},
                                     "tool_calls": [{"id": "c1", "type": "function",
                                                     "function": {"name": "open_layer", "arguments": "{not json"}}]})
        self.assertEqual([{"id": "c1", "name": "open_layer", "arguments": {}}], message["tool_calls"])
        self.assertEqual("tool_calls", message["finish_reason"])
        empty = assistant_message({"content": "", "tool_calls": None, "finish_reason": "length"})
        self.assertEqual(("", [], "length"), (empty["content"], empty["tool_calls"], empty["finish_reason"]))

    def test_layers_merge_into_one_search(self):
        from datetime import datetime, timezone
        now = datetime(2026, 10, 9, tzinfo=timezone.utc)
        lambda_profile = {"queries": [
            {"item_types": ["image"], "source_applications": ["EO optical (fictional)"], "recent_days": 365,
             "limit": 200, "layer": "Satellite", "all_fields": True},
            {"source_applications": ["ADINT"], "recent_days": 365, "limit": 200, "layer": "ADINT",
             "fields": ["item_id", "location"]}]}
        body, exact = layers_search(lambda_profile, now)
        self.assertEqual(["EO optical (fictional)", "ADINT"], body["source_applications"])
        self.assertNotIn("item_types", body)  # only Satellite filters on type: dropping it keeps ADINT
        self.assertTrue(body["time"]["from"].startswith("2025-10-09"))
        self.assertFalse(exact)
        body, exact = layers_search({"queries": [{"source_applications": ["A"], "recent_days": 30},
                                                 {"source_applications": ["B"], "recent_days": 30}]}, now)
        self.assertEqual((["A", "B"], True), (body["source_applications"], exact))
        body, exact = layers_search({"filters": [{"field": "scenario", "values": ["syria"]}]}, now)
        self.assertEqual(({"filters": [{"field": "scenario", "values": ["syria"]}]}, True), (body, exact))

    def test_no_memory_tool(self):
        # What the investigation holds is asked of i360 and shown from its citations.
        from hl.chat import TOOLS
        self.assertNotIn("show_memory", [t["function"]["name"] for t in TOOLS])

    def test_the_panel_scope_is_never_narrowed(self):
        asked = []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append(body)
                return iter([("answer", {"content": "x", "citations": []})])

        class Host:
            def layers_scope(self):
                return {"kind": "results", "ids": [], "exact": True}

        ctx = TurnContext.from_request({"message": "x", "investigation_id": "INV-1", "scope": "layers"})
        turn = ChatTurn(None, Chat(), Host(), lambda e, d: None, ctx)
        turn.ask_i360({"question": "find him", "scope": "investigation"})
        self.assertNotIn("focus", asked[-1])
        self.assertEqual("results", asked[-1]["scope"]["kind"])
        turn.ask_i360({"question": "find him everywhere", "scope": "all"})  # there is no wider scope
        self.assertEqual("results", asked[-1]["scope"]["kind"])

    def test_auto_scope_comes_from_the_model_every_time(self):
        asked = []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append(body)
                return iter([("answer", {"content": "x", "citations": []})])

        class Host:
            def layers_scope(self):
                return {"kind": "results", "ids": [], "exact": True}

        ctx = TurnContext.from_request({"message": "x", "investigation_id": "INV-1", "scope": "auto"})
        turn = ChatTurn(None, Chat(), Host(), lambda e, d: None, ctx)
        turn.ask_i360({"question": "show the calls"})  # the question does not say where: our layers
        self.assertEqual("results", asked[-1]["scope"]["kind"])
        self.assertNotIn("focus", asked[-1])
        turn.ask_i360({"question": "linked records", "scope": "investigation"})
        self.assertEqual("INV-1", asked[-1]["focus"]["id"])
        no_case = ChatTurn(None, Chat(), Host(), lambda e, d: None, TurnContext.from_request({"message": "x", "scope": "auto"}))
        self.assertIn("error", no_case.ask_i360({"question": "linked records", "scope": "investigation"}))

    def test_an_inexact_layers_scope_is_never_sent_as_one_search(self):
        asked = []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append(body)
                return iter([("answer", {"content": "x", "citations": []})])

        class Host:
            def layers_scope(self):
                return {"kind": "results", "ids": [], "exact": False}

        turn = ChatTurn(None, Chat(), Host(), lambda e, d: None, TurnContext.from_request({"message": "x", "scope": "auto"}))
        self.assertIn("error", turn.ask_i360({"question": "what data do we have", "scope": "layers"}))
        self.assertEqual([], asked)

    def test_inexact_layers_are_asked_one_at_a_time(self):
        asked = []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append((body, conversation_id))
                name = body["scope"]["name"]
                return iter([("answer", {"content": f"{name} has 1", "citations": [{"id": f"{name}-1"}], "total": 1,
                                         "cards": {"agg": {"buckets": []}}}),
                             ("done", {"conversation_id": "fresh-" + name})])

        class Host:
            def layers_scope(self):
                return {"kind": "results", "ids": [], "exact": False}

            def layer_scopes(self):
                return [{"kind": "results", "name": n, "ids": [], "request": {"source_applications": [n]}}
                        for n in ("ADINT", "IPDR")]

        ctx = TurnContext.from_request({"message": "x", "scope": "auto", "i360_conversation_id": "panel",
                                        "i360_scope": "layers"})
        turn = ChatTurn(None, Chat(), Host(), lambda e, d: None, ctx)
        result = turn.ask_i360({"question": "what data do we have", "scope": "layers"})
        self.assertEqual({"ADINT", "IPDR"}, {b["scope"]["name"] for b, _ in asked})
        self.assertEqual([None, None], [c for _, c in asked])  # each layer is a fresh i360 conversation
        self.assertEqual(["ADINT-1", "IPDR-1"], sorted(c["id"] for c in result["cited_items"]))
        self.assertIn("[ADINT] ADINT has 1", result["answer"])
        self.assertTrue(result["has_counts"])
        self.assertEqual("panel", turn.i360_conversation_id)
        self.assertNotIn("scope_note", result)

    def test_our_data_is_counted_in_our_layers(self):
        asked = []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append(body)
                return iter([("answer", {"content": "x", "citations": []})])

        class Host:
            def layers_scope(self):
                return {"kind": "results", "ids": [], "exact": True}

        question = "What data types and volume do we have in the system?"
        turn = ChatTurn(None, Chat(), Host(), lambda e, d: None, TurnContext.from_request({"message": question, "scope": "auto"}))
        turn.ask_i360({"question": question, "scope": "all"})
        self.assertEqual("results", asked[-1]["scope"]["kind"])
        self.assertEqual("How many records are there, by type and month?", asked[-1]["question"])
        everywhere = "how many calls do we have everywhere in i360"
        turn = ChatTurn(None, Chat(), Host(), lambda e, d: None, TurnContext.from_request({"message": everywhere, "scope": "auto"}))
        turn.ask_i360({"question": everywhere, "scope": "all"})  # i360 is never asked outside our layers
        self.assertEqual("results", asked[-1]["scope"]["kind"])

    def test_a_layer_in_the_investigation_is_filtered_from_i360s_listing(self):
        # "IPDR" means nothing to i360: the investigation's records it lists are grouped by our layers.
        asked = []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append(body["question"])
                if len(asked) == 1:  # i360 answers from outside the investigation
                    return iter([("answer", {"leg": "agent", "content": "none", "citations": [{"id": "outside-1"}]})])
                return iter([("answer", {"leg": "search", "citations": [{"id": "ipdr-1"}, {"id": "img-1"}]})])

        class Host:
            def catalog_layers(self):
                return [{"id": "events:IPDR", "kind": "events", "source_type": "IPDR"},
                        {"id": "events:Cellular Calls", "kind": "events", "source_type": "Cellular Calls"},
                        {"id": "events:Calls", "kind": "events", "source_type": "Calls"}]

            def item_layers(self, ids):
                return [{"label": "IPDR", "rows": [{"i360_item_id": "ipdr-1"}]},
                        {"label": "Satellite", "rows": [{"i360_item_id": "img-1"}]}]

        ctx = TurnContext.from_request({"message": "x", "investigation_id": "INV-1", "scope": "auto"})
        turn = ChatTurn(None, Chat(), Host(), lambda e, d: None, ctx)
        result = turn.ask_i360({"question": "Which IPDR sessions are linked to this investigation?", "scope": "investigation"})
        self.assertEqual(["ipdr-1"], [c["id"] for c in result["cited_items"]])
        self.assertIn("1 record(s) of IPDR", result["note"])
        self.assertEqual(["Cellular Calls"], turn.layers_named("show the cellular calls"))  # not also "Calls"
        self.assertEqual([], ChatTurn(None, Chat(), Host(), lambda e, d: None, ctx).layers_named("show the IPDRs"))

    def test_investigation_overview_is_listed_by_i360_search(self):
        # i360's overview leg gives counts only; a second ask reaches its search leg, which lists the records.
        asked = []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append((body, conversation_id))
                if len(asked) <= 2:  # the brief, then a listing i360 also reads as an overview
                    return iter([("answer", {"leg": "overview", "content": "1 image", "citations": [],
                                             "cards": {"case": {"total": 1}}}), ("done", {"conversation_id": "c-1"})])
                return iter([("answer", {"leg": "search", "citations": [{"id": "img-7", "type": "image"},
                                                                         {"id": "doc-1", "type": "document"}]})])

        class Host:  # img-7 is in our Satellite layer; doc-1 is in none of our layers
            def catalog_layers(self):
                return [{"id": "events:Satellite", "kind": "events", "source_type": "Satellite"}]

            def item_layers(self, ids):
                return [{"label": "Satellite", "rows": [{"i360_item_id": "img-7"}]},
                        {"label": "news", "rows": [{"i360_item_id": "doc-1"}]}]

        ctx = TurnContext.from_request({"message": "what records are linked", "investigation_id": "INV-1"})
        turn = ChatTurn(None, Chat(), Host(), lambda e, d: None, ctx)
        result = turn.ask_i360({"question": "what records are linked", "scope": "investigation"})
        self.assertEqual(["img-7"], [c["id"] for c in result["cited_items"]])
        self.assertEqual(["img-7"], [c["id"] for c in turn.cited])
        self.assertEqual(["find all items", "search all items"], [body["question"] for body, _ in asked[1:]])
        self.assertEqual([None, None], [conversation for _, conversation in asked[1:]])
        self.assertEqual("INV-1", asked[2][0]["focus"]["id"])
        self.assertIn("1 record(s) linked to the investigation are outside our layers", result["note"])  # strict
        self.assertEqual("1 image", result["answer"])  # the brief stays i360's answer
        self.assertEqual("c-1", turn.i360_conversation_id)  # the listing does not take over the conversation

    def test_entities_come_from_i360_and_open_in_the_viewer(self):
        from hl.chat import answer_entities
        answer = {"leg": "lookup", "citations": [{"id": "item-1", "type": "image"}],
                  "cards": {"list": {"rows": [{"entity_id": "p-1", "entity_type": "PERSON_OF_INTEREST", "entity_name": "Arman Rahimi"},
                                              {"id": "p-2", "entity_type": "PERSON_OF_INTEREST", "name": "Lena Rahimi"},
                                              {"entity_id": "c-1", "entity_type": "AICHAT_ENTRY"}]}}}
        self.assertEqual([{"id": "p-1", "type": "PERSON_OF_INTEREST", "name": "Arman Rahimi"},
                          {"id": "p-2", "type": "PERSON_OF_INTEREST", "name": "Lena Rahimi"}], answer_entities(answer))
        asked, events = [], []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append(body)
                return iter([("answer", answer)])

        class Host:
            def entity(self, entity_type, entity_id):
                return {"entity_id": entity_id, "entity_type": "person", "canonical_name": "Arman Rahimi"}

            def layers_scope(self):
                return {"kind": "results", "ids": [], "exact": True}

        turn = ChatTurn(None, Chat(), Host(), lambda e, d: events.append((e, d)),
                        TurnContext.from_request({"message": "open Arman Rahimi", "scope": "layers"}))
        self.assertIn("error", turn.open_entity({"entity_id": "p-1"}))  # not returned by i360 yet
        result = turn.ask_i360({"question": "open Arman Rahimi", "scope": "all"})
        self.assertEqual(["p-1", "p-2"], [e["id"] for e in result["entities"]])
        self.assertEqual("Arman Rahimi", turn.open_entity({"entity_id": "p-1"})["opened"])
        self.assertEqual("p-1", [d for e, d in events if e == "action"][-1]["entity_id"])
        turn.ask_i360({"question": "his calls", "entity_id": "p-1"})
        self.assertEqual({"id": "p-1", "type": "PERSON_OF_INTEREST", "name": "Arman Rahimi"}, asked[-1]["entity"])
        self.assertEqual("results", asked[-1]["scope"]["kind"])  # people too are asked about inside our layers
        # The shape i360's entity leg returned on LAMBDA (cards.card), and the top-level people list.
        lambda_answer = {"leg": "entity", "cards": {"card": {
            "id": "da1cbd3a", "type": "PERSON_OF_INTEREST", "label": "Person", "kind": "entity", "name": "Arman Rahimi",
            "links": [{"type": "INTELLIGENCE_INVESTIGATION", "id": "aii-demo-military-convoy", "name": "Suspicious military convoy"}],
            "alts": [{"name": "Arman Rahimi - old", "label": "Person"}]}},
            "people": [{"id": "p-9", "kind": "entity", "type": "PERSON_OF_INTEREST", "name": "Lena"}]}
        self.assertEqual(["p-9", "da1cbd3a"], [e["id"] for e in answer_entities(lambda_answer)])
        ctx = TurnContext.from_request({"message": "his calls", "previous_entities": [
            {"id": "p-1", "type": "PERSON_OF_INTEREST", "name": "Arman Rahimi"}, {"no": "id"}]})
        self.assertEqual(["p-1"], [e["id"] for e in ctx.previous_entities])

    def test_layers_on_screen_carry_their_filters(self):
        ctx = TurnContext.from_request({"message": "x", "open_layers": [
            "Old name only",
            {"label": "ADINT", "filters": [{"field": "keyboard_language", "value": "fa"}], "shown": 12, "total": 120},
            {"label": "IPDR", "filters": [], "start_time": "2026-09-01T00:00:00Z", "end_time": "", "shown": 5, "total": 5},
            {"label": "CCTV", "filters": [], "shown": 3, "total": 3}, {"no": "label"}]})
        ctx.open_layers[2]["filters"].append({"field": "i360.ip.source_ip", "value": "10.0.0.1", "where": "table"})
        ctx.open_layers[3]["filters"].append({"field": "Keyboard language", "value": "he", "where": "table"})

        turn = ChatTurn(None, None, None, lambda e, d: None, ctx)
        turn.catalog_cache = []
        self.assertIn("Old name only; "
                      'ADINT (filtered: keyboard_language contains "fa"; 12 of 120 records shown); '
                      'IPDR (filtered: ip.source_ip contains "10.0.0.1" (table column filter); time 2026-09-01T00:00:00Z to …); '
                      'CCTV (filtered: Keyboard language contains "he" (table column filter))', turn.context_text())

    def test_a_raw_test_question_goes_to_i360_as_typed(self):
        asked, events = [], []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append(body)
                return iter([("answer", {"content": "3 found", "citations": [{"id": "a-1"}], "total": 3})])

        ctx = TurnContext.from_request({"message": "/i360 location_update items from ADINT where x is fa"})
        turn = ChatTurn(None, Chat(), None, lambda e, d: events.append((e, d)), ctx)
        turn.raw_test = True
        turn.run()
        self.assertEqual("location_update items from ADINT where x is fa", asked[0]["question"])
        self.assertNotIn("scope", asked[0])
        self.assertEqual("done", events[-1][0])
        off = ChatTurn(None, Chat(), None, lambda e, d: None, ctx)  # off by default: the usual turn
        self.assertFalse(off.raw_test)

    def test_a_named_layer_is_asked_alone_with_our_field_names_as_labels(self):
        asked = []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append(body)
                return iter([("answer", {"content": "2 found", "citations": [{"id": "a-1"}, {"id": "a-2"}]})])

        class Host:
            def layers_scope(self):
                return {"kind": "results", "ids": [], "exact": False}

            def layer_scopes(self):
                return [{"kind": "results", "name": n, "ids": [], "request": {"source_applications": [n]}}
                        for n in ("ADINT", "IPDR", "Cellular Calls", "Calls")]

            def index_field(self, path):
                return path if path in {"user_agents_data.language_code", "event_time"} else ""

            def profile_labels(self):
                return {"related_objects.id": ["linked record"]}

        events = []
        ctx = TurnContext.from_request({"message": "Show me all adint records with fa keyboard", "scope": "auto", "labels": {
            "user_agents_data.language_code": ["keyboard language", "שפת מקלדת"], "not.a.field": ["thing"],
            "event_time": "timestamp utc", "empty": []}})
        turn = ChatTurn(None, Chat(), Host(), lambda e, d: events.append((e, d)), ctx)
        result = turn.ask_i360({"question": "ADINT records with fa keyboard language", "scope": "layers"})
        self.assertEqual(1, len(asked))  # ADINT only, not one question per layer
        self.assertEqual("ADINT", asked[0]["scope"]["name"])
        self.assertEqual("records with fa keyboard language", asked[0]["question"])  # the layer name is not i360's word
        self.assertEqual({"event_time": ["timestamp utc"], "related_objects.id": ["linked record"],
                          "user_agents_data.language_code": ["keyboard language", "שפת מקלדת"]},
                         asked[0]["labels"])  # the profile's words plus the screen's, only the index's fields
        self.assertIn("not.a.field", [d.get("detail") for e, d in events if e == "step"][0])
        self.assertEqual(2, result["cited_count"])
        asked.clear()
        turn = ChatTurn(None, Chat(), Host(), lambda e, d: None, TurnContext.from_request({"message": "x", "scope": "auto"}))
        turn.ask_i360({"question": "Cellular Calls and IPDR on the 3rd", "scope": "layers"})
        self.assertEqual({"Cellular Calls", "IPDR"}, {b["scope"]["name"] for b in asked})  # not also "Calls"

    def test_the_model_sets_the_scope_and_the_layers_are_ored_by_fields(self):
        asked = []

        class Chat:
            def ask(self, body, conversation_id):
                asked.append(body)
                return iter([("answer", {"content": "1", "citations": [{"id": "ipdr-1"}], "total": 1})])

        class Llm:
            def complete(self, messages, tools):
                self.seen = messages
                return {"content": "", "tool_calls": [{"id": "c1", "name": "set_scope", "arguments": {
                    "layers": ["ipdr", "ADINT", "Nope"], "question": "records where linked record is X"}}]}

        class Host:
            def layers_scope(self):
                return {"kind": "results", "ids": [], "exact": False}

            def layer_scopes(self):
                return [{"kind": "results", "name": n, "ids": [], "request": {"source_applications": [n]}}
                        for n in ("ADINT", "IPDR", "CCTV")]

            def combined_scope(self, names):
                return {"kind": "results", "name": " + ".join(names), "request": {"filters": [{"any_of": [
                    [{"field": "source_application", "values": [n]}] for n in names]}]}}

        llm = Llm()
        turn = ChatTurn(llm, Chat(), Host(), lambda e, d: None, TurnContext.from_request({"message": "x", "scope": "auto"}))
        turn.ask_i360({"question": "IPDR and ADINT records where linked record is X", "scope": "layers"})
        self.assertIn("- IPDR: {\"source_applications\": [\"IPDR\"]}", llm.seen[0]["content"])
        self.assertEqual(1, len(asked))  # one request: the two layers ORed by their fields and values
        self.assertEqual("records where linked record is X", asked[0]["question"])
        self.assertEqual("IPDR + ADINT", asked[0]["scope"]["name"])

    def test_without_a_model_layer_names_are_matched_and_taken_out(self):
        turn = ChatTurn(None, None, None, lambda e, d: None, TurnContext.from_request({"message": "x"}))
        named, question = turn.plan_scope("IPDR records where linked record is X",
                                          [{"name": "IPDR"}, {"name": "ADINT"}])
        self.assertEqual(["IPDR"], [s["name"] for s in named])
        self.assertEqual("records where linked record is X", question)

    def test_open_item_takes_an_id_the_user_typed(self):
        class Host:
            def item_layers(self, ids):
                return [{"label": "Satellite", "rows": [{"i360_item_id": i} for i in ids]}]

        ctx = TurnContext.from_request({"message": "open 2a8dbf57-1234"})
        turn = ChatTurn(None, None, Host(), lambda e, d: None, ctx)
        self.assertEqual("2a8dbf57-1234", turn.open_item({"item_id": "2a8dbf57-1234"})["opened"])
        self.assertIn("error", turn.open_item({"item_id": "other-record"}))

    def test_open_item_returns_no_record_fields(self):
        class Host:
            def item_layers(self, ids):
                return [{"label": "Satellite", "rows": [{"i360_item_id": i, "text": "3x cargo truck"} for i in ids]}]

        ctx = TurnContext.from_request({"message": "open it", "previous_citations": ["img-1"]})
        turn = ChatTurn(None, None, Host(), lambda e, d: None, ctx)
        result = turn.open_item({"item_id": "img-1"})
        self.assertEqual("img-1", result["opened"])
        self.assertNotIn("record", result)
        self.assertNotIn("3x cargo truck", json.dumps(result))
        self.assertEqual(1, turn.show_items({"item_ids": ["img-1"], "label": "x", "view": "map"})["already_on_screen"])

    def test_model_rounds_get_their_own_timeout(self):
        from hl.chat import LlmClient
        from hl.client import HlClient
        base = HlClient("http://hl.example", "token", timeout=30)
        llm = LlmClient(base, "m", timeout=180)
        self.assertEqual((180, 30), (llm.client.timeout, base.timeout))

    def test_context_is_validated(self):
        with self.assertRaises(ValueError):
            TurnContext.from_request({"message": "  "})
        ctx = TurnContext.from_request({"message": "hi", "scope": "everything",
            "previous_citations": ["a", {"id": "b", "type": "call"}, {"no": "id"}]})
        self.assertEqual("auto", ctx.scope)
        self.assertEqual(["a", "b"], [c["id"] for c in ctx.previous_citations])

    def test_app_tools_refuse_ids_i360_did_not_cite(self):
        events = []

        class Host:
            def catalog_layers(self):
                return []

            def item_layers(self, ids):
                return []  # i360 has no such record

            def memory_layers(self, investigation_id):
                return []

        ctx = TurnContext.from_request({"message": "x", "previous_citations": ["known"]})
        turn = ChatTurn(None, None, Host(), lambda e, d: events.append((e, d)), ctx)
        self.assertIn("error", turn.show_items({"item_ids": ["made-up"], "label": "x", "view": "map"}))
        self.assertIn("error", turn.open_item({"item_id": "made-up"}))
        self.assertIn("error", turn.save_to_memory({"layer": "x"}))  # no investigation open
        self.assertEqual([], [e for e in events if e[0] == "action"])


class ChatApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.estate = FakeEstate({"analyst": "analyst"}, result_window=200)
        cls.estate.load_fixture(FIXTURE)
        cls.estate.provision(type_definitions("AII_"))
        cls.fake = start(make_server("127.0.0.1", 0, cls.estate))
        chat_server, cls.chat = make_chat_server("127.0.0.1", 0, cls.estate)
        cls.chat_server = start(chat_server)
        os.environ.update({
            "HL_API_URL": f"http://127.0.0.1:{cls.fake.server_address[1]}",
            "APP_COOKIE_SECURE": "false", "APP_SCENARIO": "syria", "APP_SNAPSHOT_TTL": "300",
            "CHAT_SERVICE_URL": f"http://127.0.0.1:{chat_server.server_address[1]}",
        })
        import server as app_server
        from http.server import ThreadingHTTPServer
        try:
            handler = type("ChatHandler", (app_server.Handler,), {"app": app_server.App(app_server.load_settings()), "quiet": True})
            os.environ["CHAT_SERVICE_URL"] = ""
            off = type("ChatOffHandler", (app_server.Handler,), {"app": app_server.App(app_server.load_settings()), "quiet": True})
        finally:
            os.environ.pop("CHAT_SERVICE_URL", None)
        cls.app = start(ThreadingHTTPServer(("127.0.0.1", 0), handler))
        cls.app_off = start(ThreadingHTTPServer(("127.0.0.1", 0), off))
        cls.base = f"http://127.0.0.1:{cls.app.server_address[1]}"
        cls.base_off = f"http://127.0.0.1:{cls.app_off.server_address[1]}"

    @classmethod
    def tearDownClass(cls):
        for server in (cls.app, cls.app_off, cls.chat_server, cls.fake):
            server.shutdown()

    def setUp(self):
        self.estate.llm_off = False
        self.estate.llm_empty = False
        self.chat.asks.clear()

    def signed_in(self, base=None):
        browser = Browser(base or self.base)
        self.assertEqual(200, browser.login()[0])
        return browser

    def ask(self, browser, body):
        request = urllib.request.Request(browser.base + "/api/chat/ask", data=json.dumps(body).encode(), method="POST",
                                         headers={"Content-Type": "application/json"})
        with browser.opener.open(request, timeout=30) as response:
            self.assertEqual("text/event-stream", response.headers.get_content_type())
            return events_of(response.read())

    def actions(self, events, kind=None):
        return [d for e, d in events if e == "action" and (kind is None or d["kind"] == kind)]

    def test_status_says_the_chat_is_on(self):
        self.assertTrue(Browser(self.base).call("GET", "/api/status")[1]["features"]["ai"])
        self.assertFalse(Browser(self.base_off).call("GET", "/api/status")[1]["features"]["ai"])

    def test_question_asks_i360_then_shows_what_it_cited(self):
        events = self.ask(self.signed_in(), {"message": "convoy trucks", "tz": "Asia/Jerusalem"})
        relayed = [d["event"] for e, d in events if e == "i360"]
        self.assertEqual(["status", "token", "token", "answer", "done"], relayed)
        shown = self.actions(events, "show_items")
        self.assertEqual(1, len(shown))
        self.assertEqual("map", shown[0]["view"])  # the cited items have places
        rows = [r for g in shown[0]["groups"] for r in g["rows"]]
        cited = [d["data"]["citations"] for e, d in events if e == "i360" and d["event"] == "answer"][0]
        self.assertEqual([c["id"] for c in cited], [r["i360_item_id"] for r in rows])
        self.assertTrue(all(r.get("record_id") for r in rows))
        done = [d for e, d in events if e == "done"][0]
        self.assertTrue(done["i360_conversation_id"].startswith("conv-"))
        self.assertEqual(len(cited), len(done["citations"]))
        self.assertIn("Showed", [d for e, d in events if e == "note"][0]["text"])
        ask = self.chat.asks[-1]
        self.assertEqual(("convoy trucks", "app", "Asia/Jerusalem"), (ask["question"], ask["origin"], ask["tz"]))
        self.assertNotIn("focus", ask)  # no investigation open
        self.assertEqual({"kind": "results", "name": "Our layers", "query": "the app's layers",
                          "request": {"filters": [{"field": "scenario", "values": ["syria"]}]}},
                         {k: v for k, v in ask["scope"].items() if k not in {"ids", "total"}})
        self.assertEqual(min(100, ask["scope"]["total"]), len(ask["scope"]["ids"]))

    def test_open_investigation_is_the_focus(self):
        self.ask(self.signed_in(), {"message": "convoy", "investigation_id": "INV-1", "investigation_name": "Convoy"})
        self.assertEqual({"kind": "entity", "id": "INV-1", "name": "Convoy", "type": "AII_INVESTIGATION",
                          "label": "Investigation"}, self.chat.asks[-1]["focus"])
        self.ask(self.signed_in(), {"message": "convoy", "investigation_id": "INV-1", "scope": "layers"})
        self.assertNotIn("focus", self.chat.asks[-1])
        self.assertEqual("results", self.chat.asks[-1]["scope"]["kind"])
        self.ask(self.signed_in(), {"message": "convoy", "investigation_id": "INV-1", "scope": "all"})
        self.assertNotIn("focus", self.chat.asks[-1])
        self.assertEqual("results", self.chat.asks[-1]["scope"]["kind"])  # there is no "all data" scope

    def test_investigation_questions_avoid_i360_memory_words(self):
        browser = self.signed_in()
        first = self.ask(browser, {"message": "What's saved in this investigation?", "investigation_id": "INV-1"})
        # A bare "What's linked" reads to i360 as an entity name, so the whole question is replaced.
        self.assertEqual("What records are linked in this investigation?", self.chat.asks[-1]["question"])
        self.assertEqual("INV-1", self.chat.asks[-1]["focus"]["id"])
        done = [d for e, d in first if e == "done"][0]
        self.ask(browser, {"message": "convoy", "investigation_id": "INV-1", "scope": "all",
                           "i360_conversation_id": done["i360_conversation_id"]})
        self.assertIsNone(self.chat.asks[-1]["focus"])  # the conversation's focus is cleared, not kept

    def test_new_scope_starts_a_new_i360_conversation(self):
        browser = self.signed_in()
        first = self.ask(browser, {"message": "convoy", "investigation_id": "INV-1"})
        done = [d for e, d in first if e == "done"][0]
        self.assertEqual("investigation", done["i360_scope"])
        self.ask(browser, {"message": "convoy", "investigation_id": "INV-1", "scope": "all",
                           "i360_conversation_id": done["i360_conversation_id"], "i360_scope": "investigation"})
        self.assertNotIn("conversation_id", self.chat.asks[-1])  # the investigation's evidence stays behind
        self.assertNotIn("focus", self.chat.asks[-1])

    def test_investigation_wording(self):
        from hl.chat import investigation_wording
        for question in ("What is in memory?", "what's stored", "What is linked to this investigation?"):
            self.assertEqual("What records are linked in this investigation?", investigation_wording(question))
        self.assertEqual("Which linked records mention trucks?", investigation_wording("Which saved records mention trucks?"))

    def test_one_unreadable_record_does_not_hide_the_rest(self):
        browser = self.signed_in()
        first = self.ask(browser, {"message": "convoy trucks"})
        cited = [c["id"] for c in [d for e, d in first if e == "done"][0]["citations"]]
        self.assertGreater(len(cited), 1)
        self.estate.get_items_poison = {cited[0]}
        try:
            events = self.ask(browser, {"message": "convoy trucks"})
        finally:
            self.estate.get_items_poison = set()
        shown = [r["i360_item_id"] for a in self.actions(events, "show_items") for g in a["groups"] for r in g["rows"]]
        self.assertEqual(cited[1:], shown)

    def test_follow_up_opens_a_cited_record(self):
        browser = self.signed_in()
        first = self.ask(browser, {"message": "convoy trucks"})
        done = [d for e, d in first if e == "done"][0]
        events = self.ask(browser, {"message": "open the second record", "previous_citations": done["citations"],
                                    "i360_conversation_id": done["i360_conversation_id"]})
        opened = self.actions(events, "open_item")
        self.assertEqual(done["citations"][1]["id"], opened[0]["row"]["i360_item_id"])
        self.assertTrue(done["i360_last_turns"][0].startswith("AICHAT_MSG_"))
        self.assertEqual([], [e for e, d in events if e == "i360"])  # a command does not ask i360

    def test_record_in_the_viewer_can_be_opened_without_a_citation(self):
        item_id = next(iter(self.estate.items))
        events = self.ask(self.signed_in(), {"message": "open this record", "viewer_item_id": item_id})
        self.assertEqual(item_id, self.actions(events, "open_item")[0]["row"]["i360_item_id"])
        self.assertIn(f"Record open in the viewer now: {item_id}", self.estate.llm_requests[-1]["messages"][0]["content"])

    def test_made_up_record_is_not_opened(self):
        events = self.ask(self.signed_in(), {"message": "open this record", "viewer_item_id": "no-such-item"})
        self.assertEqual([], self.actions(events, "open_item"))
        failed = [d for e, d in events if e == "step" and d.get("error")]
        self.assertEqual(["Couldn't open the record"], [d["text"] for d in failed])
        self.assertIn("no readable record with id no-such-item", failed[0]["detail"])

    def test_command_opens_a_catalog_layer(self):
        events = self.ask(self.signed_in(), {"message": "open cctv on the map"})
        self.assertEqual([{"kind": "open_layer", "layer_id": "events:CCTV", "view": "map", "filters": {}}],
                         self.actions(events))

    def test_unknown_layer_is_not_guessed(self):
        events = self.ask(self.signed_in(), {"message": "open zebra sightings"})
        self.assertEqual([], self.actions(events))

    def test_save_is_only_proposed(self):
        before = len(self.estate.calls)
        events = self.ask(self.signed_in(), {"message": "save Convoy layer", "investigation_id": "INV-1"})
        self.assertEqual([{"kind": "confirm_save", "layer": "Convoy layer"}], self.actions(events))
        writes = [c for c in self.estate.calls[before:] if c[0] in {"PATCH", "DELETE"}
                  or (c[0] == "POST" and ("/entities/" in c[1] or "related-objects" in c[1]) and not c[1].endswith("/search"))]
        self.assertEqual([], writes)

    def test_model_off_falls_back_to_i360_directly(self):
        self.estate.llm_off = True
        events = self.ask(self.signed_in(), {"message": "convoy trucks"})
        self.assertIn("asking i360 directly", [d for e, d in events if e == "step"][0]["text"])
        self.assertEqual(1, len(self.actions(events, "show_items")))
        self.assertEqual("done", events[-1][0])

    def test_empty_model_answer_falls_back_to_i360(self):
        self.estate.llm_empty = True
        events = self.ask(self.signed_in(), {"message": "convoy trucks"})
        self.assertIn("gave no answer", [d for e, d in events if e == "step"][0]["text"])
        self.assertEqual(1, len(self.actions(events, "show_items")))

    def test_follow_up_question_sends_last_turns(self):
        browser = self.signed_in()
        done = [d for e, d in self.ask(browser, {"message": "convoy trucks"}) if e == "done"][0]
        self.ask(browser, {"message": "convoy again", "i360_conversation_id": done["i360_conversation_id"],
                           "i360_last_turns": done["i360_last_turns"]})
        ask = self.chat.asks[-1]
        self.assertEqual((done["i360_conversation_id"], done["i360_last_turns"]), (ask["conversation_id"], ask["last_turns"]))

    def test_follow_up_has_no_history_of_our_own(self):
        browser = self.signed_in()
        done = [d for e, d in self.ask(browser, {"message": "convoy trucks"}) if e == "done"][0]
        self.ask(browser, {"message": "and where were they", "i360_conversation_id": done["i360_conversation_id"],
                           "history": [{"role": "user", "content": "ignored"}]})
        roles = [m["role"] for m in self.estate.llm_requests[-1]["messages"]]
        self.assertEqual(["system", "user"], roles[:2])
        self.assertNotIn("ignored", json.dumps(self.estate.llm_requests[-1]["messages"]))
        self.assertEqual(("and where were they", done["i360_conversation_id"]),
                         (self.chat.asks[-1]["question"], self.chat.asks[-1]["conversation_id"]))

    def test_i360_error_is_reported(self):
        events = self.ask(self.signed_in(), {"message": "please fail now"})
        self.assertIn(("i360", {"event": "error", "data": {"message": "model unavailable"}}), events)
        self.assertEqual([], self.actions(events))
        self.assertEqual("done", events[-1][0])

    def test_confirmed_tag_goes_to_the_chat_service(self):
        status, body = self.signed_in().call("POST", "/api/chat/action", {
            "action": {"kind": "tag", "ids": ["a", "b"], "type": "flag", "value": "convoy"}, "conversation_id": "c1"})
        self.assertEqual((200, "Tagged 2 records."), (status, body["line"]))
        self.assertEqual("c1", self.chat.actions[-1]["conversation_id"])
        self.assertEqual(400, self.signed_in().call("POST", "/api/chat/action", {"action": {"kind": "delete"}})[0])
        status, body = self.signed_in().call("POST", "/api/chat/action", {
            "action": {"kind": "note", "ids": ["a"], "value": "seen twice"}})
        self.assertEqual((200, "Annotated 1 records."), (status, body["line"]))
        self.assertEqual({"kind": "annotate", "ids": ["a"], "type": None, "value": "seen twice", "text": None,
                          "conversation_id": None},
                         self.chat.actions[-1])
        self.assertEqual(400, self.signed_in().call("POST", "/api/chat/action", {
            "action": {"kind": "tag", "ids": [str(i) for i in range(51)], "type": "flag", "value": "x"}})[0])

    def test_cited_items_are_read_for_the_viewer(self):
        item_id = next(iter(self.estate.items))
        status, body = self.signed_in().call("POST", "/api/chat/items", {"ids": [item_id, "missing"]})
        self.assertEqual(200, status)
        self.assertEqual([item_id], [r["i360_item_id"] for g in body["groups"] for r in g["rows"]])

    def test_guards(self):
        self.assertEqual(401, Browser(self.base).call("POST", "/api/chat/ask", {"message": "x"})[0])
        self.assertEqual(400, self.signed_in().call("POST", "/api/chat/ask", {"message": ""})[0])
        status, body = self.signed_in(self.base_off).call("POST", "/api/chat/ask", {"message": "x"})
        self.assertEqual((501, "chat_off"), (status, body["error"]))


if __name__ == "__main__":
    unittest.main()

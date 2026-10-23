# i360 / HL API gaps met while building AI-Intelligence on LAMBDA

Where i360 or platform-hl-api (contract 261, October 2026) did not directly support what the app needed,
what the app does instead, the weakness of that choice, and what to ask the platform owners for.
Checked against LAMBDA data with a signed-in user; "the app" is `llm_investigation_orchestrator_serbia_poc/`.

## Summary table

| # | Area | What i360 / HL API does not support | What the app does instead | Weakness | Ask the platform for |
|---|---|---|---|---|---|
| 1 | Chat: investigation records | The i360 chat sends "what records are linked / show the records" to its overview leg: a case-brief card with counts, no item ids | Asks i360 again in a hidden conversation with fixed wordings ("find all items", "search all items", "find all records") and cites what its search leg returns | Depends on i360's model sorting the wording; "find all items in this investigation" flips back to overview | i360-chat: route "list / show the records" to search |
| 2 | Chat: layer names | i360 does not know the app's layer names ("IPDR" is aggregated_ip_session from HOSHENTEL to it) and answers from outside the investigation | Lists the investigation's records through i360, groups them by the app's layers and keeps the named layer | i360's own answer text can contradict what is shown | i360-chat: accept a layer / type vocabulary |
| 3 | Chat: "our layers" scope | The chat's results scope takes at most 100 ids; a search body cannot say "newest N per query" | When the merged search is inexact (on LAMBDA it keeps only the 12-month window), asks i360 once per layer in parallel, each with that layer's exact request, and joins the answers | One fresh i360 conversation per layer, so a follow-up does not see the joined answer; more i360 calls | A scope that takes a query per layer |
| 4 | Record → entity links: why | related_objects has matching_value / relation_source, but they are empty / null on our data | The app compares the person's identifiers (IMEI, MSISDN, IMSI) with the record's (asset_identifier, party identifiers) and shows "via IMEI … (matched by the app)" | An inference, not i360's statement | Fill matching_value / relation_source when links are made |
| 5 | Record → record links | Two mechanisms (see "Links" below): parent/child links, none on our data; and related_objects of type ITEM, made automatically by i360 with the matched value (1 ADINT↔IPDR pair on our data). No field names or rule on either; no write operation | ITEM links shown under "Linked raw records" with i360's matched value; the fields holding it are found by comparing values ("matched by the app") | Which fields matched is an inference | The matched fields / rule on each ITEM link; a write for item-to-item links |
| 6 | The app's memory type | AII_MEMORY_ITEM is not provisioned on LAMBDA (provisioning restarts platform services) | Records saved via items/related-objects on the investigation; persons as LINK entities (hit id only in general.entity_id; removal needs ?confirm=link id) | Saving layers and areas does not work on LAMBDA | A slot to provision AII_MEMORY_ITEM |
| 7 | Item fields | Fields arrived in stages (260: additional_info, user_agents_data, ip, context; 261: li, telephony, sms, phone_call, cell value) | Guessed meanings until then; flattening of one-entry lists, SMS parts and cell entries; call fields (call id, sides from target_indication) built by the app | Still missing: file_infos[0].path; CIN and Call_Id exist but are empty | The file storage path |
| 8 | Coverage | Facet filters take COVERAGE entity ids, not names (two coverages "calls" / "Calls"); search hits do not carry the coverage | Coverage ids in the profile; records matched to layers by type and source | A saved voice call is always named "Cellular Locations", even when it came from Cellular Calls | Coverage (or the matched query) on search hits |
| 9 | Media | CCTV originals are HEVC (browsers do not play them); entity pictures need a bearer token, no signed link | web_preview variant for video; the app proxies entity pictures | Extra hop for pictures | Signed links for entity files |
| 10 | Limits and missing operations | No "newest N" in search; no item delete; IMEI entities not readable by the user (403); empty items/context lists mean "unknown" or "none" | Limits applied in the app with paging and time-window splitting | Garbage data cannot be cleaned | Item delete or archive |
| 11 | Chat model | The assistant model is HL API's default (not pinned) | Rules in the system prompt | It occasionally drops its closing line | — |
| 12 | Freshness | No change feed used by the app | A 5-minute per-user snapshot | Changes in i360 appear after up to 5 minutes | — |
| 13 | Deployment | Not i360: every micro-apps push needs a teammate's approval, reset by any new push; the chat's in-cluster address is not documented for apps | Address taken from freelang-search-ui's configuration (http://i360-chat-py:4020) | Slow round trips | Documented in-cluster addresses |
| 14 | Presenting chat results | The chat returns citations (id, type, time, text) and cards for its own UI; no "show as a layer", no view hint | The app reads cited records again (items/get), groups them by layer, and the assistant picks map / timeline / table and the layer name; previous citations are sent back by the browser each turn | Extra calls per answer; i360's text and the app's layer can disagree; i360's own cards are not reused | A presentation hint with citations (kind of records, whether places matter) |
| 15 | Layer presentation and display names | HL API returns no field display names or default view per item type. ui-360 does have display names: its dictionary configuration (htx/ui/app/dictionary.json in environments-configuration, branch intel_2026_04_2791300, and the live /opt/app/shared/dictionary.json in the ui-360 pod) | Names copied by hand from the ingestion mappings into the profile; default view by rule (calls → timeline, map if any row has coordinates, else table); call viewer by a profile flag; collection type → layer by a table in the code | Names can drift from ingestion and from i360's own UI ("Source application"); a layer becomes a map layer as soon as one row has coordinates; renaming a layer breaks the collection table silently | An HL API endpoint for field display names (the configuration ui-360 reads) |
| 16 | Call transcripts | Lines and translations are insights per party (transcription / translation); text.english holds only one line; translation times do not match the originals' | The app pairs translations with lines per party, in order, and draws them in the call viewer | Wrong pairing if a translation is missing or entered out of order | A link from each translation to the line it translates |
| 17 | Search vs get by id return different fields | items/search and items/get describe the same item with different field sets. On ADINT, `language` is filled by search only (52 of 120 records) and is always null in items/get (no include brings it), although both contracts declare it; items/get alone has the content (user_agents_data, ip, additional_info, fe_correlation_ids, flags, tags), which search cannot return (its include takes only text / related_objects). Checked field by field on all 120 ADINT records; `language` is the only field of the layer in search and not in items/get | Two mappings per layer in the profile: `labels` for rows read through search (the layers: search, then items/get, merged) and `labels_by_id` for rows read by id (items/get alone: chat results, opening a cited record, investigation records, the report's extra records). ADINT keyboard_language is `language` in the first and `user_agents_data.language_code` in the second | Bad design: one record can show two values for the same field depending on how it was opened (ADINT 702e8fa9: empty in the layer, "fa" by id); every field has to be checked in both calls; the app needs an extra search per 100 ids to get the indexed fields by id | items/get to return every field search returns (here `language`), so one item has one set of fields |

## Links: what HL API offers and what is missing

### Record → entity (used by the app)

- **Read:** `include: ["related_objects"]` on `POST /api/v1/items/get`; each entry has `id`, `type`, `relation_type`,
  `group`, `relation_source`, `matching_value`. From the entity side: `POST /api/v1/items/search` with
  `related_to: {ids: [entity_id]}`.
- **Write:** `POST /api/v1/items/related-objects` (entity + item ids + relation type, with `dry_run`); `DELETE` removes.
- **On our data:** Arman Rahimi (PERSON_OF_INTEREST da1cbd3a…) is linked from 306 records: 300 Cellular Locations and
  2 calls (`attachment_associated`), 4 IPDR (`associated`). `matching_value` is empty and `relation_source` null on all.
- **Missing:** why a record is linked. The app shows the shared identifier as its own check ("matched by the app").

### Record → record: related_objects of type ITEM (used by the app)

- **Read:** the same `include: ["related_objects"]`; an entry whose `type` is `ITEM` points to another item, e.g. on
  IPDR 4e981670 (HOSHENTEL): `{id: 70097b75…, type: "ITEM", label: "location_location_technical", relation_type:
  "associated", relation_source: "automatic", matching_value: ["203.0.113.107"]}`, and the mirror entry on ADINT 70097b75.
- **On our data:** 1 pair across all six layers (both records carry it). The value 203.0.113.107 is stored only in the
  links and in `ip.ip_sessions[0].destination_ip` (IPDR) / `ip.ip_sessions[0].source_ip` (ADINT).
- **Given by i360:** that the records are linked, automatically, on that value. **Not given:** which fields or rule.
  The app finds the fields holding the value and labels them "matched by the app".
- These links do not appear in items/context's buckets or in parent_ids.

### Record → record: parent / child ("Related items")

- **Documented** in platform-hl-api/docs/okf-api:
  - `filtering-items-by-field.md`: `{"field": "parents_ids", "values": ["<item_id>"]}` returns an item's children
    (e.g. the photo attached to a post), "the same connection the platform itself uses"; do not use `has_children`.
  - `item-field-reference.md`: `parents_ids` is filterable on all item types.
  - `searching-items.md`: `POST /api/v1/items/context` returns i360's seven relation buckets: duplicates,
    attachments, triggering_items, alert_items, similar_items, parent_items, repost_items.
- **In the contract:** `parent_ids` on every hit and on items/get (its description carries the children recipe);
  `ItemRelations` (the 7 buckets, each `{item_id, item_type}`) on items/context; `thread` (before/after, one item per call).
- **The name "Related items"** appears only in the team's letter UI-AND-GEO-TEAM-REPLY-4 (contract v36): parents_ids
  is what the old viewer's "Related items" tab is built on.
- **On our data:** no children for any layer (first 100 records of each); only the 2 CCTV videos have a parent, and
  it cannot be read (`found: false`); items/context buckets empty on 99 records; threads empty.
- **Missing:**
  - a write operation (parent_ids is set at ingestion only);
  - a reason or relation type per link beyond the bucket name;
  - a way to tell "unknown" from "none" in items/context.
- **Workable today:** link both records to a shared entity (e.g. an IP entity: type IP exists, 0 instances, creatable
  with `POST /api/v1/entities/IP`) through items/related-objects; the app would then show the two records as linked
  through that entity. On our data this is 2 shared IPs (203.0.113.107, 203.0.113.80): 20 ADINT and 2 IPDR records.
  Not done; it writes to the shared estate.

## Search and get by id: different fields for the same item

Example (LAMBDA, ADINT 72715428-c56e-11f1-b31b-0be3e65f42aa):

```
POST /api/v1/items/get     {"item_ids":["72715428-…"],"include":["user_agents_data"]}
  -> "language": null, "user_agents_data": [{"language_code": "ar", "language": null, …}]
POST /api/v1/items/search  {"include_ids":["72715428-…"],"page_size":1}
  -> "language": "ar"
```

ADINT fields in the two calls (all 120 records; number of records with the field filled):

| Field | search | items/get |
|---|---|---|
| item_id, item_type, sub_type, event_time, end_time, source_application, secrecy_holder_status, media | 120 | 120 (same values) |
| location.point, location.accuracy ("gps") | 84 | 84 (same values) |
| fe_correlation_ids, ip, user_agents_data | 0 | 120 |
| additional_info (accuracy_m) | 0 | 84 |
| flags, tags | 0 | 120 |
| **language** | **52** | **0** |

Where the app reads by id: `server.py` `App.item_layers` (chat show_items / listing, open_item, `POST /api/chat/items`,
the report's records outside the layers) and `hl/state.py` `attached_items` (investigation records; search then items/get,
items/get winning). The layers (`hl/items.py` `ItemReader.items`) read search then items/get and keep the search value
where items/get has none.

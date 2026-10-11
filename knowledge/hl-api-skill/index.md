# What this deployment can tell you

Every topic below is served by `GET /api/v1/meta/docs/{topic}` on the deployment you are building
against. **Do not read them all** — 42 topics is far more than your context is worth
spending. Ask `GET /api/v1/meta/docs?q=<your question>` and it ranks the sections that answer it.

## Guides — written for a reader, start here

Each one answers a question rather than covering a subject. Pick the one whose line matches what you
are trying to do.

* `access-control` — Type-level permission and instance-level visibility are independent, and both must pass.
* `asking-a-question` — POST /api/v1/ask reads an ordinary question, searches both halves of the platform, and hands back the criteria it built so you can change one thing without asking again.
* `audio-enhancement` — Run the platform's noise or echo reduction on up to 30 seconds of a call, get the result in the same call, and play the cleaned audio; how ui-360 does it, and what was measured.
* `authentication` — How to get a token, how it is forwarded, and why we never store a credential.
* `bookmarks-on-the-timeline` — Add, read, change and remove an analyst's bookmark on a call, video or message, and how to tell your own from the pipeline's.
* `checking-permissions` — Ask the platform whether the signed-in user holds a permission, so a screen can hide a button instead of failing on click.
* `counting-and-trends` — How many items match, broken down by field, over time, clustered on a map, or by the entities they name — one operation, four dimensions.
* `entity-instances` — The lifecycle of an actual record once its type exists: create it, read it, patch it, search it, link it, remove it.
* `errors` — Every failure has the same shape and carries a hint telling you the next action.
* `estates` — Deployments run different platform generations and hold different data. Ask, do not assume.
* `filtering-items-by-field` — How `filters` works, the seven nested roots, finding items linked to an entity, and why an empty result is not proof of absence.
* `getting-started` — Get a token, search for items with their text included, show a picture. Says plainly why you do NOT fetch each hit.
* `inspecting-what-exists` — Before you create anything, find out what this deployment already has: which types, what fields they carry, which link types, and who you are.
* `item-audit` — Record that a user played a recording, the way ui-360's player does, and download an item's history report as a PDF; what is stored, where it shows, and what was measured.
* `item-field-reference` — The complete field list behind `filters`, with each field's type, sub-fields and which deployment generation has it.
* `link-analysis-graph` — Open an entity's network one to three hops out, find the links among a set of entities, and find the paths between two; what an empty answer means, and when one is cut.
* `llm-access` — Run a chat completion on whatever model this deployment serves, with streaming, and see what we do not do for you.
* `media-and-files` — Two supported patterns for a browser, what each file entry means, and the traps.
* `modelling-entity-types` — Create a type with sections and typed fields, link types between them, and provision a whole model with one publish.
* `reuse-or-create` — A type is not free — deciding when to read someone else's type, when to own your own, and why a near-duplicate is the worst answer.
* `safe-concurrent-writes` — How to change a record without losing somebody else's change, and how several writers share one record safely.
* `searching-items` — Text, semantic, visual, time, location, filters, scope, paging and sort compose in a single request, and `include` with "text" brings each hit's body back with it.
* `searching-with-a-picture` — Give the search an image instead of words, from the platform or from a laptop, and ask either what looks like it or where it was taken.
* `source-application-icons` — Fetch the image for an item's source_application, what a 200 does and does not prove, and the three errors.
* `tags-and-notes` — Flags, read/unread, priority and hashtags are one operation; analyst notes are another.
* `the-skill` — One download that teaches a coding agent to build on i360. What it contains, why it holds almost nothing, and how it stays true.
* `transcript-lines` — Add a line to a call's transcript, correct the text of a line a person wrote, overwrite a machine line on request, or remove one, and what the platform does that you would not expect.
* `using-this-api-as-mcp-tools` — The tool list says WHICH tool to call and nothing more. Ask describe_operations for the field meanings, traps and examples once you have picked one.
* `watching-for-changes` — GET /api/v1/records/stream keeps an open connection and sends you a short event each time one of the records you named changes, so a screen does not have to poll.
* `when-a-new-type-does-not-work` — A publish says SUCCEEDED and record writes still 404. Four checks, in order, that tell you whether the estate's model compiles, whether your type reached the entity service, and whether the fault is even yours.

## Reference — generated from the contract, one page per area

Every operation, every field, every value shape, straight from the published contract. These are for
looking something up once you know what you are calling, not for reading. If you need to know exactly
what a request takes, this is where it is written down.

* `reference-auth` — Token exchange and identity.
* `reference-dictionaries` — Closed value sets behind dropdown fields.
* `reference-entity-types` — Creating, editing and deleting types.
* `reference-graph` — An entity's network, and the paths between two entities.
* `reference-instances` — Creating, reading, patching and linking instances.
* `reference-item-files` — Listing an item's files and fetching the bytes.
* `reference-items` — Every operation over items and their content.
* `reference-link-types` — Declaring relationships between types.
* `reference-llm` — Brokered access to the estate's model backend.
* `reference-meta` — Estate profile, field types, facet groups, documentation.
* `reference-recovery` — Guard-railed repair operations.
* `reference-search` — What this deployment can actually do.

## The three calls

```
GET /api/v1/meta/docs                  the list above, live
GET /api/v1/meta/docs?q=<question>     the sections that answer it, ranked
GET /api/v1/meta/docs/<topic>          one topic in full
```

All three need your token. The deployment's copy is always the current one — prefer it over anything
baked into this skill.

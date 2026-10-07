# AI-Intelligence on i360: implementation plan (i360-only branch)

Oct 7, 2026 (revision 3) · base `main` @ `c47774f` · HL API contract 252

Companion to `claude/HL-API-CAPABILITY-MAPPING.md`. Paths are relative to `llm_investigation_orchestrator_serbia_poc/`.

## Status (Oct 7, 2026): implemented on `feature/i360-only`

Six commits on top of `main` @ `c47774f`. **Not pushed yet:** this session has no write access to the GitHub repo; the branch was handed over as a git bundle.

| Package | State |
| --- | --- |
| A. Cut down | Done. `oracle.key` removed from the tree; **the credential still has to be rotated**. |
| B. Runtime | Done. Dockerfile (tests in the build, non-root runtime), `/healthz`, env config, LF. Image build not run here: the sandbox cannot pull `python:3.12-slim`; the runtime file set was checked as a non-root user. |
| C. Client and sign-in | Done. Cookie `__Host-aii_session` (HttpOnly, Secure, SameSite=Strict); same-origin JSON required on writes. |
| D. Fake HL API | Done. `devtools/fake_hlapi.py` + `devtools/fixtures/syria.json.gz` (Syria, 726 items). |
| E. Data | Done against the fake. **Waiting on the ingestion field list** to fill `mapping/default.json` and `items_query`. |
| F. Saved work | Code done and tested on the fake. **Waiting on a building login** to run `tools/provision_types.py --grant-profile <profile>` (dry run, then one publish). |
| G. Deploy | Not started. |

Changes from the plan below, made during implementation:

- **Reading is a per-user snapshot**, not paged queries: search + get for the whole scenario, mapped to rows, cached per token for 5 minutes. The existing layer and link logic runs unchanged and `app.js` still loads the user's rows once. Pushing filters to HL API is the next step if datasets grow.
- **`actors` is left out** on create, so HL API grants each record to its creator (the documented default). Investigations are personal for now.
- **No link types.** Each saved item carries its `investigation_key` as a field, so nothing needs a link that HL API cannot delete.
- `hl/auth.py` and `hl/entities.py` folded into `server.py` and `hl/items.py`.

Tests: 36 backend tests against the fake, 49 UI text tests and 12 UI behaviour tests pass. The full browser flow passed end to end in Playwright: sign-in, layers, viewers, derivation approval, memory, reload, locale and sign-out.

## 1. Scope

Branch `feature/i360-only`. **i360 through platform-hl-api is the only backend. No backward compatibility.**

- **In:** analyst UI (map, timeline, table, viewers, layers, links, telecom derivations), i360 sign-in, data read from i360 items and entities, saved work (investigations and their memory, telecom approvals) stored as i360 entity records.
- **Out, deleted from the branch** (it stays in `main` and Git history): AI (Hermes, personas, MCP server, OpenAI, chat, saved questions, recorded runs, workstreams, evidence fusion, targets, assessments), playback, local data files, file and SQLite state, scenario activation, VM deployment.
- **Consequence:** the branch cannot run without an HL API. Development and CI use a **fake HL API** (§6, package D); real checks run against the estate. Until the demo data is ingested, the app shows whatever items the estate already holds.

## 2. Delete list

| Remove | Why |
| --- | --- |
| `data/`, `assets/demo/`, `assets/audio/`, `artifacts/`, `scenario_manifests/`, `demo_profiles/` data parts | data comes from i360 |
| `recorded_runs*/`, `saved_questions/`, `test_runs/`, root videos and `*.png` | AI demo and history |
| `mcp_server/` (all), `moshe_profile/`, `talia_profile/`, `openai_general.py`, `agent_routing.py`, `agent_result_pipeline.py`, `demo_admission.py` | AI |
| `scenario_playback.py`, `workstream_artifacts.py` | playback, workstreams |
| `evidence_catalog.py`, `ipdr_evidence.py` (package verification) | evidence layer dropped until AI returns |
| `demo_runtime.py`, `activate_demo.py`, `provision_demo.py`, `run_server.py`, `deployment/`, `build_*`, `import_*`, `replace_*`, `update_*`, `generate_english_projection.py` | VM runtime and data build scripts |
| `server.py.before-*`, `../llm_investigation_orchestrator_poc/`, `../*_english_wip_*`, `../oracle.key` (after rotation) | stale copies, secret |
| Tests for everything above (roughly 35–40 of 70 files; data-shape tests are rewritten against the fake) | no subject left |

In `server.py`, remove `HermesClient` (3338–4742), the AI, playback, workstream, saved-question, recorded-run, live-step and queue routes, `demo_guard`, the performance log, and all file and SQLite readers and writers. Most of its 6,400 lines go; an estimate of what remains comes after the first cut.

In `app.js` (8,818 lines), remove the chat panel, agent mentions, workstream panel, playback controls, saved and recorded questions, the evidence layer UI, and the full-dataset download.

## 3. Target shape

```
browser  index.html · app.js · polygon_draw.js · MapLibre (external tiles unchanged)
   │ same-origin /api/*, HttpOnly session cookie
   ▼
app pod (stateless, N replicas, Python 3.12 stdlib)
   server.py        routing, static files, /healthz, sign-in guard
   hl/client.py     HlClient(token): one error type, 401/501 handling, GET-only retries
   hl/auth.py       login → POST /auth/token, cookie, whoami
   hl/items.py      layers, rows, records, counts, files, built on items search/get/aggregate/context
   hl/mapping.py    i360 item / entity  ⇄  the row shape app.js already draws
   hl/entities.py   reference entities and locations from i360
   hl/state.py      investigations, memory items, approvals as i360 entity records
   link_graph.py    kept; fed from hl/items.py
   │ Authorization: Bearer <signed-in user's token>
   ▼
platform-hl-api (http://platform-hl-api:8080)
```

### `hl/mapping.py` is the key module

`app.js` draws rows shaped like today's wide CSV, with `source_type` and source-specific columns. Instead of rewriting every view, a mapping table per item type converts an HL item (`item_id`, `item_type`, `event_time`, `location`, `text`, `media`, fields) into that row shape. The table is configuration (`mapping/*.json`). It is filled from the ingestion team's field list, and until then from items already on the estate. Views change only where a column has no i360 equivalent.

## 4. Route plan

| Route | Becomes |
| --- | --- |
| `POST /api/login`, `POST /api/logout`, `GET /api/me` | new: token exchange, cookie, `whoami` |
| `GET /api/status` | app build and version, user, `GET /meta/estate` summary, scenario profile (camera, labels) |
| `GET /api/layers` | layer catalog from `/items/aggregate` grouped by item type (one layer per type with counts) plus `entities` and `locations` |
| `GET /api/layers/{id}/rows?filters&page` | `/items/search` (filters, `include:["text"]`, paging) → mapping; **paged** |
| `GET /api/records/{id}` *(new)* | `/items/get` with parties/detections, for the viewer |
| `GET /api/records/{id}/files` *(new)* | item files with signed URLs (absolute, prefixed with `HL_API_PUBLIC_ORIGIN`) |
| `GET /api/links`, `GET /api/derivations` | `link_graph.py` over records fetched by identifier search; `/items/context` and `/graph/neighbors` where they give the same answer |
| `GET/POST /api/investigations` | `AII_INVESTIGATION` search and create |
| `GET/PUT /api/investigation-memory`, `POST .../layer`, `.../artifact`, `/api/collection-request`, `.../delete` | `AII_MEMORY_ITEM` create, search by investigation, soft-delete |
| `GET .../layers/{id}/presentation` | re-run the saved filters through `/items/search` |
| `POST /api/derivations/review` | `AII_TELECOM_APPROVAL` create/patch |
| `/api/dataset/*`, every AI, playback, workstream, saved/recorded question, queue and performance route | **deleted** |

## 5. Entity model (dry run first)

All records are created with `actors` (the signed-in user) and an `owner` field. The type prefix is `AII_`.

| Type | Fields | Links |
| --- | --- | --- |
| `AII_INVESTIGATION` | name, owner, scenario, locale, created/updated | — |
| `AII_MEMORY_ITEM` | kind (`layer`, `object`, `area`, `collection_request`, `entity_enrichment`), label, comment, payload (JSON: filters, view, object ref, polygon ring), location | → investigation |
| `AII_TELECOM_APPROVAL` | derivation_id, entity_id, msisdn, imsi, review_state, supporting_record_ids | — |

Persons, organizations and locations are **read** from whatever types ingestion creates (`reuse-or-create`). We do not create our own copies.

## 6. Work packages

### A. Cut the branch down (start now)
- [ ] Rotate the `oracle.key` credential
- [ ] Branch `feature/i360-only` from `main`; apply the §2 delete list in one commit, so it reviews as "removals only"
- [ ] Strip the deleted features from `server.py` and `app.js`; the app starts and serves static UI with empty data
- [ ] `.gitattributes` LF; `docs/` rewritten for the new architecture (the repo's rule)

### B. Runtime (start now)
- [ ] Bind `0.0.0.0:$PORT`; `/healthz` without HL API calls
- [ ] Config from env vars only (§7); fail fast at start if `HL_API_URL` is missing
- [ ] Dockerfile: python:3.12-slim, non-root, tests in the build, clean runtime stage; logs to stdout

### C. Client and sign-in (start now)
- [ ] `hl/client.py`:
  - errors carry `code`/`hint`/`status`
  - 401 → re-login, 501 → "not on this estate"
  - no write retries
- [ ] `hl/auth.py`:
  - form-encoded `POST /auth/token`
  - cookie that is HttpOnly, Secure and SameSite=Strict, holds only the token, and expires at `expires_in`
- [ ] Guard on all `/api/*`; login screen and 401 redirect in `app.js`
- [ ] The role comes from the user, never from the client (`COLLECTION_REQUEST_TYPES_BY_ROLE`)

### D. Fake HL API for development and CI (start now)
- [ ] `devtools/fake_hlapi.py`: a stdlib server implementing only the operations we call (token, whoami, items search/get/aggregate/context/files, entities CRUD/search/links, entity-types read), with HL API's error envelope
- [ ] Seed it from a small fixture built once from today's demo data, shaped as i360 items and entities
- [ ] Run tests against the fake; recorded real responses keep it honest once a login exists

### E. Data from items (start now against the fake; finish with ingestion)
- [ ] `hl/items.py` and `hl/mapping.py` per §3–4; `include:["text"]` on search, `/items/get` only for an opened record, `text_available_via_get` handled
- [ ] `hl/entities.py` for entities and locations
- [ ] `link_graph.py` and the subscriber-identity derivation fed from `hl/items.py`
- [ ] `app.js`: rows paged from `/api/layers/{id}/rows`; viewer uses `/api/records/{id}`; media from signed URLs
- [ ] Scenario: profile (camera, labels) + item filter from config
- [ ] With the ingestion field list: fill `mapping/*.json`, check every view

### F. Saved work as entities (needs the building login)
- [ ] With a token, read guides: `modelling-entity-types`, `entity-instances`, `access-control`, `safe-concurrent-writes`, `authentication`
- [ ] `GET /entity-types` reuse check; `MODEL-DECISIONS.md`; dry run; one batch publish
- [ ] `hl/state.py`: send `actors`, use the returned `entity_id`, read back after writes, safe concurrent writes
- [ ] Verify as a normal user: search and fetch by id

### G. Deploy (per `DEPLOY-GITHUB-CODE-TO-LAMBDA.md`)
- [ ] `git archive` into `apps/<name>/` with the SHA; bake target; `CLAUDE.md` bullet; MR to `develop` + CR; Jenkins
- [ ] Skipper values file, `APP_RELEASES`; LAMBDA owner's go-ahead; skipper job
- [ ] Verify:
  - the image digest matches
  - a normal user signs in through the public host
  - layers page, viewers and media open
  - a saved memory item survives a reload and a different replica

## 7. Configuration

| Var | Purpose |
| --- | --- |
| `PORT` | listen port |
| `HL_API_URL` | `http://platform-hl-api:8080` in cluster; the fake's address in dev |
| `HL_API_PUBLIC_ORIGIN` | origin for signed media URLs in the browser |
| `APP_SCENARIO` | `kosovo` / `syria` profile and item filter |
| `APP_TYPE_PREFIX` | default `AII_` |
| `APP_PAGE_SIZE` | rows per page |

No secrets: the app holds no password, key or service account.

## 8. Order

```
A ─┬─ B ──────────────────────────────┐
   └─ C ─┬─ D ─ E (fake) ─ E (estate) ┼─ G
         └───────────── F (login) ────┘
```

A–E can run fully against the fake. F and the end of E need i360.

## 9. Risks

- **`app.js` is large.** Removing features and moving to paged rows are the two biggest edits. Some views assume the full dataset is in memory (local filtering, counts, the timeline extent) and must use `/items/aggregate` instead.
- **Mapping gaps.** CSV columns with no i360 field lose their UI until mapped.
- **Fake drift.** The fake can diverge from the real API; recorded responses and an early real run limit this.
- **Empty until ingested.** Demos need the ingestion first.

## 10. Needed from Zvika

1. Rotate `oracle.key`.
2. An i360 building login that is **not** an admin account, and its grant profile. Zvika signs in himself.
3. App name.
4. Ingestion field list (fills `mapping/*.json`).

# AI-Intelligence → HL API: capability mapping

Oct 7, 2026 · read from the live estate (contract **252**) through the in-app browser on aws-zvika-win

## What was read

- Kit pages: `/map/kit`, quickstart, demo, architecture, runtime, devtime, deployment, use-cases
- Capability map `GET /map` (JSON: 13 capabilities with what is *not served*, 30 guide titles)
- Agent skill `/map/skill.zip`: `SKILL.md`, `getting-started`, `reuse-or-create`, `index`, `capabilities.json`
- Full contract `/openapi.json` (~650 KB, 69 operations)
- **Not read yet:** the 30 guides in full (they need a token: `GET /api/v1/meta/docs/{topic}`), and `kit.zip` (~3 MB; too large for the browser bridge)

## Basics of the API

- Base: `/api/v1`. In-cluster `http://platform-hl-api:8080`; outside the cluster, the public HTTPS host. The kit's deployment page confirms that is the only value that changes between "inside i360" and "on its own".
- Token: `POST /api/v1/auth/token`, **form-encoded** password grant, send the raw password. Returns `access_token` and `expires_in`. On 401, get a new token. Then `Authorization: Bearer <token>` on everything. `GET /api/v1/auth/whoami` says who the token belongs to.
- `client_credentials` also exists, but our deploy guide forbids a shared service account. Use the user's own token.
- One error envelope with a `hint`. A `501` means this estate does not have the feature (don't retry). Never blind-retry a write.
- Discovery first: `GET /map`, `GET /api/v1/items/search/capabilities`, `GET /api/v1/meta/estate`.

## Capability by capability

| AI-Intelligence needs | HL API | Verdict | Our work | Ask HL API team / Zvika |
| --- | --- | --- | --- | --- |
| **Sign-in** (replace role picker and shared Hermes key) | `POST /auth/token` (password grant) against the i360 auth service; `whoami`; `POST /auth/permissions/check` | **Covered** | Login form → backend exchanges for token → HttpOnly cookie; on 401 send the user back to sign in (no refresh token documented; we must not keep the password) | Is there an SSO/OIDC redirect for apps inside the i360 shell, or is the password form the intended way? |
| **User state**: investigations, layers, objects, areas, comments, workstreams, leads, playback runs, collection requests, approved telecom identities, fused evidence | Entity types + link types (`/entity-types/batch`, `/link-types/batch`, one publish), instances CRUD, per-type search with exact field predicates, `include_ids` multi-get, safe concurrent writes | **Covered**: SQLite and in-memory state can go | Design the model (~8–12 types), dry run, one batch publish, `MODEL-DECISIONS.md`; send `actors` on every create; use the returned `entity_id` | Which grant profile our app users are in; a building login (not admin) |
| — removing a link | none | **Gap** (on request) | Model "unlink" as a status field, or avoid links that must be removed | Request delete-link if needed |
| — permissions per profile | only as a side effect of creating a type | **Partial** | Pick the right `grant_profile` at create time | |
| **Data**: Kosovo / Syria synthetic datasets | No ingestion (ETL state *none*); records have **no batch write** | **Biggest decision** | Option A: load synthetic data as entity records, one call per record (OK for hundreds–low thousands). Option B: switch the app to the estate's real ingested **items** (`/items/search`, `/items/get`, `/items/context`, graph) | **Zvika:** demo on synthetic data, or real estate data? |
| **Search / semantic index** | `POST /items/search` (text + semantic + picture + place + time + facets), `POST /ask` (plain words → criteria), `similar-images`, entity text/field search | **Covered for items**; entity search is text/prefix/exact only | If data stays synthetic as entities, keep our own index in the image (or drop semantic); if we move to items, **drop the index** | Is semantic search over *entity* records planned? |
| **Aggregation / dashboards** | `POST /items/aggregate` (by field, over time, geo clusters) | **Covered for items** (partial) | For our own entity types, count in the backend | |
| **AI and agents** (replace Hermes + direct OpenAI call) | `GET /llm/models`, `POST /llm/chat`: OpenAI chat format, streaming, `tools` (calls returned, never run), `response_format` JSON schema, embedded images | **Covered** | Small in-app tool loop over `/llm/chat`; tools = our HL API calls with the user's token; drop the OpenAI key | Which model(s) are served; the night-time shutdown; no per-caller quota exists yet |
| **Annotations / comments on intel** | `/items/tags`, `/items/annotations`, `/items/indications` (timeline bookmarks), transcript lines | **Covered for items** | Comments on our own records go in a field or a Comment type | |
| **Media / evidence files** | Items' files + signed URLs; entity attachments readable | **Read only** | Use signed URLs (prefix the API origin) | **No upload path exists**: any feature where users add files must go |
| **Live updates** (playback progress, shared views) | `GET /records/stream` SSE (watches named records; no replay, no discovery) | **Partial** | One stream per app; keep polling for new records | Note: the kit's use-cases page says nothing notifies the app; the API has this stream |
| **Map tiles** | none | **Not needed** (decided Oct 7) | Keep the existing external tile services (ArcGIS, CARTO); tiles are fetched by the user's browser, not the pod | Users' browsers must reach those hosts |
| **Health** | the API's own probes are placeholders | n/a | Our `/healthz` must not depend on HL API being up | |

## What this changes in the plan

1. **Hermes, dashboard, MCP servers and the OpenAI call can all go.** HL API covers sign-in, state and LLM with tools.
2. **Evidence SQLite and every local state file become entity types.** The app becomes stateless and can run several replicas. A persistent volume is not needed.
3. **Data source decided (Oct 7):** the demo data will be ingested into i360 as items. The app reads it through items search/get/context/aggregate, and the semantic index is dropped.
4. **Features that cannot survive:** user file uploads (none exist), and webhooks/replay of missed changes.

## Decisions (Oct 7, 2026)

- Demo data (Kosovo/Syria) will be ingested into i360 by the platform's own pipelines in the near future. The app reads **items**, not its own copies.
- Implementation runs in parallel with ingestion: every data read goes behind one interface with two backends, `local` (today's files, for development and tests) and `hlapi`, switched by an env var.
- Maps keep using the existing external tile services.

## Implementation plan

**Phase 0: inputs (Zvika)**
- [ ] i360 login for building apps (not admin) and its grant profile
- [ ] From the ingestion team: which item types and fields each demo dataset lands as (the field mapping)
- [ ] Which LLM models the estate serves (`GET /llm/models`), and the night shutdown hours
- [ ] Rotate the `oracle.key` credential
- [ ] Name for the app (`apps/<name>`, image, host)

**Phase 1: import and cluster-ready (no HL API needed)**
- [ ] `git archive` the package into `apps/<name>/` in `elbitbox/micro-apps`, with the agreed exclusions; drop Hermes, dashboard, MCP servers, remote deploy scripts
- [ ] `requirements.txt`, Dockerfile (tests before stripping dev deps), non-root, bind `0.0.0.0:$PORT`, `/healthz`, `.gitattributes` LF, config from env vars
- [ ] Triage the test failures (stale / real bug / missing data)

**Phase 2: seams**
- [ ] `DataSource` interface over every dataset read; `local` implementation wraps today's code
- [ ] `StateStore` interface over every state write (investigations, workstreams, playback runs, evidence DB, …); `local` implementation wraps today's code
- [ ] `HlApiClient`: token forwarding, error envelope and `hint`, 401 → sign in again, no blind write retries

**Phase 3: sign-in**
- [ ] Login screen → `POST /auth/token` → HttpOnly cookie; `whoami` for the user's name; remove the role picker and shared key

**Phase 4: state into i360 entities**
- [ ] Inventory every state item → entity/link model + `MODEL-DECISIONS.md`
- [ ] Check reuse first (`GET /entity-types`), dry run, one batch publish (needs the building login)
- [ ] `hlapi` StateStore; SQLite removed; verify as a normal user (search **and** fetch by id)

**Phase 5: AI**
- [ ] Replace the Hermes/OpenAI path with a tool loop over `POST /llm/chat`; tools are HL API calls with the user's token

**Phase 6: data from items (once ingested)**
- [ ] `hlapi` DataSource over `/items/search`, `/items/get`, `/items/context`, `/items/aggregate`, graph, signed media URLs; `/ask` for free-text questions
- [ ] Remove the semantic index and `INTELLIGENCE_POC_SEMANTIC_INDEX`

**Phase 7: deploy** (per `DEPLOY-GITHUB-CODE-TO-LAMBDA.md`)
- [ ] Bake target, `CLAUDE.md` bullet, MR to `develop` + CR, Jenkins build; skipper values file + `APP_RELEASES`; LAMBDA owner's go-ahead; verify digest and the public host

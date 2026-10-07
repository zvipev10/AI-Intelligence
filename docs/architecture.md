# Architecture

This branch (`feature/i360-only`) runs the analyst UI on i360. **i360, reached through
platform-hl-api, is the only backend.** There is no local data, no local state and no AI on
this branch; the earlier VM, Hermes and file-based architecture is in `main` and in Git history.

## Shape

```
browser: index.html · demo_bootstrap.js · app.js · polygon_draw.js · MapLibre
   │  same-origin /api/*, HttpOnly session cookie (holds only the i360 token)
   ▼
app (llm_investigation_orchestrator_serbia_poc/, Python 3.12 standard library, stateless)
   server.py          routing, static allowlist, /healthz, sign-in guard
   analysis.py        layers, entity/location summaries, links, saved-item validation (pure)
   hl/client.py       HL API calls: bearer token, one error type, no blind write retry
   hl/items.py        per-user snapshot of the scenario's items, entities and locations
   hl/mapping.py      i360 item / entity → the row shape app.js draws (mapping/*.json)
   hl/state.py        saved work as i360 entity records
   link_graph.py      field-equality link rules and the subscriber-identity derivation
   catalog_filters.py layer filters
   │  Authorization: Bearer <the signed-in user's token>
   ▼
platform-hl-api  (in cluster: http://platform-hl-api:8080)
```

## Identity

- `POST /api/login` sends the user's i360 username and password to `POST /api/v1/auth/token`
  (form-encoded password grant) and puts the returned token in an HttpOnly, SameSite=Strict,
  Secure cookie that expires with the token. The password is not stored anywhere.
- Every HL API call carries that token. What a user sees is what i360 lets that user see.
- A 401 from HL API clears the cookie and the UI shows the sign-in screen again.
- There is no service account and no shared key.

## Reading data

`hl/items.py` builds a **snapshot per user** (keyed by a hash of the token, kept for
`APP_SNAPSHOT_TTL` seconds, rebuilt on `POST /api/refresh`):

1. `POST /api/v1/items/search` for the scenario (`items_query` in `demo_profiles/<scenario>.json`),
   sorted by time, `include: ["text"]`, 100 per page. When a search matches more than the
   estate's `result_window`, the time range is split in halves until each part fits.
2. `POST /api/v1/items/get` per page of 100, for the parts search does not carry (tags, parties).
3. `POST /api/v1/entities/{type}/search` for the reference entities and locations named in the mapping.
4. The user's telecom-identity reviews from `hl/state.py`.

`hl/mapping.py` turns each item into a flat row with the columns `app.js` already uses
(`event_id`, `timestamp_utc`, `source_type`, `location_id`, `target_imei`, `ip_public` ...).
Where each column comes from is configuration in `mapping/default.json`, written as path
expressions (`tags[type=imei].value | parties[0].identifiers[type=imei].value`). The default
mapping matches the development fixture. **When the ingestion team publishes how the demo data
lands in i360, only the mapping file changes.**

`analysis.Dataset` then runs the existing logic on the rows: entity and location summaries,
the layer catalog, layer filters, field-backed links and the subscriber-identity derivation.

The snapshot is only a cache. It holds exactly what that user may see, and any replica can
rebuild it. It suits the demo datasets (hundreds to tens of thousands of records); for larger
estates the next step is pushing filters and counts down to `items/search` and `items/aggregate`.

## Saved work

Three entity types, prefix `APP_TYPE_PREFIX` (default `AII_`), one section `main`, created by
`tools/provision_types.py` with a dry run and one batch publish:

| Type | One record per | Key fields |
| --- | --- | --- |
| `AII_INVESTIGATION` | investigation | investigation_key, name, scenario, created/updated |
| `AII_MEMORY_ITEM` | saved item (layer, object, polygon, collection request) | investigation_key, item_key, group, kind, label, comment, payload (JSON) |
| `AII_TELECOM_APPROVAL` | reviewed derivation | derivation_id, entity_ref, scenario, review_state, msisdn, imsi, payload |

- HL API assigns its own `entity_id`; our keys are fields we search by.
- `actors` is left out on create, so HL API grants each record to the user who made it and it
  appears in that user's searches. Investigations are personal; sharing is a later step.
- Every saved item is its own record: two writers never overwrite each other, and deleting an
  item is a soft delete of its record (HL API has no delete-link operation).
- Creates are read back before success is reported. Writes are never retried automatically.

## Browser

- `demo_bootstrap.js` asks `/api/status`. Signed out, it shows the sign-in form and does not load
  `app.js`. Any later 401 brings the form back.
- `app.js` loads the user's rows from `/api/dataset/events` (CSV) and locations from
  `/api/dataset/locations`, and uses the layer, memory, investigation and derivation routes.
- Media load from HL API signed URLs (`/api/records/{id}/files`).
- Map tiles still come from the existing external services (CARTO, Esri), fetched by the
  browser. Users' browsers must reach them.

## Scenarios

`APP_SCENARIO` selects `demo_profiles/<scenario>.json`: camera, labels, the list of known
sources, and the `items_query` that selects the scenario's items. One deployment serves one
scenario; run a second deployment for the other.

## What this branch does not have

AI agents and chat, saved and recorded questions, workstreams, playback, the evidence catalog,
target bank and assessments. User file upload is not possible (HL API has no upload), and the
app is not told about changes as they happen (it rebuilds the snapshot on refresh or expiry).

# Corrective Checkpoint 008 — Cross-source entity symbology

## Scope decision
At the user's direction, explicit organization mappings now apply to raw event
records in every source layer, not only to organization aggregates and UAV
observations. This expands the original MVP boundary that kept public-source
reports as generic markers.

## Presentation precedence
1. A supported UAV observation uses its object-class symbol and `observed`
   claim state.
2. Any other location-bearing event whose `entity_id` exists in the curated
   organization registry uses that organization's affiliation and icon with a
   `reported` claim state.
3. Events without an explicit organization mapping remain regular markers.

Every raw-event symbol continues to open the raw record rather than the
organization viewer, preserving evidence traceability. Release assets are
`app.js?v=177`, `styles.css?v=147`, and `deployment/SHA256SUMS-v181.txt`.

## Publication and production acceptance
- Implementation commit on remote `main`: `1c755a5`.
- Production target: `/opt/serbia-poc-ui` on `151.145.93.180`.
- Rollback backup: `/home/ubuntu/deploy-backups/cross-source-symbology-1c755a5`.
- Deployed `index.html` and `app.js` hashes match `SHA256SUMS-v181.txt`.
- `serbia-poc-ui` is active and serves `app.js?v=177`.
- Exact browser acceptance: filtering International news channel to
  `REC-V2-000104` produces one row and a red hostile NATO `Reported` marker
  inside the map. Show on map preserves the symbol, opens one popup, selects
  the row action, and retains raw-record viewer ID `REC-V2-000104`.

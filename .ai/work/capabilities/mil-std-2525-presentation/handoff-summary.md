# Handoff Summary

## Outcome
MIL-STD-2525E Change 1 presentation is implemented, tested, and deployed to the production VM.

## Product behavior
- The 12 approved organization entities render at their top explicit presence locations as assessed or reported organization symbols.
- Supported UAV records render as armored vehicle, logistics truck, convoy, or helicopter observation symbols with unknown affiliation.
- Symbols expose claim state, confidence, time, evidence count/IDs, and open the existing single-object viewer.
- Organization details list presence evidence by location. Mention-only entity/location associations do not create presence symbols.
- The map legend was removed in corrective checkpoint 002 at the user's direction; symbol semantics remain available through accessible marker labels and evidence details.

## Data results
- Full dataset: 12 selected organizations, 4,293 connected evidence records.
- Current top-location profile: 139 organization-presence symbols supported by 2,542 explicit presence records; five mention-only top-location entries are excluded.
- Production smoke at deployment time: 12 organizations and 4,237 connected records visible under the active playback timeframe.

## Validation
- `node --check app.js`
- Full 146-test application suite passed.
- Focused 29-test regression set passed.
- Runtime entity-layer probe passed.
- Public HTTP 200; v172 script, v143 stylesheet, legend, registry, observation renderer, evidence viewer, and uncertainty halo verified.
- `serbia-poc-ui` active after restart.

## Deployment
- Target: `/opt/serbia-poc-ui` on `151.145.93.180`.
- Rollback: `/home/ubuntu/deploy-backups/mil-std-2525-20260910T230410Z`.
- Manifest: `deployment/SHA256SUMS-v174.txt`.

## Limitations and follow-up
This demo uses a curated HTML/CSS presentation profile. It does not claim external conformance certification, persisted object correlation, or a confirmed asset inventory. A future operational version should validate formal SIDCs and renderer output against the standard and introduce persisted assessment identity/deduplication.

## Corrective checkpoint 002
The unnecessary collapsible map legend and its dedicated styles were removed. The change does not alter MIL-STD symbol selection, rendering, confidence, evidence, or viewer behavior. The stylesheet reference advances to `styles.css?v=144`.

The correction is merged into `main` at `1122051` and deployed to production. The UI service is healthy, the public site serves the v144 stylesheet without legend markup or CSS, and the rollback backup is `/home/ubuntu/deploy-backups/remove-map-legend-1122051`.

## Corrective checkpoint 003
At the user's direction, the four KFOR entities and the NATO reserve entity are classified as hostile rather than neutral for map presentation. Hostile organizations use a red diamond frame. Serbian Armed Forces remain friendly; UAV observations remain affiliation-unknown.


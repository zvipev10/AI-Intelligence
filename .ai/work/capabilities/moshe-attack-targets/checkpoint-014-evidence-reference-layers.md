# Checkpoint 014 — Structured evidence-reference layers

## Outcome

- `מזהי ראיות` is now a structured list of agent-selected evidence layers.
- Each layer name opens only that evidence on its declared map or timeline view.
- Each evidence layer has independent show/hide state and also appears in the standard layer list.
- Requested results remain controlled only by `הצג תוצאות`.
- Neither requested results nor evidence layers are presented automatically when the answer arrives.

## Shared contract

- `present_requested_results` now accepts two independent arrays:
  - `layers` for data directly requested by the user;
  - `evidence_layers` for canonical records that materially support the final conclusion.
- The MCP boundary validates canonical IDs and view compatibility.
- Evidence references accept map or timeline only in this slice.
- The shared result pipeline returns `requested_result_layers` and `evidence_reference_layers` separately.
- Both General and Moshe use the same contract and frontend implementation.

## Presentation

- The UI derives displayed identifiers from validated layer rows.
- Up to 14 identifiers are displayed per layer, followed by an overflow count.
- The display limit does not remove any row from the map or timeline layer.
- A legacy free-text `מזהי ראיות:` block remains read-only for old saved answers.
- When structured references exist, the legacy block is suppressed to avoid duplication.

## Agent instructions

- General and Moshe are instructed to select evidence by relevance to the conclusion, not by tool call.
- Intermediate searches, rejected candidates, duplicate checks, and unrelated tool output are prohibited.
- New answers no longer generate a free-text `מזהי ראיות:` footer.
- Canonical IDs may remain in narrative prose when needed to explain a specific claim.

## Validation

- JavaScript syntax passes on Node 22.
- 47 shared UI, routing, profile, result-pipeline, and target-catalog API tests pass.
- 39 MCP, fusion, target-bank, migration, semantic-limit, catalog, and boundary tests pass.
- Total automated regression tests: 86.
- Production contract smoke returned separate requested and evidence layers with the declared timeline view.
- Live General-agent smoke selected one requested layer and one structured evidence layer.
- Live Moshe smoke returned:
  - `responding_agent=moshe`;
  - one requested layer;
  - one structured timeline evidence layer;
  - no legacy free-text evidence footer;
  - no target write.

## Deployment

- VM: `151.145.93.180`
- Rollback backup: `/home/ubuntu/deploy-backups/evidence-reference-layers-20260724T140000Z`
- Asset versions: `styles.css?v=89`, `app.js?v=110`
- `hermes-gateway`, `hermes-moshe-gateway`, and `serbia-poc-ui` are active with zero restarts after deployment.
- Both gateway health endpoints return `status=ok`.
- No SQLite schema or target-data migration was performed.

## Browser verification

The in-app browser reached the HTTPS endpoint but rejected the VM's untrusted certificate. UI interaction coverage is therefore provided by the deployed live-agent results, static interaction regression tests, served-asset verification, and user visual acceptance.

## Review state

Implementation, automated QA, deployment, contract verification, and live General/Moshe smoke verification are complete. Product visual acceptance is pending.


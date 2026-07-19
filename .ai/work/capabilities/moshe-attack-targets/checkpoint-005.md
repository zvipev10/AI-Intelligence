# Checkpoint Summary

## Checkpoint

005 - Slice 5 shared attack-target presentation

## Checkpoint status

Implemented and validated; pending UX and General-agent regression acceptance before deployment

## Completed

- Added `attack_targets` to the shared typed-layer contract.
- Derived presentation rows only from successful, audited target-tool results.
- Enriched canonical location/entity references for display without copying them into SQLite.
- Deduplicated refreshed targets by `target_id` while retaining full evidence returned by detail tools.
- Rendered candidate targets through the common map/table pipeline; no Moshe-specific apply or render entry point exists.
- Added target title/ID, object class, entity, canonical location, confidence, quantity/range, summary, independent-source count, evidence records, and fusion explanation.
- Added a non-color-only diamond map marker, canonical-area popup, and small offsets for multiple candidates at one canonical location.
- Kept narrative/clarification and no-candidate replies layer-free.
- Reused existing loading, attributed error, permission-failure, RTL, mobile-scroll, and activity-step behavior.

## Validation

- 20 shared-result, target-presentation, routing, and member-UI tests pass on the Linux VM.
- JavaScript syntax and Python compilation pass on the Linux VM.
- `git diff --check` passes.
- Static UX/accessibility review confirms visible table labels, keyboard-native evidence disclosure, accessible evidence/marker labels, RTL content, mobile horizontal table behavior, and marker shape independent of color.
- Browser rendering against this undeployed slice remains part of the pending UX checkpoint; production was not changed.

## General-agent regression boundary

- The existing `applyAgentResult` entry point remains the only final-result path.
- Existing event, location, entity, aggregation, map, timeline, table, and member contracts are unchanged.
- Unknown or malformed typed layers continue to be rejected.
- General responses without typed layers retain the legacy result behavior.

## Risks and notes

- A search summary can show target metadata and evidence counts, but full evidence rows require Moshe to use the existing detail/create/update tools.
- Dense groups of targets use small visual offsets around the canonical area; the popup and table continue to identify the canonical location rather than implying exact coordinates.
- Production visual verification and representative Moshe target creation remain required before Slice 5 acceptance.

## Recommendation

Review the Slice 5 table/map behavior and General-agent regression boundary. If approved, deploy Slice 5 and run one representative target-result smoke test before starting Slice 6.

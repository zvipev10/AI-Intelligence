# Checkpoint 001 — semantic model and viewer integration

## Status
Implementation complete; QA recommendation: continue to release after final checks.

## Delivered
- Versioned MIL-STD-2525E Change 1 mapping registry for 12 organization candidates and four UAV observation classes.
- Organization presences derived from explicit location-bearing activity language, grouped by entity and location.
- `ASSESSED`, `REPORTED`, and `OBSERVED` claim states with separate confidence and affiliation presentation.
- Location-level evidence counts, timestamps, and raw record IDs in the entity-layer API and organization viewer.
- Individual UAV observation symbols linked to the raw-record viewer without implying ownership from entity association.
- Bilingual accessible legend, marker names, popup evidence, and single-object viewer actions.
- Release manifest v174 and focused contract coverage.

## Verified data behavior
- 12 selected organizations and 4,293 connected records remain represented in entity metadata.
- The top-location display produces 139 organization-presence symbols from 2,542 explicit presence-supporting records in those displayed locations. Five top-location entries contain mention-only evidence and do not generate symbols.
- The full 4,293 records remain available as organization evidence; presence-symbol counts are deliberately smaller than raw-record counts.

## Review findings resolved
- Removed dashed affiliation frames for low confidence because they can imply anticipated/planned status. Reported confidence now uses a separate uncertainty halo and explicit label.
- Added explicit mention-only exclusion instead of converting every entity/location association into a presence.

## Checks
- JavaScript syntax check passed.
- 29 focused MIL-STD, viewer, asset, and welcome contracts passed.
- Full 146-test application suite passed after updating stale asset-version assertions.
- Entity API runtime probe passed for selected organization and evidence fields.

## Limitations
This is a demo presentation profile using curated HTML/CSS symbol primitives and versioned mappings. It does not claim external MIL-STD conformance certification or persisted cross-record real-world object deduplication.


# Capability Brief

## Capability
MIL-STD-2525 assessed-presence and observation presentation

## Status
Approved for implementation by the user on 2026-09-10, with product, development, UX, and QA decisions delegated for end-to-end delivery.

## Problem and goal
The map currently presents records as generic dots. Analysts need standard military symbology while retaining a clear distinction between catalog entities, assessed organization presences, raw reports, and UAV-observed objects.

## Approved behavior
- Use MIL-STD-2525E Change 1 as the versioned presentation target.
- Present 12 organization candidates from the 28-entity catalog.
- Derive organization map presences from location-bearing records, grouped by entity and location, and label them as assessed or reported rather than treating every report as a separate organization.
- Present structured UAV observations for armored vehicles, logistics trucks, vehicle convoys, and helicopters.
- Present any other location-bearing raw event with an explicitly mapped organization `entity_id` using that organization's affiliation and icon, labeled as a reported source record.
- Keep every symbol traceable to supporting raw record IDs and open the existing single-object details viewer from a symbol.
- Show confidence through an explicit assessment label, source/evidence count, time, and uncertainty/evaluation information; do not overload affiliation color or frame shape.
- Weak location-bearing claims may appear as `REPORTED`; mere mentions remain viewer evidence only.
- Never imply ownership of an observed object from its record's entity association.

## Verified data baseline
- 14,800 records: 11,000 public-source and 3,800 UAV.
- 28 entities; 12 initial organization candidates.
- The 12 organizations connect to 4,293 evidence records: 2,954 public and 1,339 UAV.
- 1,509 UAV records match the four initial observation classes across all entities; 508 connect to the selected 12 organizations.
- These counts are record candidates, not deduplicated real-world object inventories.

## MVP scope
Client-side assessed-presence and UAV-observation symbol descriptors derived from currently visible layers; a curated, versioned symbol mapping registry; accessible legend; symbol popups; links into the existing record/organization viewer; focused tests and deployment documentation.

## Non-goals
Claiming formal certification, reconstructing command hierarchy or ownership, entity resolution across observations, changing the source dataset, and converting reports for unmapped entities into symbols.

## Acceptance criteria
1. The map distinguishes organization presences from UAV observations with MIL-STD-compatible framed symbols and a visible legend/version label.
2. Organization presences are grouped by entity and location and expose evidence count, assessment state, time, and supporting records.
3. Supported UAV records render by observed object class and open the corresponding raw record.
4. Low-confidence location-bearing reports are marked `REPORTED`; mere mentions do not create presence symbols.
5. Affiliation, object type, confidence, and evidence provenance remain separate fields.
6. Existing grouped markers, grid behavior, filters, localization, target presentation, and viewers do not regress.
7. The implementation is tested, reviewed, merged, and deployed with rollback documentation.


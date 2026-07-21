# Chapter 1 - Target Bank Schema Contract

## Status

Approved by Product and Development on 2026-07-19. Ready for architecture/security, QA, and UX review; not yet an implementation plan.

## Persistence

- Use SQLite.
- Present the stored targets through the existing layer API/UI conventions.
- Store final-state MVP assessments only; no movement history or immutable revisions.

## Lifecycle and permissions

- The MVP implements only `candidate`.
- Moshe may create and update `candidate` targets.
- Human approval and rejection are deferred beyond the MVP.
- Freshness is not a lifecycle status in the MVP.

## Fusion and duplicate rules

- Moshe performs fusion using investigation/fusion tools and writes the resulting assessment.
- A saved candidate requires at least two independent source groups supporting the same object, entity, canonical location, and compatible time window.
- Reposts and duplicated reporting count as one source group.
- Multiple records from one UAV mission count as one source group.
- Low-confidence clusters are reported as insufficient corroboration and are not saved.
- Before creation, search for the same assessed object class, `entity_id`, and `location_id` with overlapping evidence.
- Update a matching candidate when evidence overlaps.
- Keep ambiguous identities separate and explain the ambiguity; never silently merge.

## Confidence and quantity

- Saved confidence is `medium` or `high`.
- Quantity fields are `count_min`, `count_max`, optional `count_estimate`, and `count_assessment`.
- `count_assessment` is `exact`, `approximate`, `range`, or `unresolved`.
- Quantity disagreement does not block creation when presence is sufficiently corroborated.

## References

- Store `location_id`; resolve location name, coordinates, type, and precision from the existing locations layer.
- Store `entity_id`; resolve canonical entity information from the existing entities layer.
- Store Moshe's final `object_class`; classification is part of the fusion assessment supported by tools.

## `targets` table

- `target_id`
- `title`
- `summary`
- `status`
- `object_class`
- `entity_id`
- `location_id`
- `confidence`
- `count_min`
- `count_max`
- `count_estimate`
- `count_assessment`
- `fusion_explanation`
- `mission_run_id`
- `created_by`
- `created_at`
- `updated_at`
- `reviewed_by`
- `reviewed_at`
- `review_note`

## `target_evidence` table

- `target_id`
- `record_id`
- `source_group`
- `source_type`
- `observed_at`
- `location_id`
- `reported_object`
- `reported_count`
- `relevant_text`
- `evidence_role`
- `added_at`

## Constraints

- Enforce the MVP candidate status, confidence, and count-assessment values.
- Enforce a unique `(target_id, record_id)` pair.
- Evidence belongs to exactly one target record and is deleted with an administratively deleted candidate.
- Do not store evaluator-only fields or identifiers.

## Deferred beyond MVP

- Movement history and stable identity across movement.
- Revisions and audit-event tables.
- Stale and revoked states.
- Nearby-location fusion.
- Concurrency conflict handling.
- Cross-mission target merge/split behavior.
- Approved/rejected lifecycle operations and human review UI.

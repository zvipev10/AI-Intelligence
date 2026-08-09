# Execution Plan — Main-based workstream simplification

## Gate

- Product behavior approved by the user.
- Main-based developer, UX, and QA reviews ready.
- Clean baseline: `origin/main` commit `01c21ff`.

## Slice 1

1. Update persistent Moshe instructions.
2. Update main's runtime Moshe instructions without changing playback authorization.
3. Update the creation MCP description.
4. Add alignment, boundary, and evaluation coverage.
5. Run focused tests and broad current-main regression suites.
6. Publish the implementation and checkpoint; do not deploy in this slice.

## Corrective slice 2 — durable supplied targets

1. Extend the creation handoff with resolved `target_ids`.
2. Persist validated, deduplicated `target_ids` on the workstream root.
3. Include root workstream targets in presentation output even before an assessment artifact exists.
4. Require Moshe to pass every resolved supplied or discovered existing target to the creation handoff.
5. Cover MCP validation, application persistence, presentation, compatibility, and instruction alignment.
6. Deploy narrowly with a new rollback point and verify Hebrew and English creation.

Decision: root-level target references represent creation inputs; assessment artifacts remain separately
governed analytical work and are not synthesized during creation.

## Corrective slice 3 — durable raw-record artifacts

1. Extend the creation handoff with verified `record_ids`.
2. Persist supplied raw records as indications in one initial `target_assessment_lead` artifact.
3. Use the inferred objective as the initial lead statement and the explicit creation request as the
   artifact authorization.
4. Preserve all root-level target references for mixed TGT/REC requests.
5. Cover record validation, artifact persistence, target-only compatibility, and mixed creation.
6. Deploy narrowly with a fresh rollback point and verify both locales.

Decision: raw records are evidence indications in an artifact, never workstream-root targets and never
authorization to create or update a target candidate.

## Rollback

Revert the focused implementation commit. No migration is involved; existing workstreams default to
an empty `target_ids` collection.

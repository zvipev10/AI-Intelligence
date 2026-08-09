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

## Corrective slice 4 — target-result visibility control

1. Update the UI presentation predicate so root-level `target_ids` make a workstream presentable.
2. Preserve the existing raw-record artifact predicate and shared show/hide toggle path.
3. Add regression coverage for target-only and raw-record-based button eligibility.
4. Run the UI/backend regression suite and deploy only the tested UI asset with a rollback backup.

Decision: target and raw-record workstreams use the same results visibility control and presentation
endpoint; no parallel target-specific toggle is introduced.

## Corrective slice 5 — target IDs in saved wording

1. Require target-backed creation wording to include every resolved `TGT-*` ID.
2. Enforce the requirement at persistence time for both title and objective, within existing limits.
3. Preserve wording that already includes the IDs without duplication.
4. Cover target-backed, already-labeled, and record-only creation.
5. Deploy the server and Moshe instruction changes narrowly for bilingual validation.

Decision: target IDs are part of the durable title and description contract, not optional model copy.

## Rollback

Revert the focused implementation commit. No migration is involved; existing workstreams default to
an empty `target_ids` collection.

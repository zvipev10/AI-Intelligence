# Developer Review

## Review status

Approved on 2026-07-19. The user explicitly reported: "Developer approved."

## Approved scope

- SQLite persistence with `targets` and `target_evidence`.
- Final-state V2.1 MVP without movement history, revisions, staleness, revocation, or concurrency workflows.
- Existing `location_id` and `entity_id` references rather than duplicated canonical data.
- Moshe owns fusion, classification, candidate summaries, and evidence snapshots.
- Moshe writes only `candidate`; humans alone set `approved` or `rejected`.
- At least two independent source groups are required for a saved candidate.
- Low-confidence assessments are reported but not stored.
- Approved and rejected targets are immutable to Moshe.

## Feasibility conclusion

The Chapter 1 schema contract is accepted as the MVP persistence baseline and is ready to inform tool-contract design. This approval does not authorize implementation before the remaining architecture/security, QA, and UX gates and an execution plan.

## Technical constraints carried forward

- Keep evaluator-only V2.1 truth outside runtime paths.
- Expose targets through existing layer conventions.
- Resolve canonical location/entity details at read time.
- Keep object classification in Moshe's fusion workflow rather than embedding it in SQLite.
- Preserve source independence and compact evidence snapshots.

## Required checks before coding

- Inspect existing server storage and layer API patterns.
- Review exact SQLite DDL, initialization, file location, backup, and deployment behavior.
- Define separate candidate-write and human-review tool permissions.
- Define the bounded Moshe mission contract and fusion-tool outputs.
- Complete QA and architecture/security reviews.

## Recommended next gate

Architecture/security review of permissions, database placement, evaluator-truth isolation, and production write boundaries.

## Chapter 2 approval

Approved on 2026-07-19 after Product added the shared General/Moshe backend and presentation architecture to scope.

Development accepts the following planning baseline:

- Explicit `@משה` routing and native Hermes session continuity.
- Shared Hermes invocation, result normalization, layer construction, and frontend result application.
- Generic agent attribution through the shared result envelope.
- `attack_targets` as a shared layer kind rather than a Moshe-specific renderer.
- Moshe-owned clarification, fusion, candidate writes, explanation, and presentation.
- No separate Moshe UI or duplicated backend modules.

Exact extraction boundaries, DDL, interfaces, and execution slices remain work for the formal execution plan after the remaining reviews.

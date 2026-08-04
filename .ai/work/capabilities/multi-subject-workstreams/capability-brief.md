# Capability Brief

## Capability name
Multi-subject and question-based workstreams

## Capability slug
`multi-subject-workstreams`

## Parent issue
Not created; draft body is stored under `issues/parent-capability.md`.

## Current status
Draft pending product, development, UX, and QA review. See `status.md`.

## User problem
A workstream can express a broad question or mention several objects only inside the free-text `objective`. The system cannot preserve those objects as structured scope, distinguish them in later assessments, or show which subject an indication addresses.

## Business goal
Allow an analyst to create one continuing workstream around a general investigative question, several concrete subjects, or both, and preserve that scope throughout follow-up analysis.

## Target users
Analysts who monitor a question, compare several entities/locations/records/targets, or progressively add subjects as evidence develops.

## Proposed behavior
- A workstream has an explicit scope mode: `question`, `subjects`, or `hybrid`.
- A general question is stored separately from the operational `objective`.
- A workstream may contain multiple structured subject references.
- Supported initial subject kinds are `event`, `entity`, `location`, `attack_target`, and `free_text`.
- Each subject has a stable `subject_id`, kind, label, optional canonical reference ID, optional analyst note, and lifecycle state.
- Evidence and assessment artifacts can reference zero, one, or several workstream subjects.
- Subjects can be added, updated, or retired without archiving the whole workstream.
- Existing schema-v1 workstreams continue to load as question/objective-only workstreams.

## Proposed data contract

```json
{
  "schema_version": 2,
  "scope": {
    "mode": "hybrid",
    "question": "What explains the coordinated activity?",
    "subjects": [
      {
        "subject_id": "subject-1",
        "kind": "entity",
        "reference_id": "ENT-V2-001",
        "label": "Subject A",
        "note": "Compare activity across the period",
        "status": "active"
      }
    ]
  }
}
```

Artifact proposals should replace the single-subject assumption with `subject_ids: []`. The existing `target_id` remains readable during migration and is mapped to an `attack_target` subject when possible.

## MVP scope
- Extend workstream persistence to schema version 2 with `scope`.
- Accept a general question, multiple subjects, or both during creation.
- Resolve canonical IDs where supplied and retain `free_text` for unresolved subjects.
- Show the question and subject list in the workstream summary.
- Allow adding and retiring subjects.
- Associate indications and assessment artifacts with multiple subject IDs.
- Preserve read compatibility for existing schema-v1 workstreams.

## Non-goals
- Automatic merging of two workstreams.
- Automatic subject discovery without analyst confirmation.
- Cross-investigation subjects.
- Deleting or rewriting historical workstream files in place.
- Changing investigation selection or investigation-memory behavior.

## Acceptance criteria
- An analyst can create a workstream with only a general question.
- An analyst can create a workstream containing at least two structured subjects.
- An analyst can create a hybrid workstream with both a question and subjects.
- The API validates subject kind, stable identity, duplicates, limits, and references.
- The UI clearly distinguishes the workstream objective, investigative question, and tracked subjects.
- A later indication can be associated with several subjects or with the workstream generally.
- Adding or retiring one subject does not affect the other subjects.
- Existing schema-v1 workstreams still list and open successfully.
- Workstream isolation by `investigation_id` remains unchanged.

## Edge cases
- Duplicate canonical references in one workstream.
- The same label referring to different object kinds.
- A canonical record is unavailable after creation.
- A question-only workstream later gains subjects.
- A subject is retired while historical artifacts still reference it.
- An artifact is relevant to the general question but no specific subject.
- Subject list grows beyond a practical UI or prompt size.

## Technical constraints
- Current storage is one JSON file per workstream.
- Current creation handoff accepts only `title`, `objective`, and `responsibility`.
- Current target-assessment proposal accepts many `record_ids` but only one optional `target_id`.
- Prompt payloads must remain bounded; proposed MVP limit is 25 active subjects per workstream.
- Migration should normalize schema-v1 records at read time and write schema v2 only on the next explicit update.

## UX notes
- Creation should ask for the monitoring question and/or subjects, not force both.
- Render subjects as a compact list or chips grouped by kind, not as multiple “active” workstreams.
- Show retired subjects separately and preserve their artifact history.
- When adding evidence, allow “general to workstream” as well as selecting one or more subjects.

## QA notes
- Cover question-only, multi-subject, and hybrid creation.
- Validate duplicate and invalid canonical references.
- Validate schema-v1 read compatibility and schema-v2 update behavior.
- Confirm artifacts retain references after a subject is retired.
- Confirm no cross-investigation workstream leakage.

## Risks
- A generic “object” abstraction could blur important differences among events, entities, locations, and attack targets.
- Subject lists can make agent prompts too large without bounding and summarization.
- Replacing `target_id` outright would break current target-assessment artifacts; migration must be additive.
- UX could become cumbersome if subject management is placed inside the chat flow only.

## Open questions
- Should `free_text` subjects later be resolvable into canonical subjects while preserving identity?
- Should evidence default to the whole workstream or require explicit subject association?
- Is 25 active subjects an appropriate MVP limit?
- Should question changes be revisioned like artifacts?

## Missing inputs
- Product approval of the three scope modes and supported subject kinds.
- UX approval of creation and subject-management interactions.
- Developer review of migration and artifact compatibility.
- QA approval of compatibility and isolation coverage.

## Required reviewers
- Product
- Development
- UX
- QA

## Required child issues
- [ ] Product review
- [ ] Developer review
- [ ] UX review
- [ ] QA review
- [ ] Execution planning

## Proposed execution checkpoints
1. Schema-v2 normalization and backward-compatible API tests.
2. Creation handoff for question-only, subjects-only, and hybrid scope.
3. Workstream summary and subject-management UI.
4. Multi-subject artifact association and agent-context changes.
5. Migration regression, final QA, and deployment.

## Handoff to developer
Review read-time schema migration, subject-reference validation, and the additive transition from `target_id` to `subject_ids`.

Expected output:
- feasibility notes
- affected API/tool contracts
- recommended migration approach
- test strategy
- reviewable execution slices

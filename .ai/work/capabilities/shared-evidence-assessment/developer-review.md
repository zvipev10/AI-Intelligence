# Developer / Architecture Review

## Status

AI-authored draft — pending human Development/Architecture approval

## Feasibility

Feasible as a bounded demo capability, but replay visibility must be enforced below the prompt layer. The current UI and MCP runtimes load/index the full corpus; therefore a prompt telling Moshe to ignore future records is not sufficient.

## Recommended design

### Scenario manifest

Store an immutable manifest containing scenario ID, anchor target, ordered stages, simulated timestamps, and released record IDs. Do not store evaluator truth or expected conclusions.

### Shared replay state

Store a small server-side state document with scenario ID, current stage, revision, status, and timestamps. Both the UI server and MCP processes resolve it on each retrieval operation. For MVP, one global demo state is the lowest-complexity option.

### Visibility boundary

Introduce a shared visibility predicate used by:

- UI event loading and raw-record endpoints;
- ID lookup and batch retrieval;
- text and structured search;
- semantic/vector results through post-filtering or an equivalent visibility-aware constraint;
- fusion and source-group operations;
- any target-evidence expansion used by Moshe.

Hidden records must behave as nonexistent to the active replay context.

### Workstream state

Persist a separate workstream document keyed by target/scenario. It should contain objective, scenario revision, agent run status, structured contributions, human decisions, and append-only revisions. Keep it separate from investigation memory and the read-only target catalog.

### Stage advance and agent trigger

An advance operation should:

1. validate the expected current revision;
2. atomically move to the next stage;
3. append a workstream stage event;
4. schedule one bounded Moshe reevaluation bound to the new revision;
5. expose `running`, `current`, `needs-human-decision`, or `failed`.

Only one run may be active. Duplicate advance requests must be idempotent. A result for an older revision must be stored as stale or discarded before artifact application.

### Candidate API surface

- `GET /api/scenario-replay`
- `POST /api/scenario-replay/start`
- `POST /api/scenario-replay/advance`
- `POST /api/scenario-replay/reset`
- `GET /api/validation-workstreams/{target_id}`
- `POST /api/validation-workstreams/{target_id}/decisions`

Exact naming is subject to implementation review.

## Likely affected areas

- UI server event-loading and API routing.
- MCP server global event/index access and every retrieval/fusion tool.
- Semantic retrieval filtering.
- Moshe gateway invocation and result normalization.
- New scenario manifest/state and workstream persistence modules.
- Frontend target-bank/workstream presentation.

## Reuse boundaries

- Reuse target IDs, raw record references, Moshe gateway, investigation identity where needed, and existing presentation primitives.
- Do not reuse investigation memory as the workstream database.
- Do not write replay state or review decisions into the target SQLite database.
- Do not duplicate full event rows into the workstream.

## Alternatives considered

### Prompt-only replay

Rejected. It cannot prevent future-record retrieval and makes the demo unverifiable.

### Per-user replay state

Architecturally cleaner for concurrent use but larger than the first slice because MCP calls currently lack a reliable request-scoped scenario context.

### Manual “run Moshe” after each stage

Simpler operationally but fails to demonstrate agent initiative. Retain only as a recovery control.

### Separate replay corpus/process

Strong isolation but adds deployment/process cost and risks divergence from the real runtime. Reconsider if shared filtering proves unsafe.

## Technical risks

- Missed retrieval surfaces leak future records.
- Process-level caches become inconsistent after reset/advance.
- Semantic post-filtering returns too few results unless candidate depth is expanded.
- A global replay state causes cross-user interference.
- Background jobs duplicate or outlive the stage that created them.
- Gateway/model latency makes stage transitions feel broken.
- Current static identity is not an authorization boundary.

## Required architecture decisions

- Approve global demo state or require request-scoped state.
- Choose persistence and atomicity mechanism for replay/workstream revisions.
- Define how the UI and MCP processes receive the same scenario revision.
- Define the bounded Moshe invocation contract and stale-result policy.
- Enumerate every data-access path covered by visibility tests.

## Proposed implementation slices after approval

1. Scenario manifest/state plus exhaustive visibility boundary and leakage tests.
2. Persistent workstream shell and target-bank entry point.
3. Stage advance, bounded Moshe trigger, stale-run protection, and structured update.
4. Human ambiguity decision, history, reset/recovery, and end-to-end demo validation.

These are review inputs, not an authorized execution plan.

## Approval

- [ ] Approved
- [ ] Approved with changes recorded below
- [ ] Changes requested

Human reviewer:

Date:

Notes:

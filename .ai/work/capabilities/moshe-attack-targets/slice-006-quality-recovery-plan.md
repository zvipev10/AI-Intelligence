# Slice 6 Quality Recovery Plan

## Status

Approved by the user and implemented through recovery slices A-D. All quantitative gates passed in checkpoint 008; deployment remains pending human review.

## Objective

Raise Moshe's V2.1 fusion results from the failed baseline to the already approved release gates without changing the MVP product model:

- chain recall: at least 90%
- evidence precision: at least 90%
- evidence recall: at least 90%
- hard-negative rejection: at least 95%
- false-merge rate: at most 5%
- duplicate-target rate: at most 2%
- deterministic source-independence: 100%
- evaluator leakage: zero

Current final baseline: 8% chain recall, 49.27% evidence precision, 11.22% evidence recall, 99% hard-negative rejection, and 8.75% false merges.

## Diagnosis

The failure is upstream of presentation and persistence:

1. Retrieval does not place most corroborating records in the same bounded neighborhood.
2. Object-cue filtering removes noise but also removes paraphrases and synonyms, causing very low recall.
3. Surviving records are selected by broad compatibility rather than a ranked evidence-pair decision.
4. Shared entity, canonical area, and time are currently strong enough to merge distinct chains.

The target-bank schema, source-independence grouping, duplicate prevention, Moshe routing, and shared presentation are not the recovery focus.

## Recommended design decisions

### 1. Improve Moshe's fusion tools, not the agent prompt

Implement deterministic retrieval, evidence-pair scoring, and ambiguity handling inside the Serbia MCP fusion boundary. Moshe receives ranked, explainable evidence packets and remains responsible for the candidate summary and tool invocation.

Do not rely on the language model to search all 14,800 records or repair weak retrieval in its prompt.

### 2. Use a bounded sparse retrieval index

Reuse runtime-visible V2.1 fields and the existing dataset process. Add no service, no target-bank table, and no dense embedding build on the VM.

Build a compact sparse index over normalized visible text and structured fields:

- event summary
- object class and public aliases
- canonical location
- entity
- timestamp
- source and collection family

For each anchor, retrieve a high-recall top-K neighborhood, then apply the stricter pair scorer. The index must be reusable across anchors and bounded by an explicit memory budget.

### 3. Rank evidence pairs before constructing candidates

Score each independent pair using explainable visible features:

- semantic/token similarity after normalization and synonym expansion
- object-class compatibility
- canonical-location compatibility
- entity compatibility when present
- temporal distance
- quantity compatibility
- independent-source confirmation
- repost/same-observation penalty
- contradiction penalty

Exact location/entity/time overlap is supporting context, not sufficient proof. Object incompatibility, strong quantity conflict, or weak semantic agreement must be able to veto a merge.

Return the component scores and reasons to Moshe for auditability; do not expose evaluator data.

### 4. Add conservative ambiguity handling

Use mutual-best matching plus a minimum score and a winner-margin requirement. When two possible partners are too close:

- do not persist a candidate;
- return an ambiguous, report-only result to Moshe;
- include the competing record IDs and visible reasons.

Within one fusion batch, one evidence record may support only one candidate unless a deterministic rule establishes separate observations. This directly addresses the seven observed false merges.

### 5. Keep source independence as a final hard gate

Run the existing mission, observation, and visible-repost collapse after retrieval and before persistence. A high pair score never overrides the requirement for two independent groups.

### 6. Preserve evaluator isolation and prevent metric overfitting

- Runtime code, Moshe, prompts, configuration, SQLite, and deployed indexes use only public V2.1 fields.
- Development fixtures are synthetic and cover paraphrases, synonyms, competing chains, contradictions, reposts, and hard negatives.
- QA alone runs the root-only 400-case evaluator after a code/configuration freeze.
- Development receives metrics and aggregate failure categories, not truth identifiers or truth-derived lookup artifacts.
- Any second evaluation round requires a documented general rule justified by public fields and a new frozen build.

## Execution slices

### Recovery slice A - Diagnostic fixtures and retrieval contract

Deliver:

- synthetic positive, paraphrase, synonym, collision, repost, and negative fixtures;
- a retrieval-result contract containing record ID, visible fields, retrieval score, and retrieval reasons;
- a resource measurement harness for index build/load/query.

Development gate:

- all synthetic corroborating records appear within the configured top-K;
- all negative fixtures remain available to the scorer rather than being silently filtered by one cue;
- peak incremental RSS stays within 150 MB on the production-class VM;
- no evaluator/truth import or field exists.

Checkpoint: Development and Architecture/Security review.

### Recovery slice B - Explainable evidence-pair scorer

Deliver:

- normalized object alias compatibility;
- temporal, location, entity, quantity, semantic, independence, repost, and contradiction features;
- deterministic total score and reason list;
- unit tests for every feature and veto.

Development gate:

- synthetic positive pair top-1 accuracy at least 95%;
- synthetic hard-negative abstention at least 95%;
- deterministic output across repeated runs;
- no score component uses evaluator-only data.

Checkpoint: Development and QA review of feature behavior and thresholds.

### Recovery slice C - Candidate graph and ambiguity control

Deliver:

- mutual-best and winner-margin selection;
- single-assignment control within a batch;
- ambiguous report-only output;
- integration with `prepare_candidate` and existing persistence gates.

Development gate:

- zero false merges in the synthetic shared-location/entity/time collision set;
- no regression in repost collapse, source independence, duplicate prevention, or target-bank transactions;
- ambiguous cases are visible to Moshe but are not persisted.

Checkpoint: Product, Development, and QA review because candidate behavior changes.

### Recovery slice D - Frozen full evaluation

Procedure:

1. Freeze code, configuration, alias lists, and scoring thresholds.
2. Run all 300 positive chains and 100 hard negatives with the public-data runtime user.
3. Run the root-only evaluator afterward.
4. Compare with `evaluation-006.json` and apply every approved release gate.
5. Run General-agent, routing, SQLite, presentation, and resource regressions.

Exit:

- proceed to Slice 7 only if every gate passes;
- otherwise stop with aggregate failure categories and a reviewed next hypothesis.

## Expected implementation areas

- `mcp_server/fusion_tools.py`: normalization, pair features, scoring, and ambiguity decisions.
- A focused sparse-retrieval module under `mcp_server/`, or the existing semantic-search module if its public contract and resource bounds are suitable.
- `mcp_server/server.py`: constrained tool contract returning ranked evidence packets.
- `mcp_server/test_fusion_tools.py` plus focused retrieval and collision tests.
- Slice 6 evaluator runner: reporting only; no runtime dependency.

No planned changes to:

- SQLite schema or existing target data
- Moshe routing/session architecture
- shared UI presentation
- General-agent behavior
- human approval lifecycle

## Risks and controls

| Risk | Control |
|---|---|
| Recall increases by admitting noise | Separate high-recall retrieval from strict pair scoring and abstention |
| Hand-written aliases overfit V2.1 | Keep aliases domain-level, reviewable, and justified without evaluator labels |
| Shared locations cause false merges | Require semantic/object agreement plus mutual-best margin; location alone cannot establish a pair |
| VM memory incident repeats | Sparse reusable index, 150 MB incremental-RSS gate, no dense rebuild |
| Evaluator leakage | Root-only evaluator, deployment scans, import/config checks, aggregate-only feedback |
| Moshe persists uncertain output | Ambiguous results are report-only; existing confidence and independence gates remain |

## Recommended approval

Approve recovery slices A-D as the Slice 6 remediation plan. Authorize implementation one checkpoint at a time, starting with synthetic fixtures and the bounded retrieval contract.

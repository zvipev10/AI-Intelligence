# V2.1 and Moshe Implementation Handoff

## Purpose of this handoff

This file is the continuation point for implementing Moshe from another computer. It records the completed dataset work, current repository and production state, accepted product decisions, unresolved decisions, and the recommended implementation sequence.

## Repository continuation

- Repository: `zvipev10/AI-Intelligence`
- Working branch: `codex/v2-1-fusion-evidence`
- Latest handoff-base commit before this update: `0bc89dd`
- Previous slice commits:
  - `0a03768` - plan V2.1 cross-source fusion evidence
  - `fbea284` - generate V2.1 cross-source fusion evidence
  - `0bc89dd` - enable and validate V2.1 semantic fusion
- The branch includes the earlier V2 semantic-readiness work.

On another computer:

```text
git fetch origin
git switch --track origin/codex/v2-1-fusion-evidence
git status --short
```

Do not use Graphify for this work. Read `AGENTS.md` and the repository workflow skills before starting a meaningful implementation slice.

## Completed outcome

V2.1 is ready as the evaluation corpus for Moshe. It corrects V2's independently sampled public/UAV evidence without modifying V1 or V2.

- 14,800 runtime records.
- 3,800 UAV observations.
- 11,000 public-source records.
- 300 evaluator-known shared-object chains.
- Each positive chain has one UAV anchor and two public confirmations from distinct public platforms.
- 900 positive evidence records.
- 100 hard negatives that are geographically and semantically tempting but refer to another affiliation/object instance.
- Public confirmations vary terminology and express exact-approximate, range, and unresolved counts.
- All operational events remain synthetic.

## Why V2.1 was required

V2 generated each public and UAV record independently from common event, actor, time, and canonical-location distributions. It was aligned at the scenario level but did not reliably establish that two sources described the same physical object. Accidental correlations were therefore unsuitable as ground truth for Moshe.

V2.1 retains the existing records and schema but intentionally binds selected public records to UAV anchors. Evaluator-only labels identify the true shared object and hard negatives.

## Dataset and generator files

Generator and validation:

- `llm_investigation_orchestrator_serbia_poc/data/generate_serbian_intelligence_v2_1.py`
- `llm_investigation_orchestrator_serbia_poc/data/validate_serbian_intelligence_v2_1.py`
- `llm_investigation_orchestrator_serbia_poc/mcp_server/validate_v2_1_semantic_fusion.py`

V2.1 runtime directory:

- `llm_investigation_orchestrator_serbia_poc/data/serbian_intelligence_v2_1/`

Runtime-visible artifacts:

- `north_kosovo_serbian_intelligence_v2_1_14800.csv`
- `north_kosovo_serbian_intelligence_v2_1_14800.jsonl`
- `serbia_kosovo_events_projection_v2_1.csv`
- `serbian_uav_observations_v2_1.jsonl`
- `serbia_kosovo_entities_v2_1.json`
- `serbia_kosovo_locations_v2_1.json`

Evaluator-only artifacts:

- `serbia_kosovo_evaluator_labels_v2_1.csv`
- `fusion_target_truth_v2_1.jsonl`

Moshe, MCP retrieval, and the UI must never load evaluator-only truth. It is exclusively for automated evaluation.

## Location model and geographic implications

Raw records do not carry observation-level coordinates. Every record has a `location_id` resolving to the canonical locations table, which supplies latitude, longitude, place type, and precision.

Consequences:

- A shared `location_id` is a candidate geographic bucket, not proof of an identical point.
- Canonical latitude/longitude is a representative area anchor.
- Some different location IDs share coordinates.
- UAV `geolocation_confidence` does not add a sensor coordinate.
- Moshe may create area-level target estimates but must not claim point accuracy beyond the canonical location precision.

Recommended geographic matching tiers:

1. Exact canonical match: identical `location_id`.
2. Nearby canonical match: different location IDs within a type-specific radius, used only with stronger semantic, temporal, and source evidence.
3. Target artifacts retain the canonical location, representative coordinates, precision, match tier, and an uncertainty radius.

V2.1 positive truth asserts that records refer to the same synthetic object inside the canonical area. It does not assert an exact coordinate.

## Semantic and runtime readiness

The semantic index version is `semantic-event-index-v11-v2-1-fusion-terminology`. It includes the varied terminology used by public confirmations for convoys, armored vehicles, roadblocks, observation posts, helicopters, logistics vehicles, and engineering activity.

Optional local selection:

```text
INTELLIGENCE_POC_DATASET_VERSION=v2.1
```

Accepted aliases are `v2.1`, `v2_1`, and `v21`. Both the MCP and UI loaders support V2.1.

Validation results:

- V1 loader: 10,000 records.
- V2 loader: 14,800 records.
- V2.1 loader: 14,800 records.
- Deterministic V2.1 double regeneration passed.
- V1/V2 artifacts remained unchanged.
- No evaluator truth was found in raw or projection data.
- Every positive public confirmation emitted the expected semantic object concept.
- All 300 chains recovered both public confirmations: 600/600 recall in the top 20 after area, entity, and time filtering with the UAV record as semantic seed.
- Pure-Python semantic-cache warm load: approximately 3.5 seconds locally.
- Tested query latency: approximately 0.013-0.052 seconds.

Repeat the principal checks with:

```text
python llm_investigation_orchestrator_serbia_poc/data/validate_serbian_intelligence_v2_1.py --regenerate
python llm_investigation_orchestrator_serbia_poc/mcp_server/validate_v2_1_semantic_fusion.py --chains 300
```

## Production state

Production remains on V2. V2.1 has not been uploaded, indexed, selected, or deployed.

The current production V2 environment was previously healthy with 14,800 records. Do not assume the V2.1 branch's semantic v11 cache is present remotely. Deploying V2.1 requires a newly built portable cache because the semantic vocabulary and projection content signatures changed.

Do not switch production as an incidental part of Moshe development. Treat V2.1 deployment as a separate release checkpoint with rollback to V2.

## Accepted Moshe product decisions

- The knowledge-layer name is `attack targets`.
- It is a global bank, not mission-local storage.
- It contains both Moshe-created candidate targets and human-approved targets.
- The bank is not populated automatically. Moshe runs only when commanded for a specific mission.
- Moshe is a new Hermes agent/persona specializing in target intelligence and the target bank.
- Moshe uses all permitted raw evidence and fusion tools.
- A new target requires at least two supporting sources referring to the same object and location.
- Moshe checks the global bank for an existing target before creating another.
- Moshe can answer questions about all targets in the bank, their evidence, freshness, uncertainty, and approval state.
- Moshe does not approve his own target candidates.
- Serbian-side information remains limited to the permitted public-source perspective; UAV-derived records primarily concern observed opposing-side objects.

## Recommended `attack targets` record contract

Use a persistent, versioned record rather than writing targets into the raw-events dataset.

Identity and lifecycle:

- `target_id`: stable generated identifier.
- `title`: concise human-readable description.
- `status`: `candidate`, `approved`, `rejected`, `stale`, or `revoked`.
- `created_by`: Moshe agent/session identity.
- `created_at`, `updated_at`, and revision number.
- `mission_id`: mission that created or last materially updated the candidate.

Object assessment:

- canonical object class and semantic aliases observed.
- assessed affiliation/entity.
- movement/deployment state.
- count estimate as minimum, maximum, preferred estimate when justified, and count confidence.
- identification confidence and overall fusion confidence.

Geography and time:

- canonical `location_id`.
- representative latitude/longitude copied from the canonical table.
- location precision/type.
- uncertainty radius or area description.
- geographic match tier: exact canonical or nearby canonical.
- first observed, last observed, last confirmed, freshness state, and expiry/staleness time.

Evidence and reasoning:

- supporting raw record IDs.
- source family/platform for every record.
- source-independence groups.
- semantic-match rationale.
- temporal and geographic match rationale.
- disagreements, rejected evidence, and alternative hypotheses.
- explicit statement when presence is confirmed but count remains unresolved.

Approval and audit:

- approver identity and approval timestamp.
- approval/rejection/revocation note.
- immutable revision/audit history.
- references to the previous target revision when evidence changes.

## Recommended fusion workflow

1. Receive a bounded mission: area/location IDs, time window, requested object classes, affiliation scope, freshness requirement, and minimum confidence.
2. Search raw records by canonical area and time.
3. Create geographic groups using exact location IDs first; optionally inspect nearby canonical areas.
4. Within each geographic group, create semantic object clusters using structured UAV classes and multilingual concept matching.
5. Check actor/affiliation compatibility and movement/deployment compatibility.
6. Collapse dependent reporting before counting sources.
7. Require the configured independent-source threshold.
8. Preserve count disagreement as a range rather than forcing a precise count.
9. Search `attack targets` for an existing target in the same area, object family, affiliation, and relevant time window.
10. Update/version the existing target when it is the same assessed object; otherwise create a new candidate.
11. Save complete evidence lineage and fusion rationale.
12. Return a mission summary with created, updated, skipped, ambiguous, and rejected candidates.

## Source-independence rules to implement

Recommended defaults:

- Multiple frames or clips from one UAV mission count as one source.
- Separate UAV missions are distinct observations but remain in the same collection family. They strengthen confidence but should not automatically satisfy a two-family rule.
- Reposts or near-identical public wording should collapse into one reporting lineage.
- Two distinct public platforms are not automatically independent if semantic duplication indicates syndication.
- Preferred creation threshold: at least two independent source groups, ideally from two collection families.
- Allow a mission to return `insufficient corroboration` rather than creating a target.

V2.1 truth chains deliberately provide UAV plus two public platforms. Evaluation should still verify that the implementation does not count duplicate text as independent.

## Count uncertainty decision

Two sources may confirm that an object is present while disagreeing about quantity. Presence and count confidence must be separate.

Recommended representation:

- `presence_confirmed=true` when the fusion threshold is met.
- `count_min` and `count_max` derived from credible reports.
- optional `count_estimate` only when evidence supports it.
- `count_confidence` independent of overall target confidence.
- retain every original source estimate in evidence lineage.

## Staleness defaults requiring product confirmation

Suggested starting values:

- Moving convoy or withdrawing vehicle group: 1-3 hours.
- Deployed vehicles or temporary force concentration: 6-12 hours.
- Roadblock, observation post, or engineering position: 12-48 hours.
- Fixed facility or infrastructure: several days, subject to confirmation rules.

Stale targets remain historically searchable but must not appear as current. A new observation may refresh, relocate, split, or supersede a target; it must not silently erase history.

## Duplicate-target decision rules

Before creation, search by:

- same or nearby canonical location;
- compatible object class;
- compatible affiliation;
- overlapping active/freshness interval;
- compatible movement state.

Possible outcomes:

- Same object: append evidence and create a new target revision.
- Same object moved: update location through a movement/history revision, preserving the previous position.
- Similar but distinct object: create a new target and explain why it was split.
- Ambiguous: do not create automatically; return it for analyst review.

## Existing investigation capabilities

The current MCP server already provides useful building blocks:

- structured event search;
- semantic event search with time, location, entity, source, reliability, certainty, and keyword filters;
- event/object retrieval;
- location and entity resolution;
- actor history;
- event sequences;
- linkage explanation;
- related-event and semantic-clue tracing;
- location-claim comparison and hypothesis challenge.

New capabilities still required:

- geographic grouping across an area/time window;
- source-lineage and independence assessment;
- semantic same-object cluster scoring;
- target-bank duplicate search;
- candidate create/update/version operations;
- target approval/rejection/revocation operations restricted to a human role;
- target-bank query and mission-summary tools.

## Hermes agent creation and invocation plan

The repository currently exposes the Serbia MCP toolset to Hermes; it does not yet contain a completed native named-agent implementation for Moshe.

Recommended sequence:

1. Inspect the exact Hermes version/configuration on the target environment and confirm whether named agents are represented as native profiles, prompts, or dedicated sessions.
2. Create Moshe as a dedicated, manually invoked agent/persona with a narrow system instruction and access to the Serbia investigation tools plus new target-bank tools.
3. Define an explicit mission input contract rather than accepting an unbounded background task.
4. Give Moshe read access to raw runtime evidence and the global target bank.
5. Give Moshe write access only to candidate creation and evidence-backed candidate updates.
6. Keep approval/rejection/revocation outside Moshe's permissions.
7. Persist mission run IDs and audit every target-bank mutation.
8. Add an invocation path in Hermes such as a named command/profile selection after confirming the supported native mechanism; do not invent a configuration format before inspection.

Suggested mission input:

- mission title and analyst question;
- canonical area IDs or resolved area;
- start/end time;
- target object classes;
- affiliation scope;
- minimum source independence and confidence;
- freshness requirement;
- maximum candidates/results.

Suggested mission output:

- created targets;
- updated existing targets;
- possible duplicates requiring review;
- insufficiently corroborated clusters;
- rejected clusters and reasons;
- unresolved evidence gaps.

## UI plan

Add a global `attack targets` layer after the storage/tool contract is stable.

Required states and controls:

- visually distinct candidate, approved, stale, rejected, and revoked states;
- map display that communicates area uncertainty rather than false point precision;
- filters by status, object, affiliation, freshness, confidence, and mission;
- evidence drill-down and source lineage;
- count range and uncertainty display;
- revision/history view;
- human approval, rejection, and revocation controls with audit notes;
- empty, loading, conflict, stale, and permission-denied states.

## Recommended implementation slices

### Slice 1 - Target-bank persistence and contract

- Define schema, stable IDs, revisions, audit records, and lifecycle states.
- Add read/search/create-candidate/update-candidate operations.
- Add separate human-only approval operations.
- Implement duplicate candidate lookup.

Checkpoint: schema and tool contract review before proceeding.

### Slice 2 - Geographic and semantic fusion tools

- Area/time retrieval.
- Exact and nearby canonical grouping.
- semantic same-object scoring.
- source-lineage collapsing and independence checks.
- count reconciliation and confidence calculation.

Checkpoint: evaluate against a subset of V2.1 truth and hard negatives.

### Slice 3 - Moshe Hermes agent

- Confirm native Hermes agent/profile mechanism.
- Add Moshe instruction, mission contract, tool permissions, and audit identity.
- Implement manual invocation and mission summary.

Checkpoint: run bounded missions without evaluator truth access.

### Slice 4 - Full evaluation

- Run all 300 V2.1 positive chains and 100 hard negatives.
- Measure chain/target recall, evidence precision, duplicate rate, false merges, hard-negative rejection, and count uncertainty quality.
- Review incorrect targets before adjusting thresholds.

### Slice 5 - UI layer

- Add the `attack targets` map/list layer, detail view, filters, history, and approval flow.

### Slice 6 - Release

- Build a portable V2.1 semantic cache.
- Upload V2.1 runtime artifacts but never evaluator truth.
- Deploy target-bank storage and MCP tools.
- Register/invoke Moshe using the verified Hermes mechanism.
- Smoke-test services and rollback path.
- Switch dataset selection only after explicit release approval.

## Evaluation metrics

Use evaluator truth only in test code:

- target-chain recall across 300 positives;
- evidence-record precision and recall;
- false merge rate;
- duplicate target creation rate;
- rejection rate for 100 hard negatives;
- source-independence correctness;
- count-range coverage and confidence calibration;
- stale-target behavior by object type;
- proof that no evaluator truth path is accessible to Moshe.

Do not optimize solely for 100% positive recall; hard-negative rejection and false-merge prevention are equally important.

## Open decisions for the next computer/session

1. Confirm staleness thresholds by object class.
2. Decide whether two separate UAV missions may ever satisfy the minimum source rule without another collection family.
3. Choose the human role allowed to approve/reject/revoke targets.
4. Choose persistence format based on existing project patterns: durable JSON/JSONL with locking versus a small transactional database. A global versioned bank favors a transactional store if available without adding operational complexity.
5. Define nearby-location radii by canonical precision/type.
6. Define confidence thresholds for automatic candidate creation versus analyst-review-only output.
7. Confirm whether a moved object remains one target with location history or becomes a new target for particular object classes.
8. Confirm the native Hermes named-agent mechanism on the actual installed version.
9. Decide when V2.1 should be deployed and become the production default.

## Known risks

- Canonical areas can contain multiple similar objects; same location is not same identity.
- V2.1 provides evaluator truth for synthetic shared objects but not sensor-level coordinates.
- Public-platform independence can be overstated when reports copy one another.
- High recall can be achieved by over-merging; hard negatives must constrain tuning.
- Semantic v11 invalidates earlier cache versions and requires a new cache for deployment.
- The constrained VM previously required the compact pure-Python dense cache; do not rebuild a memory-heavy index on the VM.
- Target-bank concurrency and approval permissions need explicit design before global writes.

## Durable artifacts and planning references

- `.ai/work/capabilities/v2-1-fusion-evidence/capability-brief.md`
- `.ai/work/capabilities/v2-1-fusion-evidence/developer-review.md`
- `.ai/work/capabilities/v2-1-fusion-evidence/qa-review.md`
- `.ai/work/capabilities/v2-1-fusion-evidence/execution-plan.md`
- `.ai/work/capabilities/v2-1-fusion-evidence/checkpoint-001.md`
- `.ai/work/capabilities/v2-1-fusion-evidence/checkpoint-002.md`
- `.ai/work/capabilities/v2-1-fusion-evidence/status.md`
- `docs/decisions.md`

## Recommended immediate next action

Start a new capability workspace for Moshe and `attack targets`. First inspect existing persistence patterns and the installed Hermes named-agent mechanism. Then draft the target-bank schema/tool contract using the accepted decisions above and stop at the schema checkpoint before implementing global writes.

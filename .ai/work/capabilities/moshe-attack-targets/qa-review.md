# QA Review

## Review status

Approved on 2026-07-19. The user explicitly reported: "QA approved."

## Recommendation

Continue to UX review. The QA strategy is approved for planning; exact quantitative acceptance thresholds must be stated in the execution plan before the full-evaluation slice.

## Blocking issues

None for continuing role enrichment.

## Test strategy

Use layered validation:

1. Unit tests for routing, schema constraints, source grouping, duplicate checks, and result normalization.
2. MCP integration tests for investigation, fusion, candidate persistence, and target presentation tools.
3. Hermes session tests for `@משה` routing, consecutive-message continuity, clarification, and mission closure.
4. Isolated evaluator tests against all V2.1 truth and hard negatives.
5. Browser tests for Moshe attribution and shared target-layer map/table presentation.
6. Production smoke and rollback checks on the constrained VM.

## V2.1 fusion evaluation

- Run all 300 positive fusion chains.
- Run all 100 hard negatives.
- Measure target-chain recall.
- Measure evidence-record precision and recall.
- Measure false merges and duplicate target creation.
- Verify source-independence grouping, including repost and same-UAV-mission collapse.
- Verify quantity ranges and unresolved counts preserve source disagreement.
- Do not optimize positive recall at the expense of hard-negative rejection.

Evaluator truth is read only by the isolated evaluator after Moshe completes. It is never available to Moshe, runtime MCP tools, prompts, SQLite, or presentation results.

## Routing and session tests

- Current user message with exact `@משה` routes to Moshe.
- Messages without `@משה` route to General.
- Mentions in history, quoted content, agent output, or tool results do not route to Moshe.
- Consecutive `@משה` messages reuse the same Moshe mission and Hermes session.
- A non-mention closes the mission; a later mention creates a new mission/session.
- Moshe can clarify missing scope through conversation.
- A clarification reply without `@משה` goes to General, as designed.
- General and Moshe parallel histories do not leak into one another except through the explicit mission-start context packet.

## Persistence tests

- SQLite initializes idempotently at the configured path.
- Schema constraints reject invalid status, confidence, count assessment, and duplicate target/evidence pairs.
- Candidate and evidence writes commit atomically.
- Failed writes roll back without partial evidence.
- Duplicate search updates overlapping candidates and keeps ambiguous identities separate.
- Moshe has no SQL, filesystem, deletion, or lifecycle-status operation.
- Administrator reset requires explicit path/confirmation and creates a backup.
- Backup and restoration preserve target/evidence counts.

## Evaluator-isolation negative tests

- Production deployment fails if evaluator filenames exist in runtime directories.
- Production configuration fails validation if it references evaluator/truth paths or IDs.
- Runtime import checks reject evaluator/generator/validation module dependencies.
- MCP contracts expose no truth-derived fields.
- SQLite schema and content contain no evaluator fields or `FUSION-TRUTH-V2-1-` identifiers.
- Moshe runs successfully when evaluator artifacts are completely absent.

## Shared-backend regression tests

- Existing General-agent investigations retain their answer, steps, events, locations, entities, map, table, and timeline behavior.
- Existing layer selection, filters, visibility, close behavior, saved questions, and recorded runs remain functional.
- Shared normalization yields the same existing result envelope before and after extraction for General.
- `responding_agent` changes attribution without changing evidence content.
- Moshe target layers use the shared layer state and do not require a separate renderer.

## UX/browser tests

- Moshe responses are clearly attributed to `משה`.
- Candidate targets render in table and map views.
- Canonical location markers do not imply exact point accuracy.
- Target title, object class, entity, confidence, quantity, summary, and evidence access are present.
- RTL, mobile, empty, loading, no-target, error, and permission-denied states are covered.

## Reliability and production checks

- Both Hermes gateway and UI remain active after deployment.
- V2.1 remains selected and reports 14,800 rows.
- Semantic cache loads without a rebuild on the VM.
- Observe memory and swap during representative Moshe missions because the MVP imposes no application-level limits.
- Verify target-bank backup and rollback before production acceptance.

## Missing tests to define during execution planning

- Exact numeric acceptance thresholds for recall, evidence precision, hard-negative rejection, duplicate rate, and false merges.
- Representative unrestricted-mission workload for VM memory observation.

## Parent/child status

The QA planning child may close locally. The parent capability remains open. UX review and execution planning remain required.

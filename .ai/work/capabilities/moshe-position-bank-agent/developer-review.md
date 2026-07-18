# Developer/Architecture Review — Draft

## Status

Draft recommendations pending human review. Not approved for execution planning.

## Feasibility

The current application already provides raw-event loading, MCP investigation tools, layer catalog/rows endpoints, investigation memory, and a static Moshe team profile. It does not yet provide a durable cross-investigation knowledge-artifact store, source-family lineage, artifact lifecycle, or a specialized agent identity/tool allowlist.

## Recommended architecture

Use a deterministic-first pipeline:

1. normalization and source-lineage enrichment;
2. spatial/temporal candidate generation;
3. hard independence and compatibility rules;
4. scored fusion with explicit uncertainty;
5. LLM explanation and contradiction review only after deterministic gating;
6. human acceptance;
7. append-only artifact/revision persistence;
8. read-only bank tools for expert answering.

The LLM should not decide source independence or invent coordinates. Those are validated fields and deterministic calculations.

## Persistence options

### Option A — Versioned JSON artifacts

Fastest POC path and consistent with current filesystem persistence. Easy to inspect and deploy, but weak for concurrency, indexing, transactional updates, and audit integrity.

### Option B — SQLite bank (recommended MVP)

One versioned SQLite database with artifacts, revisions, evidence links, review actions, and audit records. It supports atomic writes, indexed queries, referential checks, and a later migration path without introducing a service dependency.

### Option C — External database/service

Appropriate for multi-user production, but beyond the current POC and would trigger broader identity, permissions, deployment, and operations work.

## Proposed logical components

- `source_lineage`: derives/validates independent source families.
- `position_candidate_builder`: spatial-temporal blocking and object compatibility.
- `position_fusion`: calculates fused geometry, uncertainty, count range, confidence factors, and contradictions.
- `position_bank_repository`: artifacts, revisions, evidence, review actions, audit.
- `moshe_agent_policy`: role prompt, tool allowlist, citation and refusal rules.
- MCP tools for draft creation and bank retrieval.
- UI catalog layer and review workflow.

## Recommended execution slices after approval

1. Data contract and offline gold-set validator; no agent writes.
2. Read-only position-bank repository and layer projection.
3. Deterministic candidate/fusion engine producing drafts in a sandbox.
4. Human review lifecycle and audited acceptance.
5. Moshe specialized agent with read-all-raw/read-bank/create-draft tools.
6. Bank expert Q&A, staleness/contradiction handling, performance and security validation.

Each slice changes data or behavior and requires a checkpoint before the next slice.

## Technical questions

- How will source-family lineage be generated for the existing V2 corpus?
- Which geometry library, if any, is acceptable without creating deployment friction?
- Should confidence be an explainable rule score, a calibrated probability, or only an ordinal label in MVP?
- How are mobile-object freshness and track continuity represented?
- Should accepted bank artifacts be global and investigation links many-to-many?

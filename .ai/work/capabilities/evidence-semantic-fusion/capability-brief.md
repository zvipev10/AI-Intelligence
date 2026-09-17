# Evidence semantic fusion

## Goal

Improve `prepare_evidence` and `prepare_fused_evidence` so semantically equivalent raw descriptions resolve to the same canonical object class, related records are correlated across a rolling time window, and fused evidence is available to Talia through the same repository interface used by the application.

## Scope

- Reuse the existing semantic concept vocabulary; do not introduce evaluator data or a new model dependency.
- Normalize missing public-source object classes during evidence preparation.
- Apply the same normalization before live and batch fusion.
- Replace fixed wall-clock fusion buckets with rolling temporal grouping.
- Expose precomputed fused evidence through the MCP evidence repository used by Talia.
- Preserve the existing source grouping and binary persistence eligibility behavior.

## Non-goals

- No new source-independence model.
- No new provisional/report-only evidence status.
- No cross-object assessment logic inside evidence fusion; Talia remains responsible for assessment.
- No evaluator truth or evaluator labels at runtime.

## Acceptance criteria

- The three KSF/Ibar Bridge chains resolve as armored vehicle, helicopter, and engineering activity evidence.
- Each chain produces a separate deterministic `EVD-FUSED-*` object.
- `get_evidence`, `search_evidence`, assessment validation, provenance tracing, and the Evidence Layer resolve the same fused objects.
- Fixed clock boundaries do not split otherwise compatible records inside the configured rolling window.
- Existing evidence and assessment regression tests pass.

## Review status

Approved for implementation by the user after architecture discussion on 2026-09-17.

# Execution Plan

## Capability
Hebrew and English runtime localization

## Plan status
Approved for controlled execution based on the user-supplied plan and its recommended Option A.

## Prerequisite review gate
- Product brief: `capability-brief.md` — ready
- Developer review: `developer-review.md` — ready
- QA review: `qa-review.md` — ready
- UX review: required before accepting Slice 3
- Architecture: Option A accepted as a working assumption by instruction to start from the recommended plan

## Goal
Consolidate the Hebrew application and English WIP into one runtime-localized canonical workspace.

## Approved scope
Localized projections, MCP locale argument/caches, localized agent instructions and routing, UI language/direction behavior, and verification.

## Non-goals
New investigation features, schema redesign unrelated to locale, and production deployment in early slices.

## Proposed approach
Port only localization-specific WIP changes onto current canonical code. Keep Hebrew as the compatibility default. Key all data and semantic caches by normalized locale.

## Data/API changes
Add optional `locale: "he" | "en"` to MCP tools and locale to investigation/UI requests. No existing required fields change.

## Execution slices

### Slice 1 — Localized data and MCP runtime
Import verified `.en` assets, add locale normalization and per-locale runtime state, expose locale in tool schemas, and add isolation/fallback tests.
Risk: medium. Reviewer: development/QA. Stop after slice: yes.

### Slice 2 — Agent prompt and routing
Port localized prompts and propagate session locale through investigation and MCP calls.
Risk: high (agent/tool interface). Reviewer: development/product. Stop after slice: yes.

### Slice 3 — UI consolidation
Port language toggle, i18n copy, formatting, and RTL/LTR behavior without replacing newer canonical features.
Risk: high (UX/product behavior). Reviewer: UX/QA. Stop after slice: yes.

### Slice 4 — End-to-end validation
Run bilingual automated suites, local smoke tests, manual browser checks, and prepare handoff/deployment notes.
Risk: medium. Reviewer: QA/product. Stop after slice: yes.

## Rollback/fallback notes
Each slice is independently committed. Hebrew remains the default; locale-aware behavior can be disabled by omitting locale while preserving the previous contract.


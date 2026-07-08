# Active Capability Workspace

This folder stores active capability-level AI workflow artifacts.

Use one folder per meaningful capability:

```text
.ai/work/capabilities/<capability-slug>/
  capability-brief.md
  status.md
  decisions.md
  developer-review.md
  ux-review.md
  qa-review.md
  execution-plan.md
  checkpoint-001.md
  checkpoint-002.md
  handoff-summary.md
  issues/
```

## Purpose

These files are used as shared handoff artifacts between roles.

Do not rely on long private chat history for handoff.

## Capability dashboard

| Capability | Phase | Status | Waiting on | Next artifact |
|---|---|---|---|---|
| multi-layer-query-filtering | Slice 1 UX styling review | Development complete | Product/UX | checkpoint-004.md |

## Typical flow

1. Product starts a capability and creates `capability-brief.md`, `status.md`, and the parent capability issue.
2. Product, Development, UX, and QA work through child issues for actionable review tasks.
3. Developer reviews the brief and creates or approves `developer-review.md`.
4. UX and QA create review files when relevant.
5. Codex creates `execution-plan.md` and child implementation/review issues for slices.
6. Codex executes in slices and creates checkpoint summaries.
7. `status.md` is updated whenever owner, phase, blocker, or next artifact changes.
8. Final handoff is saved in `handoff-summary.md`, and the parent issue closes only after final acceptance.

AI-prepared role reviews are drafts until the human role owner explicitly approves them or explicitly delegates that role decision to the AI. A draft role review should not be treated as ready for execution planning.

## Notes

This folder contains active task memory.

Long-term decisions should be promoted to:
- `docs/decisions.md`
- `docs/product-context.md`
- `docs/architecture.md`

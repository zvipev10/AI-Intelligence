# Active Capability Workspace

This folder stores active capability-level AI workflow artifacts.

Use one folder per meaningful capability:

```text
.ai/work/capabilities/<capability-slug>/
  capability-brief.md
  developer-review.md
  ux-review.md
  qa-review.md
  execution-plan.md
  checkpoint-001.md
  checkpoint-002.md
  handoff-summary.md
```

## Purpose

These files are used as shared handoff artifacts between roles.

Do not rely on long private chat history for handoff.

## Typical flow

1. Product starts a capability and creates `capability-brief.md`.
2. Developer reviews the brief and creates `developer-review.md`.
3. UX and QA create review files when relevant.
4. Codex creates `execution-plan.md`.
5. Codex executes in slices and creates checkpoint summaries.
6. Final handoff is saved in `handoff-summary.md`.

## Notes

This folder contains active task memory.

Long-term decisions should be promoted to:
- `docs/decisions.md`
- `docs/product-context.md`
- `docs/architecture.md`

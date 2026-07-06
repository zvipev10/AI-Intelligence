---
name: end-to-end-feature-delivery
description: Use when defining, planning, implementing, checkpointing, reviewing, and handing off a new capability or meaningful feature change.
---

# End-to-End Feature Delivery Skill

## Purpose

Use this skill for new capabilities and meaningful feature changes.

The AI should act as an observable execution engine:
- collect professional inputs
- produce shared artifacts
- execute in small slices
- expose partial results
- support review by any professional
- preserve context in issues, PRs, docs, and `.ai/work/capabilities/`

## Active capability workspace

For every meaningful capability, create or use:

`.ai/work/capabilities/<capability-slug>/`

Recommended files:

- `capability-brief.md`
- `developer-review.md`
- `ux-review.md`
- `qa-review.md`
- `execution-plan.md`
- `checkpoint-001.md`
- `checkpoint-002.md`
- `handoff-summary.md`

The workspace is the role-to-role handoff mechanism.

Do not rely on previous chat history for handoff.

## Publishing rule

Every shared artifact created or updated in this workflow should be committed and pushed before another role is expected to use it.

Before publishing:
- run `git status --short`
- identify current-task files
- identify unrelated dirty files
- stage only current-task files
- commit with a clear message
- push to a shared branch
- prefer a draft PR for capability work

Do not push directly to `main` unless explicitly instructed.

If publishing is blocked, record the blocker in the checkpoint or handoff output and list the files that remain local.

## Roles

Product contributes:
- user problem
- business goal
- target users
- expected behavior
- scope and non-goals
- acceptance criteria
- release priority

Developer contributes:
- feasibility
- implementation approach
- codebase constraints
- affected files/services
- data/API constraints
- technical risks
- test strategy
- execution slices

UX contributes:
- flows
- states
- copy
- accessibility
- interaction details

QA contributes:
- testability
- edge cases
- regression areas
- manual/automated test plan

Architect/security contributes when triggered by:
- new service
- new integration
- permissions
- sensitive data
- major data flow change
- performance risk

## Phase 1 — Capability initiation by Product

Do not code.

Create:

`.ai/work/capabilities/<capability-slug>/capability-brief.md`

Use `.ai/templates/capability-brief.md` when available.

Produce:
- capability brief
- assumptions
- missing inputs
- suggested reviewers
- proposed execution checkpoints
- specific questions for development, UX, QA, architecture, or security when relevant

Publish:
- commit and push `capability-brief.md`
- create or update the draft PR / issue with the artifact path

Checkpoint A:
Request review from relevant professionals before execution planning.

## Phase 2 — Role enrichment

Do not code.

If the current request says "developer stage", "UX stage", "QA stage", or names a review role, stop at this phase unless the user explicitly asks for execution planning after the role review is complete. Do not create `execution-plan.md` in the same pass that first creates a required role-review artifact unless the user explicitly asks to bypass the gate.

Depending on the role, create or update:

- `developer-review.md`
- `ux-review.md`
- `qa-review.md`

Developer review should include:
- review status and reviewer/source of input
- feasibility notes
- likely affected files/services
- implementation options
- recommended technical approach
- technical risks
- test strategy
- proposed execution slices
- acceptance criteria improvements
- review gates before coding
- blocking questions that must be answered before execution planning

UX review should include:
- user flow
- UI states
- empty states
- error states
- disabled states
- copy
- accessibility notes
- UX edge cases

QA review should include:
- test strategy
- acceptance criteria validation
- happy path tests
- edge cases
- negative tests
- regression areas
- automation suggestions

Publish:
- commit and push each completed role-review artifact
- update the draft PR / issue with the new artifact path and requested reviewer

## Phase 3 — Execution plan

Do not code until the execution plan exists.

Do not create the execution plan until required role-review artifacts exist and are marked ready for planning, or until the user explicitly accepts unresolved questions as assumptions. If any required review is missing or pending, update the relevant review artifact instead of creating `execution-plan.md`.

Create:

`.ai/work/capabilities/<capability-slug>/execution-plan.md`

Use `.ai/templates/execution-plan.md` when available.

Produce:
- prerequisite review gate with artifact paths and statuses
- implementation approach
- likely files/services affected
- API/data changes
- UX changes
- test plan
- execution slices
- risks
- rollback/fallback notes if relevant

Publish:
- commit and push `execution-plan.md`
- update the draft PR / issue before implementation begins

Checkpoint B:
Request review from relevant professionals before coding.

## Phase 4 — Controlled execution

Implement in slices.

Before each slice:
- describe the slice
- list expected changes
- state risk level
- identify reviewer role needed

After each slice:
- create or update `checkpoint-00N.md`
- summarize changes
- list files changed
- explain decisions
- list tests/checks
- list incomplete parts
- request relevant review
- commit and push the slice changes and checkpoint artifact
- update the draft PR with the checkpoint summary path

Use `.ai/templates/checkpoint-summary.md` after each slice.

Stop for review before continuing if the slice affects:
- product behavior
- UX
- API/interface
- data model
- architecture
- security
- permissions
- performance
- release scope

## Phase 5 — Final review and acceptance

Produce:
- final PR summary
- acceptance criteria comparison
- test results
- known risks
- follow-up tasks
- release note draft

Publish:
- commit and push final review artifacts and any final code/doc changes
- update the PR description with acceptance status, tests, risks, and follow-ups

## Phase 6 — Context update

Use the Context Maintenance Skill to suggest updates to:
- `docs/ai-workflow.md`
- `docs/decisions.md`
- `docs/product-context.md`
- `docs/architecture.md`
- issue / PR description

Publish:
- commit and push `handoff-summary.md` and any accepted durable doc updates
- update the PR / issue with the final handoff path

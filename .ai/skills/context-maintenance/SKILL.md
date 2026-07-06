---
name: context-maintenance
description: Use at the end of meaningful work to update shared memory, decision logs, architecture notes, product context, PR summaries, and handoff summaries.
---

# Context Maintenance Skill

## Purpose

Use this skill to preserve important context without relying on long chat history.

The goal is to decide what should be saved and where.

## What belongs where

### `.ai/work/capabilities/<capability-slug>/`

Use for active capability-local artifacts:
- capability brief
- role reviews
- execution plan
- checkpoint summaries
- handoff summary

This is active task memory, not necessarily long-term project memory.

### `docs/decisions.md`

Use for meaningful decisions with long-term impact:
- product direction
- architecture choice
- API/data model decision
- major tradeoff
- scope decision
- security/performance decision

### `docs/product-context.md`

Use for stable product context:
- user personas
- product goals
- common user workflows
- product terminology
- persistent business constraints

### `docs/architecture.md`

Use for stable technical context:
- system structure
- services
- data flows
- APIs
- integration patterns
- technical constraints

### Issue / PR

Use for task-local context:
- acceptance criteria
- implementation details
- temporary assumptions
- test results
- follow-up tasks
- links or paths to capability artifacts
- checkpoint and handoff summaries

### Git / draft PR

Use for publishing shared artifacts:
- capability briefs
- role reviews
- execution plans
- checkpoint summaries
- handoff summaries
- accepted durable docs updates

Before publishing, run `git status --short`, stage only current-task files, commit, and push to a shared branch.

Do not stage unrelated dirty files.

Do not push directly to `main` unless explicitly instructed.

### Do not save

Do not save:
- random brainstorming
- outdated options
- very small implementation details
- personal opinions not accepted as decisions
- chat history dumps

## Decision log format

Use this format:

### YYYY-MM-DD — Decision title

Decision:
[What was decided]

Context:
[Why this came up]

Rationale:
[Why this option was chosen]

Alternatives considered:
[Short list]

Impact:
[Product/technical impact]

Follow-ups:
[Any needed actions]

## Final output

At the end of meaningful work, produce:

1. Suggested updates to `docs/decisions.md`
2. Suggested updates to `docs/product-context.md`
3. Suggested updates to `docs/architecture.md`
4. Suggested issue/PR update
5. Final handoff summary
6. Publishing status

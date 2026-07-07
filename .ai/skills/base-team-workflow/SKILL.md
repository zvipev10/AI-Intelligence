---
name: base-team-workflow
description: Use for every meaningful product, development, review, QA, documentation, or architecture task. Defines shared AI working rules, context loading, scope control, checkpointing, and handoff behavior.
---

# Base Team Workflow Skill

## Purpose

Use this skill for every meaningful task in this repository.

The goal is to make AI-assisted work:
- consistent
- context-aware
- token-efficient
- reviewable
- easy for another person or agent to continue

## Core principles

1. Shared context beats private chat memory.
   Important context should live in repo docs, issues, PRs, decision logs, and active capability artifacts.

2. Load only relevant context.
   Do not read the entire repository or all docs unless the task requires it.

3. Make assumptions explicit.
   If information is missing, state the assumption before continuing.

4. Keep scope focused.
   Do not expand the task without a clear reason.

5. Preserve decisions.
   If a meaningful product or technical decision is made, suggest an update to `docs/decisions.md`.

6. Produce handoff-ready output.
   Every meaningful session should end with a concise summary another person or AI session can use.

7. Use artifacts for handoff.
   Handoff between roles should happen through saved files, not through hidden chat history.

8. Publish shared artifacts.
   When an artifact is needed by another role, commit and push the intended artifact files so the handoff exists in repository state.

9. Status comes before detail.
   Every active capability must have a concise `status.md` that tells each role the current phase, who needs to act now, blockers, next artifact, and linked issues.

10. Issues track work; artifacts preserve context.
   Use GitHub/GitLab issues as Jira-like work items. Use one parent capability issue for overall coordination and one child issue for each actionable role task, review, implementation slice, QA validation, or handoff.

## Start-of-task flow

When starting:

1. Identify task type:
   - capability definition
   - product review
   - developer review
   - UX review
   - QA review
   - execution planning
   - implementation
   - bug investigation
   - architecture
   - review / QA
   - documentation
   - research / spike

2. Identify relevant context:
   - current request / issue / PR
   - parent capability issue and any active child task issue
   - `.ai/work/capabilities/<capability-slug>/status.md`
   - relevant skill file
   - relevant active capability artifact
   - relevant docs
   - relevant source files

3. Summarize understanding:
   - goal
   - current phase
   - active issue / task owner
   - current scope
   - non-goals
   - relevant constraints
   - open questions

4. Decide whether to continue:
   - If clear and low-risk, proceed.
   - If ambiguous or high-risk, propose assumptions or options before making changes.

## During work

- Keep changes focused.
- Prefer small, reviewable steps.
- Explain meaningful tradeoffs.
- Do not make unrelated changes.
- Track open questions and risks.
- Keep `status.md` current whenever ownership, phase, blockers, or next action changes.
- Keep parent and child issue references current in capability artifacts.
- Update tests, docs, or acceptance criteria when relevant.
- During definition/review phases, do not modify product code.
- Before publishing, run `git status --short`, stage only current-task files, and leave unrelated dirty files untouched.
- Prefer a draft PR for reviewable capability work.

## End-of-task output

End with:

1. What was done
2. What changed
3. Important decisions
4. Assumptions made
5. Remaining risks
6. Tests/checks performed
7. Publishing status
8. Suggested updates to shared docs
9. Handoff summary
10. Recommended next role/action
11. Issue updates needed or completed

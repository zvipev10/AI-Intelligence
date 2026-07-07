---
name: review-and-qa
description: Use for checkpoint review, PR review, QA planning, product acceptance validation, regression analysis, and final quality checks.
---

# Review and QA Skill

## Purpose

Use this skill to review partial or final AI-generated work.

The reviewer mindset is different from the builder mindset:
- look for gaps
- compare against requirements
- identify risks
- check tests
- prevent regressions
- decide whether work may continue

## Review inputs

Use the available:
- original request / issue / capability brief
- parent capability issue and active child task issue
- capability `status.md`
- role reviews
- execution plan
- checkpoint summary
- PR diff / changed files
- tests/checks
- relevant docs
- previous review comments

## Check dimensions

Review against:

1. Requirement match
   - Does the result satisfy the acceptance criteria?
   - Did behavior change beyond scope?

2. Product correctness
   - Is the user problem still solved?
   - Are non-goals respected?

3. Technical correctness
   - Does the implementation follow existing patterns?
   - Are APIs, data models, and state changes reasonable?

4. UX correctness
   - Are flows, states, copy, and errors handled?

5. QA/test coverage
   - Are happy path, edge cases, negative cases, and regressions covered?

6. Security and permissions
   - Any new access-control, sensitive data, injection, or privacy risk?

7. Performance/reliability
   - Any scalability, latency, caching, or failure-mode concern?

8. Maintainability
   - Is the change readable, focused, and easy to review?

## Output format

Separate findings into:

### Blocking issues
Must be fixed before continuing or merging.

### Non-blocking comments
Useful improvements but not required now.

### Missing tests
Tests that should be added or updated.

### Questions
Clarifications needed from product, dev, UX, QA, architecture, or security.

### Recommendation
Use one:
- continue
- continue after minor fixes
- pause for review
- request changes
- approve

Also state:
- next role that must act
- issue status change needed
- whether the active child issue can close
- whether the parent capability issue remains open

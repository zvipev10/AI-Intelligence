# Handoff

Deliverable: [proposed-plan.md](proposed-plan.md) with ordered steps, source touchpoints, acceptance checks, versioning policy, state isolation, activation/rollback and resource strategy. It implements the user's planning request, not application changes.

Next action: review #68. Confirm the operator-switching/preserve-state defaults and identify the Syria dataset/map/timeframe and new-feature list. Then create the formal execution plan and actionable slice issues under #67. Start implementation with a recoverable Kosovo baseline and configuration extraction; do not begin by cloning the application for Syria.

Publishing: all documents belong on codex/single-active-demo-plan in a draft PR. Parent #67 and review #68 remain open; no production acceptance claimed. No tests of product behavior run; source inspection and documentation checks only.

Documentation suggestions after design acceptance: add one-active-demo policy to docs/decisions.md; document manifest/state/activation contracts in docs/architecture.md; document supported demo profiles in docs/product-context.md; keep implementation/release evidence in this capability workspace. Do not rewrite general documentation while design is still under review.

# Checkpoint 017 — Exact investigation selection

## Checkpoint status

Implemented, published, and deployed; pending Product/UX hands-on acceptance.

## Handoff

Next role: Product/UX reviewer.

Required action: verify that opening the investigation selector shows the full
list, exactly one row is marked active, and selecting another investigation
loads only that investigation's workspace.

Deployment was explicitly authorized by the user on 2026-08-04 and completed
from commit `c473a9787baa22a583cbf1e69243a9e33c949204`.

## Slice goal

Make “active” mean the currently selected investigation while keeping every
other investigation available in the list and making selection an exact
underlying context switch.

## What changed

- Separated the investigation search query from the active investigation name.
- Opening the selector now starts from the complete investigation list.
- Typing still filters the list and focuses/selects the existing name for replacement.
- Explicit selection loads exact investigation-scoped workstreams and memory.
- The legacy latest-investigation fallback is restricted to initial bootstrap.
- Stale workstream responses are ignored after the user selects another investigation.

## Files changed

- `llm_investigation_orchestrator_serbia_poc/app.js`
- `llm_investigation_orchestrator_serbia_poc/test_workstream_ui.py`
- `.ai/work/capabilities/shared-evidence-assessment/investigation-selection-execution-plan.md`
- `.ai/work/capabilities/shared-evidence-assessment/decisions.md`
- `.ai/work/capabilities/shared-evidence-assessment/status.md`
- `.ai/work/capabilities/shared-evidence-assessment/handoff-summary.md`
- `.ai/work/capabilities/shared-evidence-assessment/checkpoint-017.md`

## Decisions made

- Investigation selection remains browser-persisted for this POC.
- No backend investigation registry was added.
- Empty explicitly selected investigations remain empty and never adopt another investigation's workstreams.
- Bootstrap retains the legacy latest fallback to avoid breaking existing desktop continuity.

## Tests/checks run

- `node --check app.js`: passed.
- `python -m unittest test_workstream_ui test_workstreams test_scenario_playback`: 45 passed.
- Full Python discovery: 113 passed.
- Python compilation: passed.
- `git diff --check`: passed.
- Public `app.js?v=131` SHA-256 matched the committed/deployed file:
  `6d43ca9e230db931eef11be14caaf1e870498997e4cb249932d70fbe024bdfe1`.
- Public `/api/status`: Hermes configured, V2.1, 14,800 rows.
- `serbia-poc-ui.service`, `hermes-gateway.service`, and
  `hermes-moshe-gateway.service`: active after deployment.
- `/api/live-steps`: returned valid JSON.

## Not completed yet

- Product/UX hands-on interaction validation.
- Automated in-app browser validation could not bypass the VM's self-signed
  certificate; public endpoint and asset checks passed through `curl`.

## Risks

- The investigation registry remains local to the browser.
- Bootstrap fallback behavior still exists intentionally and should be removed if server-owned investigation persistence is introduced.

## Continue / pause recommendation

Pause for Product/UX hands-on acceptance before merging PR #47. Deployment is
complete and recoverable from
`/opt/serbia-poc-ui/deploy-backups/app.js.before-c473a97`.

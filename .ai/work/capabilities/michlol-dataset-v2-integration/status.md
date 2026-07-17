# Capability Status

## Capability

Integrate `מכלול` team-management UI with Serbian intelligence dataset v2 runtime.

## Current phase

Integration merge prepared locally; validation and publishing in progress.

## Overall status

In progress.

## Who needs to act now

| Role | Status | Required action | Due before |
|---|---|---|---|
| Development | In progress | Merge both branches, preserve both feature sets, validate, publish integration branch. | Current task |
| Product/UX/QA | Pending | Review combined branch after publishing. | Before deployment/merge |

## Latest change

Created integration branch `codex/integrate-michlol-dataset-v2` from `codex/michlol-team-management` and merged `origin/codex/serbian-intelligence-dataset-v2`.

## Current blockers

No blocking merge conflicts remain.

## Current risks

- Python syntax validation is blocked in this shell because only Windows App Execution Alias stubs for `python`/`python3` are available.
- The merged branch still needs deployment review before it should replace either existing deployed runtime.

## Next expected artifact

`checkpoint-001.md`


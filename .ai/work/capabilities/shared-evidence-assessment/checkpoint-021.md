# Checkpoint 021 — Global playback workstream reevaluation

## Outcome

Moshe playback reevaluation now discovers every active workstream in the run's
locale, regardless of which investigation originally started the global run.
Each workstream context is loaded with that workstream's own investigation ID.

The active-workstream gate uses the same global discovery rule, so pressing Next
from one investigation cannot incorrectly report that no workstreams exist when
an active workstream belongs to another investigation.

## Validation

- Cross-investigation focused playback tests: 2 passed.
- Full Python discovery: 135 tests passed.
- Python compilation and `git diff --check` passed.
- Production confirmed an active workstream in `NATO involvement 2` while the
  global run retained its original ID.
- Playback was reset to stage index 0, revision 9, with the initial visible
  timeframe ending at `2026-09-17T06:00:00Z`.
- UI and both Hermes gateway services were active.

## Recovery

Rollback backup:
`/home/ubuntu/deploy-backups/global-workstream-playback-20260811T174028Z`.

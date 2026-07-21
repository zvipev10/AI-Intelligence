# Checkpoint Summary

## Checkpoint

008 - Slice 6 quality recovery implementation and full rerun

## Status

Approved by the user, deployed, and verified; all approved quality gates pass.

## Authorized change

The user approved improving `prepare_target_candidate` as one Moshe-facing fusion tool and requested a repeat of the full evaluation.

## Implementation

- `prepare_target_candidate` now starts from seed evidence and retrieves compatible public records from a bounded same-location/entity context.
- Object-class aliases cover the seven approved target classes and visible paraphrases.
- Quantity, temporal distance, source type, source independence, repost similarity, and explicit contradiction signals contribute to deterministic selection.
- Public evidence pairs are ranked with component reasons and scores.
- A pair must lead competing visible UAV anchors by at least 0.5 score points.
- The winning pair must also lead the next pair by at least 0.5; otherwise the result is ambiguous and report-only.
- `create_target_candidate` remains unchanged and independently reruns the final persistence validation before writing SQLite.
- The release runtime now calls `prepare_target_candidate` directly rather than implementing a separate lexical fusion path.

## Full isolated evaluation

The public-data-only runtime processed all 3,800 UAV anchors across 14,800 V2.1 rows in 6.101 seconds. The root-only evaluator then scored all 300 positive chains and 100 hard negatives.

| Metric | Baseline | Recovery | Required | Result |
|---|---:|---:|---:|---|
| Chain recall | 8.00% | 93.67% | at least 90% | Pass |
| Evidence precision | 49.27% | 92.10% | at least 90% | Pass |
| Evidence recall | 11.22% | 95.89% | at least 90% | Pass |
| Hard-negative rejection | 99.00% | 100.00% | at least 95% | Pass |
| False-merge rate | 8.75% | 1.27% | at most 5% | Pass |
| Duplicate-target rate | 0.00% | 0.00% | at most 2% | Pass |
| Source independence | 100.00% | 100.00% | 100% | Pass |

Machine-readable aggregate result: `evaluation-008-quality-recovery.json`.

## Regression and operational checks

- 25 MCP fusion, target-bank, and security-boundary tests pass on Linux.
- 28 shared result, routing, member UI, and Moshe-profile tests pass on Linux.
- JavaScript syntax passes.
- Runtime deployment scans found no evaluator/truth files under `/opt/serbia-poc` or `/opt/serbia-poc-ui`.
- UI, General, and Moshe services remain active.
- Production SQLite was not used by the evaluation and remains integrity `ok` with 3 targets and 14 evidence links.
- Post-run available VM memory was approximately 252 MB.

## QA review

### Blocking issues

None against the approved Slice 6 quantitative gates.

### Non-blocking risks

- Four predicted candidates still contained evidence owned by more than one evaluator chain, but the 1.27% aggregate rate is below the approved 5% ceiling.
- The alias taxonomy is intentionally limited to the seven V2.1 target classes and will require extension when the product scope expands.

### Recommendation

Checkpoint 008 was approved and deployed on 2026-07-21.

## Production deployment

- Code backup: `/opt/serbia-poc-backups/moshe-quality-20260721T034228Z`.
- SQLite backup: `/opt/serbia-poc/backups/attack_targets/attack_targets-pre-quality-20260721T034228Z.db`.
- Deployed only `mcp_server/server.py` and `mcp_server/fusion_tools.py`.
- Restarted General and Moshe gateways; UI, General, and Moshe are active with zero failure restarts.
- A direct read-only `prepare_target_candidate` smoke test selected three evidence records, returned persistence eligibility, pair score, and ambiguity data, and performed no SQLite write.
- Post-deployment V2.1 status reports 14,800 rows.
- SQLite integrity remains `ok` with the original 3 targets and 14 evidence links.
- Runtime truth/evaluator scan remains zero.
- Post-deployment available memory was approximately 305 MB.

## Next action

Proceed with final Slice 7 acceptance and handoff review.

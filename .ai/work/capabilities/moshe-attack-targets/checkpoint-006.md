# Checkpoint Summary

## Checkpoint

006 - Slice 6 evaluation start and VM resource incident

## Checkpoint status

Completed with failed QA gates; development changes required

## Authorization

The user approved proceeding with Slice 6 and accepted the proposed quantitative thresholds on 2026-07-19.

## Completed before the incident

- Confirmed the repository's existing evaluator covers only a configurable semantic smoke sample and is not the approved 300-positive/100-negative release suite.
- Confirmed V2.1 contains 300 positive chains, 900 positive evidence records, and 100 hard negatives.
- Audited evaluator isolation on the VM.
- Found four legacy evaluator-label files in runtime trees. They were moved recoverably to root-only quarantine `/root/moshe-evaluator-quarantine-20260719T203803Z`.
- Verified no evaluator/truth-named files remained in `/opt/serbia-poc` or `/opt/serbia-poc-ui` immediately after quarantine.
- Started a public-data-only runtime discovery phase over all 3,800 UAV anchors. It did not read evaluator labels or fusion truth.

## Incident

The hybrid dense semantic index build exceeded safe capacity on the 954 MB VM. Before connectivity was lost, the evaluation process reached approximately 559 MB RSS, available RAM fell to approximately 58 MB, and free swap fell to approximately 308 MB. UI, General, and Moshe still reported active with zero restarts at the last successful check.

SSH subsequently stopped completing banner exchange and the application port stopped responding. Multiple kill-only SSH attempts could not connect. No further workload was started.

The dense attempt produced no valid metrics. It was superseded by the resource-bounded full runs below.

## Recovery verification

The VM was rebooted and recovered successfully on 2026-07-20. UI, General, and Moshe services were active with zero restarts; V2.1 status returned 14,800 rows; swap was clear after boot; the failed dense process was absent; and evaluator quarantine remained intact.

## Resource-bounded full evaluation

The complete suite was rerun with a public-data-only lexical runtime followed by the root-only evaluator. The runtime examined all 3,800 UAV anchors. Evaluator artifacts were unreadable by the runtime user and remained absent from `/opt/serbia-poc` and `/opt/serbia-poc-ui`.

First complete run:

- Predicted candidates: 1,863.
- Chain recall: 0.67%.
- Evidence precision: 8.25%.
- Evidence recall: 29.89%.
- Hard-negative rejection: 99%.
- False-merge rate: 0.43%.
- Duplicate-target rate: 0%.
- Source-independence deterministic pass: 100%.

Failure category: broad lexical selection over-generated candidates and selected unrelated public reports.

The permitted runtime-only correction added visible object-class cue matching and required two distinct corroborating public source types. The entire suite was then repeated.

Final repeated run:

- Positive chains evaluated: 300.
- Hard negatives evaluated: 100.
- Predicted candidates: 80.
- Matched chains: 24.
- Chain recall: 8% (required at least 90%) — fail.
- Evidence precision: 49.27% (required at least 90%) — fail.
- Evidence recall: 11.22% (required at least 90%) — fail.
- Hard-negative rejection: 99% (required at least 95%) — pass.
- False-merge rate: 8.75% (required at most 5%) — fail.
- Duplicate-target rate: 0% (required at most 2%) — pass.
- Source-independence: 100% — pass.
- Evaluator-truth leakage: zero — pass.

Exact machine-readable results: `evaluation-006.json`.

## Regression and operations

- 37 shared result, member UI, routing, fusion, and target-bank tests pass on Linux.
- JavaScript syntax passes.
- UI, General, and Moshe services remained active during the lexical runs.
- Post-run available RAM was approximately 471 MB with approximately 1.69 GB free swap.
- The production target bank remained unchanged.

## QA findings

### Blocking issues

- Candidate discovery misses most true cross-source chains.
- Evidence selection cannot reliably choose the two corroborating public records from the retrieved neighborhood.
- Object-cue filtering reduces over-generation but increases missed chains and still exceeds the false-merge ceiling.

### Non-blocking comments

- Resource-bounded lexical evaluation is viable on the current VM.
- Hard-negative rejection, duplicate prevention, source grouping, evaluator isolation, and General regressions are currently acceptable.

### Missing tests

- Add focused development fixtures for semantic synonym matching and evidence-pair ranking before repeating the full suite.
- Add false-merge fixtures where multiple potential chains share entity, canonical area, and time window.

### Recommendation

Request changes. Do not proceed to Slice 7. Development should implement a reviewed evidence-pair ranking/disambiguation change without using evaluator-only fields, then rerun all 400 cases.

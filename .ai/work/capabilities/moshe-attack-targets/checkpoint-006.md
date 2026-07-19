# Checkpoint Summary

## Checkpoint

006 - Slice 6 evaluation start and VM resource incident

## Checkpoint status

Blocked pending VM recovery; no evaluation acceptance result

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

## Evaluation result

No valid metrics were produced. The 400-case threshold gate remains untested and must not be marked pass or fail.

## Recovery and next run

1. Restore VM responsiveness through the infrastructure console or wait for the low-priority evaluation process to exit or be reclaimed.
2. Kill `/tmp/moshe-slice6-runtime.py` if it is still running.
3. Verify all three services and the application endpoint.
4. Preserve the root-only evaluator quarantine; do not restore evaluator files into runtime trees.
5. Rerun the complete suite with a resource-bounded lexical/disk-streaming runtime, not the hybrid dense index on this VM.
6. Record all 300 positive and 100 hard-negative metrics before QA acceptance.

## Recommendation

Pause Slice 6 until VM health is restored. The active Slice 6 child issue remains open, and the parent capability remains open.

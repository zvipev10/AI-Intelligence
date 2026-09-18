# Checkpoint 001 — movement scenario and evidence

## Implemented

- Added three time-ordered KSF convoy UAV observations across LOC-V2-013, LOC-V2-009, and LOC-V2-010.
- Added two independently grouped public corroborations at each point.
- Preserved the analytical limitation that the evidence supports force-pattern movement, not continuous identification of one exact convoy.
- Regenerated all derived V2.1 artifacts and the deployment evidence catalog.
- Added integration tests for the route sequence and fused evidence at every point.

## Resulting scenario records

- LOC-V2-013: REC-V2-014801 through REC-V2-014803
- LOC-V2-009: REC-V2-014804 through REC-V2-014806
- LOC-V2-010: REC-V2-014807 through REC-V2-014809

## Resulting fused evidence

- LOC-V2-013: EVD-FUSED-07DEA71F88095F86200B
- LOC-V2-009: EVD-FUSED-C6F1AAB907109BE558A4
- LOC-V2-010: EVD-FUSED-087F28DD62B6E4E1DCFE

## Validation

- Deterministic V2.1 regeneration: passed.
- Dataset validation: 14,809 rows, 3,803 UAV rows, 9 movement-demo rows, immutable V2 unchanged.
- Evidence catalog: 14,809 source records, 785 fused objects.
- Movement and evidence-catalog tests: 8 passed.
- Evidence foundation tests: 10 passed.
- Assessment-store tests: 7 passed.

## Review

No blocking local findings. Deployment and a real Talia run remain required before final acceptance.

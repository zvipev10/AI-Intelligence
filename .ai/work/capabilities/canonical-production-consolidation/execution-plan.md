# Execution Plan

1. Promote all 11 captured v162 source files mechanically into the package
   root and verify their hashes.
2. Replace the duplicate snapshot directory with a retained checksum manifest
   and documentation identifying the package root as canonical.
3. Run the complete validation suite and update only obsolete tests.
4. Record the checkpoint and handoff, review the final diff, then publish to
   remote `main` without deploying.

Rollback is Git revert of the consolidation commit. Production is unaffected.

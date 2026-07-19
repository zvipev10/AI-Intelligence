# [Developer Review] Moshe SQLite Schema and Tool Contract

## Purpose

Review the approved minimal target-bank schema against existing persistence, MCP tool, and layer API patterns.

## Required action

Inspect the repository and produce `developer-review.md` covering feasibility, affected files, schema constraints, tool boundaries, risks, tests, and proposed execution slices. Do not implement product code.

## Owner role

Development

## Inputs

- `capability-brief.md`
- `chapter-001-target-bank-schema.md`
- V2.1 handoff and production checkpoint

## Expected output

Developer review ready for human approval and the schema/tool-contract checkpoint.

## Blocking

Blocks execution planning and global target-bank writes.

## Completion criteria

- [x] Chapter 1 SQLite persistence baseline approved by Development.
- [x] Candidate and human-review responsibility boundary approved.
- [x] Existing location/entity reference approach approved.
- [ ] Exact DDL and initialization approach to be inspected before coding.
- [ ] Evaluator-truth isolation requires architecture/security review.
- [ ] Test strategy and execution slices require QA and execution planning.

## Related artifacts

- `.ai/work/capabilities/moshe-attack-targets/chapter-001-target-bank-schema.md`
- `.ai/work/capabilities/moshe-attack-targets/status.md`

## Parent capability

Moshe Attack Targets MVP; remote parent issue pending.

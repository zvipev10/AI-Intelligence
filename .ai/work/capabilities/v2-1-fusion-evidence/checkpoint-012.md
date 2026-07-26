# Checkpoint 012 — Readable Moshe tool summaries

Date: 2026-07-23

## Approved behavior

- Moshe uses the same shared activity cards as the General Agent.
- Target tools receive concise, tool-specific Hebrew labels, actions, decisions, and result summaries.
- Visible summaries keep relevant identifiers from the result, including target, record/event, location, entity, and mission identifiers.
- Identifier lists follow the existing General Agent bound: show up to 14, then report the remaining count.
- Complete structured targets remain available through the target layer; complete tool payloads remain in the audit record.

## Tools covered

- `prepare_target_candidate`
- `find_duplicate_target_candidates`
- `search_target_candidates`
- `get_target_candidate`
- `create_target_candidate`
- `update_target_candidate`
- `attach_target_evidence`

## Validation

- JavaScript syntax passed on the deployment VM.
- UI and result-pipeline suite: 25 tests passed.
- Regression tests prove oversized descriptions are omitted, summaries are bounded, and identifiers remain visible.
- Replayed the current production Moshe audit through the new summarizer:
  - previous raw target results were approximately 2,500–4,300 characters;
  - new visible target summaries are 47–204 characters;
  - success and error summaries retain the relevant `TGT-*`, `REC-*`, location, entity, and mission identifiers.

## Evidence limit

The embedded audit browser could not reach the VM, so screenshot-backed visual review was not completed. Validation covers the deployed rendering contract, code path, and current production audit payloads.

## Deployment result

- Deployed to the VM on 2026-07-23 after backing up the prior UI server and client files.
- UI, General gateway, and Moshe gateway are active; both gateway health endpoints returned `status: ok`.
- The deployed formatter replayed the current Moshe audit with target summaries bounded to 47–204 characters and identifiers retained.
- UI restart count is 0. Post-deployment resources: 309 MB available memory and 684 MB swap used.

# Checkpoint 013 — Final validation with REC-V2-007215

## Outcome

The deployed Moshe-to-workstream flow passed final validation with the historical
record `REC-V2-007215`.

The validation created an isolated workstream, exercised proposal and
confirmation as separate natural-language turns, verified durable persistence
after a UI-service restart, confirmed that the target bank was not mutated, and
archived the validation workstream after reopening it successfully.

## Deployed validation fixture

- Investigation: `investigation-final-validation-rec-v2-007215-20260728`
- Workstream: `ws_20260728_042407_9611560e`
- Artifact: `artifact_20260728_043813_63f95380`
- Final workstream status: `archived`
- Artifact revision: `1`
- Confirmation turn: `validation-moshe-confirm-turn-3`

## Moshe assessment

Moshe treated `REC-V2-007215` as a proposed indication, not as a target and not
as an automatically persisted artifact.

The proposal described possible KSF engineering, earthwork, or fortification
activity around `LOC-V2-003` and included:

- anchor evidence: `REC-V2-007215`, Serbian UAV video, medium identification
  and geolocation confidence, approximately 15 observed items;
- public-source corroboration: `REC-V2-008675`;
- weaker social-source corroboration: `REC-V2-013323`;
- explicit uncertainty around direction, exact location, object
  classification, count, attribution, and source independence;
- five questions for human assessment before any later target decision.

## Human-decision boundary evidence

1. The proposal turn called `prepare_workstream_indication_proposal`.
2. The proposal result reported `persisted: false`.
3. The workstream artifact list remained empty after the proposal turn.
4. A separate later user turn explicitly approved saving the proposal.
5. The confirmation turn called `decide_workstream_indication_proposal`.
6. The app server created exactly one `target_assessment_lead` artifact at
   revision 1.
7. A deliberately mismatched investigation context produced clarification and
   no persistence, demonstrating that browser-supplied context is not trusted
   across investigations.

Rejection, correction, stale-revision conflict, and duplicate-write boundaries
remain covered by the automated artifact, result-pipeline, routing, and UI
tests.

## Target-bank safety

The target-bank SHA-256 was captured before the proposal, after the proposal,
after confirmation, after service restart, and after archival:

`418e75fbf00760a20002456168cc2768e3c55b579764330ec02e1d4d4481fd79`

The hash did not change. The workstream artifact contains `REC` evidence
references only; no `TGT` identifier was used as evidence and no target-bank
write occurred.

## Restart and reopen

- `serbia-poc-ui.service` was restarted after persistence.
- The workstream reopened with the same artifact ID, three indications, and
  revision 1.
- The validation workstream was then archived.
- The archived workstream reopened with its artifact intact.
- `serbia-poc-ui.service` and `hermes-moshe-gateway.service` were both active at
  completion.

## Automated validation

- 78 non-profile tests passed.
- 7 Moshe profile tests passed after providing PyYAML in an isolated temporary
  test dependency directory.
- Total: 85 tests passed.
- The initial combined run's only error was the local runtime's missing
  `yaml` package; it was not a product failure.

## Harness observations

- A first validation request used a corrupted Hebrew mention and therefore
  routed to the general investigator.
- A first confirmation attempt used a suffixed investigation ID, so the server
  correctly removed the untrusted workstream context and Moshe requested
  clarification.
- Both harness issues were corrected with encoding-safe payloads and the exact
  server-owned investigation ID.

These observations confirm the intended routing and investigation-scoping
guards. They did not create artifacts or mutate the target bank.

## Release recommendation

Approve the Phase 1 MVP for the demonstrated boundary.

The principal operational risk is response latency: the full proposal run took
roughly two minutes and the confirmation run roughly one minute. This does not
affect persistence correctness, but progress and timeout handling should remain
visible in the demo.

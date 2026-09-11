# Handoff

Prepared a draft capability brief for raw-record, organization, and target viewers opened from map, grid, or the general assistant. Proposed source presentations include UAV video when playable assets exist, with text preserved in all states.

Inspected canonical source, current map/table rendering, resolution/visibility helpers, and sample dataset fields. No implementation, application tests, deployment, or human approval occurred. Documentation checks: diff whitespace and intended-file scope.

Next action: user/product reviews the concrete proposal; required role inputs precede execution planning under `.ai/skills/end-to-end-feature-delivery/SKILL.md`. Main uncertainties are playable media delivery, public organization details, and viewer UX. All proposed choices remain recommendations.

Parent #48 and review task #49 remain open. Publish these three capability artifacts on `capability/record-knowledge-viewers` and a draft PR. No unrelated files belong to this change.

Suggested durable updates after decisions are approved: describe the viewer workflow in `docs/product-context.md`, detail/media/assistant contracts in `docs/architecture.md`, and accepted interaction/media decisions in `docs/decisions.md`. No durable decision was invented or recorded as accepted in this phase.

User clarification: open only for a single object. Removed the grouped-marker chooser from scope and acceptance criteria. Existing grouped-marker behavior is preserved. This clarification does not approve the remaining draft layout or delegate role-review decisions.

The user subsequently approved the revised scope and explicitly delegated the complete implementation and approval flow. Record and organization viewers are implemented; targets remain excluded. The implementation uses visibility-scoped client layer rows, adds no endpoint or dependency, renders allowlisted media URLs when present, and preserves text with an unavailable state when absent. Automated acceptance: 58 tests plus JavaScript syntax and diff checks passed. See `checkpoint-001.md`.

VM deployment completed on 2026-09-09. The public endpoint serves `app.js?v=171` and `styles.css?v=142` over HTTP 200; the UI and both gateway services are active. Rollback backup: `/home/ubuntu/deploy-backups/record-organization-viewer-20260909T232844Z`.

On 2026-09-11 the viewer was refined locally into a compact edge drawer: left in Hebrew/RTL and right in English/LTR. UAV records now render a dedicated source-material block with mission and segment context, making explicit that footage belongs to the collection mission and may support multiple analytical records. Valid allowlisted media URLs still play; absent URLs show a designed disconnected state because the repository has no genuine UAV video asset. JavaScript syntax and diff checks pass. Python and automated browser QA were unavailable on this host. See `checkpoint-002.md`; this refinement has not been deployed.

The refinement was subsequently merged and pushed to remote `main` at `4688544`, then deployed to `/opt/serbia-poc-ui`. Production hashes match `SHA256SUMS-v182.txt`, public HTTP serves `app.js?v=179` and `styles.css?v=148`, all three services are active, and the status API still reports V2.1 with 14,800 rows. Rollback: `/home/ubuntu/deploy-backups/viewer-side-drawer-4688544`.

On 2026-09-11 a screenshot-led follow-up removed the duplicate event narrative from the header and added an automatically playing simulated UAV mission stream for every UAV record. The canvas feed is deterministic by mission, restarts per open, stops on close, and is explicitly labelled as simulation rather than authentic operational evidence. See `checkpoint-003.md`.

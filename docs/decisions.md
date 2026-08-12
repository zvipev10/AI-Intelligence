# Decision Log

Use this file for durable product and technical decisions.

## Format

### YYYY-MM-DD — Decision title

Decision:
[What was decided]

Context:
[Why this came up]

Rationale:
[Why this option was chosen]

Alternatives considered:
[Short list]

Impact:
[Product/technical impact]

Follow-ups:
[Any needed actions]

### 2026-07-18 - Preserve V2 and add evaluator-grounded V2.1 fusion evidence

Decision:
Keep V1 and deployed V2 immutable. Create V2.1 from V2 with intentional cross-source shared-object evidence chains and evaluator-only truth labels.

Context:
V2 public and UAV records were sampled independently. They were aligned to the same scenario but could not reliably prove that two sources described the same physical object, which made Moshe fusion evaluation depend on accidental correlations.

Rationale:
A small version increment preserves reproducibility and rollback while providing measurable positive and negative cases. Evaluator truth remains outside raw and runtime projection data so the investigating agent cannot use it.

Alternatives considered:
Overwrite V2; infer truth from accidental V2 correlations; create an entirely unrelated dataset.

Impact:
V2.1 contains 300 positive cross-source chains and 100 hard negatives at the existing 14,800-record scale. Runtime selection is optional; production remains on V2 until separately released.

Follow-ups:
Use V2.1 to implement and evaluate Moshe, the global `attack targets` layer, duplicate detection, source-independence rules, and human approval.

### 2026-07-28 — Define playback scenarios as scoped timeframe stages

Decision:
Represent a reusable historical playback scenario as identity/version metadata,
one data scope, and an ordered list of stages with inclusive `from` and
exclusive `to` timestamps. Keep record IDs, targets, assignments, agent state,
and transition history outside the scenario artifact.

Context:
The initial playback design placed responsibilities, released references, and
other runtime concerns in the manifest. Product proposed that a list of
time-bounded stages was sufficient and explicitly approved the simplified
design.

Rationale:
Time windows describe when scenario information becomes visible without
coupling the platform contract to a particular record sequence. Runtime and
collaboration state evolve independently and belong in persistent run and
workstream models.

Alternatives considered:
- Embed record IDs in each stage.
- Put assignments and decisions in the scenario manifest.
- Encode a domain-specific target assessment sequence.

Impact:
Manifests are strict and reject unsupported fields. Playback visibility is
cumulative, stages may contain gaps but cannot overlap, and any historical
fixture can change its records without changing platform code.

Follow-ups:
Implement retrieval visibility enforcement before exposing playback controls,
then add UI and automatic agent reevaluation in separately approved slices.

### 2026-08-08 — Isolate mutable target persistence by locale

Decision:
Use separate Hebrew and English SQLite target-bank instances. Initialize both active databases empty without migrating the former shared targets. Route every target create, update, evidence attachment, read, backup, reset, and restore by normalized locale. Reject Hebrew characters in English persisted presentation and evidence fields.

Context:
The English UI could expose Hebrew target content because both locales shared one mutable target database even after immutable English projections were corrected.

Rationale:
Physical separation matches the raw-data locale model, prevents cross-locale reads and writes by construction, and gives each language an independent lifecycle. Empty initialization follows the approved product requirement and avoids carrying mixed or ambiguous legacy records forward.

Alternatives considered:
- Keep one database with a locale column.
- Migrate existing shared records into Hebrew.
- Translate or copy shared records into English.

Impact:
Hebrew remains the default for omitted locale values, while explicit English operations use only the English database. Future English writes fail atomically if protected text contains Hebrew. The former shared database is rollback-only and is no longer active.

Follow-ups:
Apply the same explicit locale-ownership review to remaining mutable stores and finish full bilingual runtime acceptance.

### 2026-08-08 — Select one complete MCP runtime per locale

Decision:
Represent each supported locale and dataset version as a complete, manifest-validated MCP runtime containing its event, location, entity, fusion, presentation, and semantic state. Select that runtime once at the tool-call boundary. English asset failures must fail closed and must not fall back to Hebrew.

Context:
The English UI used clean projections while MCP tools remained bound to Hebrew module globals and a shared semantic cache.

Rationale:
Selecting a complete runtime prevents mixed-locale results and cache contamination while preserving existing tool implementations through locale-dispatching containers. Manifest checks make source paths, checksums, and cache identity auditable.

Alternatives considered:
- Translate individual MCP results after retrieval.
- Run entirely separate MCP processes per locale.
- Continue adding parallel English globals.

Impact:
Hebrew remains the compatibility default. English calls use only validated English sources, generated payload text is checked for Hebrew, and semantic cache identity includes locale, dataset version, and source checksums. Production semantic caches should be prebuilt off-host for the current low-memory VM.

Follow-ups:
Recover the VM, upload the prebuilt English v2.1 cache, complete production semantic acceptance, and apply locale ownership to workstream persistence.

### 2026-08-08 — Isolate workstream persistence and flows by locale

Decision:
Use separate Hebrew and English workstream roots for each dataset state. New v2.1 workstreams persist under `workstreams/v2_1/he/` or `workstreams/v2_1/en/`; legacy untagged/shared workstream files are treated as Hebrew-owned fallback data only. Route workstream list, get, create, update, archive, artifacts, presentation, chat actions, and playback reevaluation by normalized locale. Reject Hebrew characters in English persisted user-visible workstream and artifact fields.

Context:
After the immutable English dataset and MCP runtime were corrected, mutable workstream state could still mix Hebrew and English because both languages shared the same workstream files and runtime routes.

Rationale:
Physical separation prevents accidental cross-language reads and writes by construction, preserves Hebrew compatibility for existing records, and starts English workstreams cleanly without migration or automatic translation. Atomic English write validation protects future creation and updates from reintroducing Hebrew text.

Alternatives considered:
- Keep one workstream store with a `locale` field.
- Migrate existing shared workstreams into the new Hebrew root.
- Translate or copy Hebrew workstreams into English.

Impact:
Hebrew remains the compatibility default for omitted locale values. English workstreams start empty and can only be populated through explicit English flows. Cross-locale workstream IDs are not visible through list/get APIs.

Follow-ups:
Deploy the workstream slice to production and run bilingual smoke tests for physical-store separation, English rejection, and playback locale routing.

### 2026-08-08 — Use one staged playback flow with cumulative visible timeframe

Decision:
Remove the user-facing distinction between historical and real-time playback modes. Use one staged playback flow where the initial baseline exposes data from the dataset beginning through the first slice boundary, and subsequent Next actions extend the cumulative `visible_timeframe`. Moshe reevaluation is skipped for baseline creation and can run only after a later slice releases new data and active workstreams exist.

Context:
The historical mode and real-time mode created confusing UX and different mental models. Product wanted the initial state to behave like historical today while keeping staged progression and future reevaluation behavior.

Rationale:
A large initial slice preserves the analyst's ability to ask broad historical questions at the beginning of a scenario while keeping one consistent playback mechanism for UI, MCP, and data-layer visibility. Deferring Moshe until the next slice prevents an unnecessary reevaluation of the baseline state.

Alternatives considered:
- Keep separate historical and real-time modes.
- Start real-time playback only at the first narrow scenario slice.
- Trigger Moshe immediately when the baseline is created.

Impact:
Playback controls show timeframe and Next without a mode selector. UI/data-layer rows and MCP tools must respect the active `visible_timeframe`. Existing API clients that send `mode: "historical"` are treated as compatibility callers and routed to the staged flow.

Follow-ups:
Run production smoke with active playback visibility restoration, then complete UX acceptance for the simplified staged control.

### 2026-08-09 — Create workstreams from verified evidence without redundant metadata questions

Decision:
When a user explicitly requests a workstream from supplied `TGT-*` or `REC-*` identifiers, Moshe
resolves the identifiers first and infers the title, objective, and responsibility whenever the
evidence supports them. Resolved existing targets persist as root-level `target_ids`. Verified raw
records persist as indications in one initial `target_assessment_lead` artifact. Ordinary creation
does not authorize creating or updating a target candidate.

Context:
The previous creation flow asked users for metadata that could be derived from the referenced data,
and early simplification versions used targets and records only as transient inference context.

Rationale:
The workstream must retain the objects that motivated its creation. Targets are durable subjects of
the workstream, while raw records are evidence and therefore belong in an assessment artifact.
Keeping target persistence authorization separate preserves the existing safety boundary.

Alternatives considered:
- Require users to supply title, objective, and responsibility.
- Store raw records directly on the workstream root.
- Automatically create a new target candidate from raw records.

Impact:
Target-backed and record-backed workstreams can be created in one turn in Hebrew and English. Low
confidence or missing corroboration may limit target persistence but does not block an explicitly
requested evidence-tracking workstream.

Follow-ups:
If multi-target assessment is needed later, revisit the current single-active-artifact-per-type rule.

### 2026-08-11 — Keep staged playback global across investigations

Decision:
Use one active staged playback run for the deployed UI/MCP process. Changing the
selected investigation changes investigation context but does not select, create,
or advance a separate scenario run. Playback status, mode changes, reset, and Next
all resolve the same active global run.

Context:
Playback visibility was global, but the status and Next endpoints looked up runs by
the selected investigation. After switching investigations, the UI showed the global
Next control while the server attempted to create a second run and returned
`Another scenario run is already active`.

Rationale:
One global scenario clock ensures every investigation sees the same released evidence
window and makes the Next control consistent with the existing global retrieval boundary.

Alternatives considered:
- Maintain a separate playback run and visibility boundary per investigation.
- Hide Next outside the investigation that originally started playback.

Impact:
Switching investigations preserves the active run ID, revision, stage, and timeframe.
Pressing Next from any investigation advances that run once and cannot create a second run.

Follow-ups:
Retain automated coverage for switching investigations before reading status, changing
mode, or pressing Next.

### 2026-08-12 — Track the deployed production variant as an immutable source snapshot

Decision:
Store the exact non-secret source files deployed at `/opt/serbia-poc-ui` under
`llm_investigation_orchestrator_serbia_poc/deployment/vm-production-v162/`,
with SHA-256 hashes and Git text conversion disabled. Keep the canonical package
root unchanged until the two variants are deliberately consolidated.

Context:
The active VM served `app.js?v=162`, but its complete source state was not
reproducible from remote `main`. Copying that state directly over the canonical
package broke the existing regression contract.

Rationale:
An exact, hash-pinned snapshot makes the deployed state auditable immediately
without changing production or silently replacing the canonical implementation.

Alternatives considered:
- Overwrite the canonical package with the VM files.
- Leave the VM-only changes untracked.
- Reconstruct production from selected historical commits.

Impact:
Remote Git can reproduce and review the current production source while the VM
remains untouched. Two source trees temporarily exist and their roles are
explicit: the package root is canonical development code; the deployment
snapshot is the authoritative record of production v162.

Follow-ups:
Consolidate the variants through a separately reviewed capability, and require
future deployments to update the versioned snapshot and hashes in the same
change.

Update (2026-08-12):
The variants were consolidated without deploying. The v162 files now live only
in the canonical package root; `deployment/SHA256SUMS-v162.txt` retains their
capture hashes. Future application changes and deployments use the package root
instead of maintaining a second snapshot source tree.

### 2026-08-12 — Keep investigation-memory updates independent from workstreams

Decision:
After a non-baseline playback slice is released, run a general-agent update only
when the selected investigation has saved memory. Show its lifecycle and answer
only in chat. Do not supply, read, or mutate workstreams, Moshe assessments, or
target-bank state.

Context:
Analysts need a broad investigation-level interpretation of new evidence in
addition to Moshe's workstream-specific reevaluation.

Rationale:
Separate revision-scoped job state prevents the general update from changing
Moshe behavior and lets either job succeed or fail independently.

Alternatives considered:
- Extend Moshe's existing reevaluation.
- Generate an update when investigation memory is empty.
- Persist the result into workstreams or investigation memory automatically.

Impact:
Playback advancement can start two isolated background jobs. Empty memory stays
silent, and the general-agent result is conversational output only.

Follow-ups:
Monitor provider latency and consider a shared status stream if polling volume
becomes material.

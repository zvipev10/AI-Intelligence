# Capability Brief

## Capability name

Cellular Calls raw data source

## Capability slug

`cellular-calls-raw-source`

## Parent issue

Draft: `issues/parent-capability.md`

## Current status

Pending product, developer, UX, and QA approval. See `status.md`.

## User problem

The demonstration currently lacks communications metadata that can connect repeated activity across locations. Analysts need a small, realistic raw-data source containing cellular calls, and must be able to inspect both call parties and play the associated recording without leaving the standard raw-record workflow.

## Business goal

Add a cross-source analytical signal that can support the existing three-location scenario while remaining traceable as raw data and visually consistent with other raw layers.

## Target users

- Intelligence analysts using the raw layer catalog, map, table, and timeline.
- Demonstrators showing how raw collection can later support evidence and assessment.
- General and specialist agents retrieving raw records through existing tools.

## Proposed behavior

- Add a Hebrew raw source named `שיחות סלולר` and an English source named **Cellular Calls**.
- Publish 24 synthetic call records as a normal on-demand raw layer.
- Each record contains a call ID, start time, duration, Side A IMEI, Side A number, Side A canonical location, Side B IMEI, Side B number, Side B canonical location, collection metadata, a synthetic recording URL, and a short synthetic transcript/summary.
- Nine linked calls use the same Side A IMEI and number: three calls at each of `LOC-V2-013`, `LOC-V2-009`, and `LOC-V2-010`.
- In each linked call, Side B has a different IMEI and number. Both sides belong to the same canonical location, but different synthetic cell-sector identifiers represent different positions within that area.
- The remaining 15 calls provide sparse background traffic without reproducing the linked three-location pattern.
- Opening a call uses a dedicated raw-record viewer with two clearly separated party cards, call timing, source/provenance fields, recording controls, and transcript/summary.
- All identifiers and recordings are synthetic and visibly labeled as simulation data.

## MVP scope

- Dataset generation and Hebrew/English projection.
- Raw layer catalog, table, map, timeline, retrieval, and object opening through existing mechanisms.
- Dedicated responsive RTL/LTR cellular-call viewer.
- A playable recording for every record.
- Public event/tool payloads expose the call-specific fields.
- Automated dataset, API, UI, and regression tests.

## Non-goals

- Real telecommunications ingestion, lawful-intercept integration, or live streaming.
- Subscriber identity resolution or real-person data.
- Automatic call-content transcription.
- New fusion, evidence, or Talia assessment logic in this capability.
- New always-visible map behavior; the layer remains presented on demand like existing raw layers.

## Acceptance criteria

- The layer appears in the catalog as `שיחות סלולר` in Hebrew and `Cellular Calls` in English.
- Exactly 24 synthetic calls are generated deterministically.
- Every call has distinct Side A and Side B IMEI/number pairs, valid canonical locations, start time, duration, and a playable recording.
- Nine records share one Side A device and number, with three records in each of the three scenario locations.
- For those nine records, Side B changes between calls and uses a different cell sector from Side A while remaining in the same canonical location.
- The viewer presents the two parties once, without duplicating generic fields, and works in desktop/mobile and RTL/LTR layouts.
- Call records remain raw records and can be displayed only on demand through existing result-layer controls.
- Existing UAV, raw entity, evidence, fusion, and assessment viewers are unchanged.
- Agents can retrieve all call-specific fields through the existing object and search tools.

## Edge cases

- Missing or unavailable recording shows a stable localized error state without breaking the viewer.
- Unknown party attributes render as unknown rather than `undefined`.
- Two sides may share a canonical area but must not be visually described as the same exact position.
- Repeated Side A identifiers must not cause records to be collapsed into one call.
- Long numbers, IMEIs, and Hebrew transcript content must wrap correctly on mobile.

## Technical constraints

- Reuse dynamic source-layer creation based on `source_type`.
- Preserve the current CSV-backed V2.1 dataset and existing event IDs.
- Generate small deterministic WAV assets locally; do not depend on a remote media service.
- Extend the public event projection rather than creating a parallel API.
- Do not include real phone numbers, IMEIs, voices, or personal data.

## UX notes

- Use **Cellular Calls** as the English label.
- Side A and Side B should be peers in the layout; neither implies caller ownership beyond the source metadata.
- Show canonical area and cell-sector detail separately so “same area, different position” is understandable.
- The recording module should be labeled “Simulated call recording” / `הקלטת שיחה מדומה`.
- Do not repeat party fields in the generic metadata list.

## QA notes

- Validate deterministic generation, referential integrity, media existence, audio MIME/playback, translation, field exposure, viewer routing, and responsive rendering.
- Add a chain assertion for the repeated Side A identity across exactly the three requested locations.

## Risks

- Synthetic tones may not feel like a call recording unless paired with a transcript and clear simulation labeling.
- A canonical location is an area, not a coordinate; the sector distinction must not imply unsupported precision.
- Generic evidence preparation may later interpret summaries, but special fusion behavior is deliberately out of scope.

## Open questions

1. Approve the interpretation that Side B is a different device/person in the same canonical location but a different synthetic cell sector.
2. Approve deterministic, non-intelligible simulated call audio plus a visible synthetic transcript. If spoken dialogue is required, a separate TTS/media decision is needed.
3. Approve 24 total calls, including the nine-record three-location chain.

## Missing inputs

Human approval of the three open questions above.

## Required reviewers

- Product/user
- Development
- UX
- QA
- Security/privacy acknowledgement for synthetic identifiers and audio

## Required child issues

- [ ] Product review
- [ ] Developer review
- [ ] UX review
- [ ] QA review
- [ ] Execution planning

## Proposed execution checkpoints

1. Approve schema, dataset pattern, and simulation treatment.
2. Implement deterministic records and media; verify dataset and API contract.
3. Implement viewer; verify RTL/LTR and mobile behavior.
4. Run regression suite, review visually, then merge/deploy only when explicitly requested.

## Handoff to developer

Questions for developer:
- Can call fields be added without changing existing generic viewer behavior?
- What is the smallest stable media-generation and serving path?

Expected developer output:
- feasibility notes
- likely affected files/services
- implementation options
- recommended approach
- technical risks
- test strategy
- proposed execution slices

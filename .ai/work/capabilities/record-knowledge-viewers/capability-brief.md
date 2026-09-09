# Capability Brief

## Capability name
Record and knowledge entity viewers

## Capability slug
record-knowledge-viewers

## Parent issue
https://github.com/zvipev10/AI-Intelligence/issues/48

## Current status
Draft - pending human review. See `status.md`. No implementation or execution plan yet.

## User problem
Analysts need to inspect raw records and knowledge entities (organizations and targets) directly from the map, grid, and general assistant, without losing their investigation context. Text-only summaries do not provide an appropriate viewing experience for media sources.

## Business goal and target users
Enable analysts to inspect existing source material and entity details consistently across the investigation workspace.

## Explicit user requirements
- View raw records and knowledge entities: organizations and targets.
- Open from a map click or grid click.
- Allow the general assistant to open the same viewer.
- Keep text fields and add presentations appropriate to the source, including video playback for UAV data.

## Proposed behavior — recommendations awaiting review
Use one reusable details panel, opened by map, grid, or assistant for a single identified object, with a heading, canonical ID, item type, relevant details, and a close control. Keep the map, table, filters, and conversation context intact. One item is active at a time.

Entry points:
- Grid: clicking the item name/ID or row opens its details; embedded map and other action controls retain their existing behavior. Provide a keyboard-accessible open action.
- Map: a single-object marker opens that object. Grouped markers retain their existing behavior and do not open the viewer. No grouped-marker item chooser is required (explicit user clarification).
- General assistant: an explicit request to open a resolved record, organization, or target opens the same panel through a validated typed reference. Ambiguous requests ask the user to choose. Ordinary mention of an item does not repeatedly open the panel. A referenced item need not already be in the displayed grid, but it must be available under the current visibility rules.
- Changing investigations closes the panel and invalidates pending loads from the previous investigation. Closing restores focus to the originating control.

## MVP scope
Raw records show relevant user-visible text and metadata, source and collection family, timestamp, canonical identifiers, and available source presentations. Evaluator-only and hidden fields must not be exposed by a generic field dump.

Proposed presentation mapping, subject to actual dataset and media inventory:

| Data available | Presentation |
|---|---|
| UAV record with playable video | Video player with controls, alongside observation text and available mission/segment metadata |
| Image attachment | Image preview with enlarge control and available caption |
| Audio attachment | Audio controls and existing transcript, when available |
| Text/report only | Readable text and structured fields |
| Other supported attachment | Labelled attachment link and text fields |
| Referenced but missing or unsupported media | Clear unavailable/unsupported state; preserve text and identifiers |

Source labels alone must not imply that an actual media asset exists. Do not generate substitute UAV footage or treat a segment ID as a playable URL. Additional renderers depend on available sources and review agreement; UAV playback is the explicit initial media requirement.

Organization details show available canonical name, aliases, type, summary, and existing related record/entity references. Target details show existing catalog fields and source references without creating or changing assessments. Linked supported items open in the same viewer, with a way back to the previous item proposed for review.

## Non-goals
Editing records/entities, changing target generation or assessments, new collection integrations, media upload/transcoding, and automatic transcription or image/video analysis. No deployment in the definition phase.

## Acceptance criteria
1. The same canonical record, organization, or target opened from map, grid, or assistant shows consistent detail content.
2. The viewer opens only for one identified object. Grouped markers do not open it or introduce an item chooser; existing grouped-marker behavior is preserved.
3. Raw-record text remains readable with or without media. A UAV record with a supported accessible video asset plays with standard controls; missing and failed media have explicit states.
4. Organizations and targets have distinguishable detail layouts and existing references can resolve to the relevant viewer.
5. Assistant actions validate item type and canonical ID; unresolved, unavailable, and ambiguous references never show a different item.
6. Viewer opening does not reset table sorting/filtering, map visibility, or conversation state. Embedded table controls do not trigger accidental opening.
7. Loading, empty, not-found, unavailable, and media-error states work. Rapid selection and investigation switching cannot display a stale response.
8. Hebrew/RTL and English/LTR layouts, keyboard opening, close/Escape, focus restoration, and media controls are usable. Playback stops when the item is replaced or closed; audio does not autoplay.
9. Existing visibility/playback policies apply to detail and linked-record retrieval. Hidden evaluation labels remain excluded.

## Technical constraints and inspected evidence
Baseline: `main` at `24a7527`. Canonical application source is `llm_investigation_orchestrator_serbia_poc/`, per `deployment/README.md`.
- `app.js`: `renderMap()` aggregates records/entities by location and renders target markers separately; current popups provide summaries rather than a shared viewer.
- `app.js`: result tables branch on `events`, `entity_metadata`, and `attack_targets`; existing map actions and sorting/filtering must remain usable.
- `mcp_server/server.py`: `visible_event`, `scoped_entity_presentation`, `public_event`, `resolve_event_reference`, and `get_target_candidate` are relevant existing resolution/visibility paths. The exact UI detail and assistant action contracts require developer review.
- Sample combined dataset fields include `collection_family`, `mission_id`, `observation_id`, and `video_segment_id`, plus evaluation-only fields. No playable asset URL was verified from this inspection.
- Parsing the first dedicated UAV JSONL row with PowerShell failed near `source_type`; investigate encoding/format and the actual runtime loader before assuming that file is directly usable. This is an inspection finding, not a confirmed application defect.

Likely affected files after approval: `app.js`, `index.html`, `styles.css`, `server.py`, assistant result handling and MCP declarations as needed, and focused tests. No new dependency chosen.

## Risks and missing inputs
Playable UAV asset location and access method are unverified. An explicit media reference contract may be needed. Confirm whether organization is a type of the existing entity catalog and which fields are public. Decide panel sizing and behavior on narrow screens during UX review.

## Required reviewers and questions
- Product: accept the shared details-panel proposal, scope, and missing-media behavior.
- Development: inventory actual media and source families, map organization identity, choose canonical detail retrieval and assistant action contracts, and identify a representative playable fixture.
- UX: review single-object opening, grid affordances, panel/back behavior, Hebrew/English layouts, and accessibility.
- QA: cover three item types across all three entry points, media success/failure, stale responses, visibility boundaries, and existing map/grid behavior.
- Architecture/security input: review media delivery and existing access/visibility enforcement if a new retrieval path is necessary.

Review task: https://github.com/zvipev10/AI-Intelligence/issues/49

## Proposed execution checkpoints
A. Review this brief and gather developer, UX, and QA input; human owners approve readiness or explicitly delegate decisions.
B. Create a reviewed execution plan defining detail and assistant contracts plus source presentation scope.
C. Implement and review shared viewer and grid/map entry points.
D. Implement and review assistant opening and available source renderers, including UAV video.
E. Validate regressions, accessibility, and visibility; obtain release acceptance.

These are proposed checkpoints, not an approved execution plan.


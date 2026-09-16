# Capability Brief — Talia Enemy Assessments

## Goal
Add Talia (`talia`) as the enemy-assessment officer who turns shared Evidence objects into durable, revisable enemy assessments with attributable judgments, alternatives, gaps, and controlled spatial assessment overlays.

## Approved scope
1. Durable enemy-assessment artifact and revision contract.
2. Constrained persistence and MCP tools for create, update, retrieve, search, evidence attachment, and supersession.
3. A multiplexed Hermes Talia profile with isolated persona/memory/tool authorization.
4. Application routing for selected/mentioned Talia and structured result handling.
5. Assessment UX with evidence navigation and optional point, area, route/axis, and confidence-envelope overlays.

## Product boundaries
- Projection/fusion services create Evidence; Talia consumes Evidence and may request validated fusion.
- Talia cannot write Moshe's target bank.
- Assessments are not duplicate Evidence layers. They reference evidence and may add higher-order spatial conclusions.
- Existing raw, Evidence, Moshe, General, workstream, and playback behavior remains unchanged unless explicitly extended by an additive adapter.
- Presentation remains on demand through the standard result control.

## Acceptance
- A Talia request is routed to an isolated profile and labeled as Talia.
- An assessment can be created, revised, retrieved, searched, superseded, and traced to Evidence IDs.
- Invalid evidence references, malformed geometry, stale revisions, and target-writing attempts fail closed.
- The UI presents assessment text and controlled overlays without treating analytical graphics as observations.
- A real North Kosovo dataset test creates and reopens a supported assessment without mutating targets.

## Non-goals
- Claimed MIL-STD certification.
- Freehand or arbitrary agent-authored graphics.
- Automatic target creation or acceptance of judgments.
- Live ingestion or autonomous continuous assessment.

# Capability Brief

## Capability name
Hebrew and English runtime localization

## Capability slug
`he-en-runtime-localization`

## Current status
Approved for controlled execution from the user-supplied implementation plan.

## User problem
The Serbia/North Kosovo POC is Hebrew-first and an English WIP exists as a full duplicate, making language behavior inconsistent and expensive to maintain.

## Business goal
Provide clean Hebrew and English experiences from one maintained application, selected at runtime, while preserving Hebrew behavior.

## Target users
Hebrew-speaking and English-speaking intelligence analysts.

## Proposed behavior
- Select `he` or `en` at runtime.
- Route MCP retrieval to the matching projected events, locations, and entities.
- Use language-specific agent instructions and step bridges.
- Localize UI copy, formatting, and direction.

## MVP scope
Localized datasets, MCP locale contract and cache, agent prompt/routing, UI toggle/copy/formatting/direction, and regression tests.

## Non-goals
New intelligence capabilities, new datasets, redesigning the analyst workflow, or deploying without valid environment credentials.

## Acceptance criteria
- Hebrew remains the default and passes existing regressions.
- English mode returns only English projected content for supported fields.
- All retrieval tools accept optional `locale`; invalid/missing locale falls back to Hebrew.
- Agent prompt and step bridges match the session locale.
- UI switches language and RTL/LTR without reload defects.
- Automated bilingual MCP and server/UI regression checks pass.

## Technical constraints
The MCP process is read-only and currently uses module-level dataset state. The existing English WIP is a source of reusable work, not the final duplicated architecture.

## Risks
Global MCP caches, semantic-index cache separation, untranslated generated content, and regressions from merging a stale WIP with newer mainline work.

## Open questions
Deployment credentials and final VM rollout remain outside the first local execution slices.

## Required reviewers
Development and QA. UX review is required before the UI consolidation slice is accepted.

## Proposed execution checkpoints
1. Localized data assets and MCP locale boundary.
2. Agent prompt and request routing.
3. UI consolidation and directionality.
4. End-to-end bilingual validation and handoff.


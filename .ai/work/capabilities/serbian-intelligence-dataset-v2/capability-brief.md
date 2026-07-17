# Capability Brief

## Capability name

Serbian Intelligence Dataset V2

## Capability slug

`serbian-intelligence-dataset-v2`

## Current status

Approved by Product for controlled generation. See `status.md`.

## User problem

The current neutral 10,000-record synthetic corpus does not support an investigation played from Serbian Army intelligence perspective and lacks the approved rapid post-EVT-011 escalation and Serbian UAV-derived observations.

## Business goal

Create a new, independently versioned synthetic corpus for intelligence-analysis demonstrations without modifying any v1 dataset.

## Target users

Analysts playing the scenario from Serbian military intelligence perspective.

## Proposed behavior

- Preserve the EVT-001 through EVT-011 buildup in a perspective-adjusted v2 copy.
- Replace the old EVT-012 through EVT-025 story with a rapid 72-hour fictional incursion, NATO/Kosovo containment, limited Serbian territorial control, and frozen standoff without sustained battle.
- Make opposing-force activity the dominant collection target.
- Represent Serbian-side activity only as a small minority from public sources.
- Add structured, synthetic Serbian Air Force UAV-video exploitation observations focused on opposing forces.

## MVP scope

- Deterministic generator.
- New raw v2 CSV and JSONL.
- New evaluator-label v2 CSV.
- New clean runtime projection v2 CSV.
- New UAV observation v2 JSONL.
- New v2 entity and location references.
- Generation report and validation checks.

## Non-goals

- No changes to existing v1 files.
- No real or generated image/video assets.
- No current operational claims.
- No exact real-world tactical positions, live intelligence, or private data.
- No application switch to v2 in this slice.

## Acceptance criteria

- V1 files remain byte-for-byte unchanged.
- V2 contains 14,500-15,000 unique records.
- EVT-001-EVT-011 remain the buildup; post-EVT-011 records use the replacement escalation.
- Serbian-side records are no more than 10% and use public-source families only.
- At least 3,500 UAV-derived observations focus on NATO/KFOR, Kosovo Police, KSF, infrastructure, or ambiguous civilian activity.
- Runtime projection retains the canonical nine-field schema.
- Hidden truth/evaluator fields remain outside runtime projection.
- All entity/location references resolve.
- Generator is deterministic.

## Assumptions

- Product approval to start accepts structured UAV-derived records without media assets.
- Formation names are public references; every movement and operational event is synthetic.
- Coarse scenario locations are sufficient.

## Risks

- Synthetic outputs may accidentally overrepresent friendly-force information.
- Movement sequences may be internally inconsistent without validation.
- Existing runtime tools are not switched to v2 in this slice.

## Required reviewers

- Product: approved in conversation.
- Development and QA: AI review recorded as implementation guidance; human acceptance remains required after generation.

## Proposed execution checkpoints

1. Define generator, v2 schemas, entities, locations, and chronology.
2. Generate and validate v2 artifacts.
3. Review quality and decide whether to activate v2 in the application.

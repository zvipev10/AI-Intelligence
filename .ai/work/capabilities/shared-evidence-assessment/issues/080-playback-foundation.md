# Issue 80 — Timeframe-stage playback foundation

## Purpose

Implement the generic scenario manifest, persistent run state, and constrained
playback APIs.

## Owner role

Development/Architecture.

## Inputs

- `capability-brief.md`
- `playback-execution-plan.md`
- approved simplified timeframe-stage artifact

## Expected output

- manifest and runtime implementation;
- API and persistence tests;
- checkpoint 014.

## Blocking relationship

Blocks retrieval visibility enforcement. Playback must not be activated in the
UI before the next slice closes the retrieval boundary.

## Completion criteria

- full test discovery passes;
- checkpoint reviewed;
- code and artifacts published;
- Product owner approves proceeding to Slice 2.


# Issue 82 — Minimal next-stage playback and Moshe reevaluation

## Purpose

Provide one button that releases the next timeframe and runs Moshe against the
expanded evidence boundary.

## Owner role

Development/Architecture and UX.

## Inputs

- approved checkpoints 014 and 015;
- Product approval to combine minimal playback UI with the essential Moshe
  trigger;
- prepared timeframe-stage scenario.

## Expected output

- one next-stage button;
- server-derived next-stage timeframe tooltip;
- one Moshe reevaluation per released revision;
- focused API and UI regression coverage;
- checkpoint 016.

## Completion criteria

- duplicate requests do not advance or trigger Moshe twice;
- Moshe receives the new and cumulative timeframes;
- the button is disabled during processing;
- no next-stage button is rendered after the final stage;
- full test discovery passes;
- code and artifacts are published.

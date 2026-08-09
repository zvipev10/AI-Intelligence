# Checkpoint 009 — Bounded playback discovery

## Scope

Moshe's Next-slice prompt now restricts new evidence discovery to the exact released timeframe, limits
discovery to one exact event search, treats cumulative evidence as comparison context, and blocks broad
historical expansion except for resolving an already identified new record.

## Non-goals

- No shared slice snapshot.
- No parallel workstream processing.
- No server-enforced tool allowlist.

## Validation

- Python compilation passed.
- Focused playback suite: 16 passed.
- Full app/backend suite: 130 passed.
- Diff whitespace check passed.

## Publishing

Branch: `codex/playback-new-slice-instructions`. Deployment and merge require product validation.

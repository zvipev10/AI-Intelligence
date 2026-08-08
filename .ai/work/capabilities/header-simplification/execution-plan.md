# Execution Plan

## Prerequisite gate

- `capability-brief.md`: ready
- `ux-review.md`: approved by user
- `developer-review.md`: approved by explicit delegation
- `qa-review.md`: ready for execution

## Implementation approach

Target only `llm_investigation_orchestrator_serbia_poc_english_wip_20260806_0718`.

1. Move `E` and `ע` labels inside the existing language switch track while retaining `#languageToggle` and locale behavior.
2. Render dataset and Hermes status as compact focusable indicators with non-color state icons and localized detail tooltips.
3. Keep existing dynamic status text nodes and state hooks so runtime behavior remains intact.
4. Increment static asset query versions to avoid stale VM caches.

## API/data changes

None.

## Test plan

- Focused source assertions and existing UI regression tests.
- Local browser screenshots and interaction checks in both locales.
- VM service/API/public endpoint checks after deployment.

## Risks and fallback

- Tooltip clipping: place details below/end-aligned with a high stacking level.
- Mobile hover absence: focusable indicators expose the same detail on tap/focus.
- Deployment regression: back up the current VM static files before replacement and retain the backup path for rollback.

## Execution slices

1. Header markup, styles, and status-state binding.
2. Local QA and visual validation.
3. Push, VM deployment, and post-deployment smoke validation.

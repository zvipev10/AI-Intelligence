# Developer Review

## Status
Approved for planning under the user's explicit delegation on 2026-09-09.

## Findings and approach
The feature is feasible without a new API. Result layers already contain visibility-scoped record and organization rows. A single client-side viewer can resolve an object by typed canonical ID from the currently loaded layers, so map, grid, and assistant entry points use identical data.

Add a modal dialog to `index.html`, rendering/state/event handling to `app.js`, and component styles to `styles.css`. Grid rows receive keyboard-accessible open controls. Map markers open only when their accumulated references resolve to exactly one supported object. After an assistant response, explicit typed identifiers in the answer become open controls; identifiers absent from loaded visible layers remain unavailable rather than triggering unrestricted retrieval.

Media rendering is allowlisted by type (`video`, `audio`, `image`) and URL scheme/path. Existing dataset rows contain structured media references but no bundled playable assets, so the viewer must show text plus a media-unavailable state unless a valid URL is present.

## Risks and tests
Avoid accidental row opening from existing map controls. Escape all visible data and validate media URLs before assigning them to media elements. Test resolver boundaries, supported/unsupported media, single versus grouped markers, dialog focus/Escape, and existing UI regression tests.

## Execution slices
1. Shared viewer, record/organization rendering, grid and single-object map entry points.
2. Assistant reference controls, media states, regression and acceptance validation.

No blocking questions remain. Targets are excluded.

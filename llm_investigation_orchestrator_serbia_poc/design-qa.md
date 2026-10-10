# Design QA — investigation workspace refresh

## Follow-up visual correction — 2026-10-09

**Target:** supplied desktop Investigations reference, compared with the deployed English landing view at 1440px.

### Findings corrected

1. **P1 — map source shortcut pills were not part of the requested workspace.** Removed the map overlay, its source-dot styles, and the search-seeding event behavior.
2. **P1 — display typography lacked the reference’s compact, condensed hierarchy.** English workspace titles, navigation, and key panel headings now use Roboto Condensed; Hebrew continues to use the appropriate Noto Sans Hebrew fallback.
3. **P1 — the dark green surface was too saturated and varied between the landing and workspace.** Consolidated the page and header background around `#172421`, with neutralized panel, divider, and muted-text tokens.

### Verification

- Source reference: `WhatsApp Image 2026-10-08 at 09.06.05 (1).jpeg`.
- Implementation: deployed `/ux-refresh-test/?lang=en&revision=181` landing at desktop viewport.
- Font computed style: `Roboto Condensed, Noto Sans Hebrew, Arial, sans-serif`.
- Body background computed value: `rgb(23, 36, 33)`.
- Source-shortcut elements present: `0`.

**Required fidelity surfaces:** typography and colors now track the compact, condensed, dark slate-green reference; the map image and investigation rows remain intentional app-content differences rather than additional visual chrome. Layout and imagery retain the prior desktop composition.

**Final result: passed.**

---

Source visual truth: `C:/Users/user/Downloads/WhatsApp Image 2026-10-08 at 09.06.05 (1).jpeg` and `C:/Users/user/Downloads/WhatsApp Image 2026-10-08 at 09.06.05.jpeg`.

Implementation evidence: in-app Browser capture of `http://127.0.0.1:8769/index.html?lang=en` at a 1440 × 900 CSS-pixel viewport, 1× density, on 2026-10-09. The capture showed the rendered landing page and the map-first workspace. The browser-capture API does not persist image files locally.

State: English locale; landing page with one owned investigation, then that investigation open in Map view.

## Full-view comparison

The implementation adopts the reference’s dark green-black canvas, thin muted dividers, restrained amber action emphasis, condensed workspace header, map-forward active view, compact source pills and editorial investigation list. The generated preview is deliberately labeled as a preview and is not presented as evidence or a map data source.

Focused regions reviewed: landing hero/map preview, draft CTA, investigation row density, Map tab/source shortcut cluster, and map control placement. These were necessary because the reference depends on compact labels, low-contrast boundaries and dense operational controls.

## Required fidelity surfaces

- Fonts and typography: Existing Noto Sans Hebrew/Roboto system retained; heading hierarchy and small operational labels now mirror the compact reference rhythm.
- Spacing and layout rhythm: Desktop hero uses a two-column investigation/map composition; rows moved from large cards to divider-separated records.
- Colors and visual tokens: Semantic tokens were shifted to forest-green surfaces, gray-green borders and a single amber emphasis.
- Image quality and asset fidelity: `assets/ui/investigation-map-preview-v1.png` is a purpose-built, text-free raster preview, cropped without stretching. The active map remains live MapLibre imagery.
- Copy and content: All new visible copy has Hebrew/English localization attributes; source shortcuts use the existing layer selector rather than claiming that a source is already open.

## Interaction checks

- Opening the existing `New investigation` row displayed the active Map workspace.
- Selecting the CCTV quick-source chip set the existing layer-search value to `CCTV` and focused it.
- Existing Map, Timeline and Table tabs remained visible.

## Findings

No actionable P0, P1 or P2 visual differences for the implemented scope. The supplied references show a Syria-specific data state, while the local checked-in runtime shown during QA was Kosovo; this is an expected content difference, not a layout or interaction mismatch.

## Follow-up polish

- P3: Consider replacing the generic profile/status icons with the scenario’s selected analyst identities when a dedicated visual-identity system is approved.

final result: passed

---

## Historical QA retained — collection task screens

The supplied task screenshots defined the requested content and flow, while the application's existing dark workspace remained the visual authority. The ADINT and SIGINT dialogs therefore used the same panel surfaces, borders, typography, field treatment, selection colours and button hierarchy as the rest of the application. Numbered mockup badges were intentionally omitted.

In the English Kosovo runtime, a polygon was drawn on the live workspace map and opened with **Request collection**. The rendered dialog showed the exact three-vertex geometry, a derived centroid in the read-only location summary, the parent workspace’s Satellite/Street basemap mode, and native date/time pickers with selectable bid and recurrence controls. The location preview is a disposable MapLibre instance sourced from actual polygon coordinates, not a generated thumbnail. SIGINT interaction is covered by `test_collection_request.py`; the Kosovo fixture had no IPDR/IMEI entry point, so no scenario switch was made solely for a second visual capture.

Historical result: ADINT visually verified; SIGINT interaction covered by tests.

---

## Historical QA retained — cellular call timeline and viewer

**Source visual truth**

- `C:\Users\user\Downloads\WhatsApp Image 2026-10-05 at 09.51.07.jpeg`
- Source pixels: 1600 × 850.

**Rendered implementation**

- `artifacts/design-qa/cell-call-viewer.png`
- Browser URL: `http://127.0.0.1:8771/?lang=en`
- Implementation pixels and CSS viewport: 1280 × 720 at device scale factor 1.
- Combined comparison: `artifacts/design-qa/cell-call-comparison.png` (source and implementation normalized to adjacent 800 px columns).
- State: Syria `cellular-records-v13`, Cellular Calls timeline focused, first call selected, item viewer open, recording playing.

**Findings**

- No actionable P0/P1/P2 mismatch remained. The implementation preserved the dense call register, near-even list/viewer split, selected blue row, map above transcript and recording below the transcript.
- The source placed its audio waveform across the whole application width. The implementation intentionally kept the existing native audio player inside the call item viewer, as explicitly requested.
- The source showed Thai demo content and a custom waveform. The implementation intentionally used the product’s Syria records, established typography, color tokens, MapLibre map, native audio controls and existing translation transcript.

**Required fidelity surfaces**

- Fonts and typography: existing product font stack and compact label hierarchy retained; register headers, parties, metadata and transcript remained readable without changing the established type system.
- Spacing and layout rhythm: register and viewer occupied comparable halves; map, conversation and player stacked cleanly; selected-row emphasis followed existing table/timeline behavior.
- Colors and visual tokens: dark surfaces, borders, muted metadata, blue selection and call-party indicators used existing application tokens.
- Image quality and asset fidelity: the live map and existing icons were retained; no screenshot assets, CSS-drawn substitutes or placeholders were introduced.
- Copy and content: real record IDs, parties, SIM/IMEI values, locations, transcript, translation control and recording duration were preserved.

**Focused region evidence**

The full-view comparison was sufficient because both the dense register columns and the complete viewer stack were legible at normalized scale. The implementation was also inspected interactively at 1280 × 720: the first row stayed selected in blue and the audio element reported `paused: false` with advancing playback time.

**Comparison history**

- Initial rendered pass: no P0/P1/P2 issues identified, so no visual correction iteration was required.

**Implementation checklist**

- Dense cellular-call timeline register implemented.
- Selected row opens an adjacent map/transcript viewer.
- Native audio player remains inside the item viewer.
- Audio playback is requested immediately on viewer open, with browser-policy fallback to manual playback.
- Desktop and responsive layout rules added.

**Follow-up polish**

- None required for the historical scope.

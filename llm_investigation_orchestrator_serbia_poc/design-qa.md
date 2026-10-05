# Collection task screens — design QA

The supplied task screenshots define the requested content and flow, but the
application's existing dark workspace is the visual authority. The ADINT and
SIGINT dialogs therefore use the same panel surfaces, borders, typography,
field treatment, selection colours, and button hierarchy as the rest of the
application. Numbered mockup badges are intentionally omitted.

## Verified ADINT flow

In the English Kosovo runtime, a polygon was drawn on the live workspace map,
then opened with **Request collection**. The rendered dialog showed:

- the exact three-vertex geometry that was drawn, fitted inside the task map;
- its derived centroid in the read-only location summary;
- the same Satellite/Street basemap mode as the parent workspace;
- native date and time pickers, selectable bid and recurrence controls, and a
  fixed footer within the scrollable dialog.

The location preview is a disposable MapLibre instance sourced from the actual
polygon coordinates. It is not a generated thumbnail or a static approximation.

## SIGINT coverage

The SIGINT screen uses the same integrated task-dialog components. Identifier
validation, native date controls, select menus, chip choices, the add-identifier
toggle, and case/circle enablement are covered by `test_collection_request.py`.
The currently running Kosovo fixture has no IPDR/IMEI entry point, so no
scenario switch was made solely for a second visual capture.

historical result: ADINT visually verified; SIGINT interaction covered by tests

---

# Cellular call timeline and viewer — design QA

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

- No actionable P0/P1/P2 mismatch remains. The implementation preserves the source's dense call register, near-even list/viewer split, selected blue row, map above transcript, and recording below the transcript.
- The source places its audio waveform across the whole application width. The implementation intentionally keeps the existing native audio player inside the call item viewer, as explicitly requested.
- The source shows Thai demo content and a custom waveform. The implementation intentionally uses the product's real Syria records, established typography, color tokens, MapLibre map, native audio controls, and existing translation transcript.

**Required fidelity surfaces**

- Fonts and typography: existing product font stack and compact label hierarchy retained; register headers, parties, metadata, and transcript remain readable without changing the app's established type system.
- Spacing and layout rhythm: register and viewer occupy comparable halves; map, conversation, and player stack cleanly; selected-row emphasis follows existing table/timeline behavior.
- Colors and visual tokens: dark surfaces, borders, muted metadata, blue selection, and call-party indicators use existing application tokens.
- Image quality and asset fidelity: the live map and existing icons are retained; no screenshot assets, CSS-drawn substitutes, or placeholder imagery were introduced.
- Copy and content: real record IDs, parties, SIM/IMEI values, locations, transcript, translation control, and recording duration are preserved.

**Focused region evidence**

The full-view comparison is sufficient because both the dense register columns and the complete viewer stack are legible at the normalized scale. The implementation was also inspected interactively at 1280 × 720: the first row stayed selected in blue and the audio element reported `paused: false` with advancing playback time.

**Comparison history**

- Initial rendered pass: no P0/P1/P2 issues identified, so no visual correction iteration was required.

**Implementation checklist**

- Dense cellular-call timeline register implemented.
- Selected row opens an adjacent map/transcript viewer.
- Native audio player remains inside the item viewer.
- Audio playback is requested immediately on viewer open, with browser-policy fallback to manual playback.
- Desktop and responsive layout rules added.

**Follow-up polish**

- None required for the requested scope.

final result: passed

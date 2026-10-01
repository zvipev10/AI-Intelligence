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

final result: ADINT visually verified; SIGINT interaction covered by tests

# Checkpoint 001

Implementation is complete in `app.js`, `styles.css`, and `test_basemap_ui.cjs`.

Validation:

- `node test_basemap_ui.cjs` passes.
- `git diff --check` passes apart from the repository's Windows line-ending notice.

Review result: no blocking findings. Road/border layers are selected by their stable vector source-layer values rather than fragile individual layer IDs. Existing operational overlays are not included in basemap mutation.

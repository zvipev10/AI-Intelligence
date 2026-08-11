# Execution Plan

## Review gate

- Capability brief: approved by explicit user instruction to develop and deploy.
- Developer review: ready.
- UX review: ready.
- QA review: ready.

## Implementation approach

1. Add coordinate resolution and focused event-popup lifecycle.
2. Add a dedicated action column to raw event rows and exclude it from generic column controls.
3. Wire delegated activation to map view, camera, and popup.
4. Add styles and regression coverage.
5. Bump asset cache keys, deploy from the latest deployed-code branch, and run VM/browser smoke checks.

## API/data changes

None.

## Rollback

Restore the pre-deployment VM backup and previous asset files.

## Risks

- Camera race with map rerender.
- Popup lifecycle after repeated jumps.
- Table control regression from the new column.

# Checkpoint 013 — Manual requested-result presentation

## Outcome

- Final requested results are not added, activated, or rendered when the agent response arrives.
- `הצג תוצאות` is the only entry point that materializes the selected final layers.
- Once visible, the same control changes to `הסתר תוצאות`.
- Investigation-step presentation remains unchanged.

## Map bug fix

- An `aggregate_groups` selection with `group_by=location` is materialized as a map-capable `locations` layer.
- Location ID, label, count, coordinates, and aggregate metadata are preserved.
- The MCP boundary rejects incompatible requested view/layer combinations instead of returning a layer that silently renders empty.

## Scope

- Final answer text is unchanged.
- Evidence-layer links remain deferred.
- Target-catalog refresh remains independent from final-result visibility.

## Validation

- 29 shared UI and result-pipeline tests pass on Linux.
- 34 MCP, target-bank, fusion, and boundary tests pass on Linux.
- JavaScript syntax passes.
- Replaying location IDs from the reported production run returns a `locations` layer with `map=true`, all selected rows, and their coordinates.
- The deployed final-result code has a single `addResultLayers` call, scoped to `restoreOnly`, and the button routes through `toggleFinalAnswerVisibility`.
- General gateway, Moshe gateway, and UI services are active.

## Deployment

- VM: `151.145.93.180`
- Rollback backup: `/home/ubuntu/deploy-backups/manual-result-presentation-20260724T100000Z`
- The in-app browser could not navigate to the VM raw-IP URL, and local tunneling was blocked by desktop policy. Interaction coverage is therefore automated plus deployed-source verification; final visual confirmation remains with the user.

## Review state

Implementation and production contract verification complete; user visual acceptance pending.

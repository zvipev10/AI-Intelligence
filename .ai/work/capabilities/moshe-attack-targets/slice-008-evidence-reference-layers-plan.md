# Slice 8 — Evidence reference layers

## Status

Draft for Product and UX review. No product code is changed by this artifact.

## Goal

Replace the free-text `מזהי ראיות` block with a structured list of relevant evidence layers. Each layer name is an interactive control that presents that evidence through the existing map or timeline renderer.

The evidence section must not contain every tool result. It must contain only canonical records explicitly selected by the responding agent because they materially support the final conclusion.

## Product behavior

### Final answer structure

1. The narrative answer remains unchanged.
2. `הצג תוצאות` continues to control only the data directly requested by the user.
3. A separate `מזהי ראיות` section appears only when the agent selected relevant evidence.
4. The section contains one row per evidence layer:
   - a meaningful layer name;
   - its preferred view: map or timeline;
   - the number of referenced items;
   - canonical identifiers associated with the selected items.
5. Pressing a layer name materializes only that evidence layer and opens its declared map or timeline view.
6. Pressing the same control again hides that evidence layer.
7. The layer also appears in the normal layer list and uses the standard layer controls.
8. No evidence layer is presented automatically when the final answer arrives.

### Identifier presentation

- Identifiers are derived from the validated rows selected for the evidence layer, not parsed from tool prose.
- Show up to 14 identifiers per layer in the answer.
- When a layer has more than 14 identifiers, show the remaining count.
- The presentation limit does not remove rows from the layer: all selected rows are still available on the map or timeline.
- Do not show internal run IDs, tool-call IDs, source-group implementation keys, or intermediate/rejected candidate IDs.

### Empty and error states

- If no relevant evidence was selected, omit the `מזהי ראיות` section entirely.
- If an evidence selection contains invalid or incompatible identifiers, reject it at the MCP boundary so the agent can correct the call.
- If a previously valid layer cannot be restored, keep the answer visible and show a local non-blocking presentation error.

## Recommended contract

Extend the existing `present_requested_results` tool rather than add another Moshe-specific tool.

Input:

```json
{
  "layers": [
    {
      "kind": "locations",
      "ids": ["LOC-V2-014"],
      "label": "המיקומים שהתבקשו",
      "view": "map"
    }
  ],
  "evidence_layers": [
    {
      "kind": "events",
      "ids": ["REC-V2-001", "REC-V2-002"],
      "label": "דיווחים גולמיים התומכים בזיהוי",
      "view": "timeline"
    }
  ]
}
```

Output:

```json
{
  "requested_result_layers": [],
  "evidence_reference_layers": [],
  "returned_layers": 1,
  "returned_evidence_layers": 1
}
```

Both arrays use the same validated typed-layer envelope. They remain separate throughout backend normalization and frontend state.

`layers` continues to mean “data directly requested by the user.” `evidence_layers` means “other data materially supporting the final conclusion.” The tool description must explicitly prohibit intermediate searches, rejected candidates, duplicate checks, and unrelated tool output in both channels.

`layers` may be empty when the user asked for an assessment rather than displayable result data. `evidence_layers` may also be empty. At least one of the two arrays must contain a selection when the tool is called.

## Supported evidence references

| Evidence kind | Allowed view | Identifier shown |
|---|---|---|
| Raw events | Map or timeline | `event_id` / V2.1 record ID |
| Locations | Map | `location_id` |
| Entities | Map | `entity_id` |
| Attack targets | Map | `target_id` |
| Location aggregates | Map | canonical location/group key |
| Date/hour aggregates | Timeline | canonical aggregate key |

Generic aggregates that cannot be represented on a map or timeline are not accepted as evidence-reference layers in this slice.

## Agent behavior

- Both General and Moshe receive the same instruction and tool contract.
- The agent performs one final `present_requested_results` call after analysis when either requested results or evidence references exist.
- The agent selects a small number of semantically named evidence layers, grouped by why the records matter—not by which tool returned them.
- The agent does not generate a free-text `מזהי ראיות:` footer. The UI owns the structured evidence section.
- Canonical identifiers may remain in narrative prose when needed to make a specific claim understandable; the structured section is the authoritative navigation surface.

## Implementation slices

### Slice 8.1 — Shared backend contract

- Extend `present_requested_results` with optional `evidence_layers`.
- Extract the existing selection validation/materialization into a shared helper used by both arrays.
- Require map/timeline compatibility for evidence references.
- Add `evidence_reference_layers` to `agent_result_pipeline.py`.
- Preserve `requested_result_layers` behavior and manual presentation semantics.

Checkpoint: Developer review of the shared API and backward compatibility.

### Slice 8.2 — Structured answer UI

- Add `buildEvidenceReferenceLayers`.
- Replace free-text evidence parsing with a structured `מזהי ראיות` component.
- Render one accessible button/link per selected evidence layer.
- Show count and up to 14 canonical identifiers with overflow count.
- Reuse `addResultLayers`, `activateView`, layer filters, and visibility state.
- Give each evidence layer a stable source ID independent of final requested results.
- Keep all evidence layers hidden until their own control is pressed.

Checkpoint: Product and UX review of Hebrew copy, hierarchy, interaction, RTL, keyboard behavior, and long identifier lists.

### Slice 8.3 — Agent instructions and migration

- Update the shared General-agent and Moshe final-response instructions.
- Stop asking agents to produce a free-text `מזהי ראיות:` footer.
- Keep the legacy parser temporarily as a non-interactive fallback for old saved runs; do not treat it as a source of map/timeline layers.
- Confirm saved-question replay supports the new structured field.

Checkpoint: General/Moshe parity and saved-run compatibility review.

### Slice 8.4 — QA and deployment

- Run shared pipeline, UI regression, MCP-boundary, General-agent, Moshe, and saved-question tests.
- Deploy with code backup; no SQLite migration is required.
- Verify one General response and one `@משה` response in production.
- Verify that neither requested results nor evidence appear automatically.

Checkpoint: Product visual acceptance and QA release acceptance.

## Acceptance criteria

1. `מזהי ראיות` contains only agent-selected, boundary-validated evidence layers.
2. No tool output is automatically promoted into the section.
3. Each layer name opens the complete selected evidence on a map or timeline.
4. Requested results and evidence layers have independent visibility.
5. The answer arriving does not change the active view or add visible layers.
6. Identifiers displayed in the section match the materialized rows.
7. More than 14 identifiers changes only the inline presentation, not the underlying layer.
8. Invalid IDs and incompatible views are rejected deterministically.
9. General and Moshe use the same backend and frontend implementation.
10. Existing `הצג תוצאות`, step-result presentation, target layers, saved runs, and legacy answers do not regress.

## Test plan

### Backend

- Requested-only, evidence-only, and combined selections.
- Every supported kind/view combination.
- Unknown IDs, empty selections, duplicate IDs, incompatible views, and generic aggregate rejection.
- Last successful final-selection call wins without mixing earlier calls.
- Normalization preserves separation between requested and evidence layers.

### Frontend

- Section omitted when empty.
- Layer names, counts, identifiers, and overflow are correct.
- Click shows only the chosen evidence layer and activates the declared view.
- Second click hides it.
- Two evidence layers can be controlled independently.
- Requested-result button does not affect evidence-layer visibility.
- Answer arrival has no map/timeline side effect.
- RTL, keyboard activation, focus state, accessible name, narrow viewport, and long labels.

### Regression

- General and Moshe final answers.
- Existing manual `הצג תוצאות`.
- Intermediate-step `הצג תוצאות`.
- Saved-question save and replay.
- Attack-target map windows and raw-data references.

## Rollback

- Ignore or remove `evidence_reference_layers` from the normalized result.
- Restore the legacy collapsed free-text evidence block.
- No database rollback or target-bank restoration is required.

## Decisions requested

1. Approve one shared `present_requested_results` call with separate `layers` and `evidence_layers`.
2. Approve map/timeline evidence links only for this slice; table-only evidence is deferred.
3. Approve up to 14 displayed identifiers per layer with all selected rows retained underneath.
4. Approve omission of the section when no relevant evidence is selected.
5. Approve temporary read-only legacy rendering for old saved answers.


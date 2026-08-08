# Developer Review

Status: Approved under the user's explicit implement-and-deploy delegation.

The existing `applyAgentResult` function is the common boundary for all relevant completion paths. Extract final-layer presentation from its restore-only branch into a shared helper and invoke it for every completion. Keep `requested_result_layers` as the only automatically presented result data; evidence-reference layers remain user-controlled.

Risks: invalid agent view values and layers incompatible with the requested view. Normalize to map/timeline and prefer a view supported by returned layers.

Validation: static JavaScript syntax, focused source-contract regression tests, existing step-collapse tests, and deployed smoke checks.


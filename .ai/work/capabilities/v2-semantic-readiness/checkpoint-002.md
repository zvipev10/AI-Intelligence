# Checkpoint 002 — V2 Semantic Concepts and Retrieval

## Completed

- Bumped the semantic index to `semantic-event-index-v9-v2-portable-military-concepts`.
- Added multilingual deterministic concepts for UAV observation, convoys/formations, armored vehicles, air defense, logistics, observation posts, engineering activity, helicopters, roadblocks, movement, deployment/staging, stationary state, force concentration, counts, Serbian forces, NATO/KFOR, Kosovo Police, and KSF.
- Added explicit numeric object-count features.
- Included V2 collection, observation, mission, object, count, mobility, direction, and confidence values in semantic documents and MCP event results.
- Added explicit concept/count overlap to hybrid and dense scoring.
- Precomputed record concepts and delayed rationale generation until after top-result selection.
- Added `validate_v2_semantics.py` as a repeatable validation runner.
- Enabled the existing sparse dense-vector implementation for hybrid mode when NumPy is unavailable, matching the Hermes VM runtime.

## Validation results

- V2 rows: 14,800; structured UAV rows: 3,800.
- Cold index build: 77.68 seconds in the bundled local runtime.
- Warm index load: 7.373 seconds.
- Warm queries: 0.098–0.284 seconds across nine probes.
- Pure-Python/no-NumPy dense-only cold build: 33.221 seconds; queries: 0.192–0.407 seconds. All precision gates passed; KFOR was 85% and the other values remained at their accepted thresholds or above.
- Top-20 precision:
  - armored vehicle: 100%
  - vehicle convoy: 100%
  - roadblock: 100%
  - observation post: 100%
  - deployment/staging: 95%
  - UAV moving/withdrawing: 100%
  - UAV count 7: 100%
  - NATO/KFOR: 100%
  - Kosovo Police: 70%
- All requested concept-feature probes passed, including air defense, formations, force concentration, and Serbian/Kosovo/NATO terminology.
- Python compilation, V1 10,000-row loader regression, and git whitespace checks passed.

## Review findings

- The initial dense query path spent 15–35 seconds generating rationale for every positive candidate. Rationale generation now runs only for selected results.
- A generic movement field label caused false concept matches. Semantic documents now use the neutral label `mobility_status` while MCP results retain the public `movement_status` field.
- Kosovo Police and KSF require distinct concepts; splitting them raised Police top-20 precision to the accepted 70% threshold.
- The 1 GB VM cannot efficiently retain both Python sparse lexical and dense indexes; no-NumPy hybrid mode now reports `fallback_mode=dense_only`, preserving cross-language retrieval within its memory budget.
- Cache signatures now use content SHA-256 values rather than file mtimes, allowing a validated off-host cache to be uploaded to the constrained VM without a memory-heavy rebuild.

## Remaining work

Deploy the changed projection and MCP semantic implementation, prebuild the V2 index on the VM, and repeat bounded semantic probes.

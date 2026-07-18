# Checkpoint 003 - Production deployment and verification

## Deployed

- Installed the V2 projection and current MCP semantic implementation on the Hermes VM.
- Uploaded the locally validated portable cache to `/opt/serbia-poc/data/semantic_index/v2/semantic_event_index_hybrid_embedding.pkl`.
- Restarted `hermes-gateway.service` after installation.

## Production verification

- Cache version: `semantic-event-index-v10-v2-compact-portable-concepts`.
- Cache size: 50,743,532 bytes.
- Runtime engine: pure Python, dense-only fallback.
- Loaded rows: 14,800; structured UAV rows: 3,800.
- Portable-cache load on the VM: 12.766 seconds.
- Five bounded production probes completed in 0.411-0.618 seconds each.
- Armored-vehicle and convoy probes returned the correct object class in all top five results.
- The count-seven probe returned `estimated_object_count=7` in all top five results.
- NATO/KFOR and Kosovo Police probes returned the intended force terminology and entities.
- Standalone probe peak resident memory: 194,904 KiB.
- `hermes-gateway.service`: active.
- `serbia-poc-ui.service`: active.
- UI status: build `serbia-poc-v2`, dataset `v2`, 14,800 rows.

## Capability status

The requested V2 structured UAV fields, expanded military vocabulary, multilingual same-object terminology, count features, and force terminology are now available to semantic retrieval in production. Geographic multi-source fusion, source-lineage enforcement, target creation, approval workflow, and the Moshe Hermes agent remain a separate next capability.

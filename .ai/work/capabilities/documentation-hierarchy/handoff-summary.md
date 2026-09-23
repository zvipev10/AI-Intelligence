# Documentation consolidation handoff

## Result

README now routes to five guides: product, architecture, demo scenarios, operations and decisions. The cumulative handoff, application/deployment READMEs and old guide paths are short entry points. Workflow instructions name the owning guide for each topic. Existing quality references, contributor documents, source manifests and capability history remain intact.

## Preservation and validation

All 12 edited original documents were archived byte-for-byte from main commit 6bf53e9617c7fe32b9937dffe8cd70b6e260144b. The manifest inventories all 150 original headings, source lines, SHA-256 values and destinations. Current scenario/presentation/operations contracts were promoted; obsolete commands, version snapshots, experiments and prior validation evidence remain explicitly historical. Architecture and decisions retain their existing content with focused routing additions.

Run `python .ai/work/capabilities/documentation-hierarchy/verify_migration.py` from the repository. It compares the archive against Git, verifies hashes/sizes and heading coverage, checks changed Markdown file links and limits changes to documentation artifacts. `git diff --check` passed. Current guides were manually reviewed against the original documents and relevant saved-record storage source. No application tests or VM actions were required or performed; this task changes documentation only.

## Review and limits

Self-review found no blocking issue. Snapshot equality proves retention, not that historical claims are currently valid. Only the newly organized current guides are operating guidance. File-link checks do not validate external URLs or old inbound section anchors. Compatibility pages preserve former file URLs. No runtime behavior, datasets, credentials or private state changed.

## Publishing and next step

Issue #79 tracks this single documentation task; no product-capability child issues are necessary. Publish the scoped commit to codex/documentation-hierarchy and merge its PR as explicitly authorized by the user. GitHub is authoritative for final merge status. Future feature work should update the owning guide and link to it; no additional documentation update or VM deployment is needed for this consolidation.

# Checkpoint 002 — Live qualification found stale audit namespace

Hermes selected table and successfully called open_catalog_layers, but UI returned no structured layer actions. Evidence: the MCP audit record was written under Syria empty-v1 while the UI read network-v1. Existing activation refreshed scenario/dataset/generation but left provisioned INTELLIGENCE_POC_AUDIT unchanged across dataset upgrades.

Fix: activation now refreshes each role audit path alongside its environment and gateway registry. This is necessary for structured presentation delivery after dataset upgrades, including Table. Prior audit files remain preserved. Requalify all roles through activation health and verify a live IPDR request returns the Table catalog action. First failed qualification retained as diagnostic evidence; do not claim completion until the corrected run passes.

Final regression: 238 application tests, 230 passed and eight known baseline failures unchanged. MCP: 72 passed, two skipped. Node presentation/catalog/media checks pass.

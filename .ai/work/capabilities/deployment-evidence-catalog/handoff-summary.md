# Handoff — Deployment Evidence Catalog

The v2.1 demo now precomputes evidence during UI deployment and exposes it as `evidence:all` in the normal layer catalog. All 14,800 raw records are processed; the visible catalog contains 3,867 UAV observations/exact structured public extractions and 298 validated fused objects. Unstructured public reports remain in raw layers to avoid duplicate symbols.

Production verification:
- Catalog count and rows: 4,165.
- Ibar Bridge: 293 rows, including 25 fused objects.
- Public fetch: 5.1 seconds in the verification run.
- UI memory after opening: about 101 MB; VM available memory: 330 MB.
- Hermes gateway and UI services active.
- UI asset version: v182.

Users can open the layer directly from the catalog or ask the agent to open the entire Evidence layer. No live semantic search or fusion is required for that action.

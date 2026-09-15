# Execution Plan — Deployment Evidence Catalog

1. Add deterministic, versioned evidence catalog builder and compact artifact loader.
2. Add `evidence:all` to UI catalog and row endpoint.
3. Run the builder during every UI deployment before service restart.
4. Add unit, catalog, reproducibility, and Ibar Bridge coverage tests.
5. Deploy, verify counts and public catalog access, and record QA/handoff.

Rollback: remove the catalog entry and deployment build command. Raw records and the existing live evidence tools remain unchanged.

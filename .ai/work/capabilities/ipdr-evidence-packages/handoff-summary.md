# Handoff

Current behavior supersedes the initial implementation: only the acquisition package is an IPDR Evidence object. Evidence catalog counts/rows contain one package, and its viewer opens events:IPDR for the 300 raw REC records. Records retain native values, checksum/row lineage, missing identifiers and validation; no record evidence projections or duplicate EVD objects are created.
JavaScript syntax checks passed for this revision. Updated Python/UI regression tests have not run: cloud environment startup failed. Previous green tests applied to the superseded behavior. Publish on the existing feature branch; deployment remains pending.

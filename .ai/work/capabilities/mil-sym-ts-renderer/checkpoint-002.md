# Production verification — 2026-10-29

Deployed application commit: `f195dd848060c4a995f4c61b62454a8413c1e2d9`.
Active identity: Kosovo / profile 2 / `v2.1-en1`, 14,833 rows, maintenance false. Generation: `a3f8d3ec825c40d6bfd241c2ce777e03`.

The first attempt timed out in readiness and recovery. The guarded retry verified restored source, retained the failed namespace, and succeeded after eliminating repeated English translation and expensive status enrichment. Original `v2.1` state remains intact. Private recovery archive: `/home/ubuntu/deploy-backups/kosovo-english-20261029T185516Z.tar.gz`.

Verified installed source hashes in UI and MCP roots; UI/gateway/catalog and general/moshe/talia identities/counts passed. Live events, locations and layer catalog contain zero Hebrew even when requested with locale=he. Public index loads the new adapter and official 7,367,121-byte vendor bundle. Actual configured general-role semantic search returned 50 matches from the trusted v12 hybrid cache, with English event results. Syria profile/data are unchanged and its v12 cache is installed; production was not switched away from Kosovo for this acceptance.

Browser verification was explicitly waived. Four known object-viewer static-contract failures reproduce on baseline; do not claim a fully green repository suite. Final source newline normalization changes no deployed normalized hash.

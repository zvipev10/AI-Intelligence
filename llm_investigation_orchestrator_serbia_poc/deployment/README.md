# Production source provenance

The package root is the single canonical source tree for the application
captured from `/opt/serbia-poc-ui` on VM `151.145.93.180` on 2026-08-12.
That capture serves `app.js?v=162`.

`SHA256SUMS-v162.txt` records the SHA-256 hashes of the 11 non-secret source
files captured from production. The initial consolidation commit makes the
corresponding package-root files byte-identical to those hashes.

The manifest is provenance, not a second source tree. Future application
changes belong only in the package root. A deployment must be built from a
reviewed Git commit and must update the public asset version when required.

`SHA256SUMS-v163.txt` records the reviewed welcome-page source candidate. It
keeps the v162 backend sources and advances the canonical UI assets to
`app.js?v=163` and `styles.css?v=136`. It is a deployment candidate until the
corresponding commit is accepted and deployed.

Secrets, datasets, investigations, workstreams, scenario runs, recordings,
caches, logs, and generated runtime state are intentionally excluded.

No production files or services were changed during capture or consolidation.

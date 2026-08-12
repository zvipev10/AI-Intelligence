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

The v163 welcome-page source was accepted and deployed with `app.js?v=163` and
`styles.css?v=136`. `SHA256SUMS-v164.txt` records the next reviewed source
candidate, which adds the welcome-page draft-investigation composer and
advances the UI assets to `app.js?v=164` and `styles.css?v=137`.

`SHA256SUMS-v165.txt` records the participant-count copy update for the first
two mocked similar investigations and advances the script to `app.js?v=165`.

`SHA256SUMS-v166.txt` aligns each mocked investigation's visible avatar count
with its displayed participant count and advances the script to `app.js?v=166`.

`SHA256SUMS-v167.txt` adds an independent general-agent investigation update
after each newly released playback slice when saved investigation memory is
non-empty. The update appears only in chat, never mutates workstreams, and
advances the script to `app.js?v=167`.

Secrets, datasets, investigations, workstreams, scenario runs, recordings,
caches, logs, and generated runtime state are intentionally excluded.

No production files or services were changed during capture or consolidation.

# VM production source

`vm-production-v162/` is the exact non-secret source snapshot read from
`/opt/serbia-poc-ui` on VM `151.145.93.180` on 2026-08-12.

The snapshot is tracked separately because the deployed application is the
bilingual production variant, while the package root still contains the older
canonical development variant and its source-string regression suite.

Rules:

- Treat `vm-production-v162/` as the authoritative source for reproducing the
  currently deployed `app.js?v=162` build.
- Do not add `.hermes-api.json`, runtime data, saved questions, investigations,
  workstreams, scenario runs, caches, logs, or generated state.
- Future production changes must update this directory in the same commit as
  the corresponding implementation and asset-version change.
- Deployments must compare the intended files against this snapshot before
  copying them to the VM.

No production files or services were changed while capturing this snapshot.

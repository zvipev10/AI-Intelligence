# Developer Review

## Status

Ready for planning under the user's explicit end-to-end authorization.

## Findings

The deployer deletes `/opt/serbia-poc-ui`, while its staging copy omits `scenario_manifests`, `scenario_runs`, `workstreams`, and `investigations`. Its regenerated systemd unit also omits `INTELLIGENCE_POC_DATASET_VERSION`, reverting the UI to v2 although the playback manifest is v2.1.

## Recommendation

Copy code and immutable assets into the existing root without deleting it, omit mutable state from the deploy payload, include `scenario_manifests`, and pin the unit to `v2.1`.

## Test strategy

Run focused playback tests, Python compilation, JavaScript syntax validation, and production status/playback smoke checks.

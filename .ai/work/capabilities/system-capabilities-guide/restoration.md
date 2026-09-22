# Restore the capabilities guide — 2026-09-22

The user requested the same restoration as the investigation journey page. Public and backend URLs returned 404; the file was absent from production and main but present on origin/codex/system-capabilities-guide.

Restore that exact approved source, include it in the deployment FILES list, publish, and atomically upload only this static file. No new behavior, dependencies, restart, data or configuration changes. Source equality, internal anchor targets and deployment inclusion passed. Restored with atomic replacement. Public GET returns HTTP 200 and is byte-identical to the approved source. SHA256: 1f7deb08933f0b648f742d2ae19c0d32599ccadaafd4d9e6fd18991a97980ee3. Browser is not connected, so visual revalidation is unavailable. Documentation scope: this restoration record; no architecture updates needed.


## Media restoration follow-up
The HTML-only restoration missed the five referenced MP4s and poster PNGs. User reported that videos still did not appear. Restore the ten original media files from the same approved branch and add them to FILES. Existing participant images are already covered by the assets directory. Add a regression check that every local src/poster reference exists and is included in deployment. Publish and atomically upload missing media, then verify all guide resources over public HTTP, their content types and byte hashes. No new video creation or content changes. Browser playback validation remains unavailable without a connected browser.

Media outcome: all five MP4s and five posters restored atomically. All 15 guide resources (including existing participant images) return public HTTP 200 with correct video/mp4 or image/png types and byte-identical content. The deployment-coverage regression test and diff check pass. No restart or application/data changes. Browser playback remains unverified because no browser is connected.

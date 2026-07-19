# [Slice 4] Moshe Routing and Session Continuity

## Purpose

Add the restricted Moshe profile, exact `@משה` routing, consecutive-message continuity, and explicit mission closure.

## Completion criteria

- [x] Positive and negative routing tests pass for the transport-independent router.
- [x] Mission/session continuity and closure boundaries pass for the transport-independent registry.
- [ ] Moshe clarification and restricted tools pass.
- [ ] Routing/security checkpoint approved.

## Depends on

`080-slice-3-fusion-tools.md`

## Discovered implementation constraint

The installed Hermes 0.14 `/v1/runs` API does not accept a named profile or per-run tool allowlist. A transport decision is required before wiring the router to Moshe:

1. Invoke `hermes -p moshe chat` on demand and resume its returned session ID. This preserves native profile isolation and avoids a second gateway, but Moshe will not have the General path's live structured run-event stream.
2. Patch/extend the installed Hermes gateway API to accept a profile per run. This preserves streaming but creates an upstream-maintenance and security burden.
3. Run a second profile gateway, which was explicitly excluded from the approved MVP architecture.

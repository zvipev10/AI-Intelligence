# [Slice 4] Moshe Routing and Session Continuity

## Purpose

Add the restricted Moshe profile, exact `@משה` routing, consecutive-message continuity, and explicit mission closure.

## Completion criteria

- [x] Positive and negative routing tests pass for the transport-independent router.
- [x] Mission/session continuity and closure boundaries pass for the transport-independent registry.
- [x] Moshe clarification contract and restricted profile/tool allowlist pass static and integration tests.
- [ ] Routing/security checkpoint approved.

## Depends on

`080-slice-3-fusion-tools.md`

## Resolved implementation constraint

The installed Hermes 0.14 `/v1/runs` API does not accept a named profile or per-run tool allowlist. The user approved a persistent isolated Moshe gateway:

- General gateway: `127.0.0.1:8642`.
- Moshe named-profile gateway: `127.0.0.1:8643`.
- Separate audit files and sessions; shared structured API/result/presentation path.
- Memory guardrails and deployment load validation are mandatory.

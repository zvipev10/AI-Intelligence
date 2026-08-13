# Capability Decisions

## 2026-08-13 — Separate draft sessions from investigations

Decision: Draft exploration uses an ephemeral session ID and is not added to either investigation registry until creation.

Owner: Product

Impact: Chat routing and layer correlation keep a stable ID; investigation memory, workstreams, playback, and normal controls begin only after creation.

## 2026-08-13 — Creation modal and participants

Decision: Require a unique name and show the welcome-page participant/avatar presentation without participant selection. After creation, all regular participants display as they do today.

Owner: Product

Impact: No participant API or membership model is introduced.

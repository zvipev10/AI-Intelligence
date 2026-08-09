# Checkpoint 003 — Target reference acceptance gap

## Outcome

Product validation failed for target-backed workstream creation. The target is used as inference
context but is not persisted as part of the resulting workstream.

## Production evidence

- Hebrew workstream: `ws_20260809_133243_c9666283`
- English workstream: `ws_20260809_133412_b4988813`
- Source target: `TGT-F2CA47CB9859`
- Both workstreams have empty `artifacts` and `activity` collections.
- Neither saved workstream contains the target identifier or another durable target reference.

## Root cause

`prepare_workstream_creation` carries only `title`, `objective`, and `responsibility`. The application
creation handler extracts and persists only those fields. Although target references are supported
inside target-assessment artifacts, no such artifact or root-level target reference is created during
workstream creation.

## Acceptance impact

- The deployed capability does not meet the expectation that supplied targets become part of the
  created workstream.
- Merge is blocked.
- Production should remain available for diagnosis, but the current behavior is not accepted.

## Required decision before correction

Choose the durable representation for seed targets: a root-level workstream reference or an initial
target-assessment artifact. The correction must preserve locale isolation and the ordinary-chat rule
that prevents silent creation of new targets.


# Implementation review

AI technical assessment for explicitly requested implementation; no independent human approval claimed. Keep native ADINT fields in public results, source-specific Table and record viewer. Preserve raw supplied JSON as typed import provenance; CSV blanks encode nulls and public projection restores types. New dataset adint-v1/profile 7, deterministic IDs, no overwrite of network-v1. Build cache offline; controlled VM upgrade must preserve other source records and saved state.

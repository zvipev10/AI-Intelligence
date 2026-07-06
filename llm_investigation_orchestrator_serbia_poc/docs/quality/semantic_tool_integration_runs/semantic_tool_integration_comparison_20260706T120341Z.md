# Semantic Tool Integration Comparison

Previous commit: `aa82add`
Current commit: `7ea65ef+working_tree`

| Probe | Tool | Previous returned | Current returned | Previous must | Current must | Current high top20 | Current semantic candidates | Current status |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| tp_13_resolve_shooting_reference | resolve_event_reference | 0 | 20 | 0/2 | 2/2 | 2 | 80 | PASS |
| tp_14_trace_tactical_noise_clues | trace_semantic_clues | 0 | 118 | 0/16 | 16/16 | 6 | 170 | PASS |
| tp_15_related_from_zvecan_shooting_seeds | find_related_events | 2000 | 2000 | 6/6 | 6/6 | 5 | 2000 | PASS |

## Notes

- `tp_13_resolve_shooting_reference`: The reference phrase does not provide REC IDs and previously resolved to no candidates. A good result should surface the two unverified shooting/noise records at the town-entrance junction.
- `tp_14_trace_tactical_noise_clues`: This probe uses operational clue phrases that previous direct clue matching missed. A good result should recover the curated Zvecan/North-Mitrovica unverified shooting/noise records from semantic_search_events v1.
- `tp_15_related_from_zvecan_shooting_seeds`: The previous implementation already found many nearby/time-related candidates. The semantic improvement should be visible as explicit semantic_embedding linkage reasons while preserving the strong nearby shooting/noise candidates.

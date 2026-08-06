# VM Semantic Quality Comparison - Partial Run

Date: 2026-07-03  
Branch: `feature/semantic-quality-tests`  
Target: VM local UI API, `http://127.0.0.1:8769/api/investigate`

## Execution Status

Questions `fq_01` through `fq_04` completed on the deployed VM version.  
Questions `fq_05` through `fq_08` are not yet comparable because the VM gateway returned:

```text
HTTP 429: The usage limit has been reached
```

The comparison below is therefore partial.

## Completed Questions

| ID | Topic | Elapsed | View | Semantic Tool Used | Assessment |
|---|---:|---:|---|---|---|
| `fq_01_hotspots` | Main friction hotspots | 79.5s | `map` | No | Good. Correctly identifies the four northern municipalities and precise hotspot locations. No event IDs is acceptable because this is an aggregate/location answer. |
| `fq_02_force_movement` | Force movement over time and space | 303.7s | `map` | Yes | Improved depth. Uses semantic search and follow-up tools. Separates movement/presence from one proven operational chain. Main weakness is performance and low overlap with old reference IDs, but the ideal criteria are concept-based rather than fixed-ID based. |
| `fq_03_international_actor_role` | International actor behavior | 174.7s | `evidence` | Yes | Improved fit. Uses semantic search and explicitly distinguishes actor mentions from actual behavior. Correctly keeps conclusion cautious. |
| `fq_04_tactical_event_zvecan` | Tactical event near Zvecan | 222.4s | `timeline` | Yes | Stronger than previous baseline. Builds a chronological reconstruction and distinguishes verified activity, unverified shooting reports, and information noise. Uses reliability/location-comparison logic. |

## Key Comparison Against Reference And Ideal

`fq_01` did not need the semantic tool. Its goal is geographic concentration, and the new run matches the ideal: four municipality-level hotspots plus precise points on the map.

`fq_02` shows the main intended benefit of the semantic change: the agent did not rely only on exact keyword filters. It used `semantic_search_events`, then expanded through objects, related events, semantic clues, linkage checks, sequence building, and hypothesis challenge. The answer is more analytical, but latency is high.

`fq_03` also benefits from semantic retrieval. The answer separates general mentions of the international actor from activity that indicates stabilization, buffering, patrols, or road control. This closes an important conceptual gap in the previous behavior.

`fq_04` is the clearest successful case. The new answer aligns with the ideal requirement: timeline reconstruction, verified/likely vs unverified distinction, and explicit information-noise handling.

## Remaining Gap

The quality run cannot be completed until the model usage limit is cleared. After that, rerun:

```bash
cd /opt/serbia-poc-ui
python3 docs/quality/run_full_questions_vm.py --ids fq_05_escalation_assessment fq_06_violence_noise_general fq_07_geographic_deception fq_08_first_event_by_hotspot --timeout 600
```

Then copy the generated artifacts back into this folder and regenerate the comparison.


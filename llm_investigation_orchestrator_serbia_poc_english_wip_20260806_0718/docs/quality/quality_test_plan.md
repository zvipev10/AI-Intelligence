# Serbia POC Quality Test Plan

## Purpose

This folder defines the quality-test framework for deeper regression work after adding the first semantic-search/RAG capability.

The first artifact is:

```text
question_catalog_v1.json
```

It contains only step 1: stable question definitions.

The second artifact is:

```text
reference_base_v1.json
```

It contains step 2: draft current baselines and ideal-target criteria.

## Step 1: Question Definition

The catalog has two sections:

- `full_investigation_questions`: analyst questions executed through the full app/Hermes/agent flow.
- `tool_level_probes`: direct MCP tool calls used to isolate tool quality from agent orchestration quality.

These definitions deliberately do not include expected event IDs or pass/fail thresholds yet.

## Step 2: Reference Definition

The next step should add references for every question/probe:

- `current_validated_result`: what the current system already finds and must not lose.
- `ideal_target_result`: what the system should find if retrieval and orchestration perform well.

Current v1 status:

- Existing real recordings provide current baselines for `fq_01` through `fq_05`.
- `fq_06`, `fq_07`, and `fq_08` still require live standalone full-agent runs.
- Enabled tool probes have direct MCP current-output baselines.
- Ideal targets currently define criteria/output-shape expectations; reviewed must-find/must-not-prioritize ID lists still need an analyst/offline-label pass.

For full investigation questions, references should cover:

- required answer concepts
- required evidence IDs
- required locations/entities
- expected visualization
- claims that must not be made
- acceptable uncertainty/caveat language

For tool-level probes, references should cover:

- `must_find_event_ids`
- `acceptable_event_ids`
- `must_not_prioritize_event_ids`, where relevant
- ranking expectations, where relevant
- required object/layer fields

## Important Rule

Evaluator labels may be used only for offline scoring during step 2 and later. They must not be exposed to:

- the agent prompt
- MCP tool inputs
- UI-visible data
- saved/recorded question payloads

## Execution Note

`tp_12_plan_next_frontier` currently contains placeholder event IDs and is marked `disabled_until_step_2_real_seed_ids` because this step is only question definition. Replace them with real validated seed IDs during step 2 before using the probe in an automated runner.

# LLM Cross-Reference Benchmark

This is a small fictional benchmark for testing whether an LLM can cross-reference a pre-processed evidence package.

It is designed to test the capability discussed in the architecture document:

- The model should not process raw high-volume streams.
- The model receives already-filtered evidence from several fictional sources.
- The task is to connect weak signals across entity aliases, location proximity, timing, and source reliability.
- The model must distinguish meaningful convergence from coincidence and distractors.

## Files

- `entity_registry.csv` - Known entities, aliases, affiliations, and notes.
- `locations.csv` - Fictional locations with coordinates and strategic notes.
- `events.csv` - Structured event stream after pre-processing.
- `reports.md` - Short unstructured reports and analyst notes.
- `model_prompt.md` - Prompt to give to the model together with the evidence files.
- `answer_key.md` - Expected findings and scoring rubric.

## How To Use

1. Give the model `entity_registry.csv`, `locations.csv`, `events.csv`, and `reports.md`.
2. Then give it `model_prompt.md`.
3. Compare the model answer with `answer_key.md`.

The model should be judged mainly on:

- Whether it finds the primary cross-source hypothesis.
- Whether it cites the actual evidence.
- Whether it handles aliases correctly.
- Whether it avoids overclaiming.
- Whether it recognizes distractors and alternative explanations.

## Important Design Point

This benchmark does not prove that an LLM can handle raw velocity and volume.

It tests a narrower and more realistic claim:

> Given a compact, pre-processed evidence package, can the LLM synthesize a meaningful cross-reference hypothesis?


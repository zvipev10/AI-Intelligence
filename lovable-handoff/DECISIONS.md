# Product Decisions

## Why the application exists

The prototype demonstrates that the important capability is cross-reference across noisy data streams, not simple keyword search or isolated anomaly detection. The analyst should experience the difficulty of manually recovering an occurrence from hundreds or thousands of raw indicators.

## Narrative naming

Use `התרחשות` everywhere. Earlier versions used story/scenario terminology and artificial codes. Those were removed because they implied an external occurrence identifier that does not exist in the raw data.

## Raw-event identifiers

Raw events use source-based identifiers. The ID must not reveal whether the event belongs to a suspicious or benign occurrence.

## Suspicious and benign activity

The application must show both. Benign occurrences are not generic noise; they are coherent operational narratives that help evaluate false positives and competing explanations.

## Search behavior

The broad initial search intentionally produces a large result set. This illustrates that lexical filtering alone cannot recover the hidden occurrence reliably.

## Shared filtering state

The table and map must be projections of the same filtered event collection. Separate filtering implementations previously risked inconsistent results and misleading presentation.

## Map semantics

- Rectangle: filtered event count and location name.
- Numbered circle: ordered route step in the selected occurrence.
- Route line: movement inferred for the selected occurrence.
- No route is shown during manual search.

## Map technology

The current standalone prototype uses a local schematic map because it has no external dependencies. The Lovable continuation should preferably use MapLibre GL plus an OpenStreetMap-compatible tile source. Google Maps may be used only when API key ownership, billing, usage limits, and data-handling approval are explicit.

## Evaluation separation

Benchmark answer keys and private ID mappings are evaluation infrastructure, not product data. They must stay outside the client and outside prompts used to test whether a model can discover occurrences independently.

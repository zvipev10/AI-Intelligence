# Checkpoint 011 — Temporary thinking indicator

## Outcome

Every new General Agent or Moshe response begins with a temporary `חושב` indicator and three animated dots instead of Hermes-specific explanatory text.

## Behavior

- The dots animate in sequence while the request is pending.
- The indicator is replaced by live tool steps when they arrive.
- The pending indicator is removed when the final response is rendered.
- The same indicator is used for normal prompts and explicit continuation.
- Reduced-motion users receive static dots.
- Existing error-specific messages remain descriptive.

## Scope

Presentation only. Agent routing, response generation, tool progress, and stored conversation history are unchanged.

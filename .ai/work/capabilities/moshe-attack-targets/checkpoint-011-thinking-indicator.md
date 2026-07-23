# Checkpoint 011 — Temporary thinking indicator

## Outcome

Every new General Agent or Moshe response begins with a temporary `חושב` indicator and three animated dots instead of Hermes-specific explanatory text.

## Behavior

- The dots animate in sequence while the request is pending.
- Each completed live tool step is inserted above the indicator, leaving `חושב` as the temporary last item while the next step is running.
- The pending indicator is removed only when the final response is rendered.
- The same indicator is used for normal prompts and explicit continuation.
- Moshe's agent-originated opening response uses the same pending indicator.
- Reduced-motion users receive static dots.
- Existing error-specific messages remain descriptive.

## Scope

Presentation only. Agent routing, response generation, tool progress, and stored conversation history are unchanged.

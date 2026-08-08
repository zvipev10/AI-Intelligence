# UX Review

## Capability

Compact upper-section controls

## Review status

Draft - pending human approval

## Context reviewed

User request and current header markup/styles.

## User flow

The analyst sees the selected language and overall service health at a glance. Hover, focus, or tap exposes the full service name and detail without navigating away.

## UI states

- Language: `E` selected or `ע` selected.
- Service: loading/unknown, ready/connected, degraded/local-demo, or error/unavailable.
- Expanded detail: anchored tooltip/popover with service name and current status text.

## Error states

Use an error icon/shape plus color. Keep the concise indicator visible and expose the failure description in its accessible name and detail surface.

## Disabled/loading states

Loading uses a neutral indicator and “Checking…”/equivalent accessible status. Language options should not appear disabled unless switching truly cannot occur.

## Copy / terminology

- Visible language labels: `E`, `ע`.
- Detail labels: `Hermes` and either `Database` or `Dataset`, pending semantic confirmation.

## Accessibility notes

- Do not rely on hover or color alone.
- Use real buttons/radios for language selection with selected state.
- Status details must appear on focus and be available on tap.
- Preserve a useful `aria-label`/`aria-describedby` relationship as dynamic status text changes.

## UX edge cases

Mixed RTL/LTR alignment, long errors, responsive stacking, touch screens, and simultaneous service failures.

## Product questions

- Is the current dataset count intended to communicate database connectivity?
- Should tapping a status pin the detail popover open?

## Developer questions

- Is there an existing tooltip/popover primitive to reuse?
- Where does the language state currently live?

## Review recommendation

Approve the compact direction, conditional on focus/tap parity and confirmation of the DB/dataset label. Human UX/product approval is required before planning or coding.

# UX Review

## Capability

Compact upper-section controls

## Review status

Approved

## Context reviewed

User request and latest-main bilingual header markup/styles. Product confirmed that the data indicator represents dataset status.

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
- Detail labels: `Hermes` and `Dataset`, localized for the active UI language.

## Accessibility notes

- Do not rely on hover or color alone.
- Use real buttons/radios for language selection with selected state.
- Status details must appear on focus and be available on tap.
- Preserve a useful `aria-label`/`aria-describedby` relationship as dynamic status text changes.

## UX edge cases

Mixed RTL/LTR alignment, long errors, responsive stacking, touch screens, and simultaneous service failures.

## Product questions

- Should tapping a status pin the detail popover open?

## Developer questions

- Is there an existing tooltip/popover primitive to reuse?
- Reuse `#languageToggle` and its existing locale state in the bilingual WIP app.

## Review recommendation

Approved by the user on 2026-08-08. Preserve hover, focus, and tap access to details.

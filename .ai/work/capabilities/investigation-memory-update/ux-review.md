# UX Review

Status: Ready for execution planning; explicitly delegated by the user.

## Chat behavior

- Show a lightweight “Investigation memory is being updated…” message only when a memory job actually starts.
- Render the completed response as a general “Investigation update,” not as Moshe or a team member.
- Do not show anything when memory is empty.
- Show a concise, independent failure message for the general update without changing Moshe's status UI.
- Avoid an activity card or new persistent navigation surface.

## Accessibility

- Reuse the existing live conversation region.
- Use localized labels and error copy.
- Do not move focus when the asynchronous update arrives.

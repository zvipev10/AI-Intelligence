# General instruction A/B test decisions

## 2026-09-12 — Isolated candidate profile

Keep the production General gateway unchanged on port 8642. Run the persistent-instruction candidate in a separate Hermes profile (`generalpersistent`, following Hermes' alphanumeric profile-ID constraint) on port 8644 because the installed Hermes 0.14 `/v1/runs` API cannot select a profile per request. Select the candidate only through the explicit `instruction_mode=persistent` benchmark field. Invalid or omitted modes fall back to the current inline behavior.

The stable agent contract belongs in the persistent profile. Locale, new-versus-continuation classification instructions, current investigation state, and current catalog identifiers remain per-run because they can vary between requests.

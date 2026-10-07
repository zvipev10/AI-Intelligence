# AI-Intelligence application

Stateless Python (standard library) web app in front of platform-hl-api.

```bash
python3 devtools/fake_hlapi.py --port 9100 --fixture devtools/fixtures/syria.json.gz --provision &
HL_API_URL=http://127.0.0.1:9100 APP_COOKIE_SECURE=false python3 server.py   # http://localhost:8080, analyst / analyst
python3 -m unittest discover -s tests -t .
```

| Path | What |
|---|---|
| `server.py` | routes, static allowlist, sign-in guard, `/healthz` |
| `analysis.py` | layers, summaries, links, saved-item validation (pure functions) |
| `hl/` | HL API client, per-user snapshot, item→row mapping, saved work as entity records |
| `mapping/default.json` | where each UI column comes from in i360 |
| `demo_profiles/` | per-scenario camera, labels and `items_query` |
| `tools/provision_types.py` | create the app's entity types (dry run, then one publish) |
| `devtools/` | fake HL API and its fixture, for development and CI only |
| `tests/` | backend tests; `test_*.py` / `test_*.cjs` here are UI tests |

See [architecture](../docs/architecture.md) and [operations](../docs/operations.md).

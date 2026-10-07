# Operations

Branch `feature/i360-only`. The app is one stateless container that talks to platform-hl-api.

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `HL_API_URL` | (required) | platform-hl-api base URL. In cluster: `http://platform-hl-api:8080` |
| `HL_API_PUBLIC_ORIGIN` | `HL_API_URL` | origin the browser uses for signed media URLs |
| `PORT` | `8080` | listen port |
| `APP_HOST` | `0.0.0.0` | bind address |
| `APP_SCENARIO` | `syria` | `syria` or `kosovo` (`demo_profiles/<scenario>.json`) |
| `APP_MAPPING` | `mapping/default.json` | item → row mapping |
| `APP_TYPE_PREFIX` | `AII_` | prefix of the app's entity types |
| `APP_SNAPSHOT_TTL` | `300` | seconds a user's snapshot is reused |
| `APP_SNAPSHOT_MAX_ROWS` | `30000` | safety cap on items read per snapshot |
| `APP_COOKIE_SECURE` | `true` | set `false` only for plain-HTTP local runs |
| `HL_API_TIMEOUT` | `30` | seconds per HL API call |
| `APP_BUILD` | `dev` | build label shown in `/healthz` and `/api/status` |

No secrets. The app holds no password, key or service account.

## Endpoints for the platform

- `GET /healthz`: liveness and readiness. It does not call HL API, so a slow HL API does not
  restart the pod.
- Logs go to stdout.

## Local development (no i360 needed)

```bash
cd llm_investigation_orchestrator_serbia_poc
python3 devtools/fake_hlapi.py --port 9100 --fixture devtools/fixtures/syria.json.gz --provision &
HL_API_URL=http://127.0.0.1:9100 PORT=8080 APP_COOKIE_SECURE=false python3 server.py
# open http://localhost:8080 and sign in as analyst / analyst
```

`devtools/fake_hlapi.py` implements only the HL API operations the app calls, with HL API's
shapes and documented behaviour. It is a development aid, not the API.

## Tests

```bash
cd llm_investigation_orchestrator_serbia_poc
python3 -m unittest discover -s tests -t .        # backend, against the fake HL API
python3 -m unittest discover -s . -p 'test_*.py'  # UI text checks
for t in test_*.cjs; do node "$t"; done           # UI behaviour checks
```

The Dockerfile runs all three during the image build.

## First use on an estate

1. Get an i360 login for building apps (not an admin account) and note its permission profile.
2. Create the entity types, signed in as that user:
   ```bash
   HL_API_URL=https://<platform-hl-api host> python3 tools/provision_types.py --grant-profile <profile>            # dry run
   HL_API_URL=https://<platform-hl-api host> python3 tools/provision_types.py --grant-profile <profile> --apply    # one publish
   ```
   A publish restarts platform services for everyone on the estate (about 80 seconds plus two
   minutes of rolling restarts). Agree a time with the LAMBDA owner.
3. Point `items_query` in `demo_profiles/<scenario>.json` and `mapping/default.json` at how the
   demo data was ingested (item types, field names). Check every layer and viewer.
4. Run the app against the estate and verify as a normal user: sign in, layers load, viewers
   open, a saved item survives a reload.

## Deploying to LAMBDA

Follow `DEPLOY-GITHUB-CODE-TO-LAMBDA.md`:

1. `git archive` this package into `apps/<name>/` of `elbitbox/micro-apps` in one commit that
   records the GitHub SHA. `.gitattributes` keeps LF line endings.
2. Add the `docker-bake.hcl` target and the `CLAUDE.md` bullet; MR to `develop` with one CR
   approval; **Build Now** on the Jenkins `develop` job.
3. On skipper `master`: `intel360-lambda/<name>.yaml` (env vars above, `HL_API_URL=http://platform-hl-api:8080`)
   and `,<name>` in `APP_RELEASES`.
4. With the LAMBDA owner's go-ahead, run the skipper job with `ENVIRONMENT_NAME=intel360-lambda`.
5. Verify that the pod `imageID` equals the registry digest, and run the checks from step 4 above
   through the public host.

The image needs `nodejs` from the Debian mirror in its test stage. If the build network cannot
reach it, pass a base image that already has Node with `--build-arg PYTHON_IMAGE=...` or move
the `.cjs` tests to the pipeline.

## Troubleshooting

| Symptom | Look at |
| --- | --- |
| Sign-in says wrong password | the account in i360; the app forwards the raw password as HL API requires |
| Empty layers after sign-in | `GET /api/dataset/info` (rows, warnings); `items_query` and the mapping; the user's i360 rights |
| `entity type ... is not readable here` in warnings | the mapping names a reference type this estate does not have |
| Saving fails with 404 on `AII_*` | the types were not provisioned, or not granted to the user's profile |
| `truncated: true` | more items than `APP_SNAPSHOT_MAX_ROWS` |

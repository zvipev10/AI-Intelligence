# Deploying Claude-generated code from GitHub to LAMBDA

The usual case is a **new UI that works against platform-hl-api (HL API)**. It lives in its own new folder in
`elbitbox/micro-apps`, next to the existing apps, and does not change them. Read section 3 before you start.

**Verified 2026-10-06.** I checked every step below against the two services we deployed this way. Both are running on
LAMBDA as described:

- `freelang-search-ui`: a web app in `elbitbox/micro-apps`. Two pods, live since 2026-09-16.
- `i360-chat`: a backend service in `elbitbox/analytics`. Two pods.

We have not done some of the steps ourselves. Those are marked **(not exercised)**, so you know where to expect surprises.
Appendix A lists each fact and how it was checked.

---

## 1. The whole path

```
GitHub repository (the Claude-generated code)
   |  1. clone it on your laptop and copy the tracked files
   v
GitLab  gitlab.e-bitbox.com: a FOLDER inside an existing monorepo
   elbitbox/micro-apps  ->  apps/<name>/     (web apps, UIs, small servers with a page)
   elbitbox/analytics   ->  <name>/          (backend services, Python or Node)
   |  2. feature branch -> merge request -> 1 "CR" approval -> merge
   v
Jenkins  jenkins.e-bitbox.com: the repo's own pipeline runs `docker buildx bake`
   |  3. image pushed to the registry
   v
Registry  docker-registry.e-bitbox.com:5000/<repo>/<name>:<tag>
   |
   v
skipper  elbitbox/skipper, branch master
   environments-configuration/intel360-lambda/<name>.yaml   (your Helm values)
   environments-configuration/intel360-lambda/skipper.config (one entry registering the release)
   |  4. Jenkins job "skipper / master" with ENVIRONMENT_NAME=intel360-lambda
   v
Kubernetes  cluster ares-cluster (k8s.ares.e-bitbox.com:6443), namespace intel360-lambda
   https://<host>.intel360.lambda.projects.e-bitbox.com
```

"LAMBDA" is the Kubernetes namespace `intel360-lambda` on the cluster `ares-cluster`. Skipper renders the Helm chart
`simple-service-template` with your values file and installs it as a Helm release.

---

## 2. Why the code goes into an existing monorepo, not a new project

- **You cannot create a GitLab project.** On a developer account GitLab reports `can_create_project: false` and
  `projects_limit: 0`. That also rules out GitLab's "Import project from GitHub", which creates a new project.
- **The build and deploy plumbing exists per repository.** The Jenkins multibranch job, the registry path and the
  image-tag rules exist for `micro-apps` and `analytics` already. A standalone repository would need DevOps to
  create the project, the Jenkins job and the registry path. **(not exercised)**
- So the code is **copied into a folder** of one of the two monorepos. The GitHub repository stays where it is, as
  the record of where the code came from. Do not add GitHub as a remote of the GitLab clone, and never push company
  code or configuration to GitHub.

---

## 3. What you touch, and what you never touch

Other teams' apps live in the same repositories and the same namespace. **Everything you change is either new and
yours, or a single line you add to a shared list.**

| You create (yours) | You add one entry to (shared) | You never change |
|---|---|---|
| `micro-apps/apps/<name>/`, your app's whole folder | `micro-apps/docker-bake.hcl`: one new `target "<name>"` block, plus `"<name>"` in `group "default"` | Any other folder under `apps/`, for example `apps/freelang-search-ui`, `apps/federated-search` and the rest |
| `skipper/environments-configuration/intel360-lambda/<name>.yaml` | `micro-apps/CLAUDE.md`: one bullet for your app | Any other `target` block in `docker-bake.hcl` |
| Your branch `feature/<name>` | `skipper/.../intel360-lambda/skipper.config`: `,<name>` at the end of `APP_RELEASES` | Any other file in `skipper/environments-configuration/` (`freelang-search-ui.yaml`, `i360-chat.yaml`, `analytics.yaml`, ...) and the other entries of `skipper.config` |
| Your Kubernetes deployment `<name>` and your host name | | The `Jenkinsfile` of any repository |
| | | Other deployments in `intel360-lambda`: no `rollout restart`, `scale`, `edit` or `delete` on anything that is not `<name>` |
| | | **platform-hl-api itself** (`elbitbox/analytics`, folder `platform-hl-api/`). Your UI calls it and does not change it. If the UI needs something HL API does not offer, ask the HL API team. |
| | | A host name that is already in use (`kubectl --context ares-cluster -n intel360-lambda get ingress`) |

The existing apps appear in this document only as **evidence that the steps work**. Every template you need is
written out in full below, so you never have to open another app's files to copy from them.

**Check before every push.** The diff must list only the paths from the first two columns:

```bash
git fetch origin && git diff --stat origin/develop...HEAD      # micro-apps: apps/<name>/..., docker-bake.hcl, CLAUDE.md
git fetch origin && git diff --stat origin/master...HEAD       # skipper: <name>.yaml, skipper.config
```

---

## 4. What you need: access checklist

| # | Access | Used for | How to get it | How to check |
|---|---|---|---|---|
| 1 | Work laptop on the e-bitbox network | Every host below | - | `nslookup gitlab.e-bitbox.com` resolves |
| 2 | Read access to the GitHub repository | Cloning the source | Public repo: nothing. Private repo: be a collaborator and sign in when Git asks. **(not exercised)** | `git ls-remote https://github.com/<owner>/<repo>.git HEAD` prints a SHA |
| 3 | GitLab account with **Developer** role on `elbitbox/micro-apps` or `elbitbox/analytics`, and on `elbitbox/skipper` | Pushing a branch, the MR, the skipper values file | A maintainer of the `elbitbox` group adds you | You can open the project and create a branch |
| 4 | GitLab Personal Access Token, scopes `read_repository` + `write_repository` (add `api` only if you script MRs) | `git clone` / `git push` over HTTPS | Section 5.2 | `git ls-remote https://gitlab.e-bitbox.com/elbitbox/skipper.git HEAD` |
| 5 | A teammate who can approve | Merging: the MR needs one approval from the `CR` rule and **the author cannot give it** | Ask a teammate | - |
| 6 | Jenkins login plus an **API token** | Starting builds and the deploy, reading their status | Section 5.3 | `curl -sk -u "<user>:$(cat ~/.jenkins_api_token)" "https://jenkins.e-bitbox.com/me/api/json?tree=id"` returns your id |
| 7 | Personal **kubeconfig** with the context `ares-cluster` | Restarting pods, logs, verification | DevOps issues it: a client certificate per cluster. Ours came with Lens and was copied to `~/.kube/config` | `kubectl --context ares-cluster -n intel360-lambda auth can-i patch deployments` prints `yes` |
| 8 | Tools: Git for Windows (Git Bash + Git Credential Manager), `kubectl`, and the app's own runtime (Node / Python) | - | - | `git --version`, `kubectl version --client` |

**Docker is not needed on the laptop.** Jenkins builds every image. We have no Docker on our laptop and never needed it.

---

## 5. One-time laptop setup

### 5.1 Git

```bash
git config --global user.name  "First Last"
git config --global user.email "<you>@e-bitbox.com"
git config --global credential.helper manager     # Git Credential Manager, ships with Git for Windows
git config --global core.longpaths true           # some repos (core-services) have paths > 260 chars
```

If Git reports "detected dubious ownership" on a clone, run
`git config --global --add safe.directory <full path of the clone>`.

### 5.2 GitLab token

1. Create a token at `https://gitlab.e-bitbox.com/-/user_settings/personal_access_tokens`. Use the scopes from row 4
   above and set an expiry date.
2. On the first `git clone` or `git push`, Git Credential Manager asks for credentials. The username is your GitLab
   username and the **password is the token**. The token is then stored in Windows Credential Manager.
3. **Do not put the token in the remote URL** (`https://oauth2:<token>@gitlab...`). It ends up in plain text in
   `.git/config` of every clone and worktree.
4. When the token expires, pushes fail with `401`. Clear the stored credential and push again with a new token:
   ```bat
   cmdkey /delete:"LegacyGeneric:target=git:https://gitlab.e-bitbox.com"
   ```

### 5.3 Jenkins API token

1. Log in to `https://jenkins.e-bitbox.com`. Open your user menu (top right), then **Security** (on older versions,
   **Configure**), then **API Token**, then **Add new Token**.
2. Save the token in `~/.jenkins_api_token`. Only you should be able to read that file.
3. Scripted calls must use the token. **A password always answers HTTP 500** on the API.

### 5.4 Kubernetes access

```bash
mkdir -p ~/.kube && cp <the kubeconfig you received> ~/.kube/config
# kubectl: put kubectl.exe in a folder on PATH (ours lives in ~/.local/bin)
kubectl config get-contexts                                    # ares-cluster must be listed
kubectl --context ares-cluster -n intel360-lambda get deploy   # lists the LAMBDA deployments
```

- **Always pass `--context ares-cluster`.** The kubeconfig holds several clusters, and Lens switches the current
  context. Commands against the wrong context fail as `Forbidden` or show the wrong pods.
- With the kubeconfig we use, you can read pods and logs, exec into pods, and patch, restart and create deployments
  in `intel360-lambda`. Yours may differ, so check with `kubectl auth can-i`. `kubectl get nodes` is forbidden, which
  is normal. Node problems go to DevOps.

---

## 6. Pick the home repository

**A new UI goes into `elbitbox/micro-apps`, in a new folder `apps/<name>/`.** The `analytics` column is here only
for a backend service that has no page.

| | `elbitbox/micro-apps` (project 159) | `elbitbox/analytics` (project 146) |
|---|---|---|
| Fits | A web app: a page, with or without its own small server | A backend service with no page (Python or Node) |
| Folder | `apps/<name>/`, a new folder | `<name>/` at the repository root, a new folder |
| Already deployed this way (evidence, do not change) | `apps/freelang-search-ui` | `i360-chat/` |
| Register the build | A `target "<name>"` block in `docker-bake.hcl`, plus the name in `group "default"` | One line `{ name = "<name>" },` in the `services` matrix of `docker-bake.hcl` |
| Image | `docker-registry.e-bitbox.com:5000/micro-apps/<name>` | `docker-registry.e-bitbox.com:5000/analytics/<name>` |
| Deployable tag | **Only `develop`.** A feature branch publishes a `-cache` tag only, which cannot be deployed. | The branch name without `feature/`. For example, `feature/i360-chat` becomes the tag `i360-chat`. `develop` becomes `develop`. You can deploy a feature branch before merging. |
| Build trigger | Jenkins polls `develop` every 10-15 min and builds the tip. To build right away, click **Build Now** yourself. | **A push builds nothing.** Start it yourself with `PROJECTS_FILTER=<name>` (section 11). |
| Repo rules to read | Root `CLAUDE.md` | Root `CLAUDE.md`: new-service layout, `docker buildx bake` only, tests inside the build |

Both repositories have the same three rules:

- `develop` is the default branch.
- "Pipelines must succeed" is on.
- The root `Jenkinsfile` says **DO NOT TOUCH**, and that is meant literally.

---

## 7. Bring the code over from GitHub

```bash
# 1. The source, OUTSIDE any GitLab clone
git clone https://github.com/<owner>/<repo>.git ~/src/<repo>
git -C ~/src/<repo> log -1 --format=%H           # note the commit you are importing

# 2. The GitLab monorepo, on a fresh branch off develop
git clone https://gitlab.e-bitbox.com/elbitbox/micro-apps.git ~/src/micro-apps
cd ~/src/micro-apps
git fetch origin
git switch -c feature/<name> origin/develop

# 3. Copy the tracked files only: no .git, no node_modules, no git-ignored .env
mkdir -p apps/<name>                              # analytics: mkdir -p <name>
git -C ~/src/<repo> archive HEAD | tar -x -C apps/<name>
```

`git archive` exports exactly what is committed on GitHub, so anything the GitHub repo ignores stays behind.
Then remove what does not belong in our repository:

- `.github/`: GitHub Actions do not run here. Jenkins does the building.
- Any `.env`, key file, token, or `.claude/settings.local.json` (personal Claude Code permissions). Keep
  `.env.example`. Run a quick scan, and read every hit:
  ```bash
  git grep -n -i -E "password|passwd|secret|token|api[_-]?key|BEGIN .*PRIVATE KEY" -- apps/<name>
  ```
- Committed build output, `node_modules`, and large binaries.

The import is **one commit**. Put the GitHub commit SHA in the commit message and in the MR description. That is the
link back to the source, since the history is not carried over.

---

## 8. Make it deployable: what the cluster expects

Claude-generated projects usually run fine with `npm start` on a laptop and miss what a pod needs. Check every item
below. Each one is something our two services do.

1. **A `Dockerfile` in the app folder.** The folder is the build context, so the image cannot use files outside it.
2. **It listens on `0.0.0.0` and on the port in `$PORT`.** Our services use 4000 (`freelang-search-ui`) and 4020
   (`i360-chat`).
3. **`GET /healthz` answers 200 fast, without authentication.** The liveness and readiness probes call it.
4. **All configuration comes from environment variables.** Nothing points at `localhost`, and no URL or secret is
   hard-coded.
5. **It runs as a non-root user.** On `node:*-slim` that is `USER node`.
6. **A `.dockerignore`** keeps tests, tools, notes and `node_modules` out of the image.
7. **It is stateless if it runs more than one replica.** No sessions in process memory. Both our services carry the
   user's token in an HttpOnly cookie or forward the caller's bearer, so any pod can serve any request.
8. **It calls the platform by in-cluster service name**, for example `http://platform-hl-api:8080`, not the public
   host. We measured the same question at about 2.3 s in-cluster and about 21 s through the public host.
9. **It acts as the signed-in user.** The user signs in with their own i360 account, and the UI's server forwards that
   user's token on every HL API call. The UI holds no service account of its own and never gives visitors a shared login.
10. **The unit tests run inside the image build**, so a failing suite fails the Jenkins build. See the test stage
    below; `analytics` does the same for Python with `pytest`.
11. **Line endings are LF.** Shell scripts checked out with Windows line endings (CRLF) break in Linux containers.
    Add a `.gitattributes` with `* text=auto eol=lf` in the app folder. CRLF already caused a problem in skipper
    (see section 16).
12. **Review it the way you would review an outside contribution**: dependencies and their licences, every outbound
    network call, authentication, and anything that writes data.

A minimal Node Dockerfile, built from our two services:

```dockerfile
# syntax=docker/dockerfile:1
FROM node:20-slim AS base
ENV NODE_ENV=production PORT=4000
WORKDIR /opt/app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev --no-audit --no-fund
COPY src ./src

# Unit tests run inside the build. The runtime stage copies the marker file, so a red suite fails the build.
FROM base AS test
COPY test ./test
RUN node --test test/*.test.js && touch /tmp/unit-tests-passed

FROM base AS runtime
COPY --from=test /tmp/unit-tests-passed /tmp/unit-tests-passed
EXPOSE 4000
USER node
CMD ["node", "src/server.js"]
```

For a Python service in `analytics`, follow the root `CLAUDE.md` of that repository instead: one namespace under
`src/`, tests run in the bake, images built with `docker buildx bake <name>` and never with `docker build`.

---

## 9. Register the image build

**micro-apps.** In the root `docker-bake.hcl` you only **add**. Leave the existing targets exactly as they are.

1. Append this block at the end of the file. It is the same shape as every app target in the file, and no build
   arguments are needed:

   ```hcl
   target "<name>" {
     inherits = ["_base"]
     context = "apps/<name>"
     dockerfile = "Dockerfile"
     tags = [
       "${DOCKER_REGISTRY_TARGET}/<name>:${DOCKER_TAG}"
     ]
     cache-from = [
       { type = "registry", ref = "${DOCKER_REGISTRY_TARGET}/<name>:${ESCAPED_BRANCH_NAME}-cache" },
       { type = "registry", ref = "${DOCKER_REGISTRY_TARGET}/<name>:develop-cache" }
     ]
     cache-to = [
       { type = "registry", ref = "${DOCKER_REGISTRY_TARGET}/<name>:${ESCAPED_BRANCH_NAME}-cache", mode = "max" }
     ]
   }
   ```

2. Add `"<name>",` as a new line at the end of the `targets` list in `group "default"`. Do not reorder or remove the
   other names.
3. Add one bullet for your app under "Repository Structure" in the root `CLAUDE.md`. Do not edit the other bullets.

Jenkins publishes the image as `micro-apps/<name>:develop`. The file's own default prefix, `third-party`, is replaced
by the pipeline. `_base` adds the commit label used in section 11.

**analytics** (a backend service only). In the root `docker-bake.hcl`, add `{ name = "<name>" },` as a new line in
the list inside `target "services"`. The folder name, the build context and the image name are all `<name>`.

Do not touch the `Jenkinsfile` in either repository.

---

## 10. Commit, push, merge request

```bash
git add apps/<name> docker-bake.hcl CLAUDE.md        # explicit paths, never `git add -A`
git commit -m "<name>: import from github.com/<owner>/<repo>@<sha>"
git fetch origin && git rebase origin/develop         # other people merge into develop every day
git diff --stat origin/develop...HEAD                 # only apps/<name>/..., docker-bake.hcl, CLAUDE.md
git push -u origin feature/<name>
```

Open the merge request in GitLab with **target branch `develop`**. Things to know:

- **The pipeline status comes from Jenkins.** The MR shows a status from an external system, not GitLab jobs. In
  `analytics` the MR stays "pipeline running" until the branch build has reported, and a branch build only runs when
  you start one (section 11).
- **One approval from the `CR` rule is required**, from someone other than you.
- **An MR goes stale within hours** because other people merge into develop. Before asking for the merge, run
  `git fetch origin && git rebase origin/develop`, run the tests again, then `git push --force-with-lease`. Only ever
  force-push your own feature branch.

---

## 11. Build the image in Jenkins

Job addresses use the folder `elbitbox`. In URLs, a `/` in a repository or branch name is written **`%252F`** (double
encoded):

| Job | URL |
|---|---|
| micro-apps, develop | `https://jenkins.e-bitbox.com/job/elbitbox/job/elbitbox%252Fmicro-apps/job/develop` |
| analytics, a branch | `https://jenkins.e-bitbox.com/job/elbitbox/job/elbitbox%252Fanalytics/job/feature%252F<name>` |
| skipper, master (the deploy) | `https://jenkins.e-bitbox.com/job/elbitbox/job/elbitbox%252Fskipper/job/master` |

**micro-apps (a new UI).** After the merge, open the `develop` job and click **Build Now**. A build takes about 3
minutes. Without this, the poll may fold your merge into a later build. The build bakes every target in
`group "default"` from the same `develop` tip, the same as every poll does. It does not restart anyone's pods.

**analytics (a backend service only).**

1. A new branch is not known to Jenkins until it is scanned. On the `elbitbox/analytics` multibranch page, click
   **Scan Multibranch Pipeline Now**.
2. On the branch job, click **Build with Parameters** and set `PROJECTS_FILTER=<name>`. Executors are scarce, and at
   night the queue can be 30-60 minutes.

The same thing from Git Bash. This is the crumb-and-token pattern we use for our own builds:

```bash
J="https://jenkins.e-bitbox.com/job/elbitbox/job/elbitbox%252Fmicro-apps/job/develop"
AUTH="<jenkins-user>:$(cat ~/.jenkins_api_token)"
JAR=$(mktemp)
CRUMB=$(curl -sk -c "$JAR" -u "$AUTH" https://jenkins.e-bitbox.com/crumbIssuer/api/json \
  | node -e "let s='';process.stdin.on('data',d=>s+=d).on('end',()=>{const j=JSON.parse(s);console.log(j.crumbRequestField+':'+j.crumb)})")
curl -sk -b "$JAR" -u "$AUTH" -H "$CRUMB" -o /dev/null -w '%{http_code}\n' -X POST "$J/build"   # 201 = queued
curl -skg -u "$AUTH" "$J/lastBuild/api/json?tree=number,result,building"
```

For an analytics branch, set `J` to the branch job and POST `"$J/buildWithParameters?PROJECTS_FILTER=<name>"`
instead of `"$J/build"`.

| Answer | Meaning |
|---|---|
| `201` | The build is queued |
| `400 Nothing is submitted` | The job takes parameters: use `buildWithParameters?...` |
| `403` | The crumb or its cookie jar is missing: send both |
| `500` | Password authentication: use the API token |

**Check that the image exists.** Reading the registry needs no login:

```bash
curl -skI -H "Accept: application/vnd.docker.distribution.manifest.v2+json" \
  https://docker-registry.e-bitbox.com:5000/v2/micro-apps/<name>/manifests/develop \
  | grep -i -E "^HTTP|docker-content-digest"
```

`200` plus a `Docker-Content-Digest` means the image is there. If the digest is the same as before the build, the
registry still serves the old image.

**Check which commit the image was built from.** Both pipelines write the commit into the image label
`org.opencontainers.image.revision`. Save this script as `image-revision.js` and run
`node image-revision.js micro-apps/<name> develop`:

```js
process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0';
const [repo, tag] = process.argv.slice(2);
const R = `https://docker-registry.e-bitbox.com:5000/v2/${repo}`;
const ACCEPT = 'application/vnd.oci.image.index.v1+json,application/vnd.oci.image.manifest.v1+json,' +
  'application/vnd.docker.distribution.manifest.list.v2+json,application/vnd.docker.distribution.manifest.v2+json';
const get = async (p) => (await fetch(R + p, { headers: { Accept: ACCEPT } })).json();
(async () => {
  let m = await get(`/manifests/${tag}`);
  if (m.manifests) m = await get(`/manifests/${(m.manifests.find((x) => x.platform?.architecture === 'amd64') || m.manifests[0]).digest}`);
  console.log((await get(`/blobs/${m.config.digest}`)).config.Labels['org.opencontainers.image.revision']);
})();
```

The SHA it prints must be your merge commit (micro-apps) or your branch tip (analytics). A green Jenkins build can
be older than your push, so check the SHA rather than the colour.

---

## 12. Create the LAMBDA release in skipper

```bash
git clone https://gitlab.e-bitbox.com/elbitbox/skipper.git ~/src/skipper
cd ~/src/skipper && git switch master && git pull --rebase
```

- **Skipper accepts pushes to `master` only.** A server hook rejects any other branch name. Master is shared by about
  25 environments and moves often.
- **Create a new file `environments-configuration/intel360-lambda/<name>.yaml`.** Do not edit any existing file in
  that folder. This is the complete template for a new UI:

```yaml
# <name>: <one line on what it is>. Code: elbitbox/micro-apps apps/<name>; image tag = develop.
default:
    image:
        repository: docker-registry.e-bitbox.com:5000      # analytics: docker-registry.e-bitbox.com:5000/analytics
        pullPolicy: Always
        pullSecret: docker-registry-credentials

services:
    <name>:
        image:
            name: micro-apps/<name>                        # analytics: <name>
            tag: develop                                   # analytics feature branch: the branch without feature/
        enabled: true
        replicaCount: 1                                    # the chart reads replicaCount; a "replicas" key is ignored
        envVars:
            NODE_ENV: production
            PORT: "4000"
            HLAPI_BASE_URL: http://platform-hl-api:8080    # in-cluster address of the platform API
        service:
            - port: 4000
        livenessProbe:
            httpGet: { path: /healthz, port: 4000 }
            periodSeconds: 30
        readinessProbe:
            httpGet: { path: /healthz, port: 4000 }
            periodSeconds: 10
        ingress:                                           # leave out for an internal-only service
            paths:
                - /
            hosts:
                - <host>.intel360.lambda.projects.e-bitbox.com
```

- **Register the release.** In `environments-configuration/intel360-lambda/skipper.config`, add `,<name>` at the end
  of the `simple-service-template=1.2.x:...` list in `APP_RELEASES`. That is the only change to this file: leave the
  other names and the other lines as they are. Because it is a release of its own, deploying it moves only your pods.
- **Host name.** Any `<host>.intel360.lambda.projects.e-bitbox.com` already resolves: a wildcard DNS entry points it
  at the LAMBDA ingress (Traefik), and an unused name answers 404. You do not need a DNS ticket. Pick a name nothing
  else uses: `kubectl --context ares-cluster -n intel360-lambda get ingress`.
- **HL API.** `HLAPI_BASE_URL: http://platform-hl-api:8080` is the in-cluster address of HL API. Your UI's server
  forwards each user's own token to it. Do not call other apps' servers: they are not an API for you.
- **Credentials.** `envVars` are plain text in git, readable by everyone with access to skipper. Design the app so it
  needs none (forward the caller's token). We have not used a Kubernetes Secret with this chart **(not exercised)**,
  so ask DevOps before you add one.
- **Commit and push:**

```bash
git add environments-configuration/intel360-lambda/<name>.yaml environments-configuration/intel360-lambda/skipper.config
git commit -m "intel360-lambda: add <name>"
git fetch origin && git rebase origin/master
git show --stat HEAD                              # exactly these two files
git show HEAD                                     # read the diff before pushing
git push origin master
```

  If the rebase conflicts on `skipper.config`, someone else changed the version numbers in `INFRA_RELEASES`. Take
  origin's file and re-apply your one change in `APP_RELEASES`. Conflict markers were once committed into this file
  and caught only by reading `git show`, so read it before you push.

---

## 13. Deploy to LAMBDA

**Ask the LAMBDA owner before you deploy.** The deploy job applies whatever is on skipper `master` for the whole
environment, including changes other people have pushed and not yet deployed.

In Jenkins, open `elbitbox » elbitbox/skipper » master` and click **Build with Parameters**:

| Parameter | Value |
|---|---|
| `ENVIRONMENT_NAME` | `intel360-lambda` |
| `SKIPPER_COMMAND` | `build deploy app job` (the default) |
| All the others | empty |

This is how LAMBDA is normally deployed. The latest such run was build #58484 on 2026-10-06, and it succeeded.
Scripted, it is the same crumb pattern as section 11 with
`-X POST ".../job/elbitbox%252Fskipper/job/master/buildWithParameters?ENVIRONMENT_NAME=intel360-lambda"`.

**Never run `./skipper deploy` from a Windows checkout.** Skipper is written for Linux:

- The per-environment `common` folder is a git symlink. On Windows it is checked out as a small text file.
- The deploy script that skipper generates then drops the shared values layer. We rendered it once: 79 of 82 objects
  of a release changed, and two deployments would have been deleted.
- CRLF line endings also rewrite ConfigMaps.

The Jenkins job runs on Linux and has neither problem.

**A new image under the same tag** (every later micro-apps deploy, and every analytics branch rebuild) changes
nothing in skipper, so the pods keep the old image. Restart **your own deployment only**, never another app's.
Because of `pullPolicy: Always`, the new pods pull the new digest:

```bash
kubectl --context ares-cluster -n intel360-lambda rollout restart deployment/<name>
kubectl --context ares-cluster -n intel360-lambda rollout status  deployment/<name> --timeout=180s
```

---

## 14. Verify on LAMBDA

```bash
K="kubectl --context ares-cluster -n intel360-lambda"
$K get deploy <name>                                         # READY n/n
$K get pods -l app.kubernetes.io/name=<name> \
  -o jsonpath='{range .items[*]}{.metadata.name}{" "}{.status.containerStatuses[0].imageID}{"\n"}{end}'
$K logs deploy/<name> --tail=100
curl -sk -o /dev/null -w '%{http_code}\n' https://<host>.intel360.lambda.projects.e-bitbox.com/healthz   # 200
```

- The digest in each pod's `imageID` must equal the registry's `Docker-Content-Digest` from section 11. If it does
  not, the pod still runs an older image.
- Then sign in through the public host as a real user and use the feature you shipped. **It is done when it works on
  LAMBDA**, not when the build is green.

---

## 15. Shipping changes later

| Change | Steps |
|---|---|
| Code | Branch, MR, merge (section 10), build (11), `rollout restart` (13), verify (14) |
| Environment variables, replicas, host | Edit `<name>.yaml` in skipper, push `master`, run the skipper job (13) |

Changes made by hand with `kubectl` (`scale`, `set env`, `edit`) do not last. The next skipper deploy re-applies the
values file, so change the YAML instead.

---

## 16. Troubleshooting

Every problem in this table actually happened to us.

| Symptom | Cause | Fix |
|---|---|---|
| `git push` returns `401` | The GitLab token expired | `cmdkey /delete:"LegacyGeneric:target=git:https://gitlab.e-bitbox.com"`, create a new token, push again |
| "Filename too long" on clone | Windows path limit | `git config --global core.longpaths true` |
| "detected dubious ownership" | Windows folder owner check | `git config --global --add safe.directory <path>` |
| Jenkins API answers `500` | You used a password | Use the API token |
| Jenkins `400 Nothing is submitted` | The job takes parameters | `buildWithParameters?PROJECTS_FILTER=<name>` |
| Jenkins `403` on a POST | No crumb, or the crumb was sent without its cookie jar | Fetch `/crumbIssuer/api/json` with `-c jar`, send it with `-b jar` |
| A new analytics branch never builds | Jenkins has not discovered it, and pushes do not start builds | **Scan Multibranch Pipeline Now**, then build with `PROJECTS_FILTER` |
| A micro-apps feature branch has no image | By design: feature branches publish a `-cache` tag only | Merge to `develop` and build `develop` |
| Your merge has no build of its own | `develop` is polled and the tip is built, so merges fold together | Click **Build Now**, then check the image's revision label |
| The registry answers `500` on blob upload during a build | Registry storage, not your code (seen 2026-09-25) | Re-run the build. If it repeats, tell DevOps |
| Pod `ImagePullBackOff` | The tag does not exist, or the values file has a typo in `repository`/`name` | Check the manifest URL from section 11. The pull secret is `docker-registry-credentials` |
| The pod runs old code after a successful build | Same tag, and pods do not roll by themselves | `rollout restart`, then compare `imageID` with the registry digest |
| `kubectl` returns `Forbidden`, or shows the wrong pods | The current context is not `ares-cluster` (Lens changes it) | Pass `--context ares-cluster` on every command |
| Platform calls are far slower than expected (we measured about 21 s against 2.3 s for the same question) | The app calls the platform through its public URL | Use the in-cluster name, for example `http://platform-hl-api:8080` |
| AI features answer `503` at night | The LLM servers are switched off every night on purpose. LAMBDA itself stays up | Expected. Test AI features during the day |
| Strange changes in ConfigMaps or deployments after a local skipper run | The Windows symlink and CRLF trap (section 13) | Deploy only through the Jenkins skipper job |

---

## 17. Not exercised by us

- Cloning a **private** GitHub repository. Git Credential Manager should offer a GitHub sign-in on first use, or use
  a fine-grained token with read-only "Contents" permission.
- Giving an app its **own GitLab project and Jenkins job** instead of a monorepo folder. That needs DevOps.
- Using **Kubernetes Secrets** with `simple-service-template`.
- **Building images on the laptop.** Jenkins built every image we deployed.

---

## Appendix A: how this document was verified (2026-10-06)

| Fact | How it was checked | Result |
|---|---|---|
| LAMBDA is `intel360-lambda` on `ares-cluster` | `KUBECONTEXT` and `NAMESPACE` in `skipper.config`; `kubectl get deploy` | Both services listed, 2/2 ready |
| Developers cannot create GitLab projects | GitLab API `GET /user` | `can_create_project: false`, `projects_limit: 0` |
| micro-apps 159 and analytics 146 use `develop` and require a passing pipeline; skipper 70 uses `master` | GitLab API `GET /projects/...` | As stated |
| Running image paths and tags | `kubectl get deploy -o wide` | `micro-apps/freelang-search-ui:develop`, `analytics/i360-chat:i360-chat` |
| The registry can be read without login, and pods run the registry's digest | Registry manifest `HEAD`, compared with the pods' `imageID` | `200`; digests equal (`sha256:ffe382da...` for freelang-search-ui) |
| The image label carries the commit | `image-revision.js` on both images | freelang-search-ui = `origin/develop` tip `9a982aa`; i360-chat = `499d286c` |
| The micro-apps `develop` job takes no parameters; analytics branch builds use `PROJECTS_FILTER` | Jenkins API | As stated; the last i360-chat build used `PROJECTS_FILTER=i360-chat` |
| The skipper job's parameters and their defaults | Jenkins API | `ENVIRONMENT_NAME`, and `SKIPPER_COMMAND` with default `build deploy app job`; LAMBDA build #58484 succeeded |
| The Jenkins API refuses a password | Wrong-password call | `500` |
| Wildcard DNS for LAMBDA hosts | `nslookup` of an unused name; HTTPS request | Resolves to the LAMBDA ingress; answers `404` |
| A live app answers through its host | `GET https://freelang-search.intel360.lambda.projects.e-bitbox.com/healthz` | `200` |
| Developer RBAC in the namespace | `kubectl auth can-i ...` | Patch/create deployments, delete pods, exec, logs: yes. Nodes: forbidden |
| GitHub is reachable from the work network | `git ls-remote` against a public GitHub repo | Returned a SHA |
| Copying with `git archive \| tar` works in Git Bash | Ran it on a cloned GitHub repo | Tracked files copied, no `.git` |

# AI Intelligence

Bilingual (Hebrew/English) intelligence-analysis UI with Kosovo and Syria demo scenarios.

**Branch `feature/i360-only`:** the app runs on i360. Users sign in with their i360 account, data is read from i360 and saved work is stored in i360, all through platform-hl-api with the user's own token. There is no local data, local state or AI on this branch.

| Guide | Owns |
|---|---|
| [Architecture](docs/architecture.md) | Shape, identity, reading data, saved work |
| [Operations](docs/operations.md) | Configuration, local run with the fake HL API, tests, first use on an estate, LAMBDA deployment |
| [Product](docs/product.md) | Analyst workflows |
| [Demo scenarios](docs/demo-scenarios.md) | Dataset contents and narratives |
| [Decisions](docs/decisions.md) | Accepted decisions and their rationale |

The application is in [llm_investigation_orchestrator_serbia_poc/](llm_investigation_orchestrator_serbia_poc/). Contributors start with [AGENTS.md](AGENTS.md).

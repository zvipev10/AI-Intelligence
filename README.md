# AI Intelligence

One shared bilingual intelligence-analysis application, with isolated Kosovo and Syria demo packages and one active scenario at a time. General, Moshe and Talia roles share the application while retaining their authorization and memory boundaries.

## Documentation

| Guide | Owns |
|---|---|
| [Product](docs/product.md) | Analyst workflows, agent roles, results and media behavior |
| [Architecture](docs/architecture.md) | Services, state ownership and interface contracts |
| [Demo scenarios](docs/demo-scenarios.md) | Dataset versions, contents and demonstration narratives |
| [Operations](docs/operations.md) | Setup, deployment, switching, verification and rollback |
| [Decisions](docs/decisions.md) | Accepted decisions and their rationale |

The [application package](llm_investigation_orchestrator_serbia_poc/) is the canonical implementation. Check `/api/status` and the installed release manifest for live deployment identity. All demonstration data is synthetic; evaluator truth stays offline and out of runtime retrieval and prompts.

Contributors start with [AGENTS.md](AGENTS.md) and the [AI workflow](docs/ai-workflow.md). Task-specific reviews, checkpoints and handoffs live under [.ai/work/capabilities/](.ai/work/capabilities/). These are implementation history, not competing current guides. The [migration map](.ai/work/capabilities/documentation-hierarchy/migration-map.md) provides the complete pre-consolidation archive.

# Checkpoint 012 — Semantic cache recovery after UAV source-type migration

Date: 2026-07-22

## Incident

After the canonical UAV source type changed to `וידאו מכטב"מ`, the deployed V2.1
projection no longer matched the manifest of semantic index v11. Semantic calls
attempted an in-process rebuild on the constrained VM, exceeded the 30-second MCP
timeout, and caused subsequent tools and end-to-end questions to stall.

## Recovery

- Rebuilt the portable V2.1 hybrid semantic cache locally with NumPy disabled so
  its manifest matches the VM's pure-Python `dense_only` runtime.
- Validated all 300 fusion chains with 600/600 public confirmations recalled.
- Installed the cache at
  `/opt/serbia-poc/data/semantic_index/v2_1/semantic_event_index_hybrid_embedding.pkl`.
- Capped semantic candidate retrieval at 200 while preserving the existing
  2,000-row deterministic search and aggregation coverage policy.
- Restarted the General and Moshe Hermes gateways.

## Production artifacts

- Cache SHA-256: `47dd73765aab79643fa27c8fc0fc921b0eedc865d2ba42e715ee16c4a2db86f5`
- Cache size: `50,806,634` bytes
- Dataset SHA-256 in the manifest:
  `016786636148671f5276d3decbe5f286f2e4be2466efad565b3b44625afe0581`
- Cache rollback: `/opt/serbia-poc/backups/semantic-index-20260722T000300Z`
- MCP server rollback: `/opt/serbia-poc/backups/semantic-limit-20260722T001249Z`

## Validation

- Local portable-cache build: 14,800 records, 3,800 UAV records, 600/600 fusion
  confirmations, and semantic query latency of 0.017–0.081 seconds after build.
- Local focused regression suite: 16 tests passed.
- Production cold semantic call: 21.586 seconds, 200 requested and returned.
- Production warm semantic call: 1.255 seconds, 50 requested and returned.
- Exact failed question returned HTTP 200 with an 866-character answer, 39 evidence
  IDs, and 15 investigation steps.
- No MCP timeout, unreachable, or reconnect errors occurred in the final run.
- `hermes-gateway.service`, `hermes-moshe-gateway.service`, and
  `serbia-poc-ui.service` were active after validation.
- UI status remained V2.1 with 14,800 rows.

## Follow-up

Any future projection mutation must rebuild and validate the portable semantic
cache before deployment. The projection and cache manifest hashes should be a
release gate.

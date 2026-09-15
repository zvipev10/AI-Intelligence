# Deployment incident — 2026-09-15

## State
- Release commits `8aff2ad` and `0eb0e36` are pushed to `main`.
- The MCP/evidence files were uploaded and installed on the production VM.
- The corrected deployment advanced into its built-in live benchmark after gateway restart.
- The benchmark did not return; the local waiter was interrupted.
- Subsequent SSH banner exchanges and HTTP health requests timed out, consistent with VM resource saturation.
- The UI release was intentionally not deployed while backend health was unknown.

## Recovery sequence
1. Restore VM responsiveness through the hosting console if it does not recover naturally.
2. Check and stop any orphaned `benchmark_tools.py` process.
3. Verify `hermes-gateway.service`, default and Moshe evidence allowlists, and MCP server version `0.4.0`.
4. Run direct deterministic MCP evidence smoke tests without the live model benchmark.
5. Deploy the UI and verify `/api/health`, English/Hebrew evidence presentation, and provenance.

## Prevention
Split deterministic deployment smoke tests from model-backed performance benchmarks so a release to this 1 GB VM cannot be blocked by benchmark resource pressure.

# General instruction A/B test status

- Phase: implementation deployed; benchmark preparation
- Owner/action now: development
- Goal: compare the current inline General instructions with a persistent Hermes General profile while holding request, model, tools, state, and data constant.
- Current scope: isolated profile scaffold, explicit request routing, instruction/request-size telemetry, and paired benchmark runner.
- Default behavior: unchanged; omitted or invalid `instruction_mode` values use `inline`.
- Safety boundary: the persistent profile reuses General's existing MCP configuration, has a separate audit log, and is selected only by explicit benchmark traffic. Ordinary UI traffic remains inline.
- Completed: profile contract and service unit; port-8644 endpoint configuration; backend `inline|persistent` switch; performance metadata; alternating paired-run harness; isolated VM deployment.
- Validation: Python compilation passed; 43 existing regressions passed locally; all 6 profile-specific tests passed on the VM; ports 8642, 8643, 8644, and 8769 are healthy. Identical read-only smoke requests succeeded through both modes with the same answer and appropriate tool flow.
- Preliminary smoke only: persistent reduced request instructions from 33,206 to 1,460 bytes and provider input usage from 81,017 to 36,311 tokens. Its single observed total latency was 45.1 seconds versus 38.8 seconds inline, so no latency conclusion is valid before the paired run.
- Next artifact: 12-pair benchmark report and blinded quality comparison.

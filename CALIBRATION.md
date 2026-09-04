# Calibration record — Claude Fable 5.1

**Status:** `empirically-exercised`, not `empirically-calibrated`
**Calibration vocabulary:** `empirically-exercised` applies to this named replacement pilot; it is not a universal or production calibration.
**Date:** 2026-09-03
**Model ID:** `claude-fable-5-1`
**Harness:** Claude Code 2.1.258
**Experiment:** FPL (Foundation Project Labs) replacement calibration suite

## Method

Three dependency-free controls were run at each of the five Claude Code effort levels: `low`, `medium`, `high`, `xhigh`, and `max`. Each cell used a fresh disposable directory, the same frozen prompt and baseline, no session resume, and an external deterministic evaluator. The original Mark Kashef prompt `.txt` files were not available in the local guide download, so this is a replacement suite rather than a reproduction.

## Controls

| Control | Task shape | Low result | All levels |
|---|---|---:|---:|
| A | Known-shape tag normalization | PASS | PASS |
| B | Small multi-file order-cancellation feature | PASS | PASS |
| C | Seeded ambiguous replay/input-mutation bug | PASS | PASS |

All 15 cells passed visible tests, hidden tests, and corrected scope checks. All three pristine baselines failed their hidden evaluator, confirming evaluator sensitivity.

Raw prompts, per-cell JSON receipts, and evaluator logs are retained in the internal calibration workspace and are not packaged in this repository. This summary is therefore not independently reproducible from the public repository alone.

## Interpretation

The suite shows that Fable 5.1 completed these small, clearly specified tasks at low effort. This is not a universal production calibration, and Control C was not hard enough to establish the high/xhigh boundary. Keep task-specific selection:

- known shape / narrow change → low candidate;
- everyday work → medium candidate;
- genuine ambiguity, architecture, security, or independent verification → high candidate;
- long unattended multi-file work → xhigh candidate when justified;
- max → rare linchpin only when a material, repeatable gain is worth the cost.

The sweep's cost and token receipts are local experiment artifacts, not an Anthropic billing statement.

## Official documentation used

- Anthropic Fable 5.1 prompting guidance: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- Claude Code model configuration: https://docs.anthropic.com/en/docs/claude-code/model-config
- Fable 5.1 model overview: https://platform.claude.com/docs/en/models/fable-5-1/overview

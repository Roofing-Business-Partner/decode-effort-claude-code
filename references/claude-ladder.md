# Claude Code / Anthropic ladder

Sources: Anthropic Claude Code/Fable 5.1 documentation (reviewed 2026-09-03) plus Mark Kashef Effort Decoder video/guide (July 2026), mapped for Adam’s dual-machine setup.

## Effort values (API / CLI)

`low` · `medium` · `high` · `xhigh` · `max`

- **Unset ≈ high** (factory default on Claude)
- CLI: `claude --effort low` (also medium, high, xhigh, max)
- UI may show “effort” or thinking controls depending on product surface
- Anthropic: effort is a **behavioral signal**, not a hard token cap

## Model pick (2026 operator defaults — adjust as Adam’s fleet changes)

| Role | Typical pick | When |
|------|--------------|------|
| Workhorse | Sonnet-class | execution, everyday coding, most PRs, UI/docs/Excel-style generation |
| Frontier / judgment | Opus-class (or current flagship) | architecture, verification, ambiguous design, high-stakes |
| Fast/cheap | Haiku-class | tiny transforms only if available in this product |
| Long-horizon frontier | Claude Fable 5.1 | demanding reasoning, long-running agentic work, and research when task-specific evidence justifies it |

**Order:** pick workhorse vs frontier **first**, then effort.

## Claude Fable 5.1 current guidance

- Claude Code alias: `fable`; pin the full model ID `claude-fable-5-1` for a reproducible experiment.
- In Claude Code v2.1.255 or later, the `fable` alias resolves to Fable 5.1; use the full model ID to pin an experiment.
- Fable 5.1 uses always-on adaptive thinking and documents `high` as its default effort.
- Re-sweep effort levels after a model-generation change; `low`, `medium`, `high`, `xhigh`, and `max` are labels, not portable amounts of thinking.
- Anthropic recommends starting at `high` for Fable 5.1, then moving down or up according to task-specific evals. This differs from a blanket “always start low” shortcut: the decoder still chooses by task shape and evidence.
- At low effort, Fable 5.1 may call search/retrieval less often. Current-state or name-sensitive tasks need an explicit search/verification requirement.
- Do not default to `xhigh` or `max` for long prose/code merely because the task is important; leave room for the final output and require a measured quality gain.

### Calibration status

**Status:** `empirically-exercised`, not `empirically-calibrated`. The 2026-09-03 FPL replacement pilot ran three small dependency-free controls at all five effort levels. Every cell passed its external evaluator, including low effort. The ambiguous control was not hard enough to establish the high/xhigh boundary, so the result does not make low a universal setting.

Keep high for genuine architecture, security, independent verification, and other judgment-heavy work; keep xhigh for long unattended multi-file work when the task and budget justify it.

Mark’s intentional rhythm (video):
1. Sonnet low/medium for majority of generation work
2. Frontier only when deeper analysis is needed — start at **low**, climb on evidence
3. Newest flagship low often beats last-gen extra high

## Mapping universal → Claude

| Universal | Claude `--effort` | Notes |
|-----------|-------------------|--------|
| FLOOR | `low` (closest) | Claude may not have true `none` on flagships |
| LOW | `low` | doorway; use more than people think on Opus-class |
| MEDIUM | `medium` | everyday |
| HIGH | `high` | default if unset; nuclear-for-fistfight for most tasks |
| XHIGH | `xhigh` | war room; Anthropic guidance ~agentic **>30 min** |
| MAX | `max` | committee; overthink risk; rare |

## Dual-machine note

On second computer Claude B, same ladder. Prefer lower effort for scoped module work; reserve xhigh/max for Mini long runs when possible (quota).

## Claude-specific gotchas

- Unset = high → most “I never touched the dial” bills are high
- Subagents inherit parent effort
- New gen medium ≈ old gen high (label drift) — reset dial on model upgrades
- Fable 5.1 default effort is documented as high; local confidence is `empirically-exercised`, not a general production calibration
- Model Pulse video: Claude low–medium often “good enough”; extra high/max bought polish (favicon), not insight

# Claude Code / Anthropic ladder

Source: Mark Kashef Effort Decoder video + guide (July 2026), mapped for Adam’s dual-machine setup.

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

**Order:** pick workhorse vs frontier **first**, then effort.

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
- Model Pulse video: Claude low–medium often “good enough”; extra high/max bought polish (favicon), not insight

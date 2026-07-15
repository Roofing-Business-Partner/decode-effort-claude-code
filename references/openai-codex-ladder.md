# Codex / OpenAI ladder

Source: Mark Kashef Effort Decoder video + guide (July 2026), mapped for Adam’s dual-machine / Codex Max setup.

## Reasoning effort values (API)

`none` · `low` · `medium` · `high` · `xhigh` · `max`

- CLI: `codex -c model_reasoning_effort=low` (swap value)
- **Default if unset ≈ medium**
- Codex **app UI renames:**
  - `low` → **Light**
  - `xhigh` → **Extra High**
  - UI may show **Ultra** — API often **rejects** `ultra`; never recommend Ultra as an API effort value
- ChatGPT “Extra High” ≈ `xhigh`; Instant may be a different/older model — not the same as effort
- OpenAI documents that supported values are **model-dependent**

## Model pick (2026 operator defaults)

| Role | Typical pick | When |
|------|--------------|------|
| Workhorse | GPT-class coding default in Codex | everyday implementation |
| Frontier | strongest available coding/reasoning model in the plan (e.g. GPT-5.6 family tiers) | architecture, hard debug, verification |
| Floor | same model + `none` | pure classify/tag/template if supported |

Video note: GPT-5.6 family (Luna / Terra / Soul) × six effort tiers ≈ **18 combinations** — model first collapses the chaos.

**Order:** model first, then reasoning effort.

## Mapping universal → Codex

| Universal | `model_reasoning_effort` | UI label (Codex app) |
|-----------|--------------------------|----------------------|
| FLOOR | `none` | (if shown) off / none |
| LOW | `low` | **Light** |
| MEDIUM | `medium` | Medium (default) |
| HIGH | `high` | High |
| XHIGH | `xhigh` | **Extra High** |
| MAX | `max` | Max (enable in settings if hidden) |

## Dual-machine / Codex Max plan

Second email Codex Max: same ladder. Prefer Light/medium for scoped lanes; Extra High/max only for long unattended or linchpin work. Subagents inherit parent effort — don't set Extra High on a parent that fans out.

## Codex-specific gotchas

- App Ultra ≠ valid API effort
- Max may be hidden until enabled in settings
- Auto-switching surfaces (ChatGPT) can change effort mid-conversation
- Model Pulse video: Codex low already looked strong; higher rungs mostly re-skinned the same dashboard (neo-brutalist chrome, donut chart, favicon) without functional novelty
- Better prompt on medium > vague prompt on max

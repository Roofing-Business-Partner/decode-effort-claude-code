---
name: decode-effort
description: "User-only slash command. Recommend Claude model + effort for this session, a Linear issue (ADA-###), or pasted task text. Mark Kashef Effort Decoder. Never auto-run."
disable-model-invocation: true
user-invocable: true
argument-hint: "[session | ADA-### | free-text task]"
version: 1.3.0
author: Claudio / Adam Sand (source: Mark Kashef)
license: MIT
---

# /decode-effort — Claude Code Edition

**User-invocable only.** Recommend **model + effort** for a task. Do **not** load on ordinary coding turns.

You are in **Claude Code**. Use Claude effort labels. Optionally note the Codex equivalent for dual-machine planning.

## Slash forms (all the same skill)

- `/decode-effort`
- `/decode-effort session`
- `/decode-effort ADA-123`
- `/decode-effort <task description>`
- Treat `/decode effort` (space) as this skill

## Args

| Arg | What to decode |
|-----|----------------|
| empty or `session` | **This conversation** — last user ask + active goal + files/risk already in thread |
| `ADA-###` / `ada-###` | Linear issue title, description, comments if tools allow; else ask Adam to paste |
| free text | That task only |

## Procedure

1. **Harness lock:** Claude Code → read `references/claude-ladder.md` for native labels.
2. **Always** read `references/effort-decoder-core.md`.
3. **Build task brief** (1–2 lines) from:
   - session: current goal, last user ask, scope/risk already discussed
   - Linear: title + description + open questions / acceptance criteria
   - free text: as given
4. Score difficulty signals (use core decision tree):
   - known shape vs ambiguous
   - attended vs unattended
   - operating mode: actively watched single-session, unattended, or parallel-session; use this for context/handoff counsel, not automatic effort inflation
   - single-file vs multi-file
   - risk if wrong (schema, security, multi-tenant, credentials)
   - verification-of-another-agent vs original build
5. **Model first** (workhorse vs frontier/current model), then **effort**. The generic calibration prior is to start low and climb only on evidence; when a provider documents a model-specific default, state it. For Fable 5.1, Anthropic documents `high` as the default, so do not silently collapse that fact into a universal low rule.
6. Emit **Output contract** exactly.
7. **Recommend only** — do not change model/effort unless Adam says “set it.”

## Output contract (required)

```markdown
### Effort decode
- **Harness:** Claude Code
- **Task:** <1–2 lines>
- **Difficulty:** low | medium | high | long-agentic | linchpin
- **Operating mode:** actively watched single-session | unattended | parallel-session
- **Model:** <workhorse or frontier + name if known>
- **Effort:** `<native>` (universal: FLOOR|LOW|MEDIUM|HIGH|XHIGH|MAX · metaphor)
- **Set it:** `claude --effort <native>`
- **Why:** <map to decision tree>
- **Climb if:** <concrete failure signals>
- **Codex twin (optional):** model + `model_reasoning_effort=…` if dual-machine
- **Quota:** subagents inherit; avoid xhigh/max parent fan-out
- **Calibration:** official-guidance-only | empirically-exercised | empirically-calibrated | stale/unknown
- **Confidence:** high | medium | low
```

## Adam bias

- Laptop-B / second Claude account: prefer lower effort for scoped lanes
- Mini long unattended: xhigh only when justified
- Verification sessions: frontier + **high**
- Known-shape fixes: workhorse + **low**/**medium**
- Fable 5.1's documented default effort is **high**; do not assume an effort label carries the same meaning across model generations
- If the current model generation is not named in the ladder's calibration record, downgrade confidence rather than inventing a calibrated result

## Sources

- `references/effort-decoder-core.md`
- `references/claude-ladder.md`
- `references/openai-codex-ladder.md`
- Video: https://youtu.be/4__5q76f04s
- Anthropic Fable 5.1 prompting guidance: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1
- Anthropic Claude Code model configuration: https://docs.anthropic.com/en/docs/claude-code/model-config
- Guide: `AgentOps/raw/guides/2026-07-15-effort-decoder-guide-mark-kashef.pdf`

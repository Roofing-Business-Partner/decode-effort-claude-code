# Effort Decoder Core (Mark Kashef / Early AI Dopters, July 2026)

Sources:
- Video: *THIS Is the AI Setting Everyone Gets Wrong* — https://youtu.be/4__5q76f04s
- Companion PDF: `AgentOps/raw/guides/2026-07-15-effort-decoder-guide-mark-kashef.pdf`
- Used by `/decode-effort` (Claude Code + Codex editions)

## What effort actually is

A **budget for how long the model is allowed to think** before it answers.

- Same model, same knowledge, same intelligence at every rung
- More effort = more **output tokens** (expensive) + more waiting
- **Not** a smarter model
- **Not** more knowledge
- Vendors describe it as how eager the model is about spending tokens

Vendors name the same knob differently:
- Anthropic: **effort**
- OpenAI / xAI: **reasoning effort**
- Google: **thinking level**

## The addiction pattern (why people get this wrong)

People treat effort like a slot machine / intelligence proxy:
- Assume higher = smarter
- Live permanently on high / extra high / max
- Never risk low or medium — even on frontier models where low is enough

**Insurance psychology:** “I’d rather overkill an easy task than risk a wrong answer.” Fair — but you pay insurance premiums on tasks that were never going to crash.

**Overstudied exam:** Study a multiple-choice question too long and you talk yourself out of B into D. Max can **hurt accuracy**, not just cost. Anthropic’s own docs: max “can lead to overthinking.”

## Model vs harness (brain in a jar)

The model is a brain in a jar: text in, text/media out. It has no limbs.

The **harness** is the limbs: files, shell, tests, skills, MCP, permissions, checks.

Google vibe-coding whitepaper rule of thumb (directional, not lab-precise): ~**10% model / 90% harness**. Terminal-Bench and Princeton harness studies show large gains with a fixed model by redesigning only the harness.

**Implication:** cranking effort pays the brain to sit in the jar longer. It upgrades none of the hands and legs. Maxing the dial so often buys nothing.

## Core workflow (any provider)

1. **Pick the model first** — cheapest that reliably finishes (workhorse for execution, frontier for judgment)
2. **Start low**
3. **Climb one rung only when output is wrong/shallow** — never on vibes
4. **New model → reset dial** (labels drift across generations)

One-line cheat sheet:

> *Model first. Start low. Climb on evidence. New model, reset dial. Never send the committee to a multiple-choice question.*

## Universal rung meanings

| Universal | Metaphor | Use for | Skip when | Climb when |
|-----------|----------|---------|-----------|------------|
| **FLOOR** (`none` / `minimal`) | Instant | classification, tagging, pure templates | multi-step logic | any real reasoning needed |
| **LOW** | Answer from doorway | known shapes: reformat, extract, boilerplate, execute an existing plan | multi-step logic | missing steps, self-contradiction |
| **MEDIUM** | Notepad | everyday coding, structured drafts, moderate debug | pure formatting | hand-waves the hard part |
| **HIGH** | Whiteboard | plan small builds, tradeoff refactors, verification, genuine ambiguity | routine work | long multi-file unattended runs |
| **XHIGH** | War room | long agentic coding **> ~30 min**, deep multi-file, unattended | you're sitting waiting | linchpin where wrong is very expensive |
| **MAX** | Committee | rare linchpin: schema, security-sensitive system design | high already answers | almost never; if you can't say why max, it isn't |

### Anatomy of what each rung buys

- **Low:** small thinking budget; 1–2 tools fast; first good path wins. Perfect A→B with low error risk.
- **Medium:** more token budget; checks work; may reconsider path A vs B.
- **High:** plans, may check plan, executes, double-checks path of least resistance. Stark token jump. Claude factory default if unset.
- **Xhigh:** long unattended agentic; reflection at milestones. Rare for attended work.
- **Max:** plan + execute + many futures; token snowball (models re-read their own thinking). Double/triple medium for slight aesthetic/functional deltas.

## Decision tree (two seconds)

```
Model first (workhorse vs frontier)
        │
        ▼
 Known shape / execute existing plan? ──yes──► LOW
        │ no
        ▼
 Everyday real work? ──yes──► MEDIUM
        │ no
        ▼
 Ambiguity / architecture / verification? ──yes──► HIGH
        │ no
        ▼
 Long unattended multi-file agentic (>~30m)? ──yes──► XHIGH
        │ no
        ▼
 Rare linchpin where wrong is catastrophic? ──yes──► MAX (else stay HIGH)
```

Climb only on evidence: wrong, shallow, missing steps, self-contradiction, hand-waving the hard part.

## Model Pulse experiment (video receipts)

Mark ran **one identical self-contained prompt** across **Claude Code + Codex** at every effort level (control group = prompt; dial = only variable).

Task: build **Model Pulse** — X-sentiment dashboard for Grok / Codex / Claude Code (stock-tracker-for-models vibe), with skills/MCP/API access pre-provisioned, no clarifying questions.

**What differed:** aesthetics, favicon, score formatting, neo-brutalist chrome, receipt color, occasional donut chart.

**What did not differ enough to justify the bill:** functional novelty, insight quality, core dashboard job.

Video punchlines:
- Extra high vs high often bought a **favicon**
- Max vs high often bought **denominator labels / shadow text**
- Codex low already beat Claude low–medium on aesthetics/scores in that run
- A better prompt on medium beats a vague prompt on max for the same look
- Community ladder test cited in guide: same coding prompt **~12 min on low** vs **~2 hours on max**, both working
- OpenRouter: capping effort cut costs **50–75%** with accuracy inside the noise
- Newest flagship **low** often beats previous gen **extra high**

## Gotchas

1. **Overthinking** — max can hurt accuracy on simple tasks (vendor docs)
2. **Brain in a jar** — effort only lengthens thinking; harness is most of capability
3. **Silent downgrades** — unsupported levels may run lower with no error
4. **Effort is inherited** — subagents often inherit parent effort; max at top can spawn a max fleet
5. **Modes ≠ effort** — Pro/Ultra/Heavy can mean multi-agent or more compute, not a higher rung
6. **Label drift** — new gen “medium” ≈ old gen “high”; re-benchmark after model upgrades
7. **Defaults differ** — Claude/Grok unset ≈ high; OpenAI unset ≈ medium; Gemini often auto
8. **UI renames** — Codex app: low→Light, xhigh→Extra High; Ultra may show but API rejects `ultra`
9. **Encrypted receipts** — some models bill thinking tokens you cannot read

## Coding-task heuristics (FoundationPlatform / agent work)

| Signal | Suggest |
|--------|---------|
| Known shape, one file, format/test fix, apply existing plan | workhorse + **LOW** |
| Everyday feature, moderate debug, structured PR | workhorse or frontier + **MEDIUM** |
| Multi-file design tradeoffs, verification pass, ambiguous product/tech | frontier + **HIGH** |
| Long unattended multi-file build, greploop, multi-agent factory | frontier + **XHIGH** (watch subagent inheritance) |
| Schema / security / SoR adjudication / linchpin architecture | frontier + **HIGH** first; **MAX** only if high fails or wrong is catastrophic |
| Needs-jose substrate, multi-tenant credentials | frontier + **HIGH** + human/Jose; not raw max |
| Independent verification of another agent's claim | frontier + **HIGH** (verification is judgment) |
| UI polish / favicon / visual chrome | **do not climb effort** — specify in the prompt |

## Control experiment method (when Adam wants receipts)

From the video/guide — method matters as much as prompts:

1. One **fresh session** per run (never reuse context across levels)
2. One folder per run (`claude_low`, `codex_high`, …); launch from inside it
3. Paste the prompt **verbatim** — dial is the only variable
4. Record: wall-clock, tokens/cost (`/cost` or usage readout), checklist score
5. Open outputs side by side

CLI:
- Claude Code: `claude --effort low` (also medium, high, xhigh, max)
- Codex: `codex -c model_reasoning_effort=low`

Guide ships three control prompts (sentiment dashboard, sales traps, rotating-hexagon physics). Use those when re-benchmarking a new model generation.

## Output contract for `/decode-effort`

Always return:

1. **Detected harness** (Claude Code / Codex / other)
2. **Task summary** (1–2 lines from session or Linear)
3. **Difficulty band** — low | medium | high | long-agentic | linchpin (human-readable task hardness)
4. **Recommended model** (family + when to use cheaper)
5. **Recommended effort** (native label + universal rung + metaphor)
6. **UI / CLI how-to-set** for this harness
7. **Why** (map to table / decision tree above)
8. **Climb if** (concrete failure signals)
9. **Quota note** (subagents, dual-machine, don't max by default)
10. **Optional twin** — same recommendation mapped to the other harness if useful
11. **Confidence** high/medium/low

Do **not** change the user's model/effort settings yourself unless they ask. This skill **recommends only**.

### Session-context rule

When arg is empty or `session`, treat the **current thread** as the brief:
- last user ask
- stated goal / Linear link if present
- files, risk, attended vs unattended already discussed
Do not invent scope that is not in the session. If the thread is empty or ambiguous, ask one clarifying question: *What is the deliverable and what happens if it's wrong?*

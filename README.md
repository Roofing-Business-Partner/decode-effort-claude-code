# decode-effort — Claude Code Edition

User-invoked skill that recommends **which Claude model** and **effort level** to use for a task.

Slash: `/decode-effort` · `/decode-effort session` · `/decode-effort ADA-###` · free text

## Why this exists

Effort is a **thinking-token budget**, not intelligence. People max the dial by default and burn quota. This skill reviews session / Linear / pasted task context and returns:

- difficulty band
- model (workhorse vs frontier)
- native Claude effort (`low` … `max`)
- how to set it
- climb-if signals

Doctrine: **Model first. Start low. Climb on evidence. New model, reset dial.**

## Install

See [INSTALL.md](./INSTALL.md).

```bash
mkdir -p ~/.claude/skills/decode-effort/references
cp SKILL.md ~/.claude/skills/decode-effort/SKILL.md
cp references/*.md ~/.claude/skills/decode-effort/references/
```

## Layout

```text
SKILL.md                 # Claude Code skill (user-invoked only)
references/
  effort-decoder-core.md # shared doctrine + decision tree
  claude-ladder.md       # Anthropic labels
  openai-codex-ladder.md # twin mapping for dual-machine
INSTALL.md
```

## Sister repo

Codex / GPT edition: **[decode-effort-codex](https://github.com/Roofing-Business-Partner/decode-effort-codex)**

## Sources

- Mark Kashef, *THIS Is the AI Setting Everyone Gets Wrong* — https://youtu.be/4__5q76f04s
- Effort Decoder companion guide (Early AI Dopters)
- Packaged for RBP / Foundation multi-machine harnesses

## License

MIT — see [LICENSE](./LICENSE)

Not affiliated with Mark Kashef / Early AI Dopters beyond fair-use packaging of the public teaching into an internal operator skill.

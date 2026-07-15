# Install — decode-effort (Claude Code)

User-invoked only. Recommends **model + effort** for the current session, a Linear issue, or free text.

```bash
# From this repo root
mkdir -p ~/.claude/skills/decode-effort/references
cp SKILL.md ~/.claude/skills/decode-effort/SKILL.md
cp references/*.md ~/.claude/skills/decode-effort/references/
```

Optional shared path:

```bash
mkdir -p ~/.agents/skills/decode-effort/references
cp SKILL.md ~/.agents/skills/decode-effort/SKILL.md
cp references/*.md ~/.agents/skills/decode-effort/references/
```

## Use

```text
/decode-effort
/decode-effort session
/decode-effort ADA-42
/decode-effort <task description>
```

Does **not** change settings unless you ask. Recommend only.

Sister skill (Codex): `Roofing-Business-Partner/decode-effort-codex`

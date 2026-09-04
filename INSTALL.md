# Install — decode-effort (Claude Code)

Release: **v1.3.0**

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

## Validate the repository and installed copy

From the repository root, run:

```bash
python3 scripts/validate_skill.py --repo . --scope repo --edition claude --expected-version 1.3.0
python3 -m unittest discover -s tests -v
```

After copying the skill to `~/.claude/skills/decode-effort`, validate the installed subset from this repository root:

```bash
python3 scripts/validate_skill.py --repo "$HOME/.claude/skills/decode-effort" --scope installed --edition claude --expected-version 1.3.0
```

Sister skill (Codex): `Roofing-Business-Partner/decode-effort-codex`

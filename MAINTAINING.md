# Maintaining decode-effort

This repository contains a user-invoked recommendation skill. It is not self-editing software and it does not own the user's model or effort settings.

## Source and authority order

1. Current provider documentation and model configuration documentation.
2. Reproducible local control results with named prompts, fixtures, model IDs, and CLI versions.
3. Adam's explicit owner ruling for this repository.
4. Trusted engineering references named by Adam.
5. Agent suggestions, videos, and usage telemetry as leads or hypotheses.

A thought such as “we should add this” is not a law. Record it as a proposal until the owner accepts it.

## Change lifecycle

```text
source / insights / evidence
  → proposal classified as FACT, HYPOTHESIS, PROPOSED LAW, or OUT OF SCOPE
  → Adam owner ruling
  → smallest patch
  → validator + fixtures + relevant control sweep
  → independent review
  → version parity across sister editions
  → draft PRs
  → Adam merges
  → merged-main readback
  → explicit tag/release authorization
  → verified installed-copy update
```

The skill itself must not silently edit itself, change user settings, post releases, or decide that a suggestion is law.

## Sister repositories

- Claude Code edition: https://github.com/Roofing-Business-Partner/decode-effort-claude-code
- Codex edition: https://github.com/Roofing-Business-Partner/decode-effort-codex

The two editions share provider-neutral references but have separate `SKILL.md` and provider-specific ladder files. Do not blindly copy one edition's skill file into the other.

## Proposal record

Before a non-trivial enhancement, create a proposal containing:

- date and proposer;
- source links or local evidence;
- current behavior;
- proposed behavior;
- why the change matters;
- explicit non-goals;
- risk of being wrong;
- verification plan;
- owner decision: `PENDING`, `ACCEPTED`, or `REJECTED`;
- release/version target.

`PENDING` proposals do not change the shipped skill.

## v1.3.0 invariants

These must remain true:

- the skill is user-invoked only;
- it recommends rather than changes model or effort settings;
- model selection comes before effort selection;
- lower effort is the starting point for suitable tasks, with climbing based on evidence;
- provider labels are not assumed to be equivalent across generations;
- independent verification remains a separate role and session;
- parallel-session context is not treated as proof of quota pressure or as an automatic reason to raise effort;
- Model-generation claims identify whether evidence is official guidance, empirically exercised, or empirically calibrated;
- Claude-specific guidance does not become Codex-specific guidance by accident.

## Required checks

From the repository root:

```bash
# Set EDITION to the edition this repository contains.
EDITION=claude
python3 scripts/validate_skill.py --repo . --edition "$EDITION" --expected-version 1.3.0
python3 -m unittest discover -s tests -v
git diff --check
```

The validator is intentionally small and standard-library-only. It checks frontmatter, version, user-invoked-only/recommend-only flags, required output fields, calibration vocabulary, references, and edition-specific model guidance. Tests must include a good fixture and a deliberately broken fixture.

## Release discipline

- Do not tag from a dirty tree.
- Do not use a moving model alias for a reproducibility claim; record the full model ID when available.
- Do not publish a calibration claim that exceeds the prompt/fixture/task class actually tested.
- Do not change installed copies before the corresponding branch has passed review.
- Do not merge or publish a GitHub Release from an agent self-check. Adam merges and authorizes release publication.
- After installation, run the validator against the installed copy and start a fresh agent session so the skill is reloaded.

## Out of scope for this repository

- IV workflow changes;
- Matt Pocock skill changes;
- Ben AI skill installation;
- automatic Linear/GitHub/Vercel writes;
- document/PDF QA workflows;
- new agent factories or harnesses;
- model routing implementation beyond documenting the recommendation contract.

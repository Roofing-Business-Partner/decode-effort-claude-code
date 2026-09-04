# Changelog

## [1.3.0] — release candidate, 2026-09-03

GitHub Release publication is pending merged-main verification and Adam's explicit release authorization.

### Added

- Calibration vocabulary: `official-guidance-only`, `empirically-exercised`, `empirically-calibrated`, and `stale/unknown`.
- Operating mode context: actively watched single-session, unattended, or parallel-session.
- Fable 5.1 Claude Code guidance, including the pinned model ID, documented default effort, adaptive thinking, label drift, low-effort retrieval caution, and xhigh/max restraint.
- `MAINTAINING.md` proposal-first skill evolution lifecycle.
- `scripts/validate_skill.py` exact known-contract release manifest and good/broken fixture tests.

### Preserved

- User-invoked-only and recommend-only behavior.
- Model-first selection and evidence-based effort climbing.
- Independent verification as a separate role.
- Existing high guidance for architecture, security, and judgment-heavy work; xhigh for long unattended work.

### Explicitly unchanged

- No IV skill changes.
- No Matt Pocock skill changes.
- No Ben AI skill installation.
- No automatic setting changes, Linear writes, or new factory/harness.

### Calibration caveat

The 2026-09-03 Foundation Project Labs (FPL) replacement pilot ran Claude Fable 5.1 through Claude Code 2.1.258. It exercised three small dependency-free controls at five effort levels; all cells passed, including low effort. This is not a universal production calibration and does not replace task-specific evaluation.

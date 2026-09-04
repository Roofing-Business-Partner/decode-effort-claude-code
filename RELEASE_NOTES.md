# decode-effort v1.3.0

## What changed

- Added explicit calibration-status vocabulary and model-generation disclosure.
- Added operating-mode context without converting parallel sessions into automatic effort escalation.
- Added Claude Fable 5.1 guidance based on Anthropic's current Claude Code/model documentation.
- Added a proposal-first maintenance lifecycle, changelog, standard-library validator, and deliberate broken-fixture tests.
- Preserved user-invoked-only, recommend-only, model-first, and independent-verification boundaries.

## Calibration honesty

A 15-cell Foundation Project Labs (FPL) replacement pilot ran Claude Fable 5.1 through Claude Code 2.1.258 against three small dependency-free controls at five effort levels. Every cell passed, including low effort. This is not a universal production calibration and does not replace task-specific evaluation.

## Not included

No IV changes, Matt Pocock skill changes, Ben AI skill installation, automatic setting changes, Linear automation, or new factory/harness.

Release status: release candidate. Publish only after both sister repositories pass review and Adam authorizes release publication.

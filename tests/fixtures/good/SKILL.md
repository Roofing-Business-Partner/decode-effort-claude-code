---
name: decode-effort
description: "User-only recommendation skill."
disable-model-invocation: true
user-invocable: true
version: 1.3.0
---

# Claude Code Edition

Recommend only. Do not change model or effort settings.
Model first; climb on evidence.
Model first; choose the task-appropriate effort second. Climb only when evidence justifies it.

## Output contract

### Effort decode
- **Harness:** Claude Code
- **Task:** <task>
- **Difficulty:** low | medium | high
- **Operating mode:** actively watched single-session | unattended | parallel-session
- **Model:** <model>
- **Effort:** <effort>
- **Set it:** `claude --effort <effort>`
- **Why:** <why>
- **Climb if:** <evidence>
- **Calibration:** official-guidance-only | empirically-exercised | empirically-calibrated | stale/unknown
- **Confidence:** high | medium | low

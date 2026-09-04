#!/usr/bin/env python3
"""Small, dependency-free validator for decode-effort releases."""
from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_REFERENCES = (
    "references/effort-decoder-core.md",
    "references/claude-ladder.md",
    "references/openai-codex-ladder.md",
)
REQUIRED_OUTPUT_FIELDS = (
    "### Effort decode",
    "**Harness:**",
    "**Task:**",
    "**Difficulty:**",
    "**Operating mode:**",
    "**Model:**",
    "**Why:**",
    "**Climb if:**",
    "**Calibration:**",
    "**Confidence:**",
)


def parse_scalar(value: str) -> str:
    """Parse the deliberately small scalar subset used by this frontmatter."""
    value = value.strip()
    quote: str | None = None
    escaped = False
    for index, char in enumerate(value):
        if quote is not None:
            if escaped:
                escaped = False
            elif quote == '"' and char == "\\":
                escaped = True
            elif char == quote:
                quote = None
            continue
        if char in {"'", '"'}:
            if index != 0:
                raise ValueError("quotes must start a quoted scalar")
            quote = char
        elif char == "#" and (index == 0 or value[index - 1].isspace()):
            value = value[:index]
            break
    if quote is not None or escaped:
        raise ValueError("unbalanced quoted scalar")
    value = value.strip()
    if not value:
        return ""
    if value[0] in {"'", '"'}:
        quote = value[0]
        if len(value) < 2 or value[-1] != quote:
            raise ValueError("unbalanced quoted scalar")
        return value[1:-1]
    if "'" in value or '"' in value:
        raise ValueError("quotes must wrap a scalar")
    return value


def read_frontmatter(text: str) -> tuple[dict[str, str], list[str]]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        return {}, ["SKILL.md must start with YAML frontmatter"]
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, ["SKILL.md frontmatter is not closed"]
    fields: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line.strip():
            continue
        if line[0].isspace():
            errors.append(f"frontmatter key must be root-level: {line}")
            continue
        if ":" not in line:
            errors.append(f"frontmatter line is not key:value: {line}")
            continue
        key, value = line.split(":", 1)
        try:
            fields[key.strip()] = parse_scalar(value)
        except ValueError as exc:
            errors.append(f"frontmatter value for {key.strip()} is invalid: {exc}")
    return fields, errors


def strip_html_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)


def extract_section(text: str, heading: str) -> str:
    match = re.search(
        rf"(?ms)^##[ \t]+{re.escape(heading)}(?:[ \t]+\([^)]*\))?[ \t]*$.*?(?=^##[ \t]+|\Z)",
        text,
    )
    return match.group(0) if match else ""


def extract_output_contract(text: str) -> str:
    return extract_section(text, "Output contract")


def validate_skill_file(
    path: Path, expected_version: str, edition: str | None = None
) -> list[str]:
    errors: list[str] = []
    if not path.is_file():
        return [f"missing skill file: {path}"]
    text = path.read_text(encoding="utf-8")
    clean_text = strip_html_comments(text)
    procedure = extract_section(clean_text, "Procedure")
    contract = extract_output_contract(clean_text)
    fields, parse_errors = read_frontmatter(text)
    errors.extend(f"{path}: {error}" for error in parse_errors)
    if fields.get("name") != "decode-effort":
        errors.append(f"{path}: frontmatter name must be decode-effort")
    if fields.get("version") != expected_version:
        errors.append(
            f"{path}: version must be {expected_version}, got {fields.get('version', '<missing>')}"
        )
    if fields.get("disable-model-invocation") != "true":
        errors.append(f"{path}: disable-model-invocation must be true")
    if fields.get("user-invocable") != "true":
        errors.append(f"{path}: user-invocable must be true")
    for token in REQUIRED_OUTPUT_FIELDS:
        if token not in contract:
            errors.append(f"{path}: missing output-contract field {token}")
    lower = procedure.lower()
    if not procedure:
        errors.append(f"{path}: missing operative Procedure section")
    affirmative_boundary = re.search(
        r'(?mi)^\s*-\s+\*\*recommend only; do not change settings unless adam explicitly says “set it.”\*\*\s*$',
        procedure,
    )
    if affirmative_boundary is None:
        errors.append(f"{path}: affirmative recommendation-only boundary is not stated")
    affirmative_workflow = re.search(
        r"(?mi)^\s*-\s+\*\*model first; choose the task-appropriate effort second\.\*\*\s+\*\*climb only when evidence justifies it\.\*\*\s*$",
        procedure,
    )
    if affirmative_workflow is None:
        errors.append(f"{path}: affirmative model-first ordering is not stated")
    if affirmative_workflow is None:
        errors.append(f"{path}: affirmative evidence-based climbing is not stated")
    if "official-guidance-only" not in clean_text or "stale/unknown" not in clean_text:
        errors.append(f"{path}: calibration vocabulary is incomplete")

    detected_edition: str | None = None
    if "Claude Code Edition" in clean_text:
        detected_edition = "claude"
        if "**Effort:**" not in contract or "claude --effort" not in clean_text:
            errors.append(f"{path}: Claude effort output/set instructions are incomplete")
    if "Codex Edition" in clean_text:
        if detected_edition is not None:
            errors.append(f"{path}: multiple edition identities are present")
        detected_edition = "codex"
        if "**Reasoning effort:**" not in contract or "model_reasoning_effort" not in clean_text:
            errors.append(f"{path}: Codex reasoning-effort output/set instructions are incomplete")
    if edition is not None and detected_edition != edition:
        errors.append(
            f"{path}: edition identity must be {edition}, detected {detected_edition or '<missing>'}"
        )
    return errors


def validate_references(repo: Path, edition: str) -> list[str]:
    errors: list[str] = []
    core_path = repo / "references/effort-decoder-core.md"
    core = core_path.read_text(encoding="utf-8") if core_path.is_file() else ""
    for token in (
        "Calibration vocabulary",
        "Operating mode is context, not effort",
        "Parallel-session",
        "Quota pressure",
        "Model first",
        "Start low",
        "Climb on evidence",
    ):
        if token not in core:
            errors.append(f"core reference missing: {token}")
    claude_ladder = repo / "references/claude-ladder.md"
    openai_ladder = repo / "references/openai-codex-ladder.md"
    claude_text = claude_ladder.read_text(encoding="utf-8") if claude_ladder.is_file() else ""
    openai_text = openai_ladder.read_text(encoding="utf-8") if openai_ladder.is_file() else ""
    if edition == "claude":
        for token in (
            "Claude Fable 5.1",
            "claude-fable-5-1",
            "adaptive thinking",
            "empirically-exercised",
        ):
            if token not in claude_text:
                errors.append(f"Claude ladder missing: {token}")
    elif edition == "codex":
        if "model_reasoning_effort" not in openai_text:
            errors.append("Codex ladder missing model_reasoning_effort")
        if "Fable 5.1" in openai_text:
            errors.append("Codex ladder must not contain Claude Fable-specific guidance")
    else:
        errors.append(f"edition must be claude or codex, got {edition}")
    return errors


def validate_repo(repo: Path, edition: str, expected_version: str) -> list[str]:
    errors: list[str] = []
    required = [
        "SKILL.md",
        *REQUIRED_REFERENCES,
        "MAINTAINING.md",
        "CHANGELOG.md",
        "RELEASE_NOTES.md",
        "CALIBRATION.md",
        "scripts/validate_skill.py",
    ]
    for relative in required:
        if not (repo / relative).is_file():
            errors.append(f"missing required file: {relative}")
    errors.extend(validate_skill_file(repo / "SKILL.md", expected_version, edition))
    errors.extend(validate_references(repo, edition))
    for relative in ("README.md", "INSTALL.md", "CHANGELOG.md", "RELEASE_NOTES.md"):
        path = repo / relative
        if path.is_file() and expected_version not in path.read_text(encoding="utf-8"):
            errors.append(f"{relative}: expected version {expected_version} is not mentioned")
    maintaining = (repo / "MAINTAINING.md").read_text(encoding="utf-8") if (repo / "MAINTAINING.md").is_file() else ""
    for token in ("owner ruling", "PENDING", "independent review", "installed-copy"):
        if token not in maintaining:
            errors.append(f"MAINTAINING.md missing: {token}")
    calibration = (repo / "CALIBRATION.md").read_text(encoding="utf-8") if (repo / "CALIBRATION.md").is_file() else ""
    for token in ("model ID", "replacement", "not a universal"):
        if token.lower() not in calibration.lower():
            errors.append(f"CALIBRATION.md missing: {token}")
    return errors


def validate_installed(repo: Path, edition: str, expected_version: str) -> list[str]:
    """Validate the subset copied to ~/.claude/skills or ~/.codex/skills."""
    errors: list[str] = []
    for relative in REQUIRED_REFERENCES:
        if not (repo / relative).is_file():
            errors.append(f"missing installed reference: {relative}")
    errors.extend(validate_skill_file(repo / "SKILL.md", expected_version, edition))
    errors.extend(validate_references(repo, edition))
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path("."))
    parser.add_argument("--edition", choices=("claude", "codex"), required=True)
    parser.add_argument("--expected-version", required=True)
    parser.add_argument("--scope", choices=("repo", "installed"), default="repo")
    args = parser.parse_args()
    repo = args.repo.resolve()
    if args.scope == "installed":
        errors = validate_installed(repo, args.edition, args.expected_version)
    else:
        errors = validate_repo(repo, args.edition, args.expected_version)
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print(f"PASS: {args.scope} {args.edition} decode-effort {args.expected_version}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Dependency-free exact known-contract validator for decode-effort v1.3.0."""
from __future__ import annotations

import argparse
import hashlib
from pathlib import Path


KNOWN_RELEASE_VERSION = "1.3.0"
REQUIRED_REFERENCES = (
    "references/effort-decoder-core.md",
    "references/claude-ladder.md",
    "references/openai-codex-ladder.md",
)
REQUIRED_REPO_FILES = (
    "SKILL.md",
    *REQUIRED_REFERENCES,
    "MAINTAINING.md",
    "CHANGELOG.md",
    "RELEASE_NOTES.md",
    "CALIBRATION.md",
    "scripts/validate_skill.py",
)

# This is intentionally an exact release manifest, not a semantic Markdown/YAML
# parser. Any intentional contract change belongs in a new versioned release.
KNOWN_RELEASE_SHA256 = {
    "claude": {
        "SKILL.md": "75b65e73ab48dd1243ffde32304515816d4a08691ffd5c0e119f3287814dc68a",
        "references/effort-decoder-core.md": "e042c891b0bcf18ccb4991910911fc8e0b3ecd2ba272d4ba0042b13a618edf30",
        "references/claude-ladder.md": "f651a01562e4947579904fb02083cf48b95263e9d566b97e9f4ef57c94e54f97",
        "references/openai-codex-ladder.md": "1491bb79c2aa518ce365a23ab4774c295a954ffcd67fec5f89d4cf9abeccd98c",
    },
    "codex": {
        "SKILL.md": "d234bc506365634f12d5f1cad89acc11a8f9f351b45b55a079593d76a1ba3920",
        "references/effort-decoder-core.md": "e042c891b0bcf18ccb4991910911fc8e0b3ecd2ba272d4ba0042b13a618edf30",
        "references/claude-ladder.md": "1302e70f0b141352a14d7752271e781c0e42985f4bb3659abeeca05f9454e46d",
        "references/openai-codex-ladder.md": "1491bb79c2aa518ce365a23ab4774c295a954ffcd67fec5f89d4cf9abeccd98c",
    },
}

# Test-only known-good fixtures remain useful for proving the test harness, but
# are never accepted by validate_repo() or validate_installed().
KNOWN_FIXTURE_SHA256 = {
    "claude": "0efd618f72cb2e3b2a315010ce033bfadd4a2a717386ee2595490f064418a414",
    "codex": "de9e6f8440c5723cc7fb4b05c9133391e89c445c67e3935203e0e8093b0c7614",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_skill_file(
    path: Path,
    expected_version: str,
    edition: str | None = None,
    *,
    release_only: bool = False,
) -> list[str]:
    """Validate one known skill input by exact content hash.

    The fixture exception is intentionally available only to unit tests. Release
    entry points set release_only=True and accept only the approved v1.3 input.
    """
    errors: list[str] = []
    if not path.is_file():
        return [f"missing skill file: {path}"]
    if expected_version != KNOWN_RELEASE_VERSION:
        errors.append(
            f"{path}: exact known-contract validator supports {KNOWN_RELEASE_VERSION}, "
            f"not requested {expected_version}"
        )
    if edition not in KNOWN_RELEASE_SHA256:
        errors.append(f"{path}: edition must be claude or codex, got {edition}")
        return errors

    actual = sha256_file(path)
    expected = KNOWN_RELEASE_SHA256[edition]["SKILL.md"]
    allowed = {expected}
    if not release_only:
        allowed.add(KNOWN_FIXTURE_SHA256[edition])
    if actual not in allowed:
        errors.append(
            f"{path}: exact known {edition} v{KNOWN_RELEASE_VERSION} contract hash mismatch "
            f"(expected one of {sorted(allowed)}, got {actual})"
        )
    return errors


def validate_references(repo: Path, edition: str) -> list[str]:
    if edition not in KNOWN_RELEASE_SHA256:
        return [f"edition must be claude or codex, got {edition}"]
    errors: list[str] = []
    manifest = KNOWN_RELEASE_SHA256[edition]
    for relative in REQUIRED_REFERENCES:
        path = repo / relative
        if not path.is_file():
            errors.append(f"missing required reference: {relative}")
            continue
        actual = sha256_file(path)
        expected = manifest[relative]
        if actual != expected:
            errors.append(
                f"{relative}: exact known {edition} v{KNOWN_RELEASE_VERSION} reference hash mismatch "
                f"(expected {expected}, got {actual})"
            )
    return errors


def validate_repo(repo: Path, edition: str, expected_version: str) -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED_REPO_FILES:
        if not (repo / relative).is_file():
            errors.append(f"missing required file: {relative}")
    errors.extend(
        validate_skill_file(
            repo / "SKILL.md",
            expected_version,
            edition,
            release_only=True,
        )
    )
    errors.extend(validate_references(repo, edition))
    for relative in ("README.md", "INSTALL.md", "CHANGELOG.md", "RELEASE_NOTES.md"):
        path = repo / relative
        if path.is_file() and expected_version not in path.read_text(encoding="utf-8"):
            errors.append(f"{relative}: expected version {expected_version} is not mentioned")
    maintaining = (
        (repo / "MAINTAINING.md").read_text(encoding="utf-8")
        if (repo / "MAINTAINING.md").is_file()
        else ""
    )
    for token in ("owner ruling", "PENDING", "independent review", "installed-copy"):
        if token not in maintaining:
            errors.append(f"MAINTAINING.md missing: {token}")
    calibration = (
        (repo / "CALIBRATION.md").read_text(encoding="utf-8")
        if (repo / "CALIBRATION.md").is_file()
        else ""
    )
    for token in ("model ID", "replacement", "not a universal"):
        if token.lower() not in calibration.lower():
            errors.append(f"CALIBRATION.md missing: {token}")
    return errors


def validate_installed(repo: Path, edition: str, expected_version: str) -> list[str]:
    """Validate the exact subset copied to an installed skill directory."""
    errors = validate_skill_file(
        repo / "SKILL.md",
        expected_version,
        edition,
        release_only=True,
    )
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

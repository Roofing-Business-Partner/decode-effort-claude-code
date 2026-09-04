import importlib.util
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("validate_skill", ROOT / "scripts" / "validate_skill.py")
assert spec is not None and spec.loader is not None
validate_skill = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = validate_skill
spec.loader.exec_module(validate_skill)


class ValidateSkillTests(unittest.TestCase):
    def test_current_repo_passes(self):
        errors = validate_skill.validate_repo(ROOT, "claude", "1.3.0")
        self.assertEqual(errors, [])

    def test_good_fixture_passes(self):
        errors = validate_skill.validate_skill_file(ROOT / "tests/fixtures/good/SKILL.md", "1.3.0", "claude")
        self.assertEqual(errors, [])

    def test_installed_scope_passes(self):
        errors = validate_skill.validate_installed(ROOT, "claude", "1.3.0")
        self.assertEqual(errors, [])

    def test_mismatched_edition_fails(self):
        errors = validate_skill.validate_repo(ROOT, "codex", "1.3.0")
        self.assertTrue(any("edition identity" in error for error in errors))

    def test_wrong_version_fails(self):
        errors = validate_skill.validate_repo(ROOT, "claude", "1.2.0")
        self.assertTrue(any("version must be 1.2.0" in error for error in errors))

    def test_broken_fixture_fails(self):
        errors = validate_skill.validate_skill_file(ROOT / "tests/fixtures/broken/SKILL.md", "1.3.0")
        self.assertTrue(errors)
        self.assertTrue(any("disable-model-invocation" in error for error in errors))

    def test_installed_missing_reference_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory)
            (installed / "references").mkdir()
            shutil.copy2(ROOT / "SKILL.md", installed / "SKILL.md")
            for source in (ROOT / "references").glob("*.md"):
                shutil.copy2(source, installed / "references" / source.name)
            (installed / "references" / "effort-decoder-core.md").unlink()
            errors = validate_skill.validate_installed(installed, "claude", "1.3.0")
            self.assertTrue(errors)
            self.assertTrue(any("core reference missing" in error for error in errors))

    def test_claude_fable_leakage_in_codex_ladder_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "repo"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            ladder = clone / "references" / "openai-codex-ladder.md"
            ladder.write_text(ladder.read_text(encoding="utf-8") + "\nFable 5.1 leakage fixture\n", encoding="utf-8")
            errors = validate_skill.validate_repo(clone, "codex", "1.3.0")
            self.assertTrue(any("Fable-specific" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

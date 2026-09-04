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
        self.assertEqual(validate_skill.validate_repo(ROOT, "claude", "1.3.0"), [])

    def test_good_fixture_passes_unit_scope(self):
        errors = validate_skill.validate_skill_file(
            ROOT / "tests/fixtures/good/SKILL.md", "1.3.0", "claude"
        )
        self.assertEqual(errors, [])

    def test_installed_scope_passes_release_contract(self):
        self.assertEqual(validate_skill.validate_installed(ROOT, "claude", "1.3.0"), [])

    def test_mismatched_edition_fails_exact_contract(self):
        errors = validate_skill.validate_repo(ROOT, "codex", "1.3.0")
        self.assertTrue(any("hash mismatch" in error for error in errors))

    def test_wrong_version_fails_known_release_guard(self):
        errors = validate_skill.validate_repo(ROOT, "claude", "1.2.0")
        self.assertTrue(any("supports 1.3.0" in error for error in errors))

    def test_broken_fixture_fails_unit_scope(self):
        errors = validate_skill.validate_skill_file(
            ROOT / "tests/fixtures/broken/SKILL.md", "1.3.0", "claude"
        )
        self.assertTrue(any("hash mismatch" in error for error in errors))

    def test_changed_skill_contract_fails(self):
        source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text(source + "\nUnapproved contract mutation.\n", encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("hash mismatch" in error for error in errors))

    def test_changed_reference_contract_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory)
            (installed / "references").mkdir()
            for source in (ROOT / "references").glob("*.md"):
                shutil.copy2(source, installed / "references" / source.name)
            ladder = installed / "references" / "openai-codex-ladder.md"
            ladder.write_text(ladder.read_text(encoding="utf-8") + "\nMutation.\n", encoding="utf-8")
            errors = validate_skill.validate_references(installed, "claude")
            self.assertTrue(any("hash mismatch" in error for error in errors))

    def test_installed_missing_reference_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory)
            (installed / "references").mkdir()
            shutil.copy2(ROOT / "SKILL.md", installed / "SKILL.md")
            for source in (ROOT / "references").glob("*.md"):
                if source.name != "openai-codex-ladder.md":
                    shutil.copy2(source, installed / "references" / source.name)
            errors = validate_skill.validate_installed(installed, "claude", "1.3.0")
            self.assertTrue(any("missing required reference" in error for error in errors))

    def test_unit_fixture_cannot_ship_as_installed_contract(self):
        with tempfile.TemporaryDirectory() as directory:
            installed = Path(directory)
            (installed / "references").mkdir()
            shutil.copy2(ROOT / "tests/fixtures/good/SKILL.md", installed / "SKILL.md")
            for source in (ROOT / "references").glob("*.md"):
                shutil.copy2(source, installed / "references" / source.name)
            errors = validate_skill.validate_installed(installed, "claude", "1.3.0")
            self.assertTrue(any("hash mismatch" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

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
    def test_duplicate_frontmatter_key_fails(self):
        source = (ROOT / "tests/fixtures/good/SKILL.md").read_text(encoding="utf-8")
        duplicate = source.replace("name: decode-effort", "name: rejected-first-value\nname: decode-effort", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "duplicate.md"
            path.write_text(duplicate, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("duplicate root-level" in error for error in errors))

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
            (installed / "references" / "openai-codex-ladder.md").unlink()
            errors = validate_skill.validate_installed(installed, "claude", "1.3.0")
            self.assertTrue(errors)
            self.assertTrue(any("missing installed reference" in error for error in errors))

    def test_claude_fable_leakage_in_codex_ladder_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            clone = Path(directory) / "repo"
            shutil.copytree(ROOT, clone, ignore=shutil.ignore_patterns(".git", "__pycache__"))
            ladder = clone / "references" / "openai-codex-ladder.md"
            ladder.write_text(ladder.read_text(encoding="utf-8") + "\nFable 5.1 leakage fixture\n", encoding="utf-8")
            errors = validate_skill.validate_repo(clone, "codex", "1.3.0")
            self.assertTrue(any("Fable-specific" in error for error in errors))

    def test_comment_only_contract_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "SKILL.md"
            path.write_text(
                """---
name: decode-effort
description: broken
 disable-model-invocation: true
user-invocable: true
version: 1.3.0
---
# Claude Code Edition
<!-- The actual contract is absent. Never use Model first. Recommend only.\n### Effort decode\n**Harness:** **Task:** **Difficulty:** **Operating mode:** **Model:** **Why:** **Climb if:** **Calibration:** **Confidence:** -->
""".replace(" disable-model", "disable-model"),
                encoding="utf-8",
            )
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("missing output-contract field" in error for error in errors))

    def test_negated_guidance_fails(self):
        source = (ROOT / "tests/fixtures/good/SKILL.md").read_text(encoding="utf-8")
        negated = source.replace(
            "   - **Model first; choose the task-appropriate effort second.** **Climb only when evidence justifies it.**",
            "   - **Never model first; choose the task-appropriate effort second.** **Do not climb only when evidence justifies it.**",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "negated.md"
            path.write_text(negated, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("affirmative model-first" in error for error in errors))
            self.assertTrue(any("affirmative evidence-based" in error for error in errors))

    def test_negated_recommendation_boundary_fails(self):
        source = (ROOT / "tests/fixtures/good/SKILL.md").read_text(encoding="utf-8")
        negated = source.replace(
            "   - **Recommend only; do not change settings unless Adam explicitly says “set it.”**",
            "   - **Do not recommend only; change settings unless Adam explicitly says “set it.”**",
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "negated-boundary.md"
            path.write_text(negated, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("affirmative recommendation-only" in error for error in errors))

    def test_contradictory_procedure_directives_fail(self):
        source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        contradiction = source.replace(
            "\n## Output contract (required)\n",
            "\n   - Choose effort before model. Do not climb based on evidence. Change settings automatically.\n\n## Output contract (required)\n",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "contradictory.md"
            path.write_text(contradiction, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("contradictory Procedure" in error for error in errors))

    def test_paraphrased_contradictory_procedure_fails(self):
        source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        contradiction = source.replace(
            "\n## Output contract (required)\n",
            "\n   - Pick the effort first, then the model; escalate effort regardless of evidence; tune settings on your own.\n\n## Output contract (required)\n",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "paraphrased-contradiction.md"
            path.write_text(contradiction, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("contradictory Procedure" in error for error in errors))

    def test_decoy_guidance_outside_procedure_fails(self):
        source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        reversed_procedure = source.replace(
            "   - **Model first; choose the task-appropriate effort second.** **Climb only when evidence justifies it.**",
            "   - Choose effort before model. Do not climb based on evidence.",
            1,
        )
        decoy = reversed_procedure.replace(
            "## Procedure\n",
            "## Procedure notes\n   - **Model first; choose the task-appropriate effort second.** **Climb only when evidence justifies it.**\n\n## Procedure\n",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "decoy.md"
            path.write_text(decoy, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("affirmative model-first" in error for error in errors))
            self.assertTrue(any("affirmative evidence-based" in error for error in errors))

    def test_qualified_procedure_heading_does_not_shadow_real_one(self):
        source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        reversed_procedure = source.replace(
            "   - **Model first; choose the task-appropriate effort second.** **Climb only when evidence justifies it.**",
            "   - Choose effort before model. Do not climb based on evidence.",
            1,
        )
        qualified = reversed_procedure.replace(
            "## Procedure\n",
            "## Procedure (notes)\n   - **Model first; choose the task-appropriate effort second.** **Climb only when evidence justifies it.**\n\n## Procedure\n",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "qualified-procedure.md"
            path.write_text(qualified, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("affirmative model-first" in error for error in errors))

    def test_indented_frontmatter_key_fails(self):
        source = (ROOT / "tests/fixtures/good/SKILL.md").read_text(encoding="utf-8")
        indented = source.replace("name: decode-effort", "  name: decode-effort", 1)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "indented.md"
            path.write_text(indented, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("root-level" in error for error in errors))

    def test_frontmatter_comments_and_quotes(self):
        source = (ROOT / "tests/fixtures/good/SKILL.md").read_text(encoding="utf-8")
        valid = source.replace(
            "disable-model-invocation: true",
            "disable-model-invocation: true # user-only",
            1,
        )
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "valid.md"
            path.write_text(valid, encoding="utf-8")
            self.assertEqual(validate_skill.validate_skill_file(path, "1.3.0", "claude"), [])

            plain = source.replace(
                'description: "User-only recommendation skill."',
                "description: Adam's effort decoder",
                1,
            )
            path.write_text(plain, encoding="utf-8")
            self.assertEqual(validate_skill.validate_skill_file(path, "1.3.0", "claude"), [])

            malformed = valid.replace(
                "disable-model-invocation: true # user-only",
                'disable-model-invocation: "true',
                1,
            )
            path.write_text(malformed, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("unbalanced quoted scalar" in error for error in errors))

    def test_nonoperative_field_declarations_fail(self):
        source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        prefix, suffix = source.split("## Output contract (required)", 1)
        nonoperative = prefix + """## Output contract (required)
These fields are deprecated, optional, and forbidden in output.
""" + suffix
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nonoperative-fields.md"
            path.write_text(nonoperative, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("non-operative Output contract" in error for error in errors))

    def test_nonoperative_output_contract_prose_fails(self):
        source = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        prefix = source.split("## Output contract (required)", 1)[0]
        nonoperative = prefix + """## Output contract (required)
The following labels are deprecated, non-operative, and must never be output:
### Effort decode **Harness:** **Task:** **Difficulty:** **Operating mode:** **Model:** **Why:** **Climb if:** **Calibration:** **Confidence:**
"""
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "nonoperative-contract.md"
            path.write_text(nonoperative, encoding="utf-8")
            errors = validate_skill.validate_skill_file(path, "1.3.0", "claude")
            self.assertTrue(any("missing output-contract field" in error for error in errors))


if __name__ == "__main__":
    unittest.main()

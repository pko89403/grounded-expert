"""Exercise the drift guard against unintended source and host edits."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
HOST = Path("hosts/openai/skills/grounded-expert/SKILL.md")
BASH = shutil.which("bash")


class DriftGuardTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="grounded-drift-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for relative in (
            Path("plugin/SKILL.md"), HOST,
            Path("scripts/check-openai-drift.sh"),
            Path("scripts/openai-skill.patch"),
        ):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, destination)

    def run_guard(self, **environment):
        return subprocess.run(
            [BASH, str(self.root / "scripts/check-openai-drift.sh")],
            cwd=self.root, capture_output=True, text=True, check=False,
            env={**os.environ, "OPENAI_PATCH_BASE_REF": "", **environment},
        )

    def assert_drift(self, result):
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("DRIFT:", result.stderr)

    def edit(self, relative, before, after):
        file = self.root / relative
        original = file.read_text(encoding="utf-8")
        self.assertEqual(original.count(before), 1)
        file.write_text(original.replace(before, after), encoding="utf-8")

    def test_reviewed_adaptation_passes_without_modifying_inputs(self):
        original = (self.root / "plugin/SKILL.md").read_bytes()
        result = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.root / "plugin/SKILL.md").read_bytes(), original)

    def test_openai_trigger_edit_fails(self):
        self.edit(HOST, "  Use when expert-level", "  Always activate when expert-level")
        self.assert_drift(self.run_guard())

    def test_claude_trigger_edit_fails(self):
        self.edit("plugin/SKILL.md", "description: Use when", "description: Never activate when")
        self.assert_drift(self.run_guard())

    def test_host_procedure_edit_fails(self):
        self.edit(HOST, "up to 2 times", "up to 9 times")
        self.assert_drift(self.run_guard())

    def test_source_only_procedure_edit_fails(self):
        self.edit("plugin/SKILL.md", "up to 2 times", "up to 9 times")
        self.assert_drift(self.run_guard())

    def test_shared_change_outside_adaptation_can_stay_in_sync(self):
        for relative in ("plugin/SKILL.md", HOST):
            self.edit(relative, "## Why this exists", "## Purpose")
        result = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_claude_only_name_copied_to_both_files_fails(self):
        for relative in ("plugin/SKILL.md", HOST):
            self.edit(relative, "## Why this exists", "## Why this exists\n\nUse WebFetch to read pages.")
        result = self.run_guard()
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("CLAUDE TOKEN", result.stderr)

    def test_unavailable_baseline_warns_without_failing(self):
        result = self.run_guard(OPENAI_PATCH_BASE_REF="0123456789abcdef0123456789abcdef01234567")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("warning: patch baseline unavailable", result.stderr)

    def test_rejected_hunk_is_printed(self):
        self.edit("plugin/SKILL.md", "up to 2 times", "up to 9 times")
        result = self.run_guard(TMPDIR=str(self.root))
        self.assert_drift(result)
        # patch.log never prints hunk bodies, so this line proves the .rej file was printed.
        self.assertIn("+6. OpenAI only:", result.stderr)

    def test_missing_adaptation_fails(self):
        (self.root / "scripts/openai-skill.patch").unlink()
        result = self.run_guard()
        self.assertEqual(result.returncode, 1)
        self.assertIn("missing:", result.stderr)

    def test_empty_adaptation_explains_cause(self):
        (self.root / "scripts/openai-skill.patch").write_text("")
        result = self.run_guard()
        self.assertEqual(result.returncode, 1)
        self.assertIn("empty adaptation:", result.stderr)

    def test_missing_patch_tool_is_not_counted_as_drift(self):
        binaries = self.root / "bin"
        binaries.mkdir()
        for name in ("dirname", "mktemp", "diff", "awk"):
            (binaries / name).symlink_to(shutil.which(name))
        result = self.run_guard(PATH=str(binaries))
        self.assertEqual(result.returncode, 127)
        self.assertIn("error: required command unavailable: patch", result.stderr)
        self.assertNotIn("DRIFT:", result.stderr)

    def test_cleanup_preserves_success_with_unexpected_file(self):
        self.run_with_patch_shim(0)

    def test_cleanup_preserves_patch_execution_failure(self):
        self.run_with_patch_shim(2)

    def run_with_patch_shim(self, status):
        binaries = self.root / "bin"
        binaries.mkdir()
        shim = binaries / "patch"
        shim.write_text(
            "#!/bin/sh\n"
            'for argument in "$@"; do\n'
            '  case "$argument" in --output=*) touch "${argument#--output=}.unexpected" ;; esac\n'
            "done\n"
            'if [ "$PATCH_TEST_STATUS" != 0 ]; then exit "$PATCH_TEST_STATUS"; fi\n'
            'exec "$PATCH_REAL" "$@"\n'
        )
        shim.chmod(0o755)
        result = self.run_guard(
            PATH=str(binaries) + os.pathsep + os.environ["PATH"],
            TMPDIR=str(self.root), PATCH_REAL=shutil.which("patch"),
            PATCH_TEST_STATUS=str(status),
        )
        self.assertEqual(result.returncode, status, result.stdout + result.stderr)
        self.assertTrue(list(self.root.glob("grounded-expert-drift.*/expected.md.unexpected")))
        if status:
            self.assertIn("error: patch could not run successfully", result.stderr)
            self.assertNotIn("DRIFT:", result.stderr)
        else:
            self.assertIn("OK:", result.stdout)


if __name__ == "__main__":
    unittest.main()

"""Exercise the drift guard against unintended source and host edits."""
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parents[2]
HOST = Path("hosts/openai/skills/grounded-expert/SKILL.md")


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

    def run_guard(self):
        return subprocess.run(
            ["bash", str(self.root / "scripts/check-openai-drift.sh")],
            cwd=self.root, capture_output=True, text=True, check=False,
        )

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
        self.edit(HOST, "  Use when the user needs", "  Always activate; the user needs")
        self.assertNotEqual(self.run_guard().returncode, 0)

    def test_claude_trigger_edit_fails(self):
        self.edit("plugin/SKILL.md", "description: Use when", "description: Never activate when")
        self.assertNotEqual(self.run_guard().returncode, 0)

    def test_host_procedure_edit_fails(self):
        self.edit(HOST, "up to 2 times", "up to 9 times")
        self.assertNotEqual(self.run_guard().returncode, 0)

    def test_source_only_procedure_edit_fails(self):
        self.edit("plugin/SKILL.md", "up to 2 times", "up to 9 times")
        self.assertNotEqual(self.run_guard().returncode, 0)

    def test_shared_change_outside_adaptation_can_stay_in_sync(self):
        for relative in ("plugin/SKILL.md", HOST):
            self.edit(relative, "## Why this exists", "## Purpose")
        result = self.run_guard()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_missing_adaptation_fails(self):
        (self.root / "scripts/openai-skill.patch").unlink()
        self.assertNotEqual(self.run_guard().returncode, 0)


if __name__ == "__main__":
    unittest.main()

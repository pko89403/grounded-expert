"""Exercise actual package resources and malformed metadata in temporary copies."""
import importlib.util
import json
import shutil
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location("package_check", REPO / "scripts/validate_openai_package.py")
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PackageTest(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="openai-package-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for relative in ("LICENSE", "hosts/openai/LICENSE", "hosts/openai/plugin.json",
                         "hosts/openai/PRIVACY.md", "hosts/openai/skills/grounded-expert/SKILL.md",
                         ".agents/plugins/marketplace.json"):
            destination = self.root / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(REPO / relative, destination)

    def mutate_json(self, path, change):
        file = self.root / path
        value = json.loads(file.read_text())
        change(value)
        file.write_text(json.dumps(value))

    def test_valid_package(self):
        self.assertEqual(MODULE.validate(self.root), [])

    def test_malformed_json(self):
        (self.root / "hosts/openai/plugin.json").write_text("{")
        self.assertTrue(MODULE.validate(self.root))

    def test_wrong_host_path(self):
        self.mutate_json(".agents/plugins/marketplace.json",
                         lambda value: value["plugins"][0]["source"].update(path="./plugin"))
        self.assertIn("OpenAI source path", MODULE.validate(self.root))

    def test_claude_privacy_is_rejected(self):
        self.mutate_json("hosts/openai/plugin.json", lambda value:
                         value["extensions"]["com.openai"]["interface"].update(privacyPolicyURL="plugin/PRIVACY.md"))
        self.assertIn("OpenAI privacy URL", MODULE.validate(self.root))

    def test_invalid_version(self):
        self.mutate_json("hosts/openai/plugin.json", lambda value: value.update(version="unreleased"))
        self.assertIn("version", MODULE.validate(self.root))

    def test_license_mismatch(self):
        (self.root / "hosts/openai/LICENSE").write_text("different license")
        self.assertIn("license mismatch", MODULE.validate(self.root))

    def test_missing_privacy_resource(self):
        (self.root / "hosts/openai/PRIVACY.md").unlink()
        self.assertTrue(MODULE.validate(self.root))


if __name__ == "__main__":
    unittest.main()

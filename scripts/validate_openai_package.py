#!/usr/bin/env python3
"""Offline structural/resource checks, not a complete Agent Plugins schema validator."""
import json
import re
import sys
from pathlib import Path


def validate(root):
    root = Path(root)
    errors = []
    def require(condition, message):
        if not condition:
            raise ValueError(message)

    try:
        manifest = json.loads((root / "hosts/openai/plugin.json").read_text())
        catalog = json.loads((root / ".agents/plugins/marketplace.json").read_text())
        require(isinstance(manifest, dict) and isinstance(catalog, dict), "JSON roots must be objects")
        require(manifest["$schema"] == "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", "schema URL")
        require(manifest["name"] == "grounded-expert", "plugin name")
        require(re.fullmatch(r"\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?", manifest["version"]), "version")
        require(isinstance(manifest["description"], str) and manifest["description"], "description")
        require(catalog["name"] == "grounded-expert", "marketplace name")
        entries = catalog["plugins"]
        require(isinstance(entries, list) and len(entries) == 1, "one catalog entry")
        require(entries[0]["name"] == manifest["name"], "catalog plugin name")
        require(entries[0]["source"] == {"source": "local", "path": "./hosts/openai"}, "OpenAI source path")
        require(entries[0]["policy"]["installation"] == "AVAILABLE", "installation policy")
        interface = manifest["extensions"]["com.openai"]["interface"]
        require(interface["privacyPolicyURL"] == (
            "https://github.com/pko89403/grounded-expert/blob/main/hosts/openai/PRIVACY.md"
        ), "OpenAI privacy URL")
        for relative in ("hosts/openai/skills/grounded-expert/SKILL.md", "hosts/openai/PRIVACY.md"):
            require((root / relative).is_file(), "missing resource: " + relative)
        require((root / "hosts/openai/LICENSE").read_bytes() == (root / "LICENSE").read_bytes(), "license mismatch")
    except (OSError, ValueError, TypeError, KeyError) as error:
        errors.append(str(error))
    return errors


if __name__ == "__main__":
    problems = validate(Path(__file__).resolve().parents[1])
    for problem in problems:
        print("PACKAGE:", problem, file=sys.stderr)
    if not problems:
        print("OK: OpenAI JSON structure, paths, policy and license checks passed.")
    sys.exit(bool(problems))

"""Packaging checks, not a behavioral evaluation of the skills.

Run: uv run --with PyYAML==6.0.3 python -m unittest discover -s tests -v
"""
import json
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins" / "engineering-discipline"
WORKFLOWS = {"grill-design", "diagnose", "tdd-slice"}
PRIMITIVES = {"domain-language", "module-design", "feedback-loop"}
NAMES = WORKFLOWS | PRIMITIVES


def skill_parts(name):
    text = (PLUGIN / "skills" / name / "SKILL.md").read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise AssertionError(f"{name}: missing frontmatter")
    header, body = text[4:].split("\n---\n", 1)
    return yaml.safe_load(header), body


class EngineeringDisciplinePackage(unittest.TestCase):
    def test_exact_skill_inventory(self):
        self.assertEqual(
            {p.parent.name for p in (PLUGIN / "skills").glob("*/SKILL.md")},
            NAMES,
        )

    def test_manifest_and_marketplace_agree(self):
        manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
        entries = [p for p in marketplace["plugins"] if p["name"] == "engineering-discipline"]
        self.assertEqual(len(entries), 1)
        entry = entries[0]
        self.assertEqual(manifest["name"], entry["name"])
        self.assertEqual(manifest["description"], entry["description"])
        self.assertEqual(manifest["author"], entry["author"])
        self.assertTrue(marketplace["owner"]["name"])
        self.assertEqual((ROOT / entry["source"]).resolve(), PLUGIN.resolve())
        self.assertRegex(manifest["version"], r"^\d+\.\d+\.\d+$")
        self.assertNotIn("hooks", manifest)
        self.assertNotIn("mcpServers", manifest)

    def test_valid_frontmatter_and_concise_body(self):
        for name in sorted(NAMES):
            with self.subTest(skill=name):
                header, body = skill_parts(name)
                self.assertIsInstance(header, dict)
                self.assertEqual(header["name"], name)
                self.assertRegex(name, r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
                self.assertLessEqual(len(name), 64)
                self.assertIsInstance(header["description"], str)
                self.assertTrue(header["description"].startswith("Use when "))
                self.assertLessEqual(len(header["description"]), 1024)
                self.assertTrue(body.strip())
                self.assertLessEqual(len(body.split()), 900)
                for field in ("allowed-tools", "context", "agent", "model"):
                    self.assertNotIn(field, header, f"Unexpected runtime dependency: {field}")

    def test_invocation_policy_in_both_runtimes(self):
        for name in sorted(NAMES):
            with self.subTest(skill=name):
                header, _ = skill_parts(name)
                manual = name in WORKFLOWS
                self.assertIs(header["disable-model-invocation"], manual)
                self.assertIs(header["user-invocable"], manual)
                config = yaml.safe_load((PLUGIN / "skills" / name / "agents/openai.yaml").read_text(encoding="utf-8"))
                self.assertIs(config["policy"]["allow_implicit_invocation"], not manual)
                for field in ("display_name", "short_description", "default_prompt"):
                    self.assertIsInstance(config["interface"][field], str)
                    self.assertTrue(config["interface"][field])
                self.assertIn(f"${name}", config["interface"]["default_prompt"])
                self.assertNotIn("dependencies", config)

    def test_standalone_links_and_no_private_paths(self):
        for name in sorted(NAMES):
            with self.subTest(skill=name):
                _, body = skill_parts(name)
                base = (PLUGIN / "skills" / name).resolve()
                for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", body):
                    if "://" in target or target.startswith("#"):
                        continue
                    path = (base / target.split("#")[0]).resolve()
                    self.assertTrue(path.is_relative_to(base), target)
                    self.assertTrue(path.exists(), target)
                for forbidden in ("/home/", ".claude-plugins-data", "CLAUDE_PLUGIN_ROOT", "write-tests", "auto-issue", "autoplug"):
                    self.assertNotIn(forbidden, body)

    def test_project_record_contract_is_available_standalone(self):
        # Presence/consistency guard only; this does not test model compliance.
        contracts = []
        for name in sorted(NAMES):
            with self.subTest(skill=name):
                _, body = skill_parts(name)
                self.assertIn("## Project records\n", body)
                contract = body.split("## Project records\n", 1)[1].split("\n## ", 1)[0]
                for marker in ("GLOSSARY.md", "CONTEXT.md", "docs/adr/", "docs/tasks/",
                               "read-only", "superseded", "unverified", "external"):
                    self.assertIn(marker, contract)
                contracts.append(contract)
        self.assertEqual(len(set(contracts)), 1, "Standalone record rules have drifted")

    def test_instruction_only_plugin(self):
        for directory in ("hooks", "commands", "scripts", "agents"):
            self.assertFalse((PLUGIN / directory).exists(), directory)
        for path in PLUGIN.rglob("*"):
            self.assertFalse(path.is_symlink(), str(path))
            if path.is_file():
                self.assertIn(path.suffix, {".md", ".json", ".yaml"})

    def test_user_docs_and_evaluation_exist(self):
        root_readme = (ROOT / "README.md").read_text(encoding="utf-8")
        readme = (PLUGIN / "README.md").read_text(encoding="utf-8")
        for name in NAMES:
            self.assertIn(name, root_readme)
            self.assertIn(name, readme)
        self.assertIn("engineering-discipline", root_readme)
        for name in ("cases.md", "result-template.md"):
            self.assertTrue((PLUGIN / "evaluation" / name).is_file())


if __name__ == "__main__":
    unittest.main()

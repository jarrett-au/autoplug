"""Packaging and wording guards, not model-behavior tests."""
import json
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PLUGIN = ROOT / "plugins/agent-evolve"
SKILL = PLUGIN / "skills/behavior-to-context/SKILL.md"


class BehaviorToContextPackage(unittest.TestCase):
    def test_frontmatter_and_portability(self):
        text = SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\n"))
        header, body = text[4:].split("\n---\n", 1)
        meta = yaml.safe_load(header)
        self.assertEqual(meta["name"], "behavior-to-context")
        self.assertTrue(meta["description"].startswith("Use when "))
        self.assertLessEqual(len(meta["description"]), 1024)
        self.assertLessEqual(len(body.split()), 900)
        for token in ("/home/", "autoplug", "CLAUDE_PLUGIN_ROOT", ".claude-plugins-data", "~/.omp", "self-critique-loop"):
            self.assertNotIn(token, body)

    def test_distribution_metadata(self):
        manifest = json.loads((PLUGIN / ".claude-plugin/plugin.json").read_text())
        marketplace = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text())
        entries = [p for p in marketplace["plugins"] if p["name"] == "agent-evolve"]
        self.assertEqual(len(entries), 1)
        self.assertEqual(manifest["description"], entries[0]["description"])
        self.assertEqual((ROOT / entries[0]["source"]).resolve(), PLUGIN.resolve())
        for path in (ROOT / "README.md", PLUGIN / "README.md"):
            self.assertIn("behavior-to-context", path.read_text())

    def test_authorization_and_non_overcorrection_guards(self):
        text = SKILL.read_text()
        for phrase in (
            "Do not modify context files unless explicitly asked",
            "one-off corrections; do not persist them without a request",
            "Verify its official documentation",
            "neighboring legitimate use case",
            "not a behavioral test",
            "claim only checks actually performed",
            "change log or comparison still receives one",
        ):
            self.assertIn(phrase, text)


if __name__ == "__main__":
    unittest.main()

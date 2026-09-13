from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "agent_governor_validate", ROOT / "scripts" / "validate.py"
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

INSTALL_SPEC = importlib.util.spec_from_file_location(
    "agent_governor_install", ROOT / "scripts" / "install.py"
)
assert INSTALL_SPEC is not None and INSTALL_SPEC.loader is not None
INSTALL = importlib.util.module_from_spec(INSTALL_SPEC)
INSTALL_SPEC.loader.exec_module(INSTALL)


class PolicyValidationTest(unittest.TestCase):
    def test_repository_policy_is_safe(self) -> None:
        self.assertEqual(MODULE.validate(), [])

    def test_project_install_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            (project / "AGENTS.md").write_text(
                "# Example\n\n## Existing\n\nKeep me.\n", encoding="utf-8"
            )
            (project / "CLAUDE.md").write_text(
                "# Example\n\n## Existing\n\nKeep me.\n", encoding="utf-8"
            )

            INSTALL.install_project(project, "both")
            first_agents = (project / "AGENTS.md").read_text(encoding="utf-8")
            first_claude = (project / "CLAUDE.md").read_text(encoding="utf-8")
            INSTALL.install_project(project, "both")

            self.assertEqual(
                (project / "AGENTS.md").read_text(encoding="utf-8"), first_agents
            )
            self.assertEqual(
                (project / "CLAUDE.md").read_text(encoding="utf-8"), first_claude
            )
            self.assertEqual(first_agents.count(INSTALL.BEGIN), 1)
            self.assertEqual(first_claude.count(INSTALL.BEGIN), 1)
            self.assertIn("Keep me.", first_agents)
            self.assertIn("Keep me.", first_claude)
            self.assertTrue(
                (project / ".agents/skills/bdc-agentops/SKILL.md").is_file()
            )
            self.assertTrue(
                (project / ".claude/skills/bdc-agentops/SKILL.md").is_file()
            )


if __name__ == "__main__":
    unittest.main()

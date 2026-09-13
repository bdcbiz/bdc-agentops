from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "agent_governor_validate", ROOT / "scripts" / "validate.py"
)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PolicyValidationTest(unittest.TestCase):
    def test_repository_policy_is_safe(self) -> None:
        self.assertEqual(MODULE.validate(), [])


if __name__ == "__main__":
    unittest.main()

import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "profiles" / "plus" / "codex" / "config.toml"
SKILL_PATH = (
    ROOT
    / "profiles"
    / "plus"
    / "agents"
    / "skills"
    / "adaptive-orchestrator"
    / "SKILL.md"
)
WORKER_PATH = ROOT / "profiles" / "plus" / "codex" / "agents" / "worker.toml"


class PlusProfileTests(unittest.TestCase):
    def test_model_and_multi_agent_defaults(self):
        config = CONFIG_PATH.read_text(encoding="utf-8")

        self.assertIn('model = "gpt-5.6-sol"', config)
        self.assertIn('[agents]\nenabled = true', config)
        self.assertIn('default_subagent_model = "gpt-5.6-luna"', config)
        self.assertIn('default_subagent_reasoning_effort = "xhigh"', config)
        self.assertIn('[features]\nmulti_agent_v2 = true', config)

    def test_routine_delegation_requires_a_fresh_context(self):
        skill = SKILL_PATH.read_text(encoding="utf-8")
        worker = WORKER_PATH.read_text(encoding="utf-8")

        self.assertIn('fork_turns="none"', skill)
        self.assertIn("user explicitly asks", skill)
        self.assertIn('model = "gpt-5.6-luna"', worker)
        self.assertIn('model_reasoning_effort = "xhigh"', worker)
        self.assertIn('fork_turns="none"', worker)


if __name__ == "__main__":
    unittest.main()

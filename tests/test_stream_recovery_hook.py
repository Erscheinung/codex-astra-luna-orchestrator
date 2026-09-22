import json
import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HOOK = (
    Path(__file__).resolve().parents[1]
    / "profiles"
    / "plus"
    / "codex"
    / "hooks"
    / "continue_on_stream_disconnect.py"
)
MARKER = "stream disconnected before completion: stream closed before response.completed"


SPEC = importlib.util.spec_from_file_location("stream_recovery_hook", HOOK)
assert SPEC and SPEC.loader
HOOK_MODULE = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = HOOK_MODULE
SPEC.loader.exec_module(HOOK_MODULE)


class StreamRecoveryHookTests(unittest.TestCase):
    def run_hook(self, event):
        result = subprocess.run(
            [sys.executable, str(HOOK)],
            input=json.dumps(event),
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout) if result.stdout.strip() else None

    def test_exact_assistant_error_requests_one_continuation(self):
        self.assertEqual(
            self.run_hook({"last_assistant_message": MARKER}),
            {"decision": "block", "reason": "continue"},
        )

    def test_top_level_error_event_requests_a_continuation(self):
        event = {
            "error": {
                "code": "UPSTREAM_LLM_ERROR",
                "message": "invalid_encrypted_content",
                "type": "upstream_error",
            },
            "type": "error",
        }

        self.assertEqual(
            self.run_hook(event),
            {"decision": "block", "reason": "continue"},
        )

    def test_transcript_error_does_not_block_a_later_stop(self):
        with tempfile.TemporaryDirectory() as directory:
            transcript = Path(directory) / "rollout.jsonl"
            transcript.write_text(
                json.dumps(
                    {
                        "payload": {
                            "type": "task_complete",
                            "last_agent_message": None,
                            "error": {"message": MARKER},
                        }
                    }
                ),
                encoding="utf-8",
            )
            self.assertIsNone(self.run_hook({"transcript_path": str(transcript)}))

    def test_watcher_queues_once_until_successful_turn(self):
        state = HOOK_MODULE.WatchState()
        error = {
            "payload": {
                "type": "task_complete",
                "turn_id": "turn-1",
                "error": {"message": MARKER},
            }
        }
        success = {
            "payload": {
                "type": "task_complete",
                "turn_id": "turn-2",
            }
        }

        self.assertTrue(state.observe(error))
        self.assertFalse(state.observe(error))
        self.assertFalse(state.observe(success))
        self.assertTrue(state.observe(error))

    def test_watcher_queues_for_a_top_level_error_event(self):
        state = HOOK_MODULE.WatchState()
        error = {
            "error": {
                "code": "UPSTREAM_LLM_ERROR",
                "message": "invalid_encrypted_content",
                "type": "upstream_error",
            },
            "type": "error",
        }

        self.assertTrue(state.observe(error))
        self.assertFalse(state.observe(error))

    def test_stop_hook_active_prevents_a_retry_loop(self):
        self.assertIsNone(
            self.run_hook(
                {
                    "stop_hook_active": True,
                    "last_assistant_message": MARKER,
                }
            )
        )


if __name__ == "__main__":
    unittest.main()

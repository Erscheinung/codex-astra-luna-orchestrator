#!/usr/bin/env python3
"""Recover Codex provider errors without blocking normal turns.

The Stop hook is intentionally conservative: current Codex does not expose
transport errors to Stop hooks, and looking back through the transcript there
would re-trigger a stale error on the next successful turn.  The SessionStart
background mode watches the live rollout instead and queues one native
"continue" after a newly-written rollout error.
"""

from __future__ import annotations

import json
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ERROR_MARKER = (
    "stream disconnected before completion: "
    "stream closed before response.completed"
)
WATCH_POLL_SECONDS = 0.25
QUEUE_TIMEOUT_SECONDS = 10


def contains_marker(value: Any) -> bool:
    """Return whether a value contains the provider's exact error marker."""

    if isinstance(value, str):
        normalized = " ".join(value.casefold().split())
        return ERROR_MARKER in normalized
    if isinstance(value, (dict, list, tuple)):
        return contains_marker(json.dumps(value, ensure_ascii=False))
    return False


def should_continue(event: dict[str, Any]) -> bool:
    """Return whether a future Stop event explicitly reports the error.

    Do not inspect the transcript here.  Stop runs on the next successful
    completion too, so a stale transcript error would block an unrelated turn.
    """

    if event.get("stop_hook_active"):
        return False

    # Error details vary by provider, so an explicit non-null error is the
    # recovery signal rather than a particular code or message.
    if event.get("error") is not None:
        return True

    if contains_marker(event.get("last_assistant_message")):
        return True

    if contains_marker(event.get("error")):
        return True

    return False


@dataclass
class WatchState:
    """Allow one queued recovery until a later turn completes successfully."""

    recovery_queued: bool = False
    failed_turn_id: str | None = None

    def observe(self, record: dict[str, Any]) -> bool:
        payload = record.get("payload")
        event = payload if isinstance(payload, dict) else record

        turn_id = event.get("turn_id")
        if event.get("error") is not None:
            if self.recovery_queued:
                return False
            self.recovery_queued = True
            self.failed_turn_id = str(turn_id) if turn_id else None
            return True

        if self.recovery_queued and (
            self.failed_turn_id is None or turn_id != self.failed_turn_id
        ):
            self.recovery_queued = False
            self.failed_turn_id = None

        return False


def read_new_records(path: Path, offset: int) -> tuple[int, list[dict[str, Any]]]:
    """Read complete JSONL records appended since offset."""

    try:
        size = path.stat().st_size
        if size < offset:
            offset = 0
        with path.open("rb") as transcript:
            transcript.seek(offset)
            data = transcript.read()
    except OSError:
        return offset, []

    records: list[dict[str, Any]] = []
    consumed = 0
    for raw_line in data.splitlines(keepends=True):
        if not raw_line.endswith(b"\n"):
            break
        consumed += len(raw_line)
        try:
            record = json.loads(raw_line)
        except json.JSONDecodeError:
            continue
        if isinstance(record, dict):
            records.append(record)

    return offset + consumed, records


def queue_continue(session_id: str, cwd: Any) -> bool:
    """Queue the native continuation through the existing Codex session."""

    try:
        result = subprocess.run(
            ["codex", "queue", "--thread", session_id, "--message", "continue"],
            cwd=str(cwd) if cwd else None,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=QUEUE_TIMEOUT_SECONDS,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


def watch_session(event: dict[str, Any]) -> int:
    """Watch one session rollout until Codex cancels this background hook."""

    session_id = event.get("session_id")
    transcript_path = event.get("transcript_path")
    if not session_id or not transcript_path:
        return 0

    path = Path(str(transcript_path))
    try:
        offset = path.stat().st_size
    except OSError:
        offset = 0

    state = WatchState()
    while True:
        offset, records = read_new_records(path, offset)
        for record in records:
            if state.observe(record):
                queue_continue(str(session_id), event.get("cwd"))
        time.sleep(WATCH_POLL_SECONDS)


def main() -> int:
    try:
        event = json.load(sys.stdin)
    except (json.JSONDecodeError, TypeError):
        return 0

    if isinstance(event, dict) and "--watch" in sys.argv:
        return watch_session(event)

    if isinstance(event, dict) and should_continue(event):
        json.dump({"decision": "block", "reason": "continue"}, sys.stdout)
        sys.stdout.write("\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

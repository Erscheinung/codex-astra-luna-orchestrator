---
name: no-subagents
description: Work directly in the primary agent when the user explicitly requests no subagents for a task or chat.
---

# No subagents

Complete the user's task directly in the primary agent, including implementation
and proportionate validation. Do not spawn, delegate, or resume subagents. This
overrides adaptive-orchestrator and project delegation defaults without changing
models, configuration, or installed skills.

Proceed without asking for confirmation or permission to work solo. If invoked
alone, briefly acknowledge the preference and apply it to the next task; do not
ask a routing question. Ordinary missing requirements and safety constraints
still apply.

Keep this preference through the task's follow-ups and retries. Normal adaptive
routing returns for a new unrelated task unless the user requested the whole
chat. An explicit "use subagents again" restores normal routing. If scope is
unclear, stay solo without asking. Preserve the preference in continuation notes.

If workers are already running on this task, interrupt them before taking over
their files, preserve their edits, and do not resume them. Continue to honor any
applicable restrictions on reviewing prior worker-authored code.

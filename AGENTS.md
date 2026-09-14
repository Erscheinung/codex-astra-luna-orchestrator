# Adaptive Codex orchestration

For non-trivial coding implementation that benefits from a fresh context, use the `adaptive-orchestrator` skill.

The primary agent owns scope, decisions, delegation, and synthesis, not routine implementation. Treat orchestration as adaptive routing, never as a fixed explorer -> worker -> tester -> reviewer pipeline.

For small coding work, one bounded worker is enough. Specialists are conditional and multiple writers need explicit non-overlapping ownership. The worker owns implementation and focused validation through completion.

## Live subagent visibility

- Give each spawned subagent a descriptive name and a concise task/role. The native command center uses this metadata to show what each agent is doing.
- After spawning the first subagent for a task, tell the user once: `Live progress is available in another terminal: run codex agents.` This is informational; do not ask the user for status prompts or paste-back updates just to provide visibility.
- `codex agents` is a shell subcommand, separate from the `/agents` slash command. The user should run it in a second terminal, tab, or split while the main Codex TUI is running. It connects to the shared local app-server daemon and displays projects, tasks, and agent statuses without consuming model input tokens in the main thread.
- The command center's on-screen help and key hints are authoritative for navigation. Do not assume or document undocumented key bindings.
- Visibility through the command center does not change the delegation gate, model assignments, or no-automatic-review contract.

Do not inspect, diff-review, or independently review worker-authored code, and do not automatically spawn a reviewer. Review that code only after the user personally reports a bug and asks for diagnosis or repair.

User instructions always take precedence.

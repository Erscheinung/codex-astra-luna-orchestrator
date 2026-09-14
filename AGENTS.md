# Adaptive Codex orchestration

For non-trivial coding implementation that benefits from a fresh context, use the `adaptive-orchestrator` skill.

The primary agent owns scope, decisions, delegation, and synthesis, not routine implementation. Treat orchestration as adaptive routing, never as a fixed explorer -> worker -> tester -> reviewer pipeline.

For small coding work, one bounded worker is enough. Specialists are conditional and multiple writers need explicit non-overlapping ownership. The worker owns implementation and focused validation through completion.

## Live subagent visibility

- Give each spawned subagent a descriptive name and a concise task/role. The native command center uses this metadata to show what each agent is doing.
- After spawning the first subagent for a task, tell the user once: `To watch it live, type /agent (or /agents) and select the child thread.` In the interactive Codex TUI, this opens the native in-chat picker; selecting a child switches the active view to that thread's live transcript, rendered tool activity, and status updates. Choose the parent/root entry from the same picker to return. Treat V2 child views as inspection-first: they may be read-only, so do not promise that users can directly edit or steer a child from the selected view.
- `codex agents` is a separate shell subcommand for a cross-session overview. The user can run it in a second terminal, tab, or split while the main Codex TUI is running to inspect projects, tasks, agent names, and statuses; it complements the in-chat picker rather than replacing it. It connects to the shared local app-server daemon without consuming model input tokens in the main thread.
- If the parent transcript says a child started but `/agent` does not list it, treat that as a Codex app-server/TUI registration or refresh failure. Project instructions and `agents.enabled`/`features.multi_agent_v2` settings cannot repair a missing picker entry; suggest `codex agents`, `codex doctor`, and an upgrade or upstream report instead of promising another prompt will expose the child.
- The command center's on-screen help and key hints are authoritative for navigation. Do not assume or document undocumented key bindings.
- Visibility through the command center does not change the delegation gate, model assignments, or no-automatic-review contract.

Do not inspect, diff-review, or independently review worker-authored code, and do not automatically spawn a reviewer. Review that code only after the user personally reports a bug and asks for diagnosis or repair.

User instructions always take precedence.

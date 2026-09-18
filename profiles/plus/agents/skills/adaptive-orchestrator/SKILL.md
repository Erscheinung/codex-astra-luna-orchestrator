---
name: adaptive-orchestrator
description: Adaptively route non-trivial coding implementation to a bounded fresh-context worker without imposing an explorer/tester/reviewer pipeline. Use when implementation benefits from context separation, parallel ownership, or account-aware model routing; skip tiny work that is clearer in the primary context.
---

# Adaptive orchestration

Keep the GPT-5.6 Sol primary agent focused on scope, decisions, delegation, and synthesis. Delegate only when separation materially helps.

For small coding work, one `worker` should own implementation and focused validation end to end. For independent workstreams, give workers non-overlapping ownership. Add investigation or specialists only when actual risk warrants them.

Use the GPT-5.6 Luna `worker` at xhigh by default. Use `sol_worker` only when the user asks for Sol or Luna is impractical because of usage, credits, or availability. Model assignments live in Codex configuration and agent TOML files.

Every delegation states a concrete outcome, bounded scope, constraints, and acceptance criteria. Workers finish routine choices instead of repeatedly handing them back.

Spawn bounded implementation workers with `fork_turns="none"`. Never omit
`fork_turns` or use `"all"` for routine delegation: the worker must start from
its role instructions, applicable repository instructions, and the complete
self-contained delegation prompt rather than the parent conversation. Inherit
parent turns only when the user explicitly asks for that context to be shared.

## Live progress

Use descriptive agent names and concise task descriptions so the native command
center can identify each worker. After the first spawn in a task, tell the user
once: `To watch it live, type /agent (or /agents) and select the child thread.`
In the interactive TUI, this opens the native in-chat picker. Selecting a child
switches the active view to its live transcript, rendered tool activity, and
status updates; selecting the parent/root entry returns to the planner. V2
child views may be read-only, so do not promise direct editing or steering from
the selected child.

The picker is scoped to the active root thread and its descendants; it does not
merge children from other resumed or top-level sessions. If `codex agents`
shows a child under another parent, tell the user to resume that parent (or the
child directly) with `codex resume <thread-id>` before using `/agent`.
If the child belongs to the active root but was spawned before this TUI was
resumed, resume the parent once more so the picker can backfill descendants;
the 0.154 TUI can otherwise report no agents after missing the child-start
event.

Keep `codex agents` as an optional cross-session overview: it is a shell
subcommand, not the `/agent` or `/agents` slash command. The user can open it
in a second terminal, tab, or split while the main Codex TUI remains running.
It connects to the shared local app-server daemon and shows projects, tasks,
and statuses without spending model input tokens on status prompts. Let the
command center's on-screen help and key hints define navigation; do not
document undocumented key bindings.

If the parent transcript says a child started but `/agent` does not list it,
call this out as a Codex app-server/TUI registration or refresh problem. The
project's `agents.enabled` and `features.multi_agent_v2` settings cannot repair
that missing picker entry. Suggest `codex agents` and `codex doctor`, then an
upgrade or upstream report; do not promise that another prompt will expose the
child.

Do not automatically review worker output. The primary agent and orchestrator must not inspect or diff-review worker-authored code, and must not spawn a reviewer. Accept the worker's report and test evidence. Review that code only after the user personally reports a bug and asks for diagnosis or repair.

User instructions take precedence. Preserve repository constraints, unrelated user changes, and the original authorization boundary.

## Provider stream recovery

If the global SessionStart watcher sees stream disconnected before completion:
stream closed before response.completed, it may queue one native continuation
with the prompt continue. This recovery is handled locally and does not invoke
another model just to detect the error; the continuation itself is a new model
turn and can consume tokens. Do not create an agent or a separate retry
process for this condition.

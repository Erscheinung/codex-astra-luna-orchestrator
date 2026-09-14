---
name: adaptive-orchestrator
description: Adaptively route non-trivial coding implementation to a bounded fresh-context worker without imposing an explorer/tester/reviewer pipeline. Use when implementation benefits from context separation, parallel ownership, or account-aware model routing; skip tiny work that is clearer in the primary context.
---

# Adaptive orchestration — Plus profile

Keep the GPT-5.6 Sol primary agent focused on scope, decisions, delegation, and synthesis. Delegate only when separation materially helps.

For small coding work, one `worker` should own implementation and focused validation end to end. For independent workstreams, give workers non-overlapping ownership. Add investigation or specialists only when actual risk warrants them.

Use the GPT-5.6 Luna `worker` at xhigh by default. Use `sol_worker` only when the user asks for Sol or Luna is impractical because of usage, credits, or availability. Model assignments live in Codex configuration and agent TOML files.

Every delegation states a concrete outcome, bounded scope, constraints, and acceptance criteria. Workers finish routine choices instead of repeatedly handing them back.

## Live progress

Use descriptive agent names and concise task descriptions so the native command
center can identify each worker. After the first spawn in a task, tell the user
once that live progress is available from a separate terminal with
`codex agents`. This is a shell subcommand, not the `/agents` slash command:
the user should open it in a second terminal, tab, or split while the main
Codex TUI is running. It connects to the shared local app-server daemon and
shows projects, tasks, and statuses without spending model input tokens on
status prompts. Let the command center's on-screen help and key hints define
navigation; do not document undocumented key bindings.

Do not automatically review worker output. The primary agent and orchestrator must not inspect or diff-review worker-authored code, and must not spawn a reviewer. Accept the worker's report and test evidence. Review that code only after the user personally reports a bug and asks for diagnosis or repair.

User instructions take precedence. Preserve repository constraints, unrelated user changes, and the original authorization boundary.

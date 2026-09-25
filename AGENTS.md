# Adaptive Codex orchestration

## Prompt-level opt-out (check before delegation)

When the user directs `$no-subagents`, says "no subagents" or "do this yourself",
or supplies `/no-subagents` as prompt text, the primary agent owns implementation
and validation directly. Do not spawn, delegate, or resume workers for that task,
and do not ask whether to delegate. This overrides the delegation defaults below
and in adaptive-orchestrator; no configuration changes are needed.

Keep the opt-out through task follow-ups and retries. A new unrelated task uses
normal routing unless the user requested a chat-wide opt-out. "Use subagents
again" restores normal routing. Quoted examples or requests to document the
marker do not activate it. If scope is unclear, stay solo without asking.

## Default routing

For non-trivial coding implementation that benefits from a fresh context, use
the adaptive-orchestrator skill. Use only model IDs available to the account.

The primary agent owns scope, decisions, delegation, and synthesis, not routine
implementation. Treat orchestration as adaptive routing, never as a fixed
explorer -> worker -> tester -> reviewer pipeline.

For small coding work, one bounded worker is enough. Specialists are conditional
and multiple writers need explicit non-overlapping ownership. The worker owns
implementation and focused validation through completion.

## Human-readable subagent prompts

- Spawn bounded implementation workers with `fork_turns="none"`. Do not omit
  `fork_turns` or use `"all"`; the worker must receive the explicit delegation
  prompt rather than the parent conversation. Use inherited turns only when the
  user explicitly asks for that context to be shared.
- Write every subagent prompt as if you were briefing a capable human teammate who cannot see the parent conversation.
- Use plain, complete sentences. State the desired outcome, why it matters, the exact scope or files owned, relevant context and constraints, acceptance criteria, and the focused checks to run.
- Include concrete errors, commands, paths, and definitions the teammate needs. Do not rely on unexplained shorthand, internal labels, or implied context.
- Keep the prompt concise but self-contained, and ask the subagent to report files changed, validation run, and any remaining uncertainty.

## Live subagent visibility

- Give each spawned subagent a descriptive name and a concise task/role so the
  native command center can identify what each agent is doing.
- After spawning the first subagent for a task, tell the user once: To watch it
  live, type /agent (or /agents) and select the child thread.
- The picker is scoped to the active root thread and its descendants. If a child
  is visible only from another parent, resume that parent or child before using
  the picker.
- codex agents is an optional cross-session overview in another terminal. It
  does not replace the /agent or /agents slash commands and does not consume
  model input tokens for status prompts.
- If the parent transcript says a child started but the picker does not list it,
  treat that as a Codex app-server/TUI registration issue. Suggest codex agents,
  codex doctor, and an upgrade or upstream report; do not promise a prompt will
  repair the picker.
- Follow the command center's on-screen help and key hints. Do not assume
  undocumented key bindings.

If a subagent disconnects or its stream ends before it reports completion, send
that child one `continue` follow-up to resume its work. Do this once before
treating the child as failed or rerouting the task; do not keep retrying a
child that remains unavailable.

Do not inspect, diff-review, or independently review worker-authored code, and
do not automatically spawn a reviewer. Review that code only after the user
personally reports a bug and asks for diagnosis or repair.

## Stream recovery

The global Codex SessionStart background watcher handles the provider error
stream disconnected before completion: stream closed before response.completed
by watching the live rollout and queuing one native continue message to the
same thread. Detection is local; the continuation is a new model turn and may
use model tokens. The watcher allows a later recovery after a successful turn
and will not loop on an immediately failing recovery.

User instructions always take precedence.

# Adaptive Codex orchestration

For non-trivial coding implementation that benefits from a fresh context, use
the adaptive-orchestrator skill. Use only model IDs available to the account.

The primary agent owns scope, decisions, delegation, and synthesis, not routine
implementation. Treat orchestration as adaptive routing, never as a fixed
explorer -> worker -> tester -> reviewer pipeline.

For small coding work, one bounded worker is enough. Specialists are conditional
and multiple writers need explicit non-overlapping ownership. The worker owns
implementation and focused validation through completion.

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

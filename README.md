# Codex Adaptive Orchestrator

A Codex setup for adaptive Sol/Luna routing. The supported profile uses Sol for
planning and delegation, and Luna for bounded implementation workers. It does
not depend on unavailable model IDs or an automatic review stage.

## Layout

~~~text
.
├── profiles/plus/
│   ├── codex/                         # config, role files, and Stop hook
│   └── agents/skills/adaptive-orchestrator/
├── guides/
├── scripts/token_usage.py
├── tests/
├── AGENTS.md
├── setup.sh
└── setup.ps1
~~~

## Supported configuration

| Role or setting | Model / behavior |
|---|---|
| Primary agent | GPT-5.6 Sol, low reasoning |
| Implementation worker | GPT-5.6 Luna, xhigh reasoning |
| Default subagent | GPT-5.6 Luna, xhigh reasoning |
| Review | Only after a user-reported bug and an explicit diagnosis request |
| Concurrent child limit | 4 |

The installer copies profiles/plus/codex to .codex and
profiles/plus/agents to .agents in the target repository. It also appends the
repository-level AGENTS.md instructions without discarding existing contents.

## Project setup

The target project must already exist and must be different from this setup
repository.

### macOS and Linux

~~~bash
./setup.sh
~~~

### Windows

~~~powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
~~~

The installer now has one supported profile: Plus. Press Enter at the profile
prompt to select it. Existing files are listed and require confirmation before
they are replaced.

## Global setup

Codex loads global instructions from ~/.codex/AGENTS.override.md when that file
exists, otherwise from ~/.codex/AGENTS.md. Install the adaptive skill and role
files globally with:

~~~bash
mkdir -p ~/.codex/agents ~/.codex/skills/adaptive-orchestrator
cp profiles/plus/agents/skills/adaptive-orchestrator/SKILL.md \
  ~/.codex/skills/adaptive-orchestrator/SKILL.md
cp profiles/plus/codex/agents/*.toml ~/.codex/agents/
~~~

Merge profiles/plus/codex/config.toml into ~/.codex/config.toml; preserve
existing providers, MCP servers, permissions, and project trust entries.

This repository also provides a global stream-recovery hook. Install its
implementation and merge its Stop entry into ~/.codex/hooks.json:

~~~bash
mkdir -p ~/.codex/hooks
cp profiles/plus/codex/hooks/continue_on_stream_disconnect.py \
  ~/.codex/hooks/continue_on_stream_disconnect.py
~~~

Use the existing global hook file as the base when merging. The command should
invoke:

~~~text
python3 ~/.codex/hooks/continue_on_stream_disconnect.py
~~~

Open /hooks in Codex to review and trust the changed non-managed hook. The hook
itself makes no model request. When the exact provider error is detected,
Codex's native Stop-hook continuation creates one new user-equivalent prompt,
continue. That retry is a new model turn and may consume tokens; the local
error detection does not.

If a subagent stream ends before completion, send that child one `continue`
follow-up before treating it as failed or rerouting its task. Do not repeatedly
retry a child that remains unavailable.

## Adaptive orchestration

Use the adaptive-orchestrator skill for work where a fresh context materially
helps. A normal implementation task gets one bounded Luna worker that owns its
implementation and focused validation. Exploration, research, testing, and
other specialists are conditional. Do not create a fixed pipeline or an
automatic reviewer.

The native /agent picker shows children of the active root. For a cross-session
overview, use codex agents in another terminal while Codex is running. If a
child is missing from the picker, verify with codex agents and codex doctor
rather than changing orchestration settings blindly.

## Token usage

The read-only scripts/token_usage.py groups Codex rollout files by root session
and reports usage by role and model:

~~~bash
scripts/token_usage.py --list --date 2026-09-07
scripts/token_usage.py --latest --date 2026-09-07
scripts/token_usage.py --root SESSION_PREFIX --format json
~~~

See guides/ for routing, fast-iteration, routine-coding, and measurement notes.

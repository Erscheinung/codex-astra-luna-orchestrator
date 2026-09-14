# Codex Adaptive Orchestrator + Luna Subagents

A configurable Codex setup with separate Pro and Plus routing. The Plus profile uses GPT-5.6 Sol for planning and GPT-5.6 Luna at xhigh for fresh-context implementation workers, without automatic review.

The installer asks which Codex plan you are on. Pro retains the original Astra/Luna topology. Plus uses adaptive routing: the Sol primary agent owns scope and delegation, a bounded Luna worker owns routine implementation and focused validation, and specialists are used only when the task warrants them. A Sol worker is available when the user requests it or Luna is impractical because of usage, credits, or availability.

## Layout

```text
.
├── profiles/
│   ├── pro/
│   │   ├── codex/           (config.toml and agents/*.toml)
│   │   └── agents/          (skills/astra-orchestrator/SKILL.md)
│   └── plus/
│       ├── codex/           (config.toml and agents/*.toml)
│       └── agents/          (skills/adaptive-orchestrator/SKILL.md)
├── guides/
│   ├── fast-iteration.md
│   ├── complex-repo-work.md
│   ├── routine-coding.md
│   ├── full-orchestration.md
│   ├── plus-plan.md
│   └── token-usage.md
├── scripts/
│   └── token_usage.py
├── AGENTS.md
├── setup.sh
├── setup.ps1
└── LICENSE
```

## Current Plus and Pro configuration

| Role or setting | Plus | Pro |
|---|---|---|
| Orchestrator | GPT-5.6 Sol — low | GPT-6 Astra — medium |
| Implementation worker | GPT-5.6 Luna — xhigh | GPT-5.6 Luna — max |
| Default subagent | GPT-5.6 Luna — xhigh | GPT-5.6 Luna — max |
| Independent reviewer | Not installed; only review after a user-reported bug | GPT-6 Astra — low |
| Concurrent subagent limit | 4 | 4 |

### Pro — `profiles/pro/codex/config.toml`

```toml
model = "gpt-6-astra"
model_reasoning_effort = "medium"

approval_policy = "on-request"
sandbox_mode = "workspace-write"

[agents]
enabled = true
max_concurrent_threads_per_session = 4
default_subagent_model = "gpt-5.6-luna"
default_subagent_reasoning_effort = "max"
```

### Plus — `profiles/plus/codex/config.toml`

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "low"

approval_policy = "on-request"
sandbox_mode = "workspace-write"

[agents]
enabled = true
max_concurrent_threads_per_session = 4
default_subagent_model = "gpt-5.6-luna"
default_subagent_reasoning_effort = "xhigh"

[features]
multi_agent_v2 = true

[multi_agent_v2]
min_wait_timeout_ms = 1500000
default_wait_timeout_ms = 1500000
max_wait_timeout_ms = 1500000
```

The installer copies `profiles/<plan>/codex` to `.codex` and
`profiles/<plan>/agents` to `.agents` in the target repository. Each profile
is ready to copy, with no configuration rewriting during setup.

The Plus worker is explicitly pinned to Luna xhigh. Its `sol_worker` fallback is explicitly pinned to Sol xhigh. The Plus profile intentionally does not install a reviewer.

The Pro profile retains its original role assignments. In Plus, exploration and research remain optional, while the implementation worker owns focused validation rather than forcing a separate test/review pipeline.

When updating an existing installation, copy the role files along with `config.toml` from the selected profile. Replace `<plan>` below with `pro` or `plus`.

To make a named role follow `[agents]` defaults, remove both its `model` and `model_reasoning_effort` overrides.

## Project setup

Clone this repository:

```bash
git clone https://github.com/donvito/codex-astra-luna-orchestrator.git
cd codex-astra-luna-orchestrator
```

The target project must already exist and must be different from this setup
repository.

### macOS and Linux

Run the shell installer:

```bash
./setup.sh
```

### Windows

Run the PowerShell installer from Windows PowerShell:

```powershell
powershell -ExecutionPolicy Bypass -File .\setup.ps1
```

With PowerShell 7, you can use:

```powershell
pwsh -File .\setup.ps1
```

### Installer prompts

When asked for the target repository, enter its absolute or relative path. For
example:

```text
Target repository path: ../my-project
```

Next, choose your Codex plan:

```text
Codex plan:
  1) Pro  - GPT-6 Astra orchestrates, GPT-5.6 Luna executes, GPT-6 Astra reviews
  2) Plus - GPT-5.6 Sol plans, GPT-5.6 Luna (xhigh) implements, review only after a user-reported bug
Select plan [1/2] (default 1):
```

The selected configuration sets both the root and default subagent reasoning.
Agent role files are plan-specific. Plus uses an xhigh Luna implementation
worker and an opt-in xhigh Sol fallback; it does not install a reviewer.

The installer then asks whether to install each component:

- `profiles/<plan>/codex` contains the root configuration and agent role profiles, installed as `.codex`.
- `profiles/<plan>/agents` contains the plan's orchestration skill, installed as `.agents`.
- `AGENTS.md` gives Codex the project-level orchestration instructions. If it
  already exists, setup appends the instructions and preserves its contents.
  Re-running setup skips the append when the same instructions are already
  present. Symbolic links and incompatible targets are skipped.

Press Enter or answer `y` to install a component; answer `n` to skip it. All
three components are selected by default.

If a component already exists, the installer lists the exact paths that would
be overwritten and asks again before making changes:

```text
WARNING: the following existing files will be overwritten:
  - .codex/config.toml
Update .codex? New files will be added; only paths listed above will be replaced. [y/N]
```

Existing-file updates default to `n`. If approved, missing files are added and
only the listed paths are replaced. Other files already present in the target
component remain untouched.

After setup, launch Codex from the target repository. Project-scoped `.codex`
configuration is loaded only for trusted projects.

See `guides/` for copy-paste model presets and the Astra + Luna topology. The
guides are intentionally separate from the installers so you can review and
adapt settings for your Codex version without changing a global config
automatically.

## Personal/global setup

For agents, copy the TOML files from `profiles/<plan>/codex/agents/` to:

```text
~/.codex/agents/
```

For the Plus skill, copy `profiles/plus/agents/skills/adaptive-orchestrator/` to:

```text
~/.codex/skills/adaptive-orchestrator/
```

Merge the settings from `profiles/pro/codex/config.toml` (Pro) or `profiles/plus/codex/config.toml`
(Plus) into your existing:

```text
~/.codex/config.toml
```

Do not blindly overwrite your existing global config if you already have MCP servers, providers, permissions, or other settings.

## Using the skill

Codex may select the skill automatically when the task matches its description.

You can also invoke it explicitly from Codex CLI or the IDE extension with:

```text
$adaptive-orchestrator
```

## View live subagent progress

The interactive Codex TUI has a native in-chat agent picker. While the main task
continues, type:

```text
/agent
```

`/agents` is an alias. Select the parent or a child thread in the picker to
switch the active view. A selected child shows the live transcript, rendered
tool activity, and status updates that Codex exposes for that thread; completed
children remain available for transcript inspection. Use `/agent` again and
select the parent/root entry to return. V2 child views are primarily for
observation and may be read-only, so do not assume that a selected child is a
second editable chat.

Codex also has a native terminal command center for a cross-session overview.
In a second terminal, tab, or split, run:

```bash
codex agents
```

This shell subcommand is separate from the `/agent` and `/agents` slash
commands. Keep the main Codex TUI running: `codex agents` connects to the
shared local app-server daemon and shows available projects, tasks, agent names,
and statuses. It reads that live state directly, so checking the overview does
not require a status prompt in the main thread or consume model input tokens.
Use the command center's on-screen help and key hints for navigation; key
bindings can vary by Codex release and are intentionally not duplicated here.

If the parent transcript says a child started but `/agent` reports no agents or
does not list that child, this is a Codex app-server/TUI registration or refresh
failure, not something project instructions can repair. Verify the child in
`codex agents` and collect `codex doctor` output; upgrade or report the CLI
issue rather than promising that a prompt or config change will make the child
appear.

For command-line options, run `codex agents --help`.

Example prompt:

```text
$adaptive-orchestrator

Implement the new invoice export endpoint.
Use one bounded worker to implement and run focused validation.
Do not create a review stage unless I later report a bug.
```

## Pro topology

```text
                 GPT-6 Astra
             root / orchestrator
                      |
      +---------------+---------------+
      |               |               |
   explorer          worker         researcher
     Luna             Luna             Luna
      |               |
      +-------+-------+
              |
           tester
            Luna
              |
          reviewer
           Astra
              |
              v
         GPT-6 Astra
      integrate + verify
```

## Tuning

For cheaper/faster runs:
- lower Pro's Astra reasoning from `medium` to `low`
- set Luna reasoning to `low` or `medium`
- use 3-4 concurrent threads

For larger codebases:
- consider raising Pro's Astra reasoning to `high`
- start with your plan's Luna default and adjust based on results
- use 6-8 concurrent threads, only when tasks are actually independent

For the Plus profile, prefer a single bounded Luna worker for ordinary implementation. Add specialists only when the task materially benefits, and do not create an automatic review stage.

## Token usage

Orchestration is not free: the root stays in the loop for the whole task and
every subagent carries its own context. Usage depends on repository size and
task shape, so there is no single number. `scripts/token_usage.py` reads the
rollout logs Codex already writes under `~/.codex/sessions` and reports usage
per thread, role, and model, plus the change in your 5-hour and 7-day rate
limit windows:

```bash
scripts/token_usage.py --list --date 2026-09-07
scripts/token_usage.py --latest --date 2026-09-07
```

See [`guides/token-usage.md`](guides/token-usage.md) for a measurement
protocol, one sample run with real numbers, and tips for reducing usage.

Plus users: the root thread owns planning and delegation on Sol, while routine implementation runs in a fresh Luna context. For a manual or global setup see [`guides/plus-plan.md`](guides/plus-plan.md):

```toml
# Root
model = "gpt-5.6-sol"
model_reasoning_effort = "low"
```

## Important behavior

Explicit model choices during a spawn override `[agents]` defaults. Custom agent files that specify `model` or `model_reasoning_effort` also take precedence over inherited defaults.

The Plus implementation role is pinned to Luna xhigh, with an opt-in Sol fallback. The Pro profile retains the original Luna execution roles and Astra reviewer.

## License

Licensed under the [Apache License 2.0](LICENSE).

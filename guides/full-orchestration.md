# Adaptive Orchestration

Use the supported Plus profile for multi-file features, cross-component bugs,
and work where a fresh implementation context materially helps. The installer
copies profiles/plus/codex to .codex and profiles/plus/agents to .agents.

The topology is intentionally adaptive:

~~~text
Terra or Sol primary (medium/high/xhigh)
└── Luna worker (xhigh), when a fresh context helps
    ├── optional explorer
    ├── optional researcher
    └── optional tester
~~~

The worker owns implementation and focused validation through completion.
Specialists are conditional, and there is no automatic review stage. Routine
workers must start with `fork_turns="none"` and a self-contained prompt.
Use inherited parent history only when the user explicitly asks for that
context to be shared.

For project-scoped configuration, copy profiles/plus/codex/config.toml to
.codex/config.toml. For personal setup, merge the settings into
~/.codex/config.toml rather than replacing unrelated configuration:

~~~toml
model = "gpt-5.6-sol"
model_reasoning_effort = "low"

[agents]
enabled = true
max_concurrent_threads_per_session = 4
default_subagent_model = "gpt-5.6-luna"
default_subagent_reasoning_effort = "xhigh"

[features]
multi_agent_v2 = true
~~~

Use profiles/plus/codex/agents/ for named role files and
profiles/plus/agents/skills/adaptive-orchestrator/ for the skill.

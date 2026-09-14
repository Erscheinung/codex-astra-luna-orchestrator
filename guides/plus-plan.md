# Plus Plan

Choose this profile for a GPT-5.6 Sol primary agent at low reasoning and fresh-context GPT-5.6 Luna implementation workers at xhigh reasoning.

The installer copies `profiles/plus/codex/` into the target repository's `.codex/` and installs the adaptive orchestration skill from `profiles/plus/agents/`.

## Routing contract

- The primary Sol agent owns scope, decisions, delegation, and synthesis, not routine implementation.
- Delegate only when a fresh context or separate ownership materially helps.
- One bounded Luna worker is enough for ordinary coding work. It implements and runs focused validation through completion.
- Specialists are conditional, not mandatory stages.
- Do not inspect or independently review worker-authored code. Review it only after the user personally reports a bug and asks for diagnosis or repair.
- Use `sol_worker` only when the user asks for Sol or Luna is impractical because of usage, credits, or availability.

## Global installation

Merge `profiles/plus/codex/config.toml` into `~/.codex/config.toml`, copy the role files to `~/.codex/agents/`, and copy `profiles/plus/agents/skills/adaptive-orchestrator/` to `~/.codex/skills/adaptive-orchestrator/`.

The feature flag and its settings use separate tables:

```toml
[features]
multi_agent_v2 = true

[multi_agent_v2]
min_wait_timeout_ms = 1500000
default_wait_timeout_ms = 1500000
max_wait_timeout_ms = 1500000
```

`[features.multi_agent_v2]` is not valid in current Codex releases because `multi_agent_v2` is a Boolean feature flag rather than a table.

# Routine Coding

Choose this preset for predictable, routine coding tasks where lower cost and
faster orchestration are preferred.

This is an optional root override for the [Plus profile](plus-plan.md),
raising its Sol planner from `low` to `medium`. The Luna implementation worker
remains at `xhigh`, and Plus does not install an automatic reviewer.

Add or merge this into:

`~/.codex/config.toml`

```toml
model = "gpt-5.6-sol"
model_reasoning_effort = "medium"
service_tier = "fast"
```

If your Codex version does not support `service_tier`, remove that line and
keep the model and reasoning settings.

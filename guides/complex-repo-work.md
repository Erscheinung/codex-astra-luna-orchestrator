# Complex Repository Work

Choose this preset for architecture changes, difficult debugging, and work
where higher-confidence reasoning matters more than latency.

It is an optional override for the supported Plus profile. Keep Luna workers at
xhigh and raise only the Sol primary when the task benefits from deeper
planning:

~~~toml
model = "gpt-5.6-sol"
model_reasoning_effort = "medium"
service_tier = "standard"
~~~

If the Codex version does not support service_tier, remove that line. Merge this
into ~/.codex/config.toml without replacing unrelated settings.

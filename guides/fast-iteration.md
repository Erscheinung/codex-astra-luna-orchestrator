# Fast Iteration

Choose this preset when latency matters. It keeps the supported adaptive
routing while selecting the fast service tier for the Sol primary:

~~~toml
model = "gpt-5.6-sol"
model_reasoning_effort = "low"
service_tier = "fast"
~~~

If the Codex version does not support service_tier, remove that line and keep
the model and reasoning settings.

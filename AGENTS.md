# Adaptive Codex orchestration

For non-trivial coding implementation that benefits from a fresh context, use the `adaptive-orchestrator` skill.

The primary agent owns scope, decisions, delegation, and synthesis, not routine implementation. Treat orchestration as adaptive routing, never as a fixed explorer -> worker -> tester -> reviewer pipeline.

For small coding work, one bounded worker is enough. Specialists are conditional and multiple writers need explicit non-overlapping ownership. The worker owns implementation and focused validation through completion.

Do not inspect, diff-review, or independently review worker-authored code, and do not automatically spawn a reviewer. Review that code only after the user personally reports a bug and asks for diagnosis or repair.

User instructions always take precedence.

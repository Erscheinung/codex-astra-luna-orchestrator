# Token Usage

Usage depends on repository size, task shape, the number of workers actually
spawned, and how much context is served from cache. This guide gives a
repeatable way to measure the supported adaptive profile.

## What Codex records

Codex writes one rollout file per thread under
~/.codex/sessions/YYYY/MM/DD/rollout-*.jsonl. The useful records are:

- session_meta: thread identity, parent relationship, cwd, and role metadata.
- turn_context: the model and reasoning effort in force for the turn.
- token_usage_record: input, cached input, output, reasoning, and total tokens.
- token_count: cumulative totals and current rate-limit information.

Grouping rollout files by session_id gives the full cost of one task, split by
thread, role, and model. The repository script is read-only and uses only the
Python standard library.

## Measuring a run

~~~bash
scripts/token_usage.py --list --date 2026-09-07
scripts/token_usage.py --root SESSION_PREFIX --date 2026-09-07
scripts/token_usage.py --latest --date 2026-09-07
scripts/token_usage.py --root SESSION_PREFIX --format json
~~~

Omitting --date scans the whole sessions directory. Guardian threads are
excluded from totals by default; add --include-guardian when they matter to the
comparison.

## Benchmark protocol

For comparable measurements:

1. Choose representative tasks: a one-file fix, a multi-file feature, a
   cross-component bug, and a research-heavy change.
2. Run each task as a root-only baseline and with the supported Plus profile.
3. Record uncached input, cached input, output, reasoning tokens, workers,
   wall time, and five-hour and seven-day rate-limit deltas.
4. Repeat each comparison two or three times because run variance is material.
5. Record the Codex version, profile settings, service tier, and any overrides.

Suggested results table:

| Task | Configuration | Sol uncached / cached / out | Luna uncached / cached / out | Workers | Wall | 5h delta | 7d delta |
|---|---|---:|---:|---:|---:|---:|---:|
| example | Plus | 0 / 0 / 0 | 0 / 0 / 0 | 0 | 0m | 0% | 0% |

## Reading the numbers

Cached input can dominate. A raw total_tokens figure therefore overstates the
uncached work and is not enough to compare runs. Always inspect uncached input
and output separately.

Rate-limit percentages are account-wide. Other Codex sessions running at the
same time can inflate the delta. The mapping from tokens to window usage may
vary by model and is not a replacement for the account's own usage view.

The primary thread remains a significant line item because it owns the task,
polls workers, and integrates reports. Each worker re-reads its own context, so
parallelism trades tokens for latency. For small tasks, skip orchestration.

The stream-recovery Stop hook itself makes no model request. If it detects the
provider stream-disconnect error, the native continuation is a new model turn;
measure that retry as ordinary usage.

## Reducing usage

- Do not orchestrate one-file or otherwise obvious edits.
- Keep max_concurrent_threads_per_session low.
- Ask workers for concise reports and focused validation evidence.
- Add explorer, researcher, or tester roles only when they materially reduce
  risk or duplicate work would be more expensive.
- Lower reasoning effort for low-risk investigation when the account's model
  availability and quality requirements allow it.

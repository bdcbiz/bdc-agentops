---
name: agent-governor
description: Govern model choice, subagent delegation, permissions, and usage across AI coding workflows. Use before selecting models, spawning agents, parallelizing work, or escalating model cost.
---

# Agent Governor

Apply this skill as a resource-governance layer. Project instructions still decide
what may be built; this skill decides whether and how agents may be delegated.

Read [policy.md](references/policy.md) before choosing a model or spawning an
agent. Read [runtime-adapters.md](references/runtime-adapters.md) only when mapping
roles to a specific runtime. Load `routing.json` when enforcing or changing model
and concurrency limits.

## Default behavior

Use the single-agent fast path unless delegation has a clear, bounded benefit.
The default Codex manager is `gpt-5.6-sol`. Routine discovery and implementation
may use `gpt-5.6-luna` and `gpt-5.6-terra` respectively.

Never start `gpt-6-astra`, a higher-cost service tier, or a model with unknown
relative cost without explicit approval for the exact model and task. Before
asking, state the need, expected benefit, cheaper fallback, and maximum attempts.
Silence and approval from another task are not approval.

## Delegation workflow

1. Detect runtime capabilities; do not assume model overrides, usage reporting,
   named roles, or nested agents are available.
2. Reject delegation for small, sequential, or shared-state work.
3. Create a task contract from `references/task-contract.json` for each worker.
4. Enforce one writer per file, maximum two concurrent workers, one delegation
   level, and two attempts per worker.
5. Keep reviewers read-only and the manager responsible for synthesis and final
   validation.
6. Prefer tests, inspected diffs, static checks, and source evidence over agent
   confidence or consensus.
7. Record available usage using `schemas/usage-ledger.schema.json`, labeling it
   measured, estimated, or unavailable.

Delegation does not expand the user's authority. Workers cannot commit, push,
merge, deploy, delete material data, access secrets, contact third parties, or
spawn more agents unless the user separately authorized the action and the root
workflow explicitly assigned it.

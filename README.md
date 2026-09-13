# BDC AgentOps

BDC AgentOps is BDC's portable policy layer for AI coding workflows. It keeps a
manager agent in control, delegates only when useful, and blocks expensive or
unknown-cost model escalation until the user explicitly approves it.

The first release is intentionally configuration-first: it does not proxy model
traffic, store secrets, or modify projects automatically.

## Default policy

- Codex manager: `gpt-5.6-sol`
- Economy discovery: `gpt-5.6-luna`
- Standard implementation: `gpt-5.6-terra`
- Protected escalation: `gpt-6-astra`
- Unknown-cost model: approval required
- Concurrent workers: 2
- Delegation depth: 1
- Attempts per worker: 2
- File ownership: one writer per file

Protected models are not called merely because a task is difficult. The manager
must first explain the exact model, reason, expected benefit, cheaper alternative,
and bounded scope, then wait for explicit user approval.

## Repository layout

```text
SKILL.md                         Portable Codex/agent skill
agents/openai.yaml               Skill UI metadata
references/policy.md             Binding governance policy
references/routing.json          Machine-readable routing policy
references/runtime-adapters.md   Codex, Claude, and generic fallbacks
references/task-contract.json    Worker handoff contract
schemas/usage-ledger.schema.json Usage and audit schema
templates/                       AGENTS.md and CLAUDE.md integration snippets
scripts/validate.py              Dependency-free policy validation
tests/test_validate.py           Safety-invariant tests
```

## Use without modifying a project

Keep this repository outside application repositories and load or install the
skill from this folder in the agent runtime. Nothing in this repository edits an
application on its own.

When a project should permanently opt in, copy the relevant text from
`templates/AGENTS.snippet.md` or `templates/CLAUDE.snippet.md` into that project's
instruction file. That integration is an explicit project change, not an
automatic action.

## Validate

```bash
python3 scripts/validate.py
python3 -m unittest discover -s tests
```

## Status

This is a policy and workflow layer. Runtime token counts can be missing or
approximate, so the usage ledger distinguishes measured telemetry, estimates, and
confirmed billing.
# bdc-agentops

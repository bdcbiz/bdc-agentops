# Runtime adapters

Use role aliases in task logic and map them to models only at the runtime edge.
This prevents workflows from depending on a provider-specific name.

## Capability check

Before delegation, determine whether the runtime supports subagents, per-agent
model overrides, named roles, usage reporting, concurrency limits, and isolated
contexts. Unknown capability means unsupported until verified.

## Codex

Map `manager` to `gpt-5.6-sol`, `discovery` to `gpt-5.6-luna`, and routine
`implementation` to `gpt-5.6-terra`. `critical_escalation` maps to
`gpt-6-astra` but remains locked until explicit task-specific approval.

Fallback order when model override is unavailable:

1. use a named agent configuration already mapped to an approved model;
2. use the approved default subagent model;
3. remain on the manager model with a bounded role prompt;
4. remain single-agent.

Never report a selected model unless runtime metadata verifies it.

## Claude

Keep the currently configured manager model. Select a worker model automatically
only when the runtime or account policy verifies that it is cheaper and capable.
Treat higher or unknown relative cost as approval-required. Project `CLAUDE.md`
instructions may narrow roles and permissions but cannot waive the cost gate.

## Generic runtimes

Keep the current configured model and use role prompts if model price or override
support cannot be established. Disable delegation if contracts, permissions, or
concurrency cannot be bounded safely.

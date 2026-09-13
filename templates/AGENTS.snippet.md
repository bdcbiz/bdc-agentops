## Agent governance

Before model selection or delegation, load the `agent-governor` skill and apply
its economy-first policy. The current project's product and security rules remain
authoritative.

Do not use a protected, higher-cost, or unknown-cost model without first naming
the exact model and task, explaining the expected benefit and cheaper fallback,
and receiving explicit task-specific approval from the user.

Default to single-agent execution. When delegation is justified, use at most two
concurrent workers, one delegation level, two attempts, and one writer per file.
Workers cannot broaden scope or perform root-only external actions.

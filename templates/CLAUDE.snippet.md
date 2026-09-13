## Agent governance and model cost

Load the `bdc-agentops` skill before selecting a model, delegating, or creating
subagents. Existing project rules determine the work; this layer controls agent
resources and cannot weaken security or approval boundaries.

Do not switch to a higher-cost or unknown-cost model without first presenting the
exact model, task, reason, expected benefit, cheaper fallback, and bounded number
of attempts, then receiving explicit approval. Silence is not approval and an
approval expires when the named task completes.

Prefer the current configured manager and verified cheaper workers. Default to
single-agent work; cap justified delegation at two concurrent workers, one level,
two attempts, and one writer per file.

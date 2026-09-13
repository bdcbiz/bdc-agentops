## Agent governance and model cost

Load the `bdc-agentops` skill before selecting a model, delegating, or creating
subagents. Existing project rules determine the work; this layer controls agent
resources and cannot weaken security or approval boundaries.

Before substantive project inspection or tools, present Solo and Delegated economy,
including every proposed worker/model/task, relative extra usage, and a recommendation;
wait for an explicit choice. Until then, limit tools to instruction discovery,
repository location, worktree status, and shallow inventory. Do not inspect feature
implementation, run tests, edit files, or take external actions. Skip only if the
user already selected a mode for this task or no project tools are needed.

Do not switch to a higher-cost or unknown-cost model without first presenting the
exact model, task, reason, expected benefit, cheaper fallback, and bounded number
of attempts, then receiving explicit approval. Silence is not approval and an
approval expires when the named task completes.

Delegation consent and protected-model approval are separate decisions.

Prefer the current configured manager and verified cheaper workers. Default to
single-agent work; cap justified delegation at two concurrent workers, one level,
two attempts, and one writer per file.

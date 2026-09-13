# Governance policy

## Precedence and scope

The user's current request and applicable project instructions determine the work
scope. Agent Governor cannot weaken product, security, privacy, approval, or
repository rules. Delegation changes who performs approved work, not what work is
authorized.

## Cost approval gate

Default to `economy`. Block a proposed model before execution when any of these is
true:

- it is listed as protected;
- it uses a higher-cost service tier;
- its relative cost is unknown;
- the proposal exceeds concurrency, depth, or attempt limits and will add cost.

An approval request must name the exact model and task, explain why approved
models are insufficient, describe the expected benefit, offer a cheaper fallback,
and bound the number of calls or attempts. Approval is task-specific and expires
when that task ends. The manager cannot infer approval from silence or approve its
own escalation.

If approval is declined or unavailable, continue with the cheaper safe fallback
when it can satisfy the task. Otherwise report the limitation without starting
the protected model.

## Delegation decision

Stay single-agent for small tasks, sequential tasks, shared mutable state, or work
whose coordination cost is likely to exceed its benefit.

Delegate only when there are independent bounded deliverables, a distinct
specialty materially reduces risk, or an independent review is justified by the
impact. Explain the assignments briefly before starting them.

Workers receive structured contracts. A worker owns only its assigned outcome and
files, cannot spawn workers, and stops on scope expansion or ownership conflict.
Reviewers are read-only. The manager integrates results and runs objective checks.

## Permissions

Workers default to read-only. Writing requires an explicit file list and exclusive
ownership. Commits, pushes, merges, releases, deployments, material deletion,
secret access, and external communication stay with the root workflow and retain
their normal approval requirements.

Pass the minimum context required. Do not put secrets or unnecessary customer,
patient, financial, signing, or infrastructure data in prompts or usage logs.

## Failure and termination

Stop when acceptance criteria pass. Stop a worker after two failed attempts, a
repeated identical failure, contract escape, or unsafe ambiguity. Do not create an
unbounded implement-review-repair loop. The manager either takes the cheaper safe
fallback, proposes a protected escalation, or reports a blocker.

Agent agreement is not proof. Tests, linters, type checks, inspected diffs, and
primary sources have priority over confidence statements and majority votes.

## Usage reporting

Record model, role, elapsed time, attempts, status, and token fields when exposed
by the runtime. Mark the source as `measured`, `estimated`, or `unavailable`.
Operational telemetry is not a final bill unless a billing system confirms it.

# AGENTS.md — BDC AgentOps repository

Read `SKILL.md` and `references/policy.md` before changing routing, approval,
delegation, permission, or usage behavior.

Repository invariants:

- Economy-first routing remains the default.
- Protected, higher-cost, and unknown-cost model selection requires explicit,
  task-specific user approval before execution.
- A manager may propose an escalation but may not approve its own proposal.
- Delegation never broadens the user's authority.
- Preserve deterministic validation in `scripts/validate.py` and update tests when
  intentionally changing a governed invariant.
- Do not add provider credentials, account identifiers, usage exports, or private
  project data.
- Run `python3 scripts/validate.py` and the unit tests before declaring changes
  complete.

#!/usr/bin/env python3
"""Validate Agent Governor's safety-critical configuration without dependencies."""

from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def load_json(relative_path: str) -> dict:
    with (ROOT / relative_path).open(encoding="utf-8") as handle:
        return json.load(handle)


def validate() -> list[str]:
    errors: list[str] = []
    required = [
        "SKILL.md",
        "references/policy.md",
        "references/routing.json",
        "references/task-contract.json",
        "schemas/usage-ledger.schema.json",
        "templates/AGENTS.snippet.md",
        "templates/CLAUDE.snippet.md",
    ]
    for path in required:
        if not (ROOT / path).is_file():
            errors.append(f"missing required file: {path}")

    if errors:
        return errors

    routing = load_json("references/routing.json")
    limits = routing.get("limits", {})
    cost = routing.get("cost_policy", {})
    codex = routing.get("runtimes", {}).get("codex", {})
    workers = codex.get("workers", {})

    expected = {
        "manager": "gpt-5.6-sol",
        "discovery": "gpt-5.6-luna",
        "implementation": "gpt-5.6-terra",
        "protected": "gpt-6-astra",
    }
    actual = {
        "manager": codex.get("manager", {}).get("model"),
        "discovery": workers.get("discovery", {}).get("model"),
        "implementation": workers.get("implementation", {}).get("model"),
        "protected": workers.get("critical_escalation", {}).get("model"),
    }
    for role, model in expected.items():
        if actual.get(role) != model:
            errors.append(f"unexpected Codex {role} model: {actual.get(role)!r}")

    if workers.get("critical_escalation", {}).get("approval_required") is not True:
        errors.append("critical escalation must require explicit approval")
    if codex.get("unlisted_model_action") != "require_user_approval":
        errors.append("unlisted Codex models must require explicit approval")
    if cost.get("unknown_cost_action") != "require_user_approval":
        errors.append("unknown-cost models must require explicit approval")
    if cost.get("higher_service_tier_action") != "require_user_approval":
        errors.append("higher-cost service tiers must require explicit approval")
    if routing.get("default_mode") != "economy":
        errors.append("default mode must remain economy")

    required_limits = {
        "max_concurrent_workers": 2,
        "max_delegation_depth": 1,
        "max_attempts_per_worker": 2,
        "one_writer_per_file": True,
    }
    for key, expected_value in required_limits.items():
        if limits.get(key) != expected_value:
            errors.append(f"unsafe limit {key}: {limits.get(key)!r}")

    contract = load_json("references/task-contract.json")
    forbidden = set(contract.get("forbidden_actions", []))
    for action in {"spawn_subagent", "change_model", "expand_scope", "push", "deploy"}:
        if action not in forbidden:
            errors.append(f"worker contract must forbid: {action}")

    schema = load_json("schemas/usage-ledger.schema.json")
    sources = (
        schema.get("$defs", {})
        .get("agentUsage", {})
        .get("properties", {})
        .get("source", {})
        .get("enum", [])
    )
    if set(sources) != {"measured", "estimated", "unavailable"}:
        errors.append("usage source must distinguish measured, estimated, unavailable")

    return errors


def main() -> int:
    errors = validate()
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Agent Governor policy validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

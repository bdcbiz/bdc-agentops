#!/usr/bin/env python3
"""Install BDC AgentOps globally for Codex or into a project."""

from __future__ import annotations

import argparse
import os
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BEGIN = "<!-- BDC-AGENTOPS:BEGIN -->"
END = "<!-- BDC-AGENTOPS:END -->"
SKILL_PATHS = (
    "SKILL.md",
    "agents/openai.yaml",
    "references/policy.md",
    "references/routing.json",
    "references/runtime-adapters.md",
    "references/task-contract.json",
    "schemas/usage-ledger.schema.json",
)


def marked_block(snippet_name: str) -> str:
    snippet = (ROOT / "templates" / snippet_name).read_text(encoding="utf-8").strip()
    return f"{BEGIN}\n{snippet}\n{END}"


def upsert_block(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8") if path.exists() else f"# {path.name}\n"
    if BEGIN in text or END in text:
        if text.count(BEGIN) != 1 or text.count(END) != 1:
            raise ValueError(f"invalid BDC AgentOps markers in {path}")
        start = text.index(BEGIN)
        finish = text.index(END, start) + len(END)
        updated = text[:start] + block + text[finish:]
    else:
        section = text.find("\n## ")
        if section == -1:
            updated = text.rstrip() + "\n\n" + block + "\n"
        else:
            updated = text[:section].rstrip() + "\n\n" + block + "\n" + text[section:]

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(updated, encoding="utf-8")


def install_skill(destination: Path) -> None:
    for relative in SKILL_PATHS:
        source = ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def install_project(project: Path, runtime: str) -> None:
    project = project.expanduser().resolve()
    if not project.is_dir():
        raise ValueError(f"project directory does not exist: {project}")
    if runtime in {"codex", "both"}:
        install_skill(project / ".agents/skills/bdc-agentops")
        upsert_block(project / "AGENTS.md", marked_block("AGENTS.snippet.md"))
    if runtime in {"claude", "both"}:
        install_skill(project / ".claude/skills/bdc-agentops")
        upsert_block(project / "CLAUDE.md", marked_block("CLAUDE.snippet.md"))


def install_global_codex() -> None:
    codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()
    install_skill(codex_home / "skills/bdc-agentops")
    upsert_block(codex_home / "AGENTS.md", marked_block("AGENTS.snippet.md"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--global-codex", action="store_true")
    parser.add_argument("--project", type=Path)
    parser.add_argument(
        "--runtime", choices=("codex", "claude", "both"), default="both"
    )
    args = parser.parse_args()
    if not args.global_codex and args.project is None:
        parser.error("choose --global-codex and/or --project PATH")
    return args


def main() -> int:
    args = parse_args()
    if args.global_codex:
        install_global_codex()
        print("Installed BDC AgentOps global Codex guidance.")
    if args.project is not None:
        install_project(args.project, args.runtime)
        print(f"Installed BDC AgentOps into {args.project.resolve()} ({args.runtime}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

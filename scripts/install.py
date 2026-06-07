#!/usr/bin/env python3
"""Guided installer for adding AI Pit Crew to a project.

The installer intentionally uses only the Python standard library so it can be
run from a freshly cloned template without bootstrapping dependencies first.
"""

from __future__ import annotations

import argparse
import shutil
import sys
from dataclasses import dataclass
from pathlib import Path


ALL_TOOLS = ("claude", "copilot", "gemini")

CORE_FILES = (
    "AGENTS.md",
    ".agent-workflow.md",
)

DOC_FILES = (
    "docs/product.md",
    "docs/architecture.md",
    "docs/roadmap.md",
    "docs/adr/000-template.md",
)

TOOL_FILES = {
    "claude": (
        "CLAUDE.md",
        ".claude/agents/developer.md",
        ".claude/agents/planner.md",
        ".claude/agents/reviewer.md",
        ".claude/agents/tester.md",
    ),
    "copilot": (".github/copilot-instructions.md",),
    "gemini": ("GEMINI.md",),
}

NEW_PROJECT_DIRS = (
    "src",
    "tests",
    "scripts",
)

README_MARKER_START = "<!-- ai-pit-crew:start -->"
README_MARKER_END = "<!-- ai-pit-crew:end -->"


@dataclass(frozen=True)
class RepoScan:
    path: Path
    exists: bool
    is_empty: bool
    is_git_repo: bool
    has_readme: bool
    installed_files: tuple[str, ...]
    languages: tuple[str, ...]


@dataclass(frozen=True)
class InstallOptions:
    mode: str
    tools: tuple[str, ...]
    force: bool
    update_readme: bool
    project_name: str | None = None


@dataclass(frozen=True)
class InstallAction:
    kind: str
    path: Path
    description: str
    source: Path | None = None
    content: str | None = None
    overwrite: bool = False


@dataclass(frozen=True)
class InstallPlan:
    mode: str
    recommendation: str
    scan: RepoScan
    actions: tuple[InstallAction, ...]
    skipped: tuple[str, ...]
    warnings: tuple[str, ...]


def template_root() -> Path:
    return Path(__file__).resolve().parents[1]


def scan_repository(path: Path) -> RepoScan:
    exists = path.exists()
    entries = list(path.iterdir()) if exists and path.is_dir() else []
    is_empty = not exists or not entries
    installed_files = []

    for rel_path in (
        "AGENTS.md",
        "TASKS.md",
        ".agent-workflow.md",
        "CLAUDE.md",
        "GEMINI.md",
        ".github/copilot-instructions.md",
        "docs/product.md",
        "docs/architecture.md",
        "docs/roadmap.md",
    ):
        if (path / rel_path).exists():
            installed_files.append(rel_path)

    languages = []
    language_markers = {
        "Python": ("pyproject.toml", "requirements.txt", "setup.py"),
        "Node/TypeScript": ("package.json", "tsconfig.json"),
        "Rust": ("Cargo.toml",),
        "Go": ("go.mod",),
        "Ruby": ("Gemfile",),
        "Java": ("pom.xml", "build.gradle", "build.gradle.kts"),
    }
    for language, markers in language_markers.items():
        if any((path / marker).exists() for marker in markers):
            languages.append(language)

    return RepoScan(
        path=path,
        exists=exists,
        is_empty=is_empty,
        is_git_repo=(path / ".git").exists(),
        has_readme=(path / "README.md").exists(),
        installed_files=tuple(installed_files),
        languages=tuple(languages),
    )


def suggest_mode(scan: RepoScan, requested_mode: str) -> str:
    if requested_mode != "auto":
        return requested_mode
    if not scan.exists or scan.is_empty:
        return "new"
    return "append"


def parse_tools(raw_tools: str) -> tuple[str, ...]:
    normalized = raw_tools.strip().lower()
    if normalized == "all":
        return ALL_TOOLS
    if normalized == "none":
        return ()

    tools = tuple(tool.strip() for tool in normalized.split(",") if tool.strip())
    unknown = sorted(set(tools) - set(ALL_TOOLS))
    if unknown:
        names = ", ".join(unknown)
        valid = ", ".join(("all", "none", *ALL_TOOLS))
        raise argparse.ArgumentTypeError(f"unknown tool(s): {names}; valid values: {valid}")
    return tools


def clean_tasks_template() -> str:
    return """# Tasks

Active work board for this project.

Update this file when you start a task, finish a task, or discover a blocker.
See [`.agent-workflow.md`](.agent-workflow.md) for the full workflow and format guide.

Always re-read this file immediately before editing it so you do not work from stale task state.

---

## In Progress

_No tasks in progress._

## Ready For Review

_No work ready for review._

## Blocked

_No blocked tasks._

## Done

_No completed tasks yet._
"""


def new_project_readme(project_name: str) -> str:
    return f"""# {project_name}

This project uses [AI Pit Crew](https://github.com/bobbylough/ai-pit-crew) as a
human-led, multi-agent development workflow.

## AI-assisted development

- Start with [AGENTS.md](AGENTS.md).
- Keep planned work in [docs/roadmap.md](docs/roadmap.md).
- Track only active work in [TASKS.md](TASKS.md).
- Use [.agent-workflow.md](.agent-workflow.md) for the development loop.

Fill in [docs/product.md](docs/product.md) and
[docs/architecture.md](docs/architecture.md) before assigning implementation work.
"""


def readme_section() -> str:
    return f"""
{README_MARKER_START}
## AI-assisted development

This repository uses [AI Pit Crew](https://github.com/bobbylough/ai-pit-crew) as
a human-led, multi-agent development workflow.

- Agents should start with [AGENTS.md](AGENTS.md).
- Planned work belongs in [docs/roadmap.md](docs/roadmap.md), not `TASKS.md`.
- `TASKS.md` tracks only active work: in progress, ready for review, blocked, or done.
- [.agent-workflow.md](.agent-workflow.md) describes the shared development loop.
{README_MARKER_END}
"""


def target_exists(target: Path, force: bool) -> bool:
    return target.exists() and not force


def add_file_action(
    actions: list[InstallAction],
    skipped: list[str],
    *,
    source: Path | None = None,
    content: str | None = None,
    target: Path,
    description: str,
    force: bool,
) -> None:
    if target_exists(target, force):
        skipped.append(f"{target}: already exists")
        return
    actions.append(
        InstallAction(
            kind="write",
            path=target,
            source=source,
            content=content,
            description=description,
            overwrite=target.exists(),
        )
    )


def build_plan(template: Path, target: Path, options: InstallOptions) -> InstallPlan:
    scan = scan_repository(target)
    mode = suggest_mode(scan, options.mode)
    warnings: list[str] = []
    skipped: list[str] = []
    actions: list[InstallAction] = []

    if target.exists() and not target.is_dir():
        raise ValueError(f"target is not a directory: {target}")

    if mode == "new" and scan.exists and not scan.is_empty and not options.force:
        warnings.append(
            "target is not empty; installer will skip existing files unless --force is used"
        )

    if not target.exists():
        actions.append(
            InstallAction(
                kind="mkdir",
                path=target,
                description=f"Create target directory {target}",
            )
        )

    for rel_path in CORE_FILES:
        add_file_action(
            actions,
            skipped,
            source=template / rel_path,
            target=target / rel_path,
            description=f"Install {rel_path}",
            force=options.force,
        )

    add_file_action(
        actions,
        skipped,
        content=clean_tasks_template(),
        target=target / "TASKS.md",
        description="Install clean TASKS.md active work board",
        force=options.force,
    )

    for rel_path in DOC_FILES:
        add_file_action(
            actions,
            skipped,
            source=template / rel_path,
            target=target / rel_path,
            description=f"Install {rel_path}",
            force=options.force,
        )

    for tool in options.tools:
        for rel_path in TOOL_FILES[tool]:
            add_file_action(
                actions,
                skipped,
                source=template / rel_path,
                target=target / rel_path,
                description=f"Install {tool} support: {rel_path}",
                force=options.force,
            )

    if mode == "new":
        for rel_path in NEW_PROJECT_DIRS:
            gitkeep = target / rel_path / ".gitkeep"
            add_file_action(
                actions,
                skipped,
                content="",
                target=gitkeep,
                description=f"Create {rel_path}/ placeholder",
                force=options.force,
            )

        project_name = options.project_name or target.name or "my-project"
        add_file_action(
            actions,
            skipped,
            content=new_project_readme(project_name),
            target=target / "README.md",
            description="Create starter README.md",
            force=options.force,
        )
    elif options.update_readme:
        readme_path = target / "README.md"
        if not readme_path.exists():
            add_file_action(
                actions,
                skipped,
                content=new_project_readme(options.project_name or target.name),
                target=readme_path,
                description="Create README.md with AI Pit Crew section",
                force=options.force,
            )
        else:
            readme_text = readme_path.read_text(encoding="utf-8")
            if README_MARKER_START in readme_text:
                skipped.append(f"{readme_path}: AI Pit Crew README section already present")
            else:
                actions.append(
                    InstallAction(
                        kind="append",
                        path=readme_path,
                        content=readme_section(),
                        description="Append AI Pit Crew section to README.md",
                    )
                )

    recommendation = build_recommendation(scan, mode, options)
    return InstallPlan(
        mode=mode,
        recommendation=recommendation,
        scan=scan,
        actions=tuple(actions),
        skipped=tuple(skipped),
        warnings=tuple(warnings),
    )


def build_recommendation(scan: RepoScan, mode: str, options: InstallOptions) -> str:
    if mode == "new":
        return "Create a new AI Pit Crew-ready project scaffold."

    details = []
    if scan.is_git_repo:
        details.append("existing Git repository")
    if scan.has_readme:
        details.append("README.md present")
    if scan.languages:
        details.append("detected " + ", ".join(scan.languages))
    if scan.installed_files:
        details.append(f"{len(scan.installed_files)} workflow file(s) already present")
    if options.update_readme:
        details.append("README update enabled")

    suffix = f" ({'; '.join(details)})" if details else ""
    return f"Append AI Pit Crew non-destructively to this repository{suffix}."


def apply_plan(plan: InstallPlan) -> None:
    for action in plan.actions:
        if action.kind == "mkdir":
            action.path.mkdir(parents=True, exist_ok=True)
            continue
        if action.kind == "append":
            with action.path.open("a", encoding="utf-8") as handle:
                handle.write(action.content or "")
            continue
        if action.kind != "write":
            raise ValueError(f"unknown action kind: {action.kind}")

        action.path.parent.mkdir(parents=True, exist_ok=True)
        if action.source is not None:
            shutil.copy2(action.source, action.path)
        else:
            action.path.write_text(action.content or "", encoding="utf-8")


def format_plan(plan: InstallPlan) -> str:
    lines = [
        f"Target: {plan.scan.path}",
        f"Mode: {plan.mode}",
        f"Recommendation: {plan.recommendation}",
        "",
        "Scan:",
        f"- Exists: {'yes' if plan.scan.exists else 'no'}",
        f"- Empty: {'yes' if plan.scan.is_empty else 'no'}",
        f"- Git repo: {'yes' if plan.scan.is_git_repo else 'no'}",
        f"- README: {'yes' if plan.scan.has_readme else 'no'}",
        f"- Languages: {', '.join(plan.scan.languages) if plan.scan.languages else 'none detected'}",
        "",
        "Actions:",
    ]

    if plan.actions:
        for action in plan.actions:
            marker = "overwrite" if action.overwrite else action.kind
            lines.append(f"- [{marker}] {action.description}: {action.path}")
    else:
        lines.append("- No changes needed.")

    if plan.skipped:
        lines.extend(("", "Skipped:"))
        lines.extend(f"- {item}" for item in plan.skipped)

    if plan.warnings:
        lines.extend(("", "Warnings:"))
        lines.extend(f"- {item}" for item in plan.warnings)

    return "\n".join(lines)


def confirm(prompt: str, default: bool = False) -> bool:
    suffix = "Y/n" if default else "y/N"
    answer = input(f"{prompt} [{suffix}] ").strip().lower()
    if not answer:
        return default
    return answer in {"y", "yes"}


def interactive_options(args: argparse.Namespace, scan: RepoScan) -> InstallOptions:
    mode = suggest_mode(scan, args.mode)
    if args.mode == "auto":
        print(f"Suggested mode: {mode}")
        if not confirm("Use this mode?", default=True):
            mode = "append" if mode == "new" else "new"

    tools = args.tools
    print(f"Selected tools: {', '.join(tools) if tools else 'none'}")
    if confirm("Change selected tools?", default=False):
        raw_tools = input("Tools (all, none, or comma-separated claude,copilot,gemini): ")
        tools = parse_tools(raw_tools or "all")

    update_readme = args.update_readme
    if mode == "append" and not args.no_prompt_readme:
        update_readme = confirm("Append an AI Pit Crew section to README.md?", default=True)

    project_name = args.project_name
    if mode == "new" and not project_name:
        raw_name = input(f"Project name [{scan.path.name or 'my-project'}]: ").strip()
        project_name = raw_name or scan.path.name or "my-project"

    return InstallOptions(
        mode=mode,
        tools=tools,
        force=args.force,
        update_readme=update_readme,
        project_name=project_name,
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Install AI Pit Crew into a new or existing project.",
    )
    parser.add_argument(
        "target",
        nargs="?",
        default=".",
        help="Project directory to create or update. Defaults to the current directory.",
    )
    parser.add_argument(
        "--mode",
        choices=("auto", "new", "append"),
        default="auto",
        help="Installation mode. auto scans the target and recommends new or append.",
    )
    parser.add_argument(
        "--tools",
        type=parse_tools,
        default=ALL_TOOLS,
        help="Tool config to install: all, none, or comma-separated claude,copilot,gemini.",
    )
    parser.add_argument(
        "--project-name",
        help="Project name for a generated README.md when creating a new project.",
    )
    parser.add_argument(
        "--update-readme",
        action="store_true",
        help="Append or create a README.md AI Pit Crew section when appending to a repo.",
    )
    parser.add_argument(
        "--no-prompt-readme",
        action="store_true",
        help="Do not ask about README updates in interactive append mode.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing files that would otherwise be skipped.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the recommended plan without writing files.",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="Apply the recommended plan without prompting.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    target = Path(args.target).expanduser().resolve()
    scan = scan_repository(target)
    interactive = sys.stdin.isatty() and not args.yes and not args.dry_run

    if interactive:
        options = interactive_options(args, scan)
    else:
        options = InstallOptions(
            mode=suggest_mode(scan, args.mode),
            tools=args.tools,
            force=args.force,
            update_readme=args.update_readme,
            project_name=args.project_name,
        )

    plan = build_plan(template_root(), target, options)
    print(format_plan(plan))

    if args.dry_run:
        print("\nDry run only; no files changed.")
        return 0

    if not args.yes:
        if not interactive:
            print("\nRun again with --yes to apply this plan.")
            return 0
        if not confirm("Apply this plan?", default=False):
            print("No files changed.")
            return 0

    apply_plan(plan)
    print("\nAI Pit Crew installation complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

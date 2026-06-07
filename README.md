# AI Pit Crew

A lightweight workflow for building software with **multiple AI coding assistants running simultaneously in the same IDE** while keeping the human engineer close to every decision.

*Slow is smooth. Smooth is fast.*

---

## The Problem This Solves

Most AI development workflows push the engineer out of the loop. Hand over the project, cross your fingers, and hope the output is usable. That approach produces code nobody understands, architecture nobody owns, and decisions nobody remembers making.

There is also a practical problem: fully autonomous AI orchestration is expensive. Token costs add up fast when one model is instructing another, and you are locked in to a single provider until your usage limits hit.

This workflow takes the opposite approach. Modern IDEs let you run Claude Code, GitHub Copilot, Gemini Code Assist, OpenAI Codex, and other tools at the same time. AI Pit Crew gives that combination a structure that keeps the human engineer in the driver's seat:

- The human sets direction, approves decisions, and reviews every change
- Agents do the implementation, testing, and cross-review work
- All tools share the same documentation so nothing falls out of sync
- No expensive orchestration layer; you direct the agents yourself
- When you hit a usage limit on one tool, switch to another and keep moving

This works because the **repository is the shared workspace**. Every agent reads the same product, architecture, roadmap, and active task docs before starting work.

---

## How It Works

```text
Human sets direction -> Agents implement -> Different agent reviews -> Human approves
```

- The **human** owns product vision, architecture, prioritization, and final approval
- **Agents** implement tasks, write tests, and review each other's code
- All agents read from the same documentation before starting any work
- `docs/roadmap.md` tracks planned work and sequencing
- `TASKS.md` is the shared active work board

`TASKS.md` is shared mutable state. Agents must re-read it immediately before relying on task status or editing the file.

---

## Supported Tools

This workflow has explicit configuration for:

| Tool | Config File |
| --- | --- |
| Claude Code | [`CLAUDE.md`](CLAUDE.md) |
| GitHub Copilot | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) |
| Gemini Code Assist | [`GEMINI.md`](GEMINI.md) |
| OpenAI Codex / ChatGPT | Paste [`AGENTS.md`](AGENTS.md) as a system prompt |

Any tool that accepts a system prompt or instruction file can participate. Point it at [`AGENTS.md`](AGENTS.md); that is the shared agent contract.

---

## Getting Started For Agents

If you are an AI agent assigned to work on this project, follow these steps:

### Before Starting Work

1. Read [`AGENTS.md`](AGENTS.md); this is your contract for how to participate
2. Read [`docs/product.md`](docs/product.md); understand what you are building
3. Read [`docs/architecture.md`](docs/architecture.md); understand system design
4. Read [`docs/roadmap.md`](docs/roadmap.md); understand planned work and sequencing
5. Read [`TASKS.md`](TASKS.md) fresh; see what is in progress, ready for review, and blocked

### Activating Tool-Specific Instructions

**Claude Code:**

- `CLAUDE.md` is loaded automatically
- Sub-agent personas in `.claude/agents/` are also loaded automatically from the repo
- Invoke a persona by telling Claude which role to take, such as "take the Developer role"

**GitHub Copilot:**

- Pin [`.github/copilot-instructions.md`](.github/copilot-instructions.md) to your chat
- Or paste the contents as a system message

**Gemini Code Assist:**

- `GEMINI.md` is located at the repo root
- Use it as the Gemini-specific instruction file

**OpenAI Codex / ChatGPT:**

- Copy the contents of [`AGENTS.md`](AGENTS.md) into the system prompt or custom instructions
- Paste it at the start of each new conversation when persistent instructions are unavailable

### Your Workflow

1. **Take an assigned task** from the human, `docs/roadmap.md`, an issue, or a PR
2. **Re-read `TASKS.md` immediately before editing it**, then move the task to `In Progress` with your agent name
3. **Implement** by following [`.agent-workflow.md`](.agent-workflow.md)
4. **Run relevant tests**
5. **Re-read `TASKS.md` immediately before editing it**, then move the task to `Ready For Review` with implementation notes

### When You Need Help

- **Unclear requirements?** Flag the task as blocked in `TASKS.md` with specific questions
- **Architecture question?** Review [`docs/architecture.md`](docs/architecture.md) and its open questions section
- **Not sure how to review code?** See the review guidelines in [`AGENTS.md`](AGENTS.md)

---

## Repository Structure

```text
/
|-- README.md                        # This file
|-- AGENTS.md                        # Shared instructions for all agents
|-- CLAUDE.md                        # Claude Code configuration
|-- GEMINI.md                        # Gemini Code Assist configuration
|-- TASKS.md                         # Active work board
|-- .agent-workflow.md               # Workflow quick reference
|
|-- docs/
|   |-- product.md                   # What are we building?
|   |-- roadmap.md                   # What should we build next?
|   |-- architecture.md              # How does the system work?
|   `-- adr/                         # Why was each decision made?
|       |-- 000-template.md
|       `-- 001-development-workflow.md
|
|-- .github/
|   `-- copilot-instructions.md      # GitHub Copilot configuration
|
|-- .claude/
|   `-- agents/                      # Claude sub-agent personas
|       |-- developer.md
|       |-- planner.md
|       |-- reviewer.md
|       `-- tester.md
|
|-- src/                             # Application source code
|-- tests/                           # Test suite
`-- scripts/
    `-- install.py                    # Guided setup wizard
```

---

## Using This Template

### Guided Installer

The easiest way to add AI Pit Crew is the guided installer. It scans the target
directory, recommends either a new-project scaffold or an append-to-existing-repo
install, prints the exact plan, and only writes files after confirmation.

The two simplest commands cover the common paths:

```bash
# New project
python3 scripts/install.py ../my-project --mode new

# Existing project
python3 scripts/install.py /path/to/existing-repo --mode append --update-readme
```

Preview without writing files:

```bash
python3 scripts/install.py /path/to/project --dry-run
```

Run non-interactively:

```bash
python3 scripts/install.py /path/to/project --mode auto --tools all --update-readme --yes
```

The installer is intentionally conservative:

- `--mode auto` recommends `new` for missing or empty targets and `append` for
  existing repositories.
- Existing files are skipped by default; use `--force` only when you want to
  overwrite them.
- `TASKS.md` is installed as a clean active-work board, without template
  history.
- `--tools` accepts `all`, `none`, or a comma-separated list of
  `claude,copilot,gemini,codex`.
- In append mode, `--update-readme` adds a small AI Pit Crew section to an
  existing README or creates one if missing.

Get interactive help:

```bash
python3 scripts/install.py --help
```

Available options:

| Option | Values | Purpose |
| --- | --- | --- |
| `target` | path | Project directory to create or update. Defaults to the current directory. |
| `--mode` | `auto`, `new`, `append` | Choose install mode. `auto` scans the target and recommends the path. |
| `--tools` | `all`, `none`, `claude,copilot,gemini,codex` | Choose which tool-specific instruction files to install. Codex uses `AGENTS.md`, so it does not add an extra file. |
| `--project-name` | text | Name used in the generated README for new projects. |
| `--update-readme` | flag | Append or create an AI Pit Crew README section in append mode. |
| `--no-prompt-readme` | flag | Skip the interactive README update question in append mode. |
| `--force` | flag | Overwrite existing files instead of skipping them. |
| `--dry-run` | flag | Print the plan without writing files. |
| `--yes`, `-y` | flag | Apply the plan without prompting. |
| `--color` | `auto`, `always`, `never` | Control colored output. Defaults to `auto`. |
| `--no-color` | flag | Disable colored output. The installer also honors `NO_COLOR`. |
| `--help`, `-h` | flag | Show usage, examples, and options. |

### Starting A New Project

1. **Copy this repository** as your starting point.
   - On GitHub: click **Use this template** to create a new repo from it.
   - Without GitHub: `git clone https://github.com/bobbylough/ai-pit-crew my-project && cd my-project && rm -rf .git && git init`

2. **Clear template-specific work state.**
   - Clear the `## In Progress`, `## Ready For Review`, `## Blocked`, and `## Done` sections in `TASKS.md`
   - Delete `docs/adr/001-development-workflow.md` or keep it only as a reference

3. **Remove tools you are not using.**
   - Not using Gemini? Delete `GEMINI.md`
   - Not using Copilot? Delete `.github/copilot-instructions.md`
   - Not using Claude Code? Delete `CLAUDE.md` and `.claude/`

4. **Fill in the three core docs** before assigning any tasks:
   - [`docs/product.md`](docs/product.md): what you are building, for whom, and what done looks like
   - [`docs/architecture.md`](docs/architecture.md): technology choices and system design
   - [`docs/roadmap.md`](docs/roadmap.md): current milestone, upcoming work, dependencies, risks, and sequencing

5. **Use `docs/roadmap.md` for planned work** and `TASKS.md` for active state only.

### Adding This Workflow To An Existing Project

1. **Copy the workflow files** into your repo root:
   - `AGENTS.md`
   - `TASKS.md`
   - `.agent-workflow.md`
   - `CLAUDE.md` and `.claude/` if using Claude Code
   - `GEMINI.md` if using Gemini
   - `.github/copilot-instructions.md` if using Copilot

2. **Copy the `docs/` folder** if you do not already have product, architecture, and roadmap documentation. If you do, point agents to wherever those docs live by updating file references in `AGENTS.md`.

3. **Fill in `docs/product.md` and `docs/architecture.md`** to reflect your existing system.

4. **Update `docs/roadmap.md`** with planned work, priorities, sequencing, and risks.

5. **Add only current active work to `TASKS.md`** so agents have an accurate picture of what is active, ready for review, blocked, or done.

---

## Standard Development Loop

```text
Define -> Plan -> Assign -> Implement -> Review -> Merge -> Document
```

See [`.agent-workflow.md`](.agent-workflow.md) for the detailed loop with format examples.

---

## Cross-Agent Review Pairings

The goal is to have a _different_ tool review code than the one that wrote it.

| Author | Reviewer |
| --- | --- |
| Claude | Copilot or Gemini |
| Copilot | Claude or Gemini |
| Gemini | Claude or Codex |
| Codex | Claude or Copilot |

Rotate when possible. You are not looking for perfection; you are looking for blind spots.

---

## Core Principles

**Human-led.** Product vision, prioritization, architecture decisions, and final approval belong to the human. Agents may recommend alternatives but do not reprioritize work unilaterally.

**Shared source of truth.** All agents work from the same repository documentation. The repo is the single context, not each tool's conversation history.

**Roadmap for planned work, task board for active work.** `docs/roadmap.md` tracks what should be built next. `TASKS.md` tracks what is currently in progress, ready for review, blocked, or done.

**Fresh task state.** Agents always re-read `TASKS.md` immediately before relying on or editing task status.

**Small, reviewable changes.** Agents prefer focused tasks, avoid unrelated refactoring, and leave implementation notes so the next agent and the human can follow what was done.

**Cross-agent review.** Code written by one tool is reviewed by a different one. Reducing blind spots is the goal, not eliminating human judgment.

---

## Definition Of Done

A task is complete when:

- Requirements are implemented
- Code compiles without errors
- Relevant tests pass
- `TASKS.md` is updated
- Documentation reflects any changes
- A different agent has reviewed the code
- Human has approved

---

## Philosophy

Most AI development workflows are built around a single idea: hand the project to an AI and get software back. Don't look too closely at what it built or why. Just ship it and iterate.

That approach produces results that are fast to generate and slow to trust. Nobody on the team fully understands the system. Architecture decisions are buried in chat history. When something breaks in production, nobody knows where to start.

AI Pit Crew is built on the opposite assumption: **the human engineer should stay close to every meaningful decision.**

You are the orchestrator. The AI tools are your pit crew: fast, capable, specialized, but you call the stops. You decide what gets built, in what order, and why. You review every change before it merges. You own the architecture.

*Slow is smooth. Smooth is fast.*

Moving deliberately by writing clear requirements, reviewing each change, and documenting decisions as you go produces better software faster than sprinting blind. You spend less time debugging code you do not understand and more time building things that work.

This workflow also has a practical advantage: it does not require expensive autonomous orchestration. No model is paying another model to think. You direct the agents yourself, which costs nothing extra and keeps you in the loop by design. Because all agents work from the same shared documentation, you can switch tools whenever you need to.

# AI Pit Crew

A lightweight workflow for building software with **multiple AI coding assistants running simultaneously in the same IDE** — while keeping the human engineer close to every decision.

*Slow is smooth. Smooth is fast.*

---

## The Problem This Solves

Most AI development workflows push the engineer out of the loop. Hand over the project, cross your fingers, and hope the output is usable. That approach produces code nobody understands, architecture nobody owns, and decisions nobody remembers making.

There is also a practical problem: fully autonomous AI orchestration is expensive. Token costs add up fast when one model is instructing another, and you are locked in to a single provider until your usage limits hit — at which point everything stops.

This workflow takes the opposite approach. Modern IDEs let you run Claude Code, GitHub Copilot, Gemini Code Assist, and other tools at the same time. AI Pit Crew gives that combination a structure that keeps the human engineer in the driver's seat:

- The human sets direction, approves decisions, and reviews every change
- Agents do the implementation, testing, and cross-review work
- All tools share the same documentation so nothing falls out of sync
- No expensive orchestration layer — you direct the agents yourself
- When you hit a usage limit on one tool, switch to another and keep moving

This works because the **repository is the shared workspace**. Every agent reads the same product, architecture, and task docs before starting work.

---

## How It Works

```
Human sets direction → Agents implement → Different agent reviews → Human approves
```

- The **human** owns product vision, architecture, prioritization, and final approval
- **Agents** implement tasks, write tests, and review each other's code
- All agents read from the same documentation before starting any work
- `TASKS.md` is the shared work board — every agent reads and updates it

This works with any combination of AI tools. You do not need to use all of them.

---

## Supported Tools

This workflow has explicit configuration for:

| Tool                   | Config File                                                          |
| ---------------------- | -------------------------------------------------------------------- |
| Claude Code            | [`CLAUDE.md`](CLAUDE.md)                                             |
| GitHub Copilot         | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) |
| Gemini Code Assist     | [`GEMINI.md`](GEMINI.md)                                             |
| OpenAI Codex / ChatGPT | Paste [`AGENTS.md`](AGENTS.md) as a system prompt                    |

Any tool that accepts a system prompt or instruction file can participate. Point it at [`AGENTS.md`](AGENTS.md) — that is the shared agent contract.

---

## Getting Started for Agents

If you are an AI agent assigned to work on this project, follow these steps:

### Before Starting Work

1.  Read [`AGENTS.md`](AGENTS.md) — this is your contract for how to participate
2.  Read [`docs/product.md`](docs/product.md) — understand what you are building
3.  Read [`docs/architecture.md`](docs/architecture.md) — understand system design
4.  Read [`TASKS.md`](TASKS.md) — see what is in progress and blocked

### Activating Tool-Specific Instructions

**Claude Code:**

- `CLAUDE.md` is loaded automatically — no setup needed
- Sub-agent personas in `.claude/agents/` are also loaded automatically from the repo
- Invoke a persona by telling Claude which role to take (e.g. "take the Developer role")

**GitHub Copilot:**

- Pin [`.github/copilot-instructions.md`](.github/copilot-instructions.md) to your chat
- Or paste the contents as a system message
- Reference [GitHub Copilot's chat documentation](https://docs.github.com/en/copilot/github-copilot-in-the-cli/using-github-copilot-in-the-cli)

**Other Tools (Gemini, ChatGPT, etc.):**

- Paste [`AGENTS.md`](AGENTS.md) as your system prompt or custom instruction
- Supplement with tool-specific guidance if available

### Your Workflow

1.  **Take a task** from the `Backlog` section in [`TASKS.md`](TASKS.md)
2.  **Update** `**TASKS.md**` — move it to `In Progress` with your agent name
3.  **Implement** — follow the process in [`.agent-workflow.md`](.agent-workflow.md)
4.  **Commit and push** when complete
5.  **Update** `**TASKS.md**` — move to `Ready For Review` with implementation notes

### When You Need Help

- **Unclear requirements?** Flag the task as blocked in `TASKS.md` with specific questions
- **Architecture question?** Review [`docs/architecture.md`](docs/architecture.md) and open questions section
- **Not sure how to review code?** See the review guidelines in [`AGENTS.md`](AGENTS.md)

---

## Repository Structure

```
/
├── README.md                        # This file
├── AGENTS.md                        # Shared instructions for all agents
├── CLAUDE.md                        # Claude Code configuration
├── TASKS.md                         # Active work board (all agents read and update this)
├── .agent-workflow.md               # Workflow quick reference
│
├── docs/
│   ├── product.md                   # What are we building?
│   ├── roadmap.md                   # What should we build next?
│   ├── architecture.md              # How does the system work?
│   └── adr/                         # Why was each decision made?
│       ├── 000-template.md
│       └── 001-development-workflow.md
│
├── .github/
│   └── copilot-instructions.md      # GitHub Copilot configuration
│
├── .claude/
│   └── agents/                      # Claude sub-agent personas
│       ├── developer.md
│       ├── planner.md
│       ├── reviewer.md
│       └── tester.md
│
├── src/                             # Application source code
├── tests/                           # Test suite
└── scripts/                         # Utility scripts
```

---

## Using This Template

### Starting a new project

1. **Copy this repository** as your starting point.
   - On GitHub: click **Use this template** to create a new repo from it.
   - Without GitHub: `git clone https://github.com/bobbylough/ai-pit-crew my-project && cd my-project && rm -rf .git && git init`

2. **Delete the example content** that is specific to this template and should not carry over:
   - Clear the `## Done` and `## Ready For Review` sections in `TASKS.md`
   - Delete `docs/adr/001-development-workflow.md` (or keep it as a reference — it does not apply to your project)

3. **Remove the tools you are not using.** You do not need all four:
   - Not using Gemini? Delete `GEMINI.md`
   - Not using Copilot? Delete `.github/copilot-instructions.md`
   - Not using Claude Code? Delete `CLAUDE.md` and `.claude/`

4. **Fill in the three core docs** before assigning any tasks:
   - [`docs/product.md`](docs/product.md) — what you are building, for whom, and what done looks like
   - [`docs/architecture.md`](docs/architecture.md) — technology choices and system design
   - [`docs/roadmap.md`](docs/roadmap.md) — current milestone and upcoming work

   Agents read these before starting any task. Gaps in the docs become assumptions in the code.

5. **Add your first tasks to `TASKS.md`** and start the development loop below.

---

### Adding this workflow to an existing project

If you already have a codebase and want to layer this workflow on top:

1. **Copy the workflow files** into your repo root:
   - `AGENTS.md`
   - `TASKS.md`
   - `.agent-workflow.md`
   - `CLAUDE.md` and `.claude/` (if using Claude Code)
   - `GEMINI.md` (if using Gemini)
   - `.github/copilot-instructions.md` (if using Copilot)

2. **Copy the `docs/` folder** if you do not already have product, architecture, and roadmap documentation. If you do, point agents to wherever those docs live by updating the file references in `AGENTS.md`.

3. **Fill in `docs/product.md` and `docs/architecture.md`** to reflect your existing system. Agents will read these to understand what they are working with.

4. **Update `AGENTS.md`** if your project has conventions that differ from the defaults — different test commands, branch naming, deploy process, etc.

5. **Add your current in-progress work to `TASKS.md`** so agents have an accurate picture of what is active and what is blocked.

---

## Quick Start

### Step 1 — Fill in the docs

Before assigning any tasks, fill in:

1. [`docs/product.md`](docs/product.md) — what you are building, for whom, and what done looks like
2. [`docs/architecture.md`](docs/architecture.md) — technology choices and system design
3. [`docs/roadmap.md`](docs/roadmap.md) — current milestone and upcoming work

Agents read these files before starting any task. Incomplete docs become assumptions in the code.

### Step 2 — Add tasks to TASKS.md

Break your first milestone into concrete, session-sized tasks. A good task is:

- Specific ("Implement password reset email flow", not "auth stuff")
- Completable in one session
- Scoped to one area of the codebase

### Step 3 — Assign tasks to agents

Tell an agent which task to take. The agent will:

1.  Read the product, architecture, and task docs
2.  Mark the task In Progress in `TASKS.md`
3.  Ask clarifying questions before implementing
4.  Leave implementation notes when complete

### Step 4 — Have a different agent review

Ask a _different_ AI tool to review the implementation. This is the highest-value step in the workflow — cross-agent review catches blind spots that same-tool review misses.

### Step 5 — You approve

No agent merges its own code. The human reviews the final result and approves.

### Step 6 — Document decisions

When a significant technical decision is made, create an ADR in `docs/adr/`. See [`docs/adr/000-template.md`](docs/adr/000-template.md) for the format.

---

## Standard Development Loop

```
Define → Plan → Task → Assign → Implement → Review → Merge → Document
    ↑                                                              |
    └──────────────────────────────────────────────────────────────┘
```

See [`.agent-workflow.md`](.agent-workflow.md) for the detailed loop with format examples.

---

## Setting Up Each Tool

### Claude Code

`CLAUDE.md` is loaded automatically. No setup needed — Claude reads it on every session.

The `.claude/agents/` directory contains sub-agent personas for Developer, Planner, Reviewer, and Tester roles. Invoke them by telling Claude which role to take (e.g. "act as the Developer agent").

### GitHub Copilot

`.github/copilot-instructions.md` is loaded automatically in VS Code and JetBrains with the Copilot extension.

### Gemini Code Assist

`GEMINI.md` is located at the repo root. Gemini Code Assist in VS Code picks this up automatically.

### OpenAI Codex / ChatGPT

Copy the contents of [`AGENTS.md`](AGENTS.md) into the system prompt or custom instructions. Paste it at the start of each new conversation.

### Any other tool

Paste [`AGENTS.md`](AGENTS.md) at the start of your session. The shared contract is plain text — it works anywhere.

---

## Cross-Agent Review Pairings

The goal is to have a _different_ tool review code than the one that wrote it.

| Author  | Reviewer          |
| ------- | ----------------- |
| Claude  | Copilot or Gemini |
| Copilot | Claude or Gemini  |
| Gemini  | Claude or Codex   |
| Codex   | Claude or Copilot |

Rotate when possible. You are not looking for perfection — you are looking for blind spots.

---

## Core Principles

**Human-led.** Product vision, prioritization, architecture decisions, and final approval belong to the human. Agents may recommend alternatives but do not reprioritize work unilaterally.

**Shared source of truth.** All agents work from the same repository documentation. The repo is the single context, not each tool's conversation history.

**Small, reviewable changes.** Agents prefer focused tasks, avoid unrelated refactoring, and leave implementation notes so the next agent (and the human) can follow what was done.

**Cross-agent review.** Code written by one tool is reviewed by a different one. Reducing blind spots is the goal — not eliminating human judgment.

---

## Definition of Done

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

You are the orchestrator. The AI tools are your pit crew — fast, capable, specialized — but you call the stops. You decide what gets built, in what order, and why. You review every change before it merges. You own the architecture.

*Slow is smooth. Smooth is fast.*

Moving deliberately — writing clear requirements, reviewing each change, documenting decisions as you go — produces better software faster than sprinting blind. You spend less time debugging code you don't understand and more time building things that work.

This workflow also has a practical advantage: it does not require expensive autonomous orchestration. No model is paying another model to think. You direct the agents yourself, which costs nothing extra and keeps you in the loop by design. And because all agents work from the same shared documentation, you can switch tools whenever you need to — if you hit a usage limit with Claude, pick up the same task in Copilot or Gemini without losing context.

# Agent Instructions

This file provides instructions for all AI coding agents working in this repository.

## Your Role

You are a contributor, not the decision-maker.

The human developer owns:

- Product vision and requirements
- Architecture decisions
- Task prioritization
- Final code approval

Your job is to implement tasks clearly, write reviewable code, and communicate honestly about uncertainty.

## Before You Start Any Task

1. Read [`docs/product.md`](docs/product.md) to understand what we are building
2. Read [`docs/architecture.md`](docs/architecture.md) to understand system design and technology choices
3. Read [`TASKS.md`](TASKS.md) to understand what is in progress and what is blocked
4. Read the specific task description carefully before writing any code

If anything is unclear, say so before implementing. Do not guess at requirements.

## Workflow

### Taking a Task

When assigned a task:

1. Move it to **In Progress** in `TASKS.md`, noting your agent name
2. Implement the task
3. Move it to **Ready For Review** when complete
4. Leave a brief implementation note describing what you did, any decisions made, and include the branch name or relevant commit hashes for review.

### Submitting Work

Work is ready for review when:

- Requirements are implemented
- Code compiles and relevant tests pass
- `TASKS.md` is updated
- Any new architectural decisions are noted (see ADR process below)

### Code Standards

- Prefer small, focused changes
- Do not refactor code unrelated to your task
- Do not add features beyond the task scope
- Write tests for new behavior
- Leave comments only when the _why_ is non-obvious

### When You Are Uncertain

If you encounter ambiguity:

- Identify the specific question
- Propose options with tradeoffs
- Ask the human to decide before proceeding

Do not make significant architectural decisions unilaterally.

## Review Guidelines

When reviewing another agent's code:

- Verify requirements are implemented
- Check for correctness, not just style
- Flag edge cases and error conditions
- Validate test coverage
- Note anything that diverges from `docs/architecture.md`

Be specific. Vague approval ("looks good") is not useful.

## ADR Process

When a significant technical decision is made during implementation, create an ADR:

1. Copy the template from `docs/adr/`
2. Name it sequentially: `docs/adr/NNN-short-description.md`
3. Record the decision, context, and rationale
4. Note the decision in your task update

Examples of decisions that warrant an ADR:

- Choosing a framework or library
- Changing the data model
- Selecting a third-party service
- Deviating from the architecture document

## What You Should NOT Do

- Reprioritize tasks without human approval
- Make breaking changes outside your task scope
- Merge your own code
- Close or resolve tasks assigned to other agents
- Modify `docs/product.md` or `docs/architecture.md` without explicit instruction

# Claude Code Configuration

This file configures Claude Code's behavior in this repository.

## Role

You are a contributor on this project, not the decision-maker. Read [`AGENTS.md`](AGENTS.md) for the full agent contract before starting any work.

## Engineering Principles

### Primary Goal

Produce maintainable, reliable, secure, production-ready software that is easy to understand, test, operate, and modify.

### Core Principles

- Prefer the simplest solution that fully satisfies the requirements
- Follow KISS and YAGNI - do not add functionality, abstractions, or dependencies not currently needed
- Favor proven, stable technologies over custom implementations or trendy alternatives
- Optimize for maintainability, readability, and operational simplicity over cleverness
- Write code for the next developer who must support it

### Implementation Standards

- Use clear, descriptive names for variables, functions, classes, files, and modules
- Keep functions and classes focused on a single responsibility
- Follow existing project patterns and conventions unless there is a compelling reason to improve them
- Minimize coupling and unnecessary complexity
- Remove dead code, unused variables, and obsolete comments

### Testing

- Add or update automated tests for all meaningful changes
- Prefer TDD when practical
- Test business behavior and expected outcomes, not implementation details
- Ensure all tests pass before considering work complete
- Write tests at each applicable level:
  - **Unit tests** — individual functions and components in isolation
  - **Integration tests** — interactions between modules, services, or layers
  - **End-to-end tests** — full user flows from entry point to expected outcome
- A feature is not complete without coverage at each level that applies to it

### Documentation and Observability

- Write self-explanatory code; add comments only for complex business logic, non-obvious decisions, assumptions, or workarounds
- Ensure critical workflows include sufficient logging so production issues can be diagnosed without a debugger
- Keep documentation synchronized with code changes

### Security

- Never hardcode secrets, credentials, or API keys
- Validate and sanitize all external input
- Follow secure defaults and use established security libraries
- Consider the OWASP Top 10 during design, implementation, and review

### Decision Framework

When multiple solutions are viable, prefer the option that:

1. Is easiest to understand
2. Has the fewest moving parts
3. Requires the fewest dependencies
4. Is easiest to test
5. Is easiest to operate and support
6. Is easiest to modify safely in the future

## Workflow Reminders

- Update `TASKS.md` when you start and finish work
- Re-read `TASKS.md` immediately before relying on or editing task status
- Keep changes focused on the assigned task
- Create an ADR for any significant technical decisions
- Flag uncertainty before implementing - do not guess at requirements

## Sub-Agent Personas

See [`.claude/agents/`](.claude/agents/) for specialized personas:

- `developer.md` - implementing assigned tasks
- `planner.md` - breaking requirements into tasks
- `reviewer.md` - code and architecture review
- `tester.md` - validation and acceptance testing

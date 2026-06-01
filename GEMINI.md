# Gemini Code Assist Instructions

You are a contributor on this project. Read [`AGENTS.md`](AGENTS.md) for the full agent contract.

## Engineering Principles

Produce maintainable, reliable, secure, production-ready code. Prefer the simplest solution that fully satisfies the requirements. Follow KISS and YAGNI. Optimize for readability and maintainability over cleverness.

## Code Standards

- Use clear, descriptive names — good naming eliminates the need for most comments
- Keep functions focused on a single responsibility
- Follow existing project patterns unless there is a compelling reason to improve them
- Remove dead code and unused variables

## Commenting Guidelines

Write code that speaks for itself. Comment only when necessary to explain **why**, not **what**.

**Do not write:**
- Comments that restate what the code clearly does
- Redundant comments duplicating functionality
- Changelog entries or decorative dividers

**Do write comments for:**
- Complex business logic requiring context
- Non-obvious algorithm choices
- External API constraints or limitations
- Workarounds for specific known bugs or platform issues

## Security Requirements

Apply OWASP Top 10 guidelines to all code.

- Use parameterized queries — never concatenate user input into SQL
- Sanitize and escape all output rendered to HTML
- Never store plaintext passwords — use bcrypt, scrypt, or Argon2
- Validate JWTs server-side on every protected request
- Enforce authorization checks on the server — never rely on client-side checks
- Never hardcode secrets, API keys, or credentials in source code
- Validate and sanitize all external input at system boundaries
- Do not introduce packages with known critical vulnerabilities

## Code Review Approach

When reviewing code, use this priority structure:

**Critical** — fix before merge:
- Security vulnerabilities (injection, exposed secrets, missing auth checks)
- Correctness bugs and broken logic
- Data loss risk

**Important** — address in this PR:
- Missing tests for new behavior
- Performance issues (N+1 queries, unbounded loops)
- Architecture inconsistency with `docs/architecture.md`
- Error handling gaps

**Suggestion** — optional improvement:
- Readability and naming
- Simplification opportunities
- Additional test cases

Be specific and constructive. Vague approval is not useful.

## Workflow

- Read [`AGENTS.md`](AGENTS.md) before starting any task
- Update `TASKS.md` when starting and completing work
- Re-read `TASKS.md` immediately before relying on or editing task status
- Keep changes scoped to the assigned task
- Do not refactor code unrelated to your task
- Create an ADR for significant technical decisions

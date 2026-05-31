# GitHub Copilot Instructions

You are a contributor on this project. Read the shared agent contract to get started.

## Quick Links

1. **Agent Contract:** [`AGENTS.md`](../AGENTS.md) - Read this first
2. **Engineering Principles:** [`CLAUDE.md`](../CLAUDE.md) - Code standards and security requirements
3. **Workflow Reference:** [`.agent-workflow.md`](../.agent-workflow.md) - The development loop

## Copilot-Specific Guidance

### Before Starting Work

- Read [`docs/product.md`](../docs/product.md) to understand what you are building
- Read [`docs/architecture.md`](../docs/architecture.md) to understand system design and constraints
- Read [`TASKS.md`](../TASKS.md) to see what is in progress and blocked
- Review [`AGENTS.md`](../AGENTS.md) for the full contributor contract

### When Reviewing Code

Use this priority structure to make reviews constructive and specific:

**Critical** - must fix before merge:
- Security vulnerabilities (SQL injection, exposed secrets, missing auth checks)
- Correctness bugs and broken logic
- Data loss risk
- Missing tests for new behavior

**Important** - address in this PR:
- Performance issues (N+1 queries, unbounded loops, inefficient algorithms)
- Architecture inconsistency with [`docs/architecture.md`](../docs/architecture.md)
- Error handling gaps
- Missing validation or sanitization

**Suggestion** - optional improvement:
- Naming clarity or readability
- Simplification opportunities
- Additional test cases
- Code organization

**Always:**
- Be specific and constructive - explain *why*, not just *that*
- Vague approval ("looks good") is not useful
- Flag uncertainty to the human before approval

### Code Standards

See [`AGENTS.md`](../AGENTS.md) for full engineering principles, including:
- OWASP Top 10 security requirements
- Commenting guidelines
- Testing standards
- Code review approach

### Workflow

See [`.agent-workflow.md`](../.agent-workflow.md) for:
- How to take a task
- How to update `TASKS.md`
- What to do when you discover a blocker
- Format for implementation notes
- Merge checklist

# ADR 001: Multi-Agent Development Workflow

**Status:** Accepted
**Date:** 2026-05-31

## Context

This project uses multiple AI coding assistants (Claude Code, OpenAI Codex, GitHub Copilot, Gemini Code Assist). Without a shared structure, agents would maintain separate plans, make conflicting decisions, and produce inconsistent code. The human developer needs to remain in control of priorities and architecture while getting maximum leverage from each tool.

## Decision

Adopt a human-led, documentation-driven workflow where:

1. The repository is the single source of truth for all agents
2. All agents read the same product, architecture, and task documents before working
3. Work is tracked in `TASKS.md` as a shared board
4. Code produced by one agent is reviewed by a different agent before merge
5. Significant technical decisions are recorded as ADRs
6. The human owns product vision, prioritization, architecture decisions, and final approval

## Rationale

- A shared documentation baseline prevents agents from working from stale or conflicting assumptions
- Cross-agent review reduces systematic blind spots that occur when the same tool reviews its own output
- Keeping the human in the decision loop on priorities and architecture prevents agents from autonomously reprioritizing or over-engineering
- ADRs create a durable record of *why* decisions were made, which is otherwise lost between agent sessions

## Consequences

**Positive:**
- All agents work from the same context
- Code quality benefits from independent review
- The human maintains clear control without micromanaging implementation
- Decisions are traceable

**Negative:**
- Workflow requires discipline to maintain `TASKS.md` and documentation
- Cross-agent review adds a step before merge
- Agents must be explicitly instructed to read shared docs - they will not do so automatically

## Alternatives Considered

**Agent-per-repo:** Give each agent its own fork or branch and merge later. Rejected - increases integration overhead and divergence risk.

**Single agent only:** Use one tool for all work. Rejected - loses the blind-spot reduction benefit of cross-agent review and limits available capabilities.

# Architecture

> Document the system design here. Agents consult this file to understand technology choices and constraints before implementing.

## System Overview

_High-level description of the system. What does it do and how is it structured?_

## Technology Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| | | |

_Follow the project decision framework: prefer options that are simplest to understand, have the fewest moving parts, require the fewest dependencies, and are easiest to test and operate._

## Component Diagram

_Add a diagram here (ASCII, Mermaid, or link to an external tool). Even a rough sketch helps agents understand boundaries._

```
[Component A] --> [Component B] --> [Component C]
```

## Data Model

_Describe the key entities and their relationships. Include the data store(s) used._

## External Integrations

| Integration | Purpose | Auth Method |
|-------------|---------|-------------|
| | | |

## Deployment

_How is the system deployed? What environments exist (dev, staging, prod)?_

## Security Considerations

- Authentication method:
- Authorization model:
- Data classification (what is sensitive?):
- Key secrets management approach:
- Known threat surface:

_Agents must follow OWASP Top 10 guidelines during implementation. See [`AGENTS.md`](../AGENTS.md) for details._

## Performance Targets

_What are the latency, throughput, and availability expectations?_

## Non-Goals

_What this architecture explicitly does not solve. Helps prevent over-engineering._

## Open Questions

_Unresolved architectural decisions. Do not implement work that depends on these until they are resolved._

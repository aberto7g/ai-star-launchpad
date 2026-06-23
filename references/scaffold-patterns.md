# Scaffold Patterns

Use the simplest pattern that can support a believable demo.

## 1. Single Web App

Use for:

- landing-page-first products
- lightweight SaaS demos
- tools with one main workflow

Suggested structure:

```text
app/
components/
lib/
public/
```

## 2. Web App Plus Worker

Use for:

- background processing
- async document jobs
- scraping, indexing, or evaluation pipelines

Suggested structure:

```text
app/
components/
lib/
worker/
```

## 3. CLI Plus Examples

Use for:

- developer utilities
- repo automation
- prompt or eval tooling

Suggested structure:

```text
src/
examples/
tests/
README.md
```

## 4. SDK Plus Demo App

Use for:

- reusable infrastructure
- MCP or agent integrations
- libraries that need a visible demo

Suggested structure:

```text
packages/sdk/
apps/demo/
examples/
```

## Selection Rules

- Prefer one deployable surface.
- Add a worker only if the workflow really needs async processing.
- Add a package split only if reuse is a first-order value proposition.
- If the user wants stars, optimize for clarity before architecture purity.

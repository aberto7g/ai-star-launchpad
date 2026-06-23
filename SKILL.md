---
name: ai-star-launchpad
description: Build star-worthy AI project repos from a short user prompt. Use when Codex needs to directly turn an AI product idea into a launchable repo package, including project positioning, tech stack, file tree, README, landing page copy, MVP scope, demo plan, and initial implementation structure. Prefer this skill when the goal is to make or package an AI agent product, a vertical AI app, or an AI developer tool that can be built and shown quickly on GitHub.
---

# AI Star Launchpad

Turn a short user request into a repo that is easier to ship, demo, and share.

The default job of this skill is not idea selection. The default job is direct build planning and repo packaging.

## Default Outcome

Unless the user asks for something narrower, produce:

1. Repo name
2. One-line pitch
3. Target user
4. MVP scope
5. Recommended stack
6. File tree
7. README opening
8. Landing page copy blocks
9. Demo flow
10. Launch checklist

If the user asks to create files, create the repo scaffold instead of stopping at advice.

When turning the plan into artifacts, use the generators in `scripts/` instead of hand-formatting everything from scratch.

## Operating Modes

Pick the narrowest mode that fits the request.

### Mode 1: Direct Repo Build

Use when the user already names a product or workflow.

Examples:

- "Build an AI PR review tool"
- "Build an AI resume screening app"
- "Build an MCP debugger"

Produce the repo package directly.

### Mode 2: Tightened Build

Use when the user has a broad direction but not a crisp wedge.

Examples:

- "Build an AI agent"
- "Build an AI coding tool"

Do only a small amount of tightening:

1. Narrow the audience
2. Narrow the workflow
3. Choose the easiest demo surface
4. Then build the repo package

Do not spend the response mostly on brainstorming.

### Mode 3: Existing Repo Upgrade

Use when the user already has a repo and wants it to be more star-worthy.

Produce:

1. clearer pitch
2. sharper MVP
3. better README hook
4. better demo flow
5. better launch packaging

## Build Rules

Bias toward fast demos and obvious value.

Prefer projects that are:

- easy to explain in one sentence
- easy to show in under 20 seconds
- easy to capture as a screenshot or GIF
- narrow enough for a quick MVP
- useful enough that developers want to star or share

Avoid defaulting to:

- generic chatbots
- thin wrappers around one API
- giant platforms with no first win
- vague "AI assistant" positioning

Read `references/star-heuristics.md` before shaping the repo.

## Stack Selection

Choose the stack that minimizes time to a strong demo.

Use these defaults unless the request strongly suggests otherwise:

- Web product: Next.js + TypeScript + Tailwind
- CLI or devtool: Python or TypeScript CLI
- Agent workflow service: Python backend with minimal web UI if needed
- Dashboard or observability surface: Next.js frontend plus a simple API layer

Read `references/scaffold-patterns.md` when choosing a repo shape.

## Required Deliverables

Every normal answer should contain these sections:

1. Project snapshot
2. MVP features
3. Tech stack
4. Repo structure
5. README hook
6. Landing page copy
7. Demo plan
8. Launch notes

If the user asks for actual implementation, continue from the plan into file creation.

## Repo Structure Guidance

Pick one of these common repo shapes:

1. single app
2. app plus worker
3. app plus SDK
4. app plus examples
5. CLI plus demo fixtures

Prefer fewer folders, fewer services, and fewer moving parts.

## README Rules

The first screen of the README should answer:

1. What is it
2. Who is it for
3. Why is it better or different
4. How fast can I try it

Reuse `references/output-templates.md` for README, landing page, and MVP formatting.

## When To Create Files

Create real files when the user asks to:

- build it
- scaffold it
- generate the repo
- write the README
- start the implementation

When creating files:

1. create only the smallest credible MVP scaffold
2. prioritize a polished README and demo surface
3. add example input and output where possible
4. keep setup short

For structured generation, use this order:

1. prepare a JSON spec that follows `references/input-schema.md`
2. run `scripts/generate_readme.py` for the README
3. run `scripts/generate_landing_copy.py` for landing page copy
4. run `scripts/scaffold_repo.py` when the user asks for a repo skeleton

## Optional Comparison Step

Only compare or score multiple ideas if the user explicitly asks for options, or if the request is too vague to build responsibly in one pass.

When comparison is needed, `scripts/score_idea.py` may help, but it is not the primary workflow of this skill.

## Resources

- `references/star-heuristics.md`: use for star potential and packaging decisions
- `references/output-templates.md`: use for repo brief, README hook, and launch output structure
- `references/scaffold-patterns.md`: use for choosing a simple repo architecture
- `references/input-schema.md`: use for the JSON input shape expected by the generators
- `scripts/generate_readme.py`: generate a repo README from a project spec
- `scripts/generate_landing_copy.py`: generate landing page copy from a project spec
- `scripts/scaffold_repo.py`: generate a repo scaffold from a project spec
- `scripts/score_idea.py`: optional ranking helper for multiple candidates

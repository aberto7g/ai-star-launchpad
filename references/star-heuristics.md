# Star Heuristics

Use these heuristics to decide whether an AI repo is merely interesting or actually likely to attract stars.

## Strong Signals

- The project pitch is clear in one sentence.
- The output is visible without a long explanation.
- The repo improves a workflow developers already do often.
- The first success can happen in minutes, not hours.
- The project sits on top of an existing wave: agents, coding tools, video, automation, evaluation, MCP, browser workflows, or vertical copilots.
- The repo has a strong share surface: screenshot, GIF, chart, benchmark, or before/after artifact.

## Weak Signals

- The idea depends on "trust me, it is powerful" instead of a visible demo.
- The project is a broad framework with no obvious wedge.
- The repo is a thin wrapper around a model or API.
- The value only appears after heavy integration work.
- The README cannot explain who it is for.

## Lane Selection

Prefer one of these lanes when the user has no market picked:

## Agent Products

Best when the trend is around automation, coding, operations, or workflow glue.

Look for:

- Repeated manual multi-step tasks
- Missing observability or evaluation
- Missing polish around a powerful but messy primitive
- Places where AI can produce a visible artifact, not only text

## Vertical AI Apps

Best when a niche audience has one painful repeated workflow and a strong before/after story.

Look for:

- Sales, support, research, hiring, finance, legal, content, ecommerce, or education workflows
- Inputs and outputs that are easy to visualize
- A narrow audience that can still recommend the repo to others

## Developer Tools

Best when a trend is already hot and developers need reliability, speed, insight, testing, benchmarking, or packaging around it.

Look for:

- Debugging
- Evaluation
- Prompt and workflow versioning
- Repo and release automation
- Data pipelines around models

## Scoring Rubric

Score each category from 1 to 5:

- `heat`: how much the surrounding space already has momentum
- `clarity`: how quickly a new visitor understands the value
- `demoability`: how easy it is to show in a GIF or screenshot
- `build_speed`: how realistic the MVP is in a short build window
- `distribution_fit`: how naturally the project can spread through GitHub, X, Reddit, Discord, or developer groups
- `wedge_strength`: how different it feels from adjacent repos
- `expansion_room`: how many believable next features or integrations can grow from the MVP

## README Rules

- Put the outcome before the technology.
- Open with a short, direct promise.
- Show one artifact early.
- Explain the first win before the architecture.
- Include one comparison line: what this does that nearby repos do not.

# Input Schema

Use this JSON shape with the generators in `scripts/`.

## Required Fields

- `name`: repo slug, for example `mcp-trace-lens`
- `one_liner`: short project promise
- `target_user`: primary audience
- `problem`: list of pain points
- `features`: list of at least 3 features

## Optional Fields

- `title`: display title, defaults from `name`
- `repo_kind`: one of:
  - `single-web-app`
  - `web-plus-worker`
  - `cli-plus-examples`
  - `sdk-plus-demo`
- `stack`: object with overrides for frontend, backend, storage, ai_layer, deployment
- `demo_flow`: object with `input`, `flow`, `output`, `proof`
- `ctas`: object with `primary`, `secondary`

## Example

```json
{
  "name": "mcp-trace-lens",
  "title": "MCP Trace Lens",
  "one_liner": "Debug agent and MCP workflows with a faster visual trace view.",
  "target_user": "AI engineers building agent products and tool-driven automations",
  "problem": [
    "Tool-call failures are hard to inspect quickly.",
    "Latency bottlenecks stay hidden across long traces.",
    "Debugging demos take too much manual explanation."
  ],
  "features": [
    {
      "name": "Trace Timeline",
      "description": "Show each tool call, model step, and latency spike in one scrollable view."
    },
    {
      "name": "Failure Drilldown",
      "description": "Jump straight to the broken step with payload and response context."
    },
    {
      "name": "Shareable Demo Session",
      "description": "Turn a real trace into a screenshot or short GIF for repo marketing."
    }
  ],
  "repo_kind": "single-web-app",
  "demo_flow": {
    "input": "Load a failed MCP trace from a sample session.",
    "flow": "Inspect the timeline, open the failed step, and compare timings.",
    "output": "A clear explanation of what broke and where the latency comes from.",
    "proof": "A single screenshot showing the trace view and failed step."
  },
  "ctas": {
    "primary": "Open the demo",
    "secondary": "Read the docs"
  }
}
```

## Commands

```powershell
python D:\skill\ai-star-launchpad\scripts\generate_readme.py --input spec.json
python D:\skill\ai-star-launchpad\scripts\generate_landing_copy.py --input spec.json
python D:\skill\ai-star-launchpad\scripts\scaffold_repo.py --input spec.json --output-dir .\output
```

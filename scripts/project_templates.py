#!/usr/bin/env python3

from __future__ import annotations

import json
from pathlib import Path


DEFAULT_STACKS = {
    "single-web-app": {
        "frontend": "Next.js + TypeScript + Tailwind CSS",
        "backend": "Next.js route handlers",
        "storage": "SQLite or Postgres",
        "ai_layer": "OpenAI or compatible LLM API",
        "deployment": "Vercel",
    },
    "web-plus-worker": {
        "frontend": "Next.js + TypeScript + Tailwind CSS",
        "backend": "Next.js route handlers",
        "storage": "Postgres",
        "ai_layer": "OpenAI or compatible LLM API",
        "deployment": "Vercel + background worker",
    },
    "cli-plus-examples": {
        "frontend": "None",
        "backend": "Python CLI",
        "storage": "Local files",
        "ai_layer": "OpenAI or compatible LLM API",
        "deployment": "PyPI or GitHub release",
    },
    "sdk-plus-demo": {
        "frontend": "Next.js demo app",
        "backend": "TypeScript SDK",
        "storage": "Optional local cache",
        "ai_layer": "OpenAI or compatible LLM API",
        "deployment": "npm package + demo deployment",
    },
}


def slugify(value: str) -> str:
    lowered = value.strip().lower()
    chars = []
    last_dash = False
    for char in lowered:
        if char.isalnum():
            chars.append(char)
            last_dash = False
        elif not last_dash:
            chars.append("-")
            last_dash = True
    return "".join(chars).strip("-") or "ai-project"


def package_name(value: str) -> str:
    return slugify(value).replace("-", "_")


def title_from_name(name: str) -> str:
    return " ".join(part.capitalize() for part in slugify(name).split("-"))


def format_label(value: str) -> str:
    return value.replace("_", " ").title()


def load_spec(path: str) -> dict:
    raw = Path(path).read_text(encoding="utf-8-sig")
    return normalize_spec(json.loads(raw))


def normalize_spec(spec: dict) -> dict:
    if not isinstance(spec, dict):
        raise ValueError("Project spec must be a JSON object.")

    name = str(spec.get("name", "")).strip()
    if not name:
        raise ValueError("Project spec requires a non-empty 'name'.")

    repo_kind = str(spec.get("repo_kind", "single-web-app")).strip()
    if repo_kind not in DEFAULT_STACKS:
        allowed = ", ".join(sorted(DEFAULT_STACKS))
        raise ValueError(f"Unsupported repo_kind '{repo_kind}'. Allowed: {allowed}")

    title = str(spec.get("title", "")).strip() or title_from_name(name)
    one_liner = str(spec.get("one_liner", "")).strip()
    if not one_liner:
        raise ValueError("Project spec requires a non-empty 'one_liner'.")

    target_user = str(spec.get("target_user", "")).strip()
    if not target_user:
        raise ValueError("Project spec requires a non-empty 'target_user'.")

    problems = spec.get("problem") or spec.get("problems") or []
    if not isinstance(problems, list):
        raise ValueError("'problem' must be a list of strings.")
    problems = [str(item).strip() for item in problems if str(item).strip()]
    if not problems:
        raise ValueError("Project spec requires at least one problem entry.")

    features = spec.get("features") or []
    if not isinstance(features, list):
        raise ValueError("'features' must be a list.")
    normalized_features = []
    for item in features:
        if isinstance(item, dict):
            feature_name = str(item.get("name", "")).strip()
            description = str(item.get("description", "")).strip()
        else:
            feature_name = str(item).strip()
            description = ""
        if feature_name:
            normalized_features.append(
                {"name": feature_name, "description": description or "Describe the user payoff here."}
            )
    if len(normalized_features) < 3:
        raise ValueError("Project spec requires at least three features.")

    stack = dict(DEFAULT_STACKS[repo_kind])
    user_stack = spec.get("stack") or {}
    if user_stack:
        if not isinstance(user_stack, dict):
            raise ValueError("'stack' must be an object.")
        for key, value in user_stack.items():
            stack[str(key)] = str(value).strip()

    demo_flow = spec.get("demo_flow") or {}
    if not isinstance(demo_flow, dict):
        raise ValueError("'demo_flow' must be an object.")
    demo_flow = {
        "input": str(demo_flow.get("input", "A realistic user request or example file.")).strip(),
        "flow": str(demo_flow.get("flow", "Run the main workflow from start to finish in one short recording.")).strip(),
        "output": str(demo_flow.get("output", "A visible result that proves the workflow worked.")).strip(),
        "proof": str(demo_flow.get("proof", "Capture the most convincing screen or before/after moment.")).strip(),
    }

    ctas = spec.get("ctas") or {}
    if not isinstance(ctas, dict):
        raise ValueError("'ctas' must be an object.")
    ctas = {
        "primary": str(ctas.get("primary", "Try the demo")).strip(),
        "secondary": str(ctas.get("secondary", "Read the README")).strip(),
    }

    return {
        "name": slugify(name),
        "title": title,
        "one_liner": one_liner,
        "target_user": target_user,
        "problem": problems,
        "features": normalized_features[:5],
        "stack": stack,
        "demo_flow": demo_flow,
        "ctas": ctas,
        "repo_kind": repo_kind,
        "tagline": str(spec.get("tagline", "")).strip(),
    }


def render_readme(spec: dict) -> str:
    features = "\n".join(
        f"- **{item['name']}**: {item['description']}" for item in spec["features"]
    )
    problems = "\n".join(f"- {item}" for item in spec["problem"])
    stack = "\n".join(
        f"- **{format_label(label)}**: {value}" for label, value in spec["stack"].items()
    )
    demo = spec["demo_flow"]
    return f"""# {spec['title']}

{spec['one_liner']}

Built for {spec['target_user']} who need a faster way to solve this workflow without extra glue code and manual busywork.

## Why It Exists

{problems}

## What It Does

{features}

## Demo Flow

1. **Input**: {demo['input']}
2. **Flow**: {demo['flow']}
3. **Output**: {demo['output']}
4. **Proof**: {demo['proof']}

## Suggested Stack

{stack}

## Fast Start

1. Clone the repo.
2. Install dependencies.
3. Add your API keys and local config.
4. Run the demo workflow and capture the first shareable result.
"""


def render_landing_copy(spec: dict) -> str:
    feature_lines = []
    for item in spec["features"]:
        feature_lines.append(f"- **{item['name']}**: {item['description']}")
    problems = "\n".join(f"- {item}" for item in spec["problem"])
    return f"""# Landing Page Copy

## Hero

- **Headline**: {spec['title']}
- **Subheadline**: {spec['one_liner']}
- **Primary CTA**: {spec['ctas']['primary']}
- **Secondary CTA**: {spec['ctas']['secondary']}

## Audience

- Built for {spec['target_user']}

## Problem

{problems}

## Feature Blocks

{chr(10).join(feature_lines)}

## Proof

- **Demo setup**: {spec['demo_flow']['input']}
- **Demo flow**: {spec['demo_flow']['flow']}
- **Proof moment**: {spec['demo_flow']['proof']}
"""


def render_tree(spec: dict) -> str:
    kind = spec["repo_kind"]
    if kind == "single-web-app":
        return """repo/
  app/
    layout.tsx
    page.tsx
    globals.css
  components/
    landing-page.tsx
  lib/
    config.ts
  docs/
    landing-copy.md
  public/
  README.md"""
    if kind == "web-plus-worker":
        return """repo/
  app/
    layout.tsx
    page.tsx
    api/
      jobs/
        route.ts
    globals.css
  components/
    landing-page.tsx
  lib/
    config.ts
  worker/
    main.py
  docs/
    landing-copy.md
  README.md"""
    if kind == "cli-plus-examples":
        return f"""repo/
  src/
    {package_name(spec['name'])}/
      __init__.py
      cli.py
  examples/
    sample-input.txt
  tests/
    test_smoke.py
  docs/
    landing-copy.md
  README.md"""
    return """repo/
  packages/
    sdk/
      src/
        index.ts
  apps/
    demo/
      app/
        layout.tsx
        page.tsx
        globals.css
  docs/
    landing-copy.md
  README.md"""


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def ensure_writable_root(output_dir: Path, force: bool) -> None:
    if output_dir.exists() and any(output_dir.iterdir()) and not force:
        raise ValueError(f"Output directory '{output_dir}' is not empty. Use --force to overwrite files.")
    output_dir.mkdir(parents=True, exist_ok=True)


def scaffold_repo(spec: dict, output_dir: Path, force: bool = False) -> list[Path]:
    ensure_writable_root(output_dir, force)
    generated = []
    files = build_files(spec)
    for relative_path, content in files.items():
        target = output_dir / relative_path
        write_text(target, content)
        generated.append(target)
    return generated


def build_files(spec: dict) -> dict[str, str]:
    kind = spec["repo_kind"]
    base = {
        "README.md": render_readme(spec),
        "docs/landing-copy.md": render_landing_copy(spec),
        ".gitignore": "node_modules/\n.next/\ndist/\n.env\n__pycache__/\n.venv/\n",
    }
    if kind == "single-web-app":
        base.update(build_single_web_app(spec))
    elif kind == "web-plus-worker":
        base.update(build_web_plus_worker(spec))
    elif kind == "cli-plus-examples":
        base.update(build_cli_plus_examples(spec))
    else:
        base.update(build_sdk_plus_demo(spec))
    return base


def build_single_web_app(spec: dict) -> dict[str, str]:
    features = ",\n  ".join(
        "{ name: '" + item["name"] + "', description: '" + item["description"] + "' }"
        for item in spec["features"]
    )
    return {
        "package.json": f"""{{
  "name": "{spec['name']}",
  "private": true,
  "scripts": {{
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  }},
  "dependencies": {{
    "next": "15.0.0",
    "react": "19.0.0",
    "react-dom": "19.0.0"
  }},
  "devDependencies": {{
    "typescript": "^5.6.0"
  }}
}}""",
        "tsconfig.json": """{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "es2022"],
    "strict": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "noEmit": true
  },
  "include": ["app/**/*", "components/**/*", "lib/**/*"]
}""",
        "app/layout.tsx": f"""import './globals.css';
import type {{ Metadata }} from 'next';

export const metadata: Metadata = {{
  title: '{spec['title']}',
  description: '{spec['one_liner']}',
}};

export default function RootLayout({{ children }}: {{ children: React.ReactNode }}) {{
  return (
    <html lang="en">
      <body>{{children}}</body>
    </html>
  );
}}
""",
        "app/page.tsx": """import { LandingPage } from '../components/landing-page';

export default function HomePage() {
  return <LandingPage />;
}
""",
        "app/globals.css": """body {
  margin: 0;
  font-family: Arial, sans-serif;
  background: linear-gradient(180deg, #f8fafc 0%, #e2e8f0 100%);
  color: #0f172a;
}

main {
  max-width: 960px;
  margin: 0 auto;
  padding: 48px 24px 72px;
}

.card {
  background: #ffffff;
  border-radius: 18px;
  padding: 24px;
  box-shadow: 0 18px 48px rgba(15, 23, 42, 0.08);
}
""",
        "components/landing-page.tsx": f"""import {{ projectConfig }} from '../lib/config';

export function LandingPage() {{
  return (
    <main>
      <section className="card">
        <p>{'{'}projectConfig.targetUser{'}'}</p>
        <h1>{'{'}projectConfig.title{'}'}</h1>
        <p>{'{'}projectConfig.oneLiner{'}'}</p>
        <ul>
          {{projectConfig.features.map((feature) => (
            <li key={{feature.name}}>
              <strong>{{feature.name}}</strong>
              <p>{{feature.description}}</p>
            </li>
          ))}}
        </ul>
      </section>
    </main>
  );
}}
""",
        "lib/config.ts": f"""export const projectConfig = {{
  title: '{spec['title']}',
  oneLiner: '{spec['one_liner']}',
  targetUser: '{spec['target_user']}',
  features: [{features}],
}};
""",
        "public/.gitkeep": "",
    }


def build_web_plus_worker(spec: dict) -> dict[str, str]:
    files = build_single_web_app(spec)
    files["app/api/jobs/route.ts"] = """import { NextResponse } from 'next/server';

export async function GET() {
  return NextResponse.json({
    status: 'ok',
    message: 'Queue this route into a real background job next.',
  });
}
"""
    files["worker/main.py"] = f"""#!/usr/bin/env python3

def process_job(payload: dict) -> dict:
    return {{
        "status": "queued",
        "project": "{spec['name']}",
        "payload": payload,
    }}


if __name__ == "__main__":
    print(process_job({{"sample": True}}))
"""
    return files


def build_cli_plus_examples(spec: dict) -> dict[str, str]:
    pkg = package_name(spec["name"])
    return {
        "pyproject.toml": f"""[project]
name = "{spec['name']}"
version = "0.1.0"
description = "{spec['one_liner']}"
requires-python = ">=3.10"

[project.scripts]
{spec['name']} = "{pkg}.cli:main"
""",
        f"src/{pkg}/__init__.py": "from .cli import main\n\n__all__ = ['main']\n",
        f"src/{pkg}/cli.py": f"""import argparse


def main() -> None:
    parser = argparse.ArgumentParser(description='{spec['one_liner']}')
    parser.add_argument('input', nargs='?', default='sample-input')
    args = parser.parse_args()
    print('Running {spec['title']} with', args.input)


if __name__ == '__main__':
    main()
""",
        "examples/sample-input.txt": "Replace this file with a realistic demo input.\n",
        "tests/test_smoke.py": f"""def test_project_name():
    assert '{spec['name']}'.startswith('{spec['name'].split('-')[0]}')
""",
    }


def build_sdk_plus_demo(spec: dict) -> dict[str, str]:
    return {
        "package.json": f"""{{
  "name": "{spec['name']}-workspace",
  "private": true,
  "workspaces": ["packages/*", "apps/*"]
}}""",
        "packages/sdk/package.json": f"""{{
  "name": "@{spec['name']}/sdk",
  "version": "0.1.0",
  "main": "src/index.ts"
}}""",
        "packages/sdk/src/index.ts": f"""export function describeProject() {{
  return {{
    name: '{spec['name']}',
    title: '{spec['title']}',
    oneLiner: '{spec['one_liner']}',
  }};
}}
""",
        "apps/demo/package.json": f"""{{
  "name": "{spec['name']}-demo",
  "private": true,
  "dependencies": {{
    "next": "15.0.0",
    "react": "19.0.0",
    "react-dom": "19.0.0"
  }}
}}""",
        "apps/demo/app/layout.tsx": f"""import './globals.css';

export const metadata = {{
  title: '{spec['title']} Demo',
  description: '{spec['one_liner']}',
}};

export default function RootLayout({{ children }}: {{ children: React.ReactNode }}) {{
  return (
    <html lang="en">
      <body>{{children}}</body>
    </html>
  );
}}
""",
        "apps/demo/app/page.tsx": f"""export default function DemoPage() {{
  return (
    <main style={{padding: 32}}>
      <h1>{spec['title']}</h1>
      <p>{spec['one_liner']}</p>
    </main>
  );
}}
""",
        "apps/demo/app/globals.css": "body { margin: 0; font-family: Arial, sans-serif; }\n",
    }

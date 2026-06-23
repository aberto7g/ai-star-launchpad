#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from project_templates import load_spec, render_readme


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a README from an AI project spec.")
    parser.add_argument("--input", required=True, help="Path to a JSON project spec.")
    parser.add_argument("--output", help="Optional output path. Defaults to stdout.")
    args = parser.parse_args()

    content = render_readme(load_spec(args.input))
    if args.output:
        target = Path(args.output)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content.rstrip() + "\n", encoding="utf-8")
    else:
        print(content)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3

from __future__ import annotations

import argparse
from pathlib import Path

from project_templates import load_spec, scaffold_repo


def main() -> int:
    parser = argparse.ArgumentParser(description="Scaffold an AI repo from a JSON project spec.")
    parser.add_argument("--input", required=True, help="Path to a JSON project spec.")
    parser.add_argument(
        "--output-dir",
        required=True,
        help="Directory where the scaffold should be written.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into a non-empty directory.",
    )
    args = parser.parse_args()

    generated = scaffold_repo(load_spec(args.input), Path(args.output_dir), force=args.force)
    for path in generated:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

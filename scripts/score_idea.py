#!/usr/bin/env python3
"""
Rank candidate AI repo ideas by star-potential heuristics.

Input JSON format:
[
  {
    "name": "Idea name",
    "heat": 4,
    "clarity": 5,
    "demoability": 4,
    "build_speed": 3,
    "distribution_fit": 5,
    "wedge_strength": 4,
    "expansion_room": 4,
    "notes": "Optional notes"
  }
]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

FIELDS = (
    "heat",
    "clarity",
    "demoability",
    "build_speed",
    "distribution_fit",
    "wedge_strength",
    "expansion_room",
)

WEIGHTS = {
    "heat": 1.2,
    "clarity": 1.4,
    "demoability": 1.4,
    "build_speed": 1.1,
    "distribution_fit": 1.3,
    "wedge_strength": 1.5,
    "expansion_room": 1.1,
}


def load_items(input_path: str | None) -> list[dict]:
    if input_path:
        raw = Path(input_path).read_text(encoding="utf-8-sig")
    else:
        raw = sys.stdin.read().lstrip("\ufeff")

    data = json.loads(raw)
    if not isinstance(data, list):
        raise ValueError("Input JSON must be a list of idea objects.")
    return data


def validate_score(value, field: str, idea_name: str) -> float:
    if not isinstance(value, (int, float)):
        raise ValueError(f"{idea_name}: field '{field}' must be numeric.")
    if not 1 <= float(value) <= 5:
        raise ValueError(f"{idea_name}: field '{field}' must be between 1 and 5.")
    return float(value)


def score_item(item: dict) -> dict:
    name = str(item.get("name", "")).strip() or "Untitled idea"
    scored = {"name": name, "notes": str(item.get("notes", "")).strip()}
    total = 0.0
    max_total = 0.0

    for field in FIELDS:
        score = validate_score(item.get(field), field, name)
        weight = WEIGHTS[field]
        total += score * weight
        max_total += 5 * weight
        scored[field] = score

    scored["weighted_score"] = round(total, 2)
    scored["normalized_score"] = round((total / max_total) * 100, 1)
    return scored


def render_table(items: list[dict]) -> str:
    lines = []
    header = f"{'Rank':<4}  {'Idea':<32}  {'Score':>5}  {'Pct':>5}"
    lines.append(header)
    lines.append("-" * len(header))
    for idx, item in enumerate(items, start=1):
        lines.append(
            f"{idx:<4}  {item['name'][:32]:<32}  {item['weighted_score']:>5.1f}  {item['normalized_score']:>4.1f}%"
        )
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Score AI repo ideas.")
    parser.add_argument("--input", help="Path to a JSON file. Defaults to stdin.")
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print ranked JSON instead of a plain-text table.",
    )
    args = parser.parse_args()

    try:
        ranked = [score_item(item) for item in load_items(args.input)]
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    ranked.sort(key=lambda item: item["weighted_score"], reverse=True)

    if args.json:
        print(json.dumps(ranked, ensure_ascii=False, indent=2))
        return 0

    print(render_table(ranked))
    print()
    for item in ranked:
        if item["notes"]:
            print(f"- {item['name']}: {item['notes']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

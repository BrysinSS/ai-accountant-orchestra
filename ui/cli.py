"""Portable command-line interface with machine-meaningful exit codes."""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Dict, List, Optional

from orchestrator.controller import run_recipe


def parse_kv_params(pairs: List[str]) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for item in pairs:
        if "=" not in item:
            raise ValueError(f"Expected key=value, got: {item!r}")
        key, value = (part.strip() for part in item.split("=", 1))
        if not key:
            raise ValueError(f"Empty key in parameter: {item!r}")
        out[key] = value
    return out


def parse_ask(text: str) -> Dict[str, str]:
    """Extract one explicit quarter and four-digit year; this is regex, not AI."""
    patterns = [
        r"(?:кв(?:артал)?|Q)\s*([1-4])\D+(\d{4})",
        r"(\d{4})\D+(?:кв(?:артал)?|Q)\s*([1-4])",
    ]
    first = re.search(patterns[0], text.strip(), flags=re.IGNORECASE)
    if first:
        quarter, year = first.group(1), first.group(2)
        return {"period": f"Q{quarter}-{year}"}
    second = re.search(patterns[1], text.strip(), flags=re.IGNORECASE)
    if second:
        year, quarter = second.group(1), second.group(2)
        return {"period": f"Q{quarter}-{year}"}
    return {}


def pretty_print_result(result: Dict) -> None:
    print(json.dumps(result, ensure_ascii=True, indent=2, sort_keys=True, default=str))


def run_cli(recipe: Optional[str], ask: Optional[str], params_kv: List[str]) -> int:
    try:
        params = parse_kv_params(params_kv)
    except ValueError as exc:
        print(f"Parameter error: {exc}", file=sys.stderr)
        return 2

    if ask:
        parsed = parse_ask(ask)
        if not parsed:
            print("Could not extract a Qn-YYYY period from --ask.", file=sys.stderr)
            return 2
        params.update(parsed)

    if not recipe:
        print("--recipe is required; --ask only extracts a period.", file=sys.stderr)
        return 2

    try:
        result = run_recipe(str(recipe), overrides={"params": params, **params})
    except Exception as exc:  # defensive boundary for unexpected controller failures
        print(f"Execution error: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 1
    if not isinstance(result, dict):
        print("Controller returned a non-dictionary result.", file=sys.stderr)
        return 1

    pretty_print_result(result)
    return 0 if result.get("status") == "OK" else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a deterministic YAML transaction recipe.")
    parser.add_argument("--recipe", help="Path to a trusted YAML recipe")
    parser.add_argument("--ask", help="Optional text containing an explicit quarter and year")
    parser.add_argument("--params", nargs="*", default=[], help="Recipe parameters as key=value")
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    args = build_parser().parse_args(argv)
    return run_cli(args.recipe, args.ask, args.params)


if __name__ == "__main__":
    raise SystemExit(main())

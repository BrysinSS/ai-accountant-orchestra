"""Command-line entry point for the deterministic recipe runner."""

from __future__ import annotations

import sys


def main() -> int:
    try:
        from ui.cli import main as cli_main
    except Exception as exc:
        print(f"ERROR: CLI dependencies could not be imported: {exc}", file=sys.stderr)
        return 2
    return cli_main()


if __name__ == "__main__":
    raise SystemExit(main())

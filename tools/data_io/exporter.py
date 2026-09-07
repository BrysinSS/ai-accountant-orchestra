"""JSON and Markdown reporting for deterministic workflow results."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, StrictUndefined, select_autoescape


def save_summary(
    summary: dict[str, Any],
    period: str,
    md_path: str = "workspace/summary_latest.md",
    json_path: str = "workspace/summary_latest.json",
    template_path: str = "templates/reports/summary.j2.md",
) -> dict[str, str]:
    """Write an already-calculated result; never infer or invent tax values."""
    if not isinstance(summary, dict):
        raise ValueError("summary must be a dictionary")
    payload = {**summary, "period": period}

    json_file = Path(json_path)
    md_file = Path(md_path)
    json_file.parent.mkdir(parents=True, exist_ok=True)
    md_file.parent.mkdir(parents=True, exist_ok=True)
    json_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    project_root = Path(__file__).resolve().parents[2]
    template_file = (project_root / template_path).resolve()
    if not template_file.is_file():
        raise ValueError(f"Summary template not found: {template_path}")
    env = Environment(
        loader=FileSystemLoader(str(template_file.parent)),
        autoescape=select_autoescape(disabled_extensions=("md",)),
        undefined=StrictUndefined,
        keep_trailing_newline=True,
    )
    rendered = env.get_template(template_file.name).render(
        summary=payload,
        period=period,
        kor_applied=bool(payload.get("kor_applied", False)),
        vat_breakdown=payload.get("vat_breakdown", {}),
    )
    md_file.write_text(rendered, encoding="utf-8")
    return {"json_path": str(json_file), "md_path": str(md_file)}

import json
from pathlib import Path

from orchestrator.controller import run_recipe


def test_demo_csv_runs_end_to_end_with_artifacts_and_ordered_log():
    json_path = Path("workspace/test-output/e2e-summary.json")
    md_path = Path("workspace/test-output/e2e-summary.md")
    result = run_recipe("recipes/btw_return.yml", {"params": {
        "period": "Q3-2024", "json_path": str(json_path), "md_path": str(md_path)
    }})

    assert result["status"] == "OK"
    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert payload["period"] == "Q3-2024"
    assert payload["n_transactions"] == 4
    assert payload["gross_revenue"] == 5.9
    assert payload["vat_total"] == 0.49
    assert payload["net_revenue"] == 5.41
    assert "not suitable for tax filing" in md_path.read_text(encoding="utf-8")

    records = [json.loads(line) for line in Path(result["log_path"]).read_text(encoding="utf-8").splitlines()]
    assert [record["step"] for record in records] == [
        "load_source", "validate_source", "normalize", "filter_period",
        "summarize", "load_vat_rules", "calculate_vat_demo", "save_artifacts",
    ]
    assert all(record["status"] == "OK" for record in records)


def test_end_to_end_empty_period_produces_failure_artifact_and_log():
    result = run_recipe("recipes/btw_return.yml", {"params": {"period": "Q2-2023"}})
    assert result["status"] == "FAILED"
    failure = result["artifacts"]["failure"]["value"]
    assert failure["step"] == "filter_period"
    assert Path(failure["error_path"]).is_file()
    assert Path(result["log_path"]).is_file()

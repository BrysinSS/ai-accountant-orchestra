import json
from pathlib import Path

from orchestrator.controller import run_recipe


def _log_records(result):
    return [json.loads(line) for line in Path(result["log_path"]).read_text(encoding="utf-8").splitlines()]


def test_successful_recipe_has_meaningful_status_and_dependency_result():
    result = run_recipe("tests/fixtures/controller_dependency.yml")
    assert result["status"] == "OK"
    assert result["artifacts"]["vat"]["value"]["vat_total"] == 21.0
    assert [record["step"] for record in _log_records(result)] == ["rules", "vat"]


def test_failed_step_stops_downstream_work():
    result = run_recipe("recipes/btw_return.yml", {"params": {"period": "Q5-2024"}})
    assert result["status"] == "FAILED"
    assert result["artifacts"]["failure"]["value"]["step"] == "filter_period"
    assert "summarize" not in result["artifacts"]


def test_continue_on_error_runs_independent_downstream_step():
    result = run_recipe("tests/fixtures/controller_continue.yml")
    assert result["status"] == "PARTIAL_SUCCESS"
    assert result["artifacts"]["failure"]["value"]["step"] == "invalid_period"
    assert "downstream" in result["artifacts"]


def test_invalid_mandatory_validation_stops_normalization():
    result = run_recipe("recipes/btw_return.yml", {"params": {
        "period": "Q3-2024", "input": "tests/fixtures/missing_column.csv"
    }})
    assert result["status"] == "FAILED"
    assert result["artifacts"]["validate_source"]["value"]["valid"] is False
    assert result["artifacts"]["failure"]["value"]["step"] == "validate_source"
    assert "normalize" not in result["artifacts"]
    records = _log_records(result)
    assert records[-1]["status"] == "FAILED"
    assert set(records[-1]) == {"ts", "level", "event", "step", "status", "duration_ms", "message"}

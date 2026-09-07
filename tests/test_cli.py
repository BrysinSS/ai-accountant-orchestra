from ui.cli import run_cli


def test_successful_cli_run_returns_zero():
    code = run_cli("recipes/btw_return.yml", None, [
        "period=Q3-2024",
        "json_path=workspace/test-output/cli-success.json",
        "md_path=workspace/test-output/cli-success.md",
    ])
    assert code == 0


def test_invalid_cli_parameter_returns_nonzero():
    assert run_cli("recipes/btw_return.yml", None, ["not-a-key-value"]) != 0


def test_validation_failure_returns_nonzero():
    code = run_cli("recipes/btw_return.yml", None, [
        "period=Q3-2024", "input=tests/fixtures/missing_column.csv"
    ])
    assert code != 0


def test_execution_exception_returns_nonzero():
    assert run_cli("recipes/does-not-exist.yml", None, []) != 0

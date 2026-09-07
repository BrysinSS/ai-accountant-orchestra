from tools.data_io.loader import load_source_dataframe
from tools.validation.schema import validate_dataframe


def test_valid_source_dataset_has_structured_report():
    report = validate_dataframe(load_source_dataframe("data/demo_transactions.csv"))
    assert report["valid"] is True
    assert report["errors"] == []
    assert report["warnings"] == []
    assert report["info"]["row_count"] == 10


def test_missing_required_column_is_validation_error():
    report = validate_dataframe(load_source_dataframe("tests/fixtures/missing_column.csv"))
    assert report["valid"] is False
    assert any("product_name" in error for error in report["errors"])


def test_malformed_values_are_validation_errors():
    report = validate_dataframe(load_source_dataframe("tests/fixtures/malformed.csv"))
    assert report["valid"] is False
    assert any("transaction_date" in error for error in report["errors"])
    assert any("monetary" in error for error in report["errors"])

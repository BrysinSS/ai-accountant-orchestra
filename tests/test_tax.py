import pandas as pd
import pytest

from tools.analysis.tax import compute_vat, load_rules


def test_dataframe_vat_uses_supported_rates_and_rounds():
    df = pd.DataFrame([
        {"amount_gross": 109.0, "category": "Food"},
        {"amount_gross": 121.0, "category": "General"},
    ])
    rules = {"category_rates": {"Food": 0.09, "General": 0.21}, "default_rate": 0.21, "kor_threshold": 0}
    result = compute_vat(df, rules)
    assert result["tax_amount"].tolist() == [9.0, 21.0]
    assert result.attrs["vat_breakdown"] == {"low": 9.0, "high": 21.0}


def test_summary_vat_updates_group_and_total_net_values():
    summary = {"gross_revenue": 230.0, "net_revenue": 230.0, "by_group": [
        {"key": "Food", "gross": 109.0}, {"key": "General", "gross": 121.0}
    ]}
    rules = {"category_rates": {"Food": 0.09, "General": 0.21}, "default_rate": 0.21, "kor_threshold": 0}
    result = compute_vat(summary, rules)
    assert result["vat_total"] == 30.0
    assert result["net_revenue"] == 200.0
    assert [group["tax_amount"] for group in result["by_group"]] == [9.0, 21.0]


def test_load_included_rules_yaml():
    rules = load_rules("rules/nl_vat_2025.yaml")
    assert rules["category_rates"]["Produce"] == 0.09


@pytest.mark.parametrize(("gross", "expected"), [(19999.99, True), (20000.0, False), (20000.01, False)])
def test_simplified_kor_threshold_contract(gross, expected):
    df = pd.DataFrame([{"amount_gross": gross, "category": "Food"}])
    rules = {"category_rates": {"Food": 0.09}, "default_rate": 0.21, "kor_threshold": 20000}
    result = compute_vat(df, rules)
    assert result.attrs["kor_applied"] is expected
    assert (float(result["tax_amount"].sum()) == 0.0) is expected


def test_kor_can_be_explicitly_disabled_for_quarter_demo():
    df = pd.DataFrame([{"amount_gross": 109.0, "category": "Food"}])
    rules = {"category_rates": {"Food": 0.09}, "default_rate": 0.21, "kor_threshold": 20000}
    result = compute_vat(df, rules, apply_kor=False)
    assert result.attrs["kor_applied"] is False
    assert result.loc[0, "tax_amount"] == 9.0

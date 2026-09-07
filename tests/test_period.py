import pandas as pd
import pytest

from tools.analysis.period import filter_period, parse_quarter


@pytest.mark.parametrize(("label", "start", "end"), [
    ("Q1-2024", "2024-01-01", "2024-03-31"),
    ("Q2-2024", "2024-04-01", "2024-06-30"),
    ("Q3-2024", "2024-07-01", "2024-09-30"),
    ("Q4-2024", "2024-10-01", "2024-12-31"),
])
def test_parse_quarter_contract(label, start, end):
    quarter = parse_quarter(label)
    assert quarter.start.isoformat() == start
    assert quarter.end.isoformat() == end


def test_filter_period_includes_both_boundaries_and_excludes_outside():
    df = pd.DataFrame({"date": ["2024-06-30", "2024-07-01", "2024-09-30", "2024-10-01"], "value": range(4)})
    result = filter_period(df, "Q3-2024")
    assert result["date"].tolist() == ["2024-07-01", "2024-09-30"]


@pytest.mark.parametrize("period", ["2024-Q3", "Q0-2024", "Q5-2024", "q3-2024", "Q3-24", ""])
def test_invalid_period_is_rejected(period):
    with pytest.raises(ValueError, match="Invalid period"):
        parse_quarter(period)


def test_empty_period_is_a_visible_failure():
    with pytest.raises(ValueError, match="No transactions"):
        filter_period(pd.DataFrame({"date": ["2024-01-01"]}), "Q3-2024")

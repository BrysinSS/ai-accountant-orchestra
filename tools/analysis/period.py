"""Calendar-quarter parsing and filtering for normalized transactions."""

from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date

import pandas as pd


_PERIOD_RE = re.compile(r"^Q([1-4])-(\d{4})$")


@dataclass(frozen=True)
class Quarter:
    label: str
    start: date
    end: date


def parse_quarter(period: str) -> Quarter:
    """Parse the exact, case-sensitive public format ``Qn-YYYY``."""
    if not isinstance(period, str) or not (match := _PERIOD_RE.fullmatch(period)):
        raise ValueError("Invalid period; expected Q1-YYYY, Q2-YYYY, Q3-YYYY or Q4-YYYY.")
    quarter, year = int(match.group(1)), int(match.group(2))
    start_month = (quarter - 1) * 3 + 1
    end_month = start_month + 2
    end_day = 31 if end_month in {3, 12} else 30
    return Quarter(period, date(year, start_month, 1), date(year, end_month, end_day))


def filter_period(df: pd.DataFrame, period: str) -> pd.DataFrame:
    """Select normalized rows inside an inclusive calendar quarter."""
    if "date" not in df.columns:
        raise ValueError("Normalized input is missing required column: date")
    quarter = parse_quarter(period)
    dates = pd.to_datetime(df["date"], errors="coerce", format="%Y-%m-%d")
    if dates.isna().any():
        raise ValueError("Normalized input contains an invalid date.")
    mask = dates.between(pd.Timestamp(quarter.start), pd.Timestamp(quarter.end), inclusive="both")
    selected = df.loc[mask].copy().reset_index(drop=True)
    if selected.empty:
        raise ValueError(f"No transactions found for period {period}.")
    selected.attrs.update(df.attrs)
    selected.attrs["period"] = period
    return selected

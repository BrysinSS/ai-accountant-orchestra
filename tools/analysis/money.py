"""Explicit monetary rounding used at report/calculation boundaries."""

from decimal import Decimal, ROUND_HALF_UP


CENT = Decimal("0.01")


def round_money(value: object) -> float:
    """Round a numeric value to cents with decimal ROUND_HALF_UP semantics."""
    return float(Decimal(str(value)).quantize(CENT, rounding=ROUND_HALF_UP))

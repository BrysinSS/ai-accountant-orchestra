"""
Validation schema stubs for datasets.

This module defines a named schema id "kaggle_grocery_v1" and a minimal
validator that checks required fields existence:
- Must have at least: "transaction_date", "product_name"
- For amount:
    - Prefer "final_amount"
    - If "final_amount" is missing, then BOTH "total_amount" AND "discount_amount"
      must be present.

No business semantics beyond presence checks.
"""

from typing import Dict, List, Tuple

import pandas as pd

KAGGLE_GROCERY_V1 = "kaggle_grocery_v1"

REQUIRED_ALWAYS = ["transaction_date", "product_name", "aisle"]
REQUIRED_FINAL = ["final_amount"]
REQUIRED_FALLBACK = ["total_amount", "discount_amount"]


def validate_dataset_columns(columns: List[str], schema_id: str = KAGGLE_GROCERY_V1) -> Tuple[bool, List[str]]:
    """
    Validate dataset columns for a given schema_id.
    Returns (is_valid, errors)
    """
    errors: List[str] = []

    if schema_id != KAGGLE_GROCERY_V1:
        errors.append(f"Unknown schema_id: {schema_id}")
        return False, errors

    # Check always-required fields
    for col in REQUIRED_ALWAYS:
        if col not in columns:
            errors.append(f"Missing required column: '{col}'")

    # Amount presence logic
    has_final = all(col in columns for col in REQUIRED_FINAL)
    has_fallback = all(col in columns for col in REQUIRED_FALLBACK)

    if not has_final and not has_fallback:
        errors.append(
            "Amount columns are insufficient: need 'final_amount' OR both 'total_amount' AND 'discount_amount'."
        )

    return len(errors) == 0, errors


def validate_dataframe(df, schema_id: str = KAGGLE_GROCERY_V1) -> Dict[str, object]:
    """
    Minimal validator for a pandas DataFrame.
    Returns a report dict with fields:
      - schema_id
      - valid (bool)
      - errors (list of strings)
    """
    if not isinstance(df, pd.DataFrame):
        return {
            "schema_id": schema_id,
            "valid": False,
            "errors": ["Input is not a pandas DataFrame."],
            "warnings": [],
            "info": {"row_count": 0},
        }

    cols = list(df.columns)
    valid, errs = validate_dataset_columns(cols, schema_id=schema_id)
    if valid:
        dates = pd.to_datetime(df["transaction_date"], errors="coerce")
        if dates.isna().any():
            errs.append(f"Invalid transaction_date values: {int(dates.isna().sum())} row(s).")
        preferred = pd.to_numeric(df["final_amount"], errors="coerce") if "final_amount" in df.columns else None
        if preferred is not None and not preferred.isna().all():
            invalid_amounts = preferred.isna()
        elif {"total_amount", "discount_amount"}.issubset(df.columns):
            total = pd.to_numeric(df["total_amount"], errors="coerce")
            discount = pd.to_numeric(df["discount_amount"], errors="coerce")
            invalid_amounts = total.isna() | discount.isna()
        else:
            invalid_amounts = preferred.isna()
        if invalid_amounts.any():
            errs.append(f"Invalid monetary values: {int(invalid_amounts.sum())} row(s).")

    warnings = ["Dataset contains no rows."] if df.empty else []
    return {
        "schema_id": schema_id,
        "valid": not errs,
        "errors": errs,
        "warnings": warnings,
        "info": {"row_count": int(len(df)), "column_count": int(len(df.columns))},
    }

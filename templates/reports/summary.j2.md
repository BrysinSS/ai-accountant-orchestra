# BTW Summary

_Period:_ **{{ period }}**

## Overview
- **Transactions:** {{ summary.n_transactions or 0 }}
- **Gross revenue:** {{ "%.2f"|format((summary.gross_revenue or 0)|float) }}
- **Net revenue:** {{ "%.2f"|format((summary.net_revenue or 0)|float) }}

## Returns
- **Count:** {{ (summary.returns.n if summary.returns else 0) }}
- **Sum:** {{ "%.2f"|format(((summary.returns.sum) if summary.returns else 0)|float) }}

## VAT Breakdown
- **Low VAT (9%)**: {{ "%.2f"|format(((vat_breakdown.low) if vat_breakdown else 0)|float) }}
- **High VAT (21%)**: {{ "%.2f"|format(((vat_breakdown.high) if vat_breakdown else 0)|float) }}
- **Total VAT represented by this demo calculation**: {{ "%.2f"|format((summary.vat_total or 0)|float) }}

## KOR Status
{% if kor_applied %}Simplified KOR switch applied: YES{% else %}Simplified KOR switch applied: NO{% endif %}

_Demonstration output only; not a BTW return and not suitable for tax filing._

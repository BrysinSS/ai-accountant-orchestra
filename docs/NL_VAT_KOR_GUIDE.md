# VAT and KOR code boundary

This page documents software behavior, not Dutch tax guidance.

`tools.analysis.tax.compute_vat` maps a category to a configured rate and calculates VAT represented in a gross amount as `gross * rate / (1 + rate)`. Public monetary results are rounded to cents with Decimal `ROUND_HALF_UP`. Tests cover the configured 9% and 21% examples and deterministic boundary behavior.

The function also retains a simplified KOR switch: when explicitly enabled, it compares the supplied total with `kor_threshold`; values strictly below the threshold zero the calculated VAT, while an equal or higher value does not. This is intentionally only a demonstration contract. It does not consider registration, annual turnover completeness, exclusions, effective dates or other eligibility rules.

The main quarter recipe passes `apply_kor: false`. A filtered quarter cannot by itself establish annual eligibility, so its output always reports `kor_applied: false`.

`rules/nl_vat_2025.yaml` is legacy example configuration with its own `last_updated` field and an official-source URL. Its legal currency was not re-verified in this iteration, and the project does not claim that its category list or KOR behavior is complete or current. Consult current official Belastingdienst information or a qualified adviser for real decisions.

No generated artifact is an official BTW-aangifte or suitable for submission to Belastingdienst.

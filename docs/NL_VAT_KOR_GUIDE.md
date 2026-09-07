# VAT/BTW and KOR behavior in this code

This document describes demonstration code, not current tax eligibility or filing guidance.

## Calculation module

[tools/analysis/tax.py](../tools/analysis/tax.py) provides `compute_vat` and `load_rules`. [tests/test_tax.py](../tests/test_tax.py) checks DataFrame and summary inputs, rule loading and simplified KOR zeroing.

The tests use rates of 0.09 and 0.21 and verify tax extraction from gross amounts. A separate KOR test passes a threshold of 20000 and checks that the code zeroes tax for its input. These are test inputs and implemented behavior, not a statement that a business legally qualifies for an exemption.

## Recipe boundary

[recipes/btw_return.yml](../recipes/btw_return.yml) does not call `compute_vat`. It summarizes transactions and supplies fixed `kor_applied: true` and zero VAT metadata to the exporter. The period parameter labels the report; it does not filter input dates.

The 2025 rules file and simplified threshold model do not demonstrate current compliance, registration status, annual turnover completeness, tax filing or submission to an authority.

See [the README](../README.md) for executable commands and known validation limitations.


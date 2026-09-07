# Changelog

## Unreleased

### Added
- Inclusive `Qn-YYYY` period parsing and transaction filtering.
- Structured source validation reports with errors, warnings and informational counts.
- Controller, CLI, period, validation, VAT/KOR, artifact, log and end-to-end tests.
- Engineering baseline and evidence documents.

### Changed
- The BTW demonstration recipe now validates raw source columns before normalization, filters the selected quarter and calls the existing VAT calculation module.
- Invalid mandatory validation stops dependent steps and fails the pipeline.
- CLI exit code `0` is now reserved for an `OK` pipeline result; failures return non-zero.
- Monetary report values use explicit cent rounding with Decimal `ROUND_HALF_UP`.
- The main quarter recipe explicitly disables the simplified KOR switch.
- CI installs dependencies and runs pytest on Python 3.11 and 3.12.
- IDE files, bytecode and generated runtime output were removed from version control and ignored.

### Breaking Changes
- `--ask` without `--recipe` no longer invokes unfinished agent scaffolding; it is only an optional period parser for an explicit recipe.
- `save_summary` requires an explicit `period` and no longer derives VAT values during export.


## [0.1.0] - 2025-11-06

### Added
- Initial skeleton: README with PyCharm quickstart and run configuration.
- `config.yaml` with `input_schema: kaggle_grocery_v1`, column mapping, and `description_format`.
- `rules/nl_vat_2025.yaml` placeholder VAT mapping (non-authoritative).
- `data/demo_transactions.csv` (includes a negative final_amount for demo).
- Validation stub in `tools/validation/schema.py` for `kaggle_grocery_v1`.
- `templates/reports/summary.j2.md` with negative totals section.
- `recipes/btw_return.yml` stub.
- `main.py` skeleton runner.
- `.env.example`, `.gitkeep` scaffolding.

### Breaking Changes
- None (public APIs are stubs; no runtime contracts promised yet).

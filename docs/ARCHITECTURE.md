# Architecture and contracts

The repository implements one advertised path: a trusted YAML recipe coordinates deterministic Python functions. There is no LLM in this path.

## Data boundaries

`load_source_dataframe` preserves source columns. `validate_dataframe` then checks the `kaggle_grocery_v1` contract: required date/description fields, an accepted amount representation, parseable dates and numeric amounts. Its result separates `errors`, `warnings` and informational row/column counts.

An invalid report is a controller failure. The normalized boundary contains `date`, `description`, `amount_gross`, `vat_rate` and `category`. `load_dataframe` remains the backward-compatible composition of source loading and normalization.

## Execution semantics

The controller resolves `${steps.<name>.result}` references immediately before each step, records each result, and stops on exceptions or invalid validation reports unless that step explicitly sets `options.continue_on_error: true`. A continued failure yields `PARTIAL_SUCCESS`.

Every attempted step produces one NDJSON record with timestamp, level, event, step, status, duration and message. A failure also produces a JSON artifact with the recipe, step, exception and bounded traceback. CLI exit `0` means `OK`; input/configuration and pipeline failures are non-zero.

## Main recipe

```text
load_source -> validate_source -> normalize -> filter_period
            -> summarize -> load_vat_rules -> calculate_vat_demo
            -> save_artifacts
```

The VAT step operates on the category summary and calculates the portion represented by configured gross-inclusive rates. The recipe passes `apply_kor: false`; the separate threshold switch is not a valid inference from one quarter.

Runtime artifacts live under `workspace/` and are ignored by Git. Recipes dynamically import functions and are therefore trusted inputs, not a sandbox.

## Non-functional scaffolding

`agents/` and `orchestrator/router.py` are not part of the advertised workflow. Controller agent steps fail visibly as unimplemented. The CLI `--ask` parser only extracts an explicit quarter/year with regular expressions.

# Engineering baseline

Baseline commit: `f22e5e4d4e92579705c0ff1a562b7cabc791c41b` (`main`).

The checkout already contained uncommitted documentation, dependency and generated-output changes before this iteration. They were inspected and preserved. Baseline commands were run on 2026-09-07 with Python 3.14.3 and pytest 9.0.2; Python 3.12 was installed but did not have the project dependencies.

| Issue | Evidence | Severity | Intended fix |
|---|---|---:|---|
| Period is only a label | `recipes/btw_return.yml` passes `period` only to exporters/rendering; all ten demo rows reach `summarize`. | P0 | Parse `Qn-YYYY`, filter normalized dates inclusively, and fail on invalid or empty periods. |
| BTW recipe does not calculate VAT | The recipe never calls `tools.analysis.tax.compute_vat` and supplies fixed `kor_applied: true` and zero VAT metadata. | P0 | Call the existing tax module explicitly and export its deterministic demonstration result. |
| Failed validation is reported as a successful step | `validate_dataframe` returns `{"valid": false}`; the controller classifies any returned dict as `OK`. | P0 | Give validation reports gate semantics: mandatory invalid results stop downstream steps and fail the run. |
| Validator and data boundary disagree | The loader returns normalized columns (`date`, `description`, `amount_gross`, `vat_rate`, `category`), while `kaggle_grocery_v1` validation expects raw source columns. | P0 | Split raw CSV loading from normalization and validate the raw schema before normalization. |
| CLI masks controller failure | `run_cli` returns `0` for every dict result, including `FAILED` and `PARTIAL_SUCCESS`. | P0 | Map only `OK` to exit 0; invalid input, validation and execution failures return non-zero. |
| Fallback reports work that never ran | With `rich` unavailable, `python main.py --recipe recipes/test_load.yml` printed `status: OK` and “no business logic executed”, exit 0. The documented BTW command rejected `--params` and exited 2. | P0 | Remove the success fallback and make dependency/import failure explicit and non-zero. |
| Money leaks binary floating-point artifacts | The recorded demo summary contains `42.269999999999996`. | P1 | Keep float inside pandas, but apply documented Decimal half-up rounding at the reporting boundary. |
| Baseline tests are narrow and currently environment-sensitive | Eight tests exist. On Python 3.14.3 with an explicit local base temp: 5 passed, 2 failed, 1 error. Failures include pandas `StringDtype` passed to `np.issubdtype`; the error is a denied pytest temp directory. Plain `pytest -q` also collects inaccessible `pytest-cache-files-*`. | P1 | Use pandas dtype predicates, add behavioral and end-to-end tests, and ignore runtime/cache directories. |
| Controller dependency/continuation behavior is not tested | No controller or CLI tests exist; no assertions cover downstream stopping, `continue_on_error`, final status or logs. | P1 | Add focused controller, CLI, artifact and NDJSON tests. |
| KOR is an oversimplified threshold switch | `_kor_applies` compares the supplied total with a configured threshold and `compute_vat` zeroes VAT. It does not establish eligibility or annual-turnover completeness. | P1 | Preserve it only as an explicitly invoked demonstration contract; do not apply or advertise it as tax advice in the main workflow. |
| Generic agent functionality is unfinished | Controller agent steps return a successful `NOOP`; `orchestrator/router.py` returns `NOT_IMPLEMENTED`; the natural-language path is regex/input based, not LLM-backed. | P1 | Keep stubs outside the advertised workflow, avoid successful NOOP semantics, and document them as non-functional. |
| CI checks only Python 3.11 | `.github/workflows/ci.yml` installs dependencies and runs `pytest -q` on one interpreter. Hosted status was not verified as part of baseline. | P1 | Test clean installation and pytest on Python 3.11 and 3.12, then verify hosted Actions after push. |
| Repository tracks local/generated artifacts | `git ls-files` includes `.idea/`, multiple `__pycache__/*.pyc`, many `workspace/logs` and `workspace/errors`, output summaries and a generated project tree. | P2 | Add a root `.gitignore` and remove local/runtime artifacts from version control without rewriting history. |
| Documentation overstates capability at baseline commit | The committed README claims a full test suite, BTW-ready output, business suitability and VAT workflow behavior not exercised by its recipe. | P2 | Rewrite documentation after implementation with reproducible commands, evidence and explicit limits. |

## Target workflow contract

The main workflow accepts an included or user-supplied CSV in the documented `kaggle_grocery_v1` source schema. It loads raw rows, validates required source fields, normalizes them to the internal schema, filters an inclusive calendar quarter, summarizes the selected transactions, applies only the explicitly configured demonstration VAT calculation, writes JSON/Markdown artifacts and an NDJSON step log, and returns a machine-readable final status.

Validation occurs before normalization because the named schema describes source column names. Missing columns and malformed values are input failures, not successful informational results. An invalid mandatory validation report stops dependent work by default. A recipe may opt into continuation explicitly; the final status must still expose that a step failed.

Internal monetary calculation may use pandas floating-point values. Values crossing the JSON/Markdown reporting boundary are rounded to two decimal places using an explicit decimal half-up policy.

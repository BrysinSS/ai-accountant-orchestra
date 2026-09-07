# Developer overview

The project is intentionally a small deterministic recipe runner, not a bookkeeping platform.

The stable public entry points are `orchestrator.controller.run_recipe`, `tools.data_io.loader.load_dataframe` and the CLI in `main.py`. The main recipe composes smaller source-loading, validation, normalization, quarter filtering, summary, VAT demonstration and export functions.

Recipes are ordered YAML definitions. A result can be referenced by later steps through `${steps.<name>.result}`. Function imports are dynamic, which keeps the engine small but means recipes must be trusted.

When extending the workflow:

- define the input/output contract of a small function;
- fail with a clear exception for unusable input;
- use a validation report only for a genuine validation boundary;
- add a behavioral test that names the guarantee;
- keep runtime output under `workspace/`;
- do not add an agent/LLM claim until executable behavior and tests exist.

See [ARCHITECTURE.md](ARCHITECTURE.md) for status, dependency and logging semantics.

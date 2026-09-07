# Run in PyCharm

1. Open the repository root as a project.
2. Create or select a Python 3.11/3.12 virtual environment.
3. In that environment, run `python -m pip install -r requirements.txt`.
4. Create a Python run configuration with script `main.py`, working directory set to the repository root, and parameters `--recipe recipes/test_load.yml`.
5. Run it and inspect the reported DataFrame shape and NDJSON log.

For the summary demonstration, use:

```text
--recipe recipes/btw_return.yml --params period=Q3-2025
```

The output files are `workspace/summary_latest.json` and `workspace/summary_latest.md`. This recipe labels the report with the supplied period but does not filter transactions or calculate VAT.

Check `python -c "from ui.cli import main"` if the entry point uses its skeleton fallback. A skeleton success message does not establish that processing happened.

Run tests with `python -m pytest -q`. See [the README](../README.md) for input/output examples, validation limitations and CI evidence.






# PyCharm quick start

1. Open the repository root.
2. Create a Python 3.11 or 3.12 virtual environment.
3. Install with `python -m pip install -r requirements.txt`.
4. Create a Python configuration for `main.py` with repository root as the working directory.
5. Use parameters `--recipe recipes/btw_return.yml --params period=Q3-2024`.

The process should exit `0` and create `workspace/summary_latest.json`, `workspace/summary_latest.md` and a timestamped `workspace/logs/*.ndjson` file.

For a failure check, use `period=Q2-2023`; the process should exit `1` and create a JSON error artifact under `workspace/errors/`.

Run tests with `python -m pytest -q`. Runtime and IDE files are ignored by Git.

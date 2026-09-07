# Engineering evidence

Verification date: 2026-09-08 (Europe/Amsterdam).

## Local verification

- Tested commit: `3eeb26a` (documentation commit over the completed code and CI configuration).
- Clean environment: Python 3.12.10 virtual environment created outside the repository.
- Installation: `python -m pip install -r requirements.txt` completed from the declared file.
- Pytest: 9.1.1.
- Exact result: 36 collected, 36 passed, 0 skipped, 0 failed, 0 errors.
- Additional environment: Python 3.14.3 / pytest 9.0.2 also produced 36 passed, but 3.14 is not part of the declared CI matrix.

## End-to-end scenario

Command:

```bash
python main.py --recipe recipes/btw_return.yml --params period=Q3-2024
```

Observed result: exit 0; 10 raw rows validated, 4 rows selected, gross 5.90, demonstration VAT 0.49, net 5.41; JSON, Markdown and an eight-step NDJSON log were written and parsed successfully.

Intentional failure:

```bash
python main.py --recipe recipes/btw_return.yml --params period=Q2-2023
```

Observed result: exit 1 at `filter_period`; a failure JSON and failed NDJSON step were written; summary/VAT/export did not run.

## CI

The workflow is configured for clean installation and pytest on Python 3.11 and 3.12. Hosted GitHub Actions status is pending push at the time of this evidence commit and is not represented as green yet.

## Known limitations

- VAT arithmetic is a configured demonstration, not tax compliance or filing output.
- KOR is a simplified opt-in threshold switch and is disabled in the main recipe.
- The documented workflow is verified with CSV; other loader formats are outside the end-to-end evidence.
- Dynamic recipe imports require trusted recipes.
- Agent/LLM scaffolding is not implemented or advertised as a working capability.

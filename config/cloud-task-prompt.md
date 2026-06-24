Use $daily-gadget-scout to run the daily product scouting workflow for YUMIUNIQ.

Run mode: dry-run unless WeCom configuration is explicitly provided in the task.

Cloud setup:
- Before running tests or the CLI, ensure the package is installed with `python -m pip install -e ".[test]"`.
- This repository uses a `src/` layout; `python -m gadget_scout.cli` may fail before editable install.

Rules:
- Use Codex to analyze, classify, score, and summarize products. Do not require OPENAI_API_KEY or any external model provider key.
- Scout both domestic and overseas sources if agent internet access allows them.
- Split candidates into domestic and overseas pools before final ranking.
- Score domestic and overseas candidates independently.
- Select at most 10 domestic items and at most 10 overseas items.
- Select fewer in either pool when fewer candidates meet the quality bar.
- Do not enforce a fixed `未来好物` / `趋势好物` ratio.
- Do not write to WeCom smart sheets and do not send WeCom bot messages unless live WeCom config is present and the task explicitly asks for live output.
- Produce a Codex report with domestic selected count, overseas selected count, candidate summaries, scoring rationale, skipped sources, missing configuration, and the combined briefing text that would be sent later.
- Do not include `负责人` in any proposed sheet fields.
- Do not create a PR, commit changes, or leave generated dry-run artifacts in the repository.
- For fixture-only dry runs, write generated files outside the repo, for example `/tmp/gadget-scout-runs`, then report their paths and relevant contents.
- If live source access is unavailable, run `python -m gadget_scout.cli --fixtures tests/fixtures/candidates.json --out /tmp/gadget-scout-runs --run-date $(date +%F)` and clearly say the run used local fixtures.

Before finishing:
- Run `python -m pip install -e ".[test]"`.
- Run `python -m pytest -q`.
- Run `git status --short` and confirm no repository files were changed for a dry run.
- Include whether tests passed.
- Include whether live source access was available.

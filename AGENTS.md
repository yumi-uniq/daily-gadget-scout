# AGENTS.md

## Project Purpose

This repo contains the cloud-ready scaffold for YUMIUNIQ's daily gadget scouting workflow. Codex should use the `daily-gadget-scout` skill to collect, classify, score, and summarize domestic and overseas high-potential electronic products.

## Key Rules

- Use Codex for analysis. Do not require `OPENAI_API_KEY` for the Codex cloud route.
- Split candidates into `domestic` and `overseas` pools before final ranking.
- Score domestic and overseas candidates independently.
- Select at most 10 domestic items and at most 10 overseas items.
- Select fewer when candidates do not meet the quality bar.
- Do not enforce a fixed `未来好物` / `趋势好物` ratio.
- Do not include `负责人` in WeCom smart sheet fields.
- Do not write to WeCom or send bot messages unless the target docid, sheet_id, and chat/webhook are configured and the task explicitly asks for live output.
- For dry runs, do not create a PR, commit changes, or leave generated artifacts in the repository.
- Write dry-run outputs outside the repository, such as `/tmp/gadget-scout-runs`, unless the user explicitly asks to persist outputs in the repo.

## Setup

Use this setup command in Codex Cloud environments:

```bash
bash scripts/codex-cloud-setup.sh
```

Equivalent direct setup:

```bash
python -m pip install --upgrade pip
python -m pip install -e ".[test]"
```

## Verification

Run:

```bash
python -m pytest -q
```

Expected:

```text
16 passed
```

## Dry Run

Run:

```bash
python -m pip install -e ".[test]"
python -m gadget_scout.cli --fixtures tests/fixtures/candidates.json --out /tmp/gadget-scout-runs --run-date 2026-06-24
```

Expected output includes:

```text
domestic_selected_count=1
overseas_selected_count=2
```

## Important Files

- `config/cloud-task-prompt.md`: prompt for a Codex Cloud dry run or production run.
- `config/agent-internet-allowlist.md`: suggested domains for agent internet access.
- `config/sources.json`: first-pass domestic and overseas source allowlist.
- `src/gadget_scout/`: deterministic dry-run harness and WeCom-ready formatting.
- `tests/`: regression tests for scoring, selection, briefing, and WeCom schema.

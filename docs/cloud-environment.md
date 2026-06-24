# Codex Cloud Environment Setup

## Goal

Run the daily gadget scout in Codex Cloud so it can work while the local computer is off.

## Repository

Codex Cloud needs a GitHub repository it can checkout. This local project must be pushed to GitHub before creating the environment.

## Environment Setup Script

Use:

```bash
bash scripts/codex-cloud-setup.sh
```

This installs the package in editable mode with test dependencies.

## Verification Command

```bash
python -m pytest -q
```

Expected:

```text
16 passed
```

## Dry Run Task Prompt

Use `config/cloud-task-prompt.md`.

## Internet Access

For fixture dry runs, keep agent internet access off.

## Dry-Run Behavior

Cloud dry runs should not create a PR, commit changes, or leave generated
artifacts in the repository diff. Use a temporary output directory:

```bash
python -m pip install -e ".[test]"
python -m pytest -q
python -m gadget_scout.cli --fixtures tests/fixtures/candidates.json --out /tmp/gadget-scout-runs --run-date "$(date +%F)"
git status --short
```

`git status --short` should be empty for a fixture dry run. Report the generated
file paths and briefing content from `/tmp/gadget-scout-runs` in the Codex
answer instead of committing them.

For live scouting, enable agent internet access with:

- Domain allowlist from `config/agent-internet-allowlist.md`
- Methods: `GET`, `HEAD`, `OPTIONS`

## Live WeCom Output

Do not enable live WeCom writes until these are configured:

- Domestic smart sheet docid and sheet_id
- Overseas smart sheet docid and sheet_id
- WeCom bot or message target
- A reviewed production prompt that explicitly allows live writes

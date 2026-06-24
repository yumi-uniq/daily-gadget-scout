Use $daily-gadget-scout to run the daily product scouting workflow for YUMIUNIQ.

Run mode: production-run unless required configuration is missing.

Rules:
- Use Codex to analyze, classify, score, and summarize products. Do not require OPENAI_API_KEY or any external model provider key.
- Scout both domestic and overseas sources.
- Split candidates into domestic and overseas pools before final ranking.
- Score domestic and overseas candidates independently.
- Select at most 10 domestic items and at most 10 overseas items.
- Select fewer in either pool when fewer candidates meet the quality bar.
- Do not enforce a fixed `未来好物` / `趋势好物` ratio.
- Write domestic selected records to the domestic WeCom smart sheet.
- Write overseas selected records to the overseas WeCom smart sheet.
- Send one combined WeCom briefing with `国内 Top` and `海外 Top` sections.
- Do not include `负责人` in either smart sheet.
- If WeCom smart sheet IDs, bot target, or source access are missing, do not perform live writes; produce a clear configuration-missing report instead.
- Do not send external messages or modify production data unless the target sheet/chat/webhook is configured.

Expected report:
- Domestic selected count.
- Overseas selected count.
- Items written to each smart sheet, or the exact missing configuration that prevented writing.
- Combined WeCom briefing text, or the exact missing configuration that prevented sending.
- Source failures and skipped candidates.

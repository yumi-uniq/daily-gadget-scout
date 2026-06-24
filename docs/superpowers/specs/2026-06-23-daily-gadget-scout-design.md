# Daily Gadget Scout Design

## Purpose

Build a Codex skill and Codex automation workflow that scouts unusual, high-potential electronic products every morning for a hybrid offline showroom and online electronic lifestyle product business.

The system should support two different business needs without forcing a fixed split:

- Content discovery: novel products, prototypes, concepts, or early signals that can create curiosity, discussion, and showroom storytelling.
- Business development: mature or near-mature products that are suitable for sourcing, supply-chain follow-up, brand partnership, or exhibition/showroom cooperation.

The daily output must be selective. It should maintain separate domestic and overseas result pools. Each pool can recommend at most 10 high-quality items per run, and fewer when the available candidates are weak. The WeCom briefing is still one combined message.

## Positioning Context

YUMIUNIQ is positioned as an offline showroom plus online electronic trend-product experience store. The reference positioning is similar to INNO100: an offline filter and amplification space for innovative hardware, future lifestyle products, and consumer electronics.

The scout should therefore optimize for products that are not merely "new", but useful for one of these outcomes:

- Build market education and curiosity.
- Help the team find early trend signals.
- Identify products worth sourcing or sampling.
- Identify brands or projects worth inviting into the showroom.

## Scope

### In Scope For 1.0

- Daily Codex automation execution at 08:00 China/Singapore time.
- International and domestic product/source collection.
- Candidate extraction from public web pages, RSS feeds, official APIs where available, newsletters, and structured source pages.
- Product classification into `未来好物`, `趋势好物`, or `观察池`.
- Recommendation action classification:
  - `内容优先`
  - `供应链推进`
  - `展厅合作`
  - `观察池`
  - `暂不推荐`
- Scoring, deduplication, and evidence capture.
- Writing domestic selected items into a domestic WeCom smart sheet.
- Writing overseas selected items into an overseas WeCom smart sheet.
- Sending one combined WeCom bot briefing after both pools finish.
- Limiting each pool to no more than 10 selected items.

### Out Of Scope For 1.0

- Deep social-media crawling from Xiaohongshu, Douyin, Bilibili, X, TikTok, Instagram, YouTube, Reddit, or Weibo.
- Anti-bot bypassing.
- Paid data acquisition.
- Automated purchasing, supplier outreach, or external message sending.
- Fully autonomous brand negotiation.

Social-media discovery belongs in 2.0 because data access, authentication, anti-scraping behavior, and compliance risk are more complex.

## Recommended Implementation Direction

Use the "scoring database" approach:

1. Cloud scheduler triggers a daily run.
2. Collectors fetch source pages and feeds.
3. The pipeline normalizes candidates into a shared product schema.
4. A deduper checks source URL, product name, brand, canonical domain, and semantic similarity.
5. Split candidates into domestic and overseas pools.
6. A scoring step ranks each pool independently by novelty, evidence, commercial value, content value, and showroom fit.
7. Qualified domestic items are written to the domestic WeCom smart sheet.
8. Qualified overseas items are written to the overseas WeCom smart sheet.
9. A WeCom bot sends one concise combined daily briefing.

This is more robust than a lightweight one-shot digest because it can accumulate source reliability, avoid repeated products, and support trend tracking.

## Codex Automation Runtime

### Recommended 1.0 Runtime

Use Codex App cron automation with `executionEnvironment=worktree` first.

Reasons:

- It keeps Codex as the analysis engine using the `daily-gadget-scout` skill.
- It does not require an external `OPENAI_API_KEY`.
- It can wake Codex on a schedule and run a self-contained prompt against the workspace.
- It avoids turning the skill into a separate model-calling service.

Schedule:

```text
FREQ=DAILY;BYHOUR=8;BYMINUTE=0;BYSECOND=0
```

Interpret the requested wall-clock time in the user's locale. The target time is 08:00 Asia/Singapore / China time.

### Alternate Runtime

Use GitHub Actions, Cloudflare Workers, AWS EventBridge + Lambda, or a small VPS only if the team later decides to run an independent non-Codex service. That alternate route would require a model provider API key if the service performs LLM analysis without Codex.

Consider an alternate runtime when the workflow needs:

- More stable browser rendering.
- Long-running crawls.
- Proxy or queue management.
- More frequent runs.
- Stateful dashboards.
- Social-media collectors.

## Candidate Sources

### International 1.0 Sources

- Kickstarter technology/design discovery pages.
- Indiegogo technology/design discovery pages.
- Crowd Supply.
- Product Hunt.
- Hackaday and Hackaday.io.
- TechCrunch hardware/AI/gadget coverage.
- Wired Gear.
- The Verge.
- Engadget.
- New Atlas.
- Yanko Design.
- Designboom technology/design product posts.

### Domestic 1.0 Sources

- 36氪.
- 极客公园.
- 爱范儿 / 玩物志.
- 少数派.
- IT之家.
- 快科技.
- 雷科技.
- 品玩.
- 机器之心.
- 量子位.
- ZEALER where useful.

### 2.0 Social Sources

- Xiaohongshu.
- Douyin.
- Bilibili.
- Weibo.
- 即刻.
- X.
- TikTok.
- Instagram.
- YouTube.
- Reddit.

2.0 should use official APIs, approved connectors, manual export, monitored accounts, or compliant data providers where possible.

## Product Classification

### 未来好物

Products, prototypes, technologies, concepts, or crowdfunding-stage projects that may shape future lifestyles or consumer electronics 3-5 years out.

Typical signals:

- Concept, prototype, lab technology, design fiction, research commercialization, pre-order, or early crowdfunding.
- High novelty or imagination.
- Strong content and discussion value.
- Weak or uncertain immediate supply-chain readiness.

### 趋势好物

Products that are already launched, near launch, or backed by early market data, and may become commercially useful within 6-18 months.

Typical signals:

- Existing product page, preorder, crowdfunding delivery plan, early sales, reviews, or reseller availability.
- Clear user problem and buyer segment.
- Potential gross margin or sourcing feasibility.
- Useful in showroom demos or retail curation.

### 观察池

Interesting candidates with insufficient evidence, unclear product status, weak differentiation, or unresolved risk.

Observation candidates should be stored only when they may become useful later. They should not appear in the daily Top items unless there is a specific reason to mention a trend signal.

## Recommendation Actions

Every selected product must receive one primary recommendation action.

| Action | Meaning |
|---|---|
| `内容优先` | Strong novelty, story, or visual/demo potential. Suitable for posts, videos, newsletters, showroom explanation, or industry discussion. Not ready for sourcing follow-up yet. |
| `供应链推进` | Product is mature enough to find suppliers, request samples, evaluate price/margin, or investigate distribution rights. |
| `展厅合作` | Brand/project has strong commercial or positioning value. Suitable for showroom residency, co-exhibition, launch event, pop-up, partnership, or exclusive display discussion. |
| `观察池` | Worth tracking but not strong enough for action today. |
| `暂不推荐` | Too noisy, too similar, too risky, too weakly evidenced, or outside the target category. Usually not written to the daily Top sheet. |

## Scoring Model

Use a 100-point total score. Domestic and overseas candidates are scored and ranked in separate pools. Only candidates above the relevant pool threshold can enter the daily briefing.

Recommended default threshold:

- `75+`: eligible for daily Top items.
- `65-74`: observation only unless strategically important.
- `<65`: discard or keep only in raw logs.

Scoring dimensions:

| Dimension | Points | Notes |
|---|---:|---|
| Novelty | 20 | How new, surprising, differentiated, or conversation-worthy it is. |
| Product-market relevance | 15 | Fit with YUMIUNIQ's electronic trend-product positioning and audience. |
| Evidence strength | 15 | Product page, prototype media, founder/team, funding data, reviews, preorder, delivery timeline, or credible media coverage. |
| Content value | 15 | Visual appeal, explainability, short-video potential, discussion value, demo value. |
| Commercial value | 15 | Pricing potential, margin, sourcing feasibility, buyer clarity, near-term demand. |
| Showroom fit | 10 | Whether it can create hands-on experience, event value, or display value. |
| Trend signal | 10 | Whether it represents a broader technology, lifestyle, or category trend. |

Risk deductions:

- `-5` to `-20` for likely vaporware, unclear claims, weak evidence, severe delivery risk, excessive similarity, or poor category fit.
- `-5` to `-15` for inaccessible source details, suspicious marketing claims, or missing product status.

## Selection Rules

- Do not enforce a fixed ratio between `未来好物` and `趋势好物`.
- Rank candidates by total score and actionability.
- Split candidates into `domestic` and `overseas` pools before final ranking.
- Select at most 10 domestic daily Top items.
- Select at most 10 overseas daily Top items.
- Select fewer than 10 in either pool when fewer items meet that pool's threshold.
- Do not compare domestic and overseas candidates against each other for final slots.
- If neither pool has qualifying candidates, send a brief "今日无高置信推荐" message with optional trend observations.
- Prefer diversity when scores are close: avoid filling the whole briefing with near-identical AI pins, headphones, robots, chargers, keyboards, or projectors.
- Avoid repeated products already sent recently unless there is a meaningful update.

## WeCom Smart Sheet Schema

Remove the `负责人` field.

Use two WeCom smart sheets with the same schema:

- Domestic product sheet: records domestic candidates and domestic scores.
- Overseas product sheet: records overseas candidates and overseas scores.

Recommended columns for both sheets:

| Field | Type | Notes |
|---|---|---|
| 日期 | date/text | Run date. |
| 分类 | single select | `未来好物`, `趋势好物`, `观察池`. |
| 产品名 | text | Product or project name. |
| 一句话亮点 | text | One-line hook. |
| 来源链接 | URL/text | Canonical source URL. |
| 国家/地区 | text/select | Origin or market. |
| 来源区域 | single select | `国内` or `海外`. |
| 产品阶段 | single select | Concept, prototype, crowdfunding, preorder, launched, shipping, unknown. |
| 预计上市时间 | text/date | Use text when uncertain. |
| 品类 | single/multi select | Wearable, AI device, robot, audio, smart home, mobility, maker tool, etc. |
| 目标人群 | text | Likely buyer/user segment. |
| 为什么新奇 | long text | Novelty explanation. |
| 为什么可能火 | long text | Trend/commercial/content reason. |
| 关键证据 | long text | Funding, comments, reviews, launch date, media coverage, specs, preorder evidence. |
| 商业判断 | long text | Sourcing, margin, partnership, or retail view. |
| 展厅适配建议 | long text | How to display, demo, or activate in showroom. |
| 风险 | long text | Delivery, price, copycat, evidence, compliance, safety, or category risk. |
| 综合分 | number | 0-100. |
| 推荐动作 | single select | `内容优先`, `供应链推进`, `展厅合作`, `观察池`, `暂不推荐`. |
| 去重ID | text | Stable ID generated from normalized product name + brand/domain. |

## Daily WeCom Bot Briefing

The bot should send one compact combined message after both smart sheets are updated.

Recommended format:

```text
今日好物雷达 YYYY-MM-DD

国内入选 X 个，海外入选 Y 个。

国内 Top

1. 产品名｜推荐动作｜综合分
一句话亮点
为什么值得看：...
下一步建议：...
链接：...

海外 Top

1. 产品名｜推荐动作｜综合分
一句话亮点
为什么值得看：...
下一步建议：...
链接：...

今日信号：
- ...
```

When no item qualifies:

```text
今日好物雷达 YYYY-MM-DD

今日无高置信推荐，未强行凑数。

观察到的弱信号：
- ...
```

## Skill Behavior

The `daily-gadget-scout` skill should guide Codex through the workflow when the user asks to scout, review, or build daily good-product discovery.

The skill should instruct the agent to:

1. Confirm the run mode: design/spec, dry run, production run, or source expansion.
2. Load source configuration.
3. Fetch candidates from configured sources.
4. Normalize products into the shared schema.
5. Assign each candidate to `domestic` or `overseas`.
6. Deduplicate against recent records within the appropriate pool.
7. Score and classify each candidate inside its pool.
8. Select at most 10 domestic high-quality Top items and at most 10 overseas high-quality Top items.
9. Write domestic results to the domestic WeCom smart sheet and overseas results to the overseas WeCom smart sheet if credentials and target sheets are configured.
10. Send one combined WeCom bot briefing only after the user has configured and approved the target chat/webhook.
11. Produce a local markdown/JSON run report for auditability.

## Configuration

Secrets should not be hardcoded.

Expected configuration:

- `WECOM_DOMESTIC_SMARTSHEET_DOCID`.
- `WECOM_DOMESTIC_SMARTSHEET_SHEET_ID`.
- `WECOM_OVERSEAS_SMARTSHEET_DOCID`.
- `WECOM_OVERSEAS_SMARTSHEET_SHEET_ID`.
- `WECOM_BOT_WEBHOOK` or approved WeCom CLI message target.
- Optional source API tokens, such as Product Hunt token.
- Source allowlist and per-source rate limits.
- Minimum score threshold.
- Maximum daily domestic item count, default `10`.
- Maximum daily overseas item count, default `10`.
- Recency window, default `48h`.

## Error Handling

- If a source fails, log it and continue with other sources.
- If WeCom smart sheet write fails, save a local JSON/Markdown fallback report and send a degraded briefing if possible.
- If bot sending fails, keep the sheet write and local report.
- If LLM scoring fails for a candidate, skip or retry once.
- If all sources fail, send an operational failure message rather than a product briefing.
- If evidence is insufficient, classify the candidate as `观察池` or `暂不推荐`.

## Testing Strategy

### Unit Tests

- Product normalization.
- Deduplication ID generation.
- Score calculation and thresholding.
- Recommendation action mapping.
- Daily domestic Top selection with fewer than 10 qualified candidates.
- Daily overseas Top selection with fewer than 10 qualified candidates.
- Independent domestic and overseas ranking pools.
- No fixed category ratio between `未来好物` and `趋势好物`.

### Integration Tests

- Fetch a small fixture set from representative international and domestic sources.
- Run the ranking pipeline on fixture data.
- Write to a mock WeCom sheet adapter.
- Generate a bot briefing from selected items.

### Dry Run

Before production:

1. Run without writing to WeCom.
2. Save `runs/YYYY-MM-DD-dry-run.json`.
3. Review the Top items manually.
4. Tune thresholds and source weights.
5. Enable WeCom smart sheet write.
6. Enable WeCom bot briefing.

## Open Decisions Before Implementation

- Exact first-batch source allowlist.
- Whether the first production automation should be created as ACTIVE or PAUSED for review.
- Whether the two WeCom smart sheets already exist or should be created by the setup workflow.
- Which WeCom chat/bot receives the briefing.
- Whether Product Hunt or other API-token sources are approved for production use.
- Whether raw rejected candidates should be stored long term.

## References

- YUMIUNIQ: https://yumiuniq.com/
- INNO100 Shenzhen government reference: https://www.sz.gov.cn/en_szgov/business/news/content/post_12521227.html
- INNO100 36Kr reference: https://eu.36kr.com/en/p/3566873750977673
- Product Hunt API docs: https://api.producthunt.com/v2/docs

# Daily Gadget Scout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a reusable `daily-gadget-scout` Codex skill plus a Codex App worktree automation that wakes Codex daily, ranks domestic and overseas novel electronic products in separate pools, writes two WeCom-ready record sets, and prepares one combined daily briefing capped at 10 domestic items and 10 overseas items.

**Architecture:** Keep Codex as the analysis engine. The `daily-gadget-scout` skill defines how Codex collects, classifies, scores, and briefs products; the Codex App cron automation wakes Codex at 08:00 and runs a self-contained prompt against this workspace. The local Python dry-run pipeline remains a deterministic fixture harness for testing schema, selection, and briefing behavior, not the primary LLM analysis engine.

**Tech Stack:** Codex App cron automation, `daily-gadget-scout` Codex skill, Python 3.11+ fixture harness, pytest, dataclasses, standard library JSON helpers, Codex skill folder under `C:\Users\Administrator\.codex\skills\daily-gadget-scout`.

---

## Current Environment Notes

- Project root: `D:\AI Project\好物搜集agent`
- Approved design spec: `D:\AI Project\好物搜集agent\docs\superpowers\specs\2026-06-23-daily-gadget-scout-design.md`
- Current workspace is not a git repository. Any "Commit" step should first run `git status --short`; if it returns `fatal: not a git repository`, record "commit skipped because workspace is not a git repository" in the task notes and continue.
- The skill install target follows `skill-creator` default behavior because no alternate location was specified: `C:\Users\Administrator\.codex\skills\daily-gadget-scout`.

## File Structure

### Workspace Pipeline Files

- Create `D:\AI Project\好物搜集agent\pyproject.toml`: Python project metadata, pytest config, and dependencies.
- Create `D:\AI Project\好物搜集agent\src\gadget_scout\__init__.py`: package marker and version.
- Create `D:\AI Project\好物搜集agent\src\gadget_scout\models.py`: enums and dataclasses for source region, candidates, scores, and selected products.
- Create `D:\AI Project\好物搜集agent\src\gadget_scout\scoring.py`: deterministic scoring and recommendation action logic.
- Create `D:\AI Project\好物搜集agent\src\gadget_scout\dedupe.py`: canonical text and URL-based dedupe ID generation.
- Create `D:\AI Project\好物搜集agent\src\gadget_scout\selection.py`: thresholding, sorting, category diversity, and independent domestic/overseas max-10 selection.
- Create `D:\AI Project\好物搜集agent\src\gadget_scout\briefing.py`: daily WeCom bot briefing text generation.
- Create `D:\AI Project\好物搜集agent\src\gadget_scout\sources.py`: fixture loader and source adapter interface.
- Create `D:\AI Project\好物搜集agent\src\gadget_scout\wecom.py`: WeCom smart sheet record and bot payload builders.
- Create `D:\AI Project\好物搜集agent\src\gadget_scout\cli.py`: dry-run command line entrypoint.
- Create `D:\AI Project\好物搜集agent\config\sources.json`: first-pass source allowlist and metadata.
- Create `D:\AI Project\好物搜集agent\tests\fixtures\candidates.json`: deterministic sample candidates.
- Create `D:\AI Project\好物搜集agent\tests\test_scoring.py`: scoring/action tests.
- Create `D:\AI Project\好物搜集agent\tests\test_selection.py`: no fixed future/trend ratio, max-10-per-region, region split, and threshold tests.
- Create `D:\AI Project\好物搜集agent\tests\test_briefing.py`: briefing format tests.
- Create `D:\AI Project\好物搜集agent\tests\test_wecom.py`: WeCom payload/schema mapping tests.
- Create `D:\AI Project\好物搜集agent\tests\test_cli.py`: dry-run output smoke test.
- Create a PAUSED Codex App cron automation: 08:00 China/Singapore scheduled Codex worktree job.

### Codex Skill Files

- Create `C:\Users\Administrator\.codex\skills\daily-gadget-scout\SKILL.md`: concise agent-facing workflow and trigger metadata.
- Create `C:\Users\Administrator\.codex\skills\daily-gadget-scout\references\scouting-rules.md`: scoring, classification, and recommendation action rules.
- Create `C:\Users\Administrator\.codex\skills\daily-gadget-scout\references\sources.md`: 1.0 and 2.0 source guidance.
- Create `C:\Users\Administrator\.codex\skills\daily-gadget-scout\references\wecom-output.md`: two-sheet WeCom schema and combined bot briefing rules.
- Create `C:\Users\Administrator\.codex\skills\daily-gadget-scout\agents\openai.yaml`: UI metadata.

---

### Task 1: Project Skeleton And Test Harness

**Files:**
- Create: `D:\AI Project\好物搜集agent\pyproject.toml`
- Create: `D:\AI Project\好物搜集agent\src\gadget_scout\__init__.py`
- Create: `D:\AI Project\好物搜集agent\tests\fixtures\candidates.json`

- [ ] **Step 1: Create the Python project metadata**

Create `D:\AI Project\好物搜集agent\pyproject.toml` with this exact content:

```toml
[build-system]
requires = ["setuptools>=69"]
build-backend = "setuptools.build_meta"

[project]
name = "gadget-scout"
version = "0.1.0"
description = "Daily scout pipeline for novel electronic products."
requires-python = ">=3.11"
dependencies = []

[project.optional-dependencies]
test = ["pytest>=8.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["src"]
addopts = "-q"
```

- [ ] **Step 2: Create the package marker**

Create `D:\AI Project\好物搜集agent\src\gadget_scout\__init__.py`:

```python
"""Daily gadget scouting pipeline."""

__version__ = "0.1.0"
```

- [ ] **Step 3: Create fixture candidates**

Create `D:\AI Project\好物搜集agent\tests\fixtures\candidates.json`:

```json
[
  {
    "source_name": "Kickstarter",
    "source_region": "overseas",
    "source_url": "https://www.kickstarter.com/projects/example/smart-ring-lab",
    "product_name": "Smart Ring Lab",
    "highlight": "A health and gesture smart ring with prototype demos.",
    "country_region": "United States",
    "stage": "crowdfunding",
    "product_category": ["wearable", "ai-device"],
    "target_audience": "Tech-forward wellness consumers",
    "novelty_reason": "Combines health sensing with gesture controls in a ring-sized form.",
    "trend_reason": "Wearable AI interfaces are moving beyond watches and phones.",
    "evidence": ["Prototype video", "Crowdfunding page", "Founder update"],
    "commercial_judgment": "Good for content first; sourcing needs delivery proof.",
    "showroom_fit": "Can be explained through gesture demos and future interface storytelling.",
    "risks": ["Delivery timeline is uncertain"],
    "raw_score_signals": {
      "novelty": 18,
      "product_market_relevance": 14,
      "evidence_strength": 11,
      "content_value": 15,
      "commercial_value": 9,
      "showroom_fit": 8,
      "trend_signal": 10,
      "risk_penalty": 5
    }
  },
  {
    "source_name": "36氪",
    "source_region": "domestic",
    "source_url": "https://www.36kr.com/p/example-ai-projector",
    "product_name": "AI Pocket Projector",
    "highlight": "A portable projector with built-in scene-aware AI setup.",
    "country_region": "China",
    "stage": "launched",
    "product_category": ["projector", "smart-home"],
    "target_audience": "Young renters and small-space entertainment users",
    "novelty_reason": "Uses AI calibration to reduce setup friction.",
    "trend_reason": "Portable home entertainment devices are becoming lifestyle objects.",
    "evidence": ["Media report", "Retail availability", "Brand product page"],
    "commercial_judgment": "Mature enough to request sample pricing and distributor terms.",
    "showroom_fit": "Strong demo fit for small-room lifestyle scenes.",
    "risks": ["Projector category is crowded"],
    "raw_score_signals": {
      "novelty": 13,
      "product_market_relevance": 15,
      "evidence_strength": 14,
      "content_value": 12,
      "commercial_value": 14,
      "showroom_fit": 9,
      "trend_signal": 8,
      "risk_penalty": 3
    }
  },
  {
    "source_name": "The Verge",
    "source_region": "overseas",
    "source_url": "https://www.theverge.com/example/desktop-robot",
    "product_name": "DeskBot Companion",
    "highlight": "A desktop robot designed for ambient AI companionship.",
    "country_region": "Japan",
    "stage": "preorder",
    "product_category": ["robot", "ai-device"],
    "target_audience": "Design-led gadget buyers",
    "novelty_reason": "Turns AI companionship into a physical desk object.",
    "trend_reason": "Embodied AI is becoming a visible consumer electronics trend.",
    "evidence": ["Preorder page", "Hands-on article", "Demo video"],
    "commercial_judgment": "Potential showroom partnership candidate if brand is open to launch displays.",
    "showroom_fit": "Excellent interaction value for visitors.",
    "risks": ["Price may be high"],
    "raw_score_signals": {
      "novelty": 19,
      "product_market_relevance": 15,
      "evidence_strength": 13,
      "content_value": 15,
      "commercial_value": 13,
      "showroom_fit": 10,
      "trend_signal": 10,
      "risk_penalty": 4
    }
  }
]
```

- [ ] **Step 4: Run the empty test suite**

Run:

```powershell
python -m pytest
```

Expected output:

```text
no tests ran
```

- [ ] **Step 5: Commit or record skip**

Run:

```powershell
git status --short
```

Expected in current workspace:

```text
fatal: not a git repository (or any of the parent directories): .git
```

Record: `commit skipped because workspace is not a git repository`.

---

### Task 2: Domain Models And Scoring

**Files:**
- Create: `D:\AI Project\好物搜集agent\src\gadget_scout\models.py`
- Create: `D:\AI Project\好物搜集agent\src\gadget_scout\scoring.py`
- Create: `D:\AI Project\好物搜集agent\tests\test_scoring.py`

- [ ] **Step 1: Write the failing scoring tests**

Create `D:\AI Project\好物搜集agent\tests\test_scoring.py`:

```python
from gadget_scout.models import ProductStage, RecommendationAction
from gadget_scout.scoring import classify_candidate, score_candidate
from gadget_scout.sources import load_fixture_candidates


def test_score_candidate_uses_weighted_signals():
    candidate = load_fixture_candidates("tests/fixtures/candidates.json")[0]

    score = score_candidate(candidate)

    assert score.total == 80
    assert score.novelty == 18
    assert score.risk_penalty == 5


def test_content_action_for_high_novelty_crowdfunding_item():
    candidate = load_fixture_candidates("tests/fixtures/candidates.json")[0]
    score = score_candidate(candidate)

    classification, action = classify_candidate(candidate, score)

    assert classification == "未来好物"
    assert action == RecommendationAction.CONTENT_FIRST


def test_supply_chain_action_for_mature_commercial_item():
    candidate = load_fixture_candidates("tests/fixtures/candidates.json")[1]
    score = score_candidate(candidate)

    classification, action = classify_candidate(candidate, score)

    assert candidate.stage == ProductStage.LAUNCHED
    assert classification == "趋势好物"
    assert action == RecommendationAction.SUPPLY_CHAIN


def test_showroom_partnership_action_for_high_showroom_fit():
    candidate = load_fixture_candidates("tests/fixtures/candidates.json")[2]
    score = score_candidate(candidate)

    classification, action = classify_candidate(candidate, score)

    assert classification == "趋势好物"
    assert action == RecommendationAction.SHOWROOM_PARTNERSHIP
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_scoring.py -q
```

Expected: FAIL with import errors for `gadget_scout.models`, `gadget_scout.scoring`, or `gadget_scout.sources`.

- [ ] **Step 3: Create domain models**

Create `D:\AI Project\好物搜集agent\src\gadget_scout\models.py`:

```python
from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ProductStage(StrEnum):
    CONCEPT = "concept"
    PROTOTYPE = "prototype"
    CROWDFUNDING = "crowdfunding"
    PREORDER = "preorder"
    LAUNCHED = "launched"
    SHIPPING = "shipping"
    UNKNOWN = "unknown"


class SourceRegion(StrEnum):
    DOMESTIC = "domestic"
    OVERSEAS = "overseas"


class ScoutCategory(StrEnum):
    FUTURE = "未来好物"
    TREND = "趋势好物"
    WATCHLIST = "观察池"


class RecommendationAction(StrEnum):
    CONTENT_FIRST = "内容优先"
    SUPPLY_CHAIN = "供应链推进"
    SHOWROOM_PARTNERSHIP = "展厅合作"
    WATCHLIST = "观察池"
    NOT_RECOMMENDED = "暂不推荐"


@dataclass(frozen=True)
class CandidateProduct:
    source_name: str
    source_region: SourceRegion
    source_url: str
    product_name: str
    highlight: str
    country_region: str
    stage: ProductStage
    product_category: list[str]
    target_audience: str
    novelty_reason: str
    trend_reason: str
    evidence: list[str]
    commercial_judgment: str
    showroom_fit: str
    risks: list[str]
    raw_score_signals: dict[str, int] = field(default_factory=dict)


@dataclass(frozen=True)
class ScoreBreakdown:
    novelty: int
    product_market_relevance: int
    evidence_strength: int
    content_value: int
    commercial_value: int
    showroom_fit: int
    trend_signal: int
    risk_penalty: int

    @property
    def total(self) -> int:
        gross = (
            self.novelty
            + self.product_market_relevance
            + self.evidence_strength
            + self.content_value
            + self.commercial_value
            + self.showroom_fit
            + self.trend_signal
        )
        return max(0, min(100, gross - self.risk_penalty))


@dataclass(frozen=True)
class SelectedProduct:
    candidate: CandidateProduct
    classification: ScoutCategory
    recommendation_action: RecommendationAction
    score: ScoreBreakdown
    dedupe_id: str
```

- [ ] **Step 4: Create fixture loader needed by tests**

Create `D:\AI Project\好物搜集agent\src\gadget_scout\sources.py`:

```python
from __future__ import annotations

import json
from pathlib import Path

from gadget_scout.models import CandidateProduct, ProductStage, SourceRegion


def load_fixture_candidates(path: str | Path) -> list[CandidateProduct]:
    fixture_path = Path(path)
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    candidates: list[CandidateProduct] = []
    for item in data:
        candidates.append(
            CandidateProduct(
                source_name=item["source_name"],
                source_region=SourceRegion(item["source_region"]),
                source_url=item["source_url"],
                product_name=item["product_name"],
                highlight=item["highlight"],
                country_region=item["country_region"],
                stage=ProductStage(item.get("stage", "unknown")),
                product_category=list(item.get("product_category", [])),
                target_audience=item.get("target_audience", ""),
                novelty_reason=item.get("novelty_reason", ""),
                trend_reason=item.get("trend_reason", ""),
                evidence=list(item.get("evidence", [])),
                commercial_judgment=item.get("commercial_judgment", ""),
                showroom_fit=item.get("showroom_fit", ""),
                risks=list(item.get("risks", [])),
                raw_score_signals=dict(item.get("raw_score_signals", {})),
            )
        )
    return candidates
```

- [ ] **Step 5: Create scoring implementation**

Create `D:\AI Project\好物搜集agent\src\gadget_scout\scoring.py`:

```python
from __future__ import annotations

from gadget_scout.models import (
    CandidateProduct,
    ProductStage,
    RecommendationAction,
    ScoreBreakdown,
    ScoutCategory,
)


LIMITS = {
    "novelty": 20,
    "product_market_relevance": 15,
    "evidence_strength": 15,
    "content_value": 15,
    "commercial_value": 15,
    "showroom_fit": 10,
    "trend_signal": 10,
    "risk_penalty": 20,
}


def _bounded(value: int, key: str) -> int:
    return max(0, min(LIMITS[key], int(value)))


def score_candidate(candidate: CandidateProduct) -> ScoreBreakdown:
    signals = candidate.raw_score_signals
    return ScoreBreakdown(
        novelty=_bounded(signals.get("novelty", 8), "novelty"),
        product_market_relevance=_bounded(
            signals.get("product_market_relevance", 8), "product_market_relevance"
        ),
        evidence_strength=_bounded(
            signals.get("evidence_strength", min(15, 5 + len(candidate.evidence) * 3)),
            "evidence_strength",
        ),
        content_value=_bounded(signals.get("content_value", 8), "content_value"),
        commercial_value=_bounded(signals.get("commercial_value", 6), "commercial_value"),
        showroom_fit=_bounded(signals.get("showroom_fit", 5), "showroom_fit"),
        trend_signal=_bounded(signals.get("trend_signal", 5), "trend_signal"),
        risk_penalty=_bounded(
            signals.get("risk_penalty", min(20, len(candidate.risks) * 3)), "risk_penalty"
        ),
    )


def classify_candidate(
    candidate: CandidateProduct, score: ScoreBreakdown
) -> tuple[ScoutCategory, RecommendationAction]:
    if score.total < 65:
        return ScoutCategory.WATCHLIST, RecommendationAction.NOT_RECOMMENDED

    future_stages = {
        ProductStage.CONCEPT,
        ProductStage.PROTOTYPE,
        ProductStage.CROWDFUNDING,
    }
    mature_stages = {
        ProductStage.PREORDER,
        ProductStage.LAUNCHED,
        ProductStage.SHIPPING,
    }

    if candidate.stage in future_stages:
        category = ScoutCategory.FUTURE
    elif candidate.stage in mature_stages:
        category = ScoutCategory.TREND
    else:
        category = ScoutCategory.WATCHLIST

    if (
        score.showroom_fit >= 9
        and score.commercial_value >= 12
        and candidate.stage in mature_stages
    ):
        action = RecommendationAction.SHOWROOM_PARTNERSHIP
    elif (
        score.commercial_value >= 13
        and score.evidence_strength >= 12
        and candidate.stage in mature_stages
    ):
        action = RecommendationAction.SUPPLY_CHAIN
    elif score.content_value >= 13 and score.novelty >= 14:
        action = RecommendationAction.CONTENT_FIRST
    elif score.total >= 65:
        action = RecommendationAction.WATCHLIST
    else:
        action = RecommendationAction.NOT_RECOMMENDED

    return category, action
```

- [ ] **Step 6: Run scoring tests**

Run:

```powershell
python -m pytest tests/test_scoring.py -q
```

Expected:

```text
4 passed
```

- [ ] **Step 7: Commit or record skip**

Run:

```powershell
git status --short
```

If not a git repo, record: `commit skipped because workspace is not a git repository`.

---

### Task 3: Dedupe And Daily Selection

**Files:**
- Create: `D:\AI Project\好物搜集agent\src\gadget_scout\dedupe.py`
- Create: `D:\AI Project\好物搜集agent\src\gadget_scout\selection.py`
- Create: `D:\AI Project\好物搜集agent\tests\test_selection.py`

- [ ] **Step 1: Write failing selection tests**

Create `D:\AI Project\好物搜集agent\tests\test_selection.py`:

```python
from dataclasses import replace

from gadget_scout.dedupe import make_dedupe_id, normalize_text
from gadget_scout.models import ProductStage, SourceRegion
from gadget_scout.scoring import classify_candidate, score_candidate
from gadget_scout.selection import select_top_products, select_top_products_by_region
from gadget_scout.sources import load_fixture_candidates


def _selected(candidate):
    score = score_candidate(candidate)
    classification, action = classify_candidate(candidate, score)
    return candidate, classification, action, score


def test_normalize_text_for_stable_ids():
    assert normalize_text(" AI  Pocket-Projector!!! ") == "ai pocket projector"


def test_make_dedupe_id_is_stable_for_same_product_and_domain():
    first = make_dedupe_id("AI Pocket Projector", "https://www.36kr.com/p/example")
    second = make_dedupe_id(" ai pocket projector ", "https://36kr.com/p/example?utm=1")

    assert first == second


def test_select_top_products_caps_at_ten():
    base = load_fixture_candidates("tests/fixtures/candidates.json")[2]
    candidates = []
    for index in range(12):
        candidates.append(
            replace(
                base,
                product_name=f"DeskBot Companion {index}",
                source_url=f"https://example.com/deskbot-{index}",
            )
        )

    selected = select_top_products(candidates, max_items=10, min_score=75)

    assert len(selected) == 10


def test_select_top_products_by_region_caps_each_region_at_ten():
    overseas_base = load_fixture_candidates("tests/fixtures/candidates.json")[2]
    domestic_base = load_fixture_candidates("tests/fixtures/candidates.json")[1]
    candidates = []
    for index in range(12):
        candidates.append(
            replace(
                overseas_base,
                product_name=f"Overseas Robot {index}",
                source_region=SourceRegion.OVERSEAS,
                source_url=f"https://example.com/overseas-robot-{index}",
            )
        )
    for index in range(11):
        candidates.append(
            replace(
                domestic_base,
                product_name=f"Domestic Projector {index}",
                source_region=SourceRegion.DOMESTIC,
                source_url=f"https://example.cn/domestic-projector-{index}",
            )
        )

    selected = select_top_products_by_region(candidates, max_items_per_region=10, min_score=75)

    assert len(selected[SourceRegion.OVERSEAS]) == 10
    assert len(selected[SourceRegion.DOMESTIC]) == 10


def test_select_top_products_prefers_category_diversity_when_scores_are_close():
    base = load_fixture_candidates("tests/fixtures/candidates.json")[2]
    candidates = []
    for index in range(8):
        candidates.append(
            replace(
                base,
                product_name=f"AI Desk Device {index}",
                product_category=["ai-device"],
                source_url=f"https://example.com/ai-device-{index}",
            )
        )
    for index in range(4):
        candidates.append(
            replace(
                base,
                product_name=f"Audio Companion {index}",
                product_category=["audio"],
                source_url=f"https://example.com/audio-{index}",
            )
        )

    selected = select_top_products(candidates, max_items=6, min_score=75)

    selected_categories = [item.candidate.product_category[0] for item in selected]
    assert selected_categories.count("ai-device") == 4
    assert selected_categories.count("audio") == 2


def test_select_top_products_allows_unfixed_future_trend_ratio():
    base = load_fixture_candidates("tests/fixtures/candidates.json")[0]
    future_candidates = [
        replace(
            base,
            product_name=f"Future Ring {index}",
            source_url=f"https://example.com/future-ring-{index}",
        )
        for index in range(6)
    ]

    selected = select_top_products(future_candidates, max_items=10, min_score=75)

    assert len(selected) == 6
    assert {item.classification for item in selected} == {"未来好物"}


def test_select_top_products_filters_low_score_candidates():
    low = replace(
        load_fixture_candidates("tests/fixtures/candidates.json")[0],
        product_name="Weak Gadget",
        stage=ProductStage.CONCEPT,
        raw_score_signals={
            "novelty": 5,
            "product_market_relevance": 4,
            "evidence_strength": 2,
            "content_value": 4,
            "commercial_value": 2,
            "showroom_fit": 2,
            "trend_signal": 2,
            "risk_penalty": 10
        },
    )

    selected = select_top_products([low], max_items=10, min_score=75)

    assert selected == []
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_selection.py -q
```

Expected: FAIL with missing `gadget_scout.dedupe` or `gadget_scout.selection`.

- [ ] **Step 3: Create dedupe helpers**

Create `D:\AI Project\好物搜集agent\src\gadget_scout\dedupe.py`:

```python
from __future__ import annotations

import hashlib
import re
from urllib.parse import urlparse


def normalize_text(value: str) -> str:
    lowered = value.strip().lower()
    cleaned = re.sub(r"[^0-9a-z\u4e00-\u9fff]+", " ", lowered)
    return re.sub(r"\s+", " ", cleaned).strip()


def _canonical_domain(url: str) -> str:
    host = urlparse(url).netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    return host


def make_dedupe_id(product_name: str, source_url: str) -> str:
    key = f"{normalize_text(product_name)}|{_canonical_domain(source_url)}"
    return hashlib.sha1(key.encode("utf-8")).hexdigest()[:16]
```

- [ ] **Step 4: Create selection logic**

Create `D:\AI Project\好物搜集agent\src\gadget_scout\selection.py`:

```python
from __future__ import annotations

from gadget_scout.dedupe import make_dedupe_id
from gadget_scout.models import CandidateProduct, RecommendationAction, SelectedProduct, SourceRegion
from gadget_scout.scoring import classify_candidate, score_candidate


def select_top_products(
    candidates: list[CandidateProduct],
    max_items: int = 10,
    min_score: int = 75,
    max_primary_category_first_pass: int = 4,
) -> list[SelectedProduct]:
    ranked: list[SelectedProduct] = []
    seen_ids: set[str] = set()

    for candidate in candidates:
        score = score_candidate(candidate)
        classification, action = classify_candidate(candidate, score)
        dedupe_id = make_dedupe_id(candidate.product_name, candidate.source_url)
        if dedupe_id in seen_ids:
            continue
        seen_ids.add(dedupe_id)
        if score.total < min_score:
            continue
        if action == RecommendationAction.NOT_RECOMMENDED:
            continue
        ranked.append(
            SelectedProduct(
                candidate=candidate,
                classification=classification,
                recommendation_action=action,
                score=score,
                dedupe_id=dedupe_id,
            )
        )

    ranked.sort(
        key=lambda item: (
            item.score.total,
            item.score.evidence_strength,
            item.score.commercial_value,
            item.score.content_value,
        ),
        reverse=True,
    )
    selected: list[SelectedProduct] = []
    deferred: list[SelectedProduct] = []
    primary_category_counts: dict[str, int] = {}

    for item in ranked:
        primary_category = (
            item.candidate.product_category[0]
            if item.candidate.product_category
            else "uncategorized"
        )
        if primary_category_counts.get(primary_category, 0) < max_primary_category_first_pass:
            selected.append(item)
            primary_category_counts[primary_category] = (
                primary_category_counts.get(primary_category, 0) + 1
            )
        else:
            deferred.append(item)
        if len(selected) == max_items:
            return selected

    for item in deferred:
        selected.append(item)
        if len(selected) == max_items:
            break

    return selected


def select_top_products_by_region(
    candidates: list[CandidateProduct],
    max_items_per_region: int = 10,
    min_score: int = 75,
) -> dict[SourceRegion, list[SelectedProduct]]:
    domestic = [
        candidate for candidate in candidates if candidate.source_region == SourceRegion.DOMESTIC
    ]
    overseas = [
        candidate for candidate in candidates if candidate.source_region == SourceRegion.OVERSEAS
    ]
    return {
        SourceRegion.DOMESTIC: select_top_products(
            domestic,
            max_items=max_items_per_region,
            min_score=min_score,
        ),
        SourceRegion.OVERSEAS: select_top_products(
            overseas,
            max_items=max_items_per_region,
            min_score=min_score,
        ),
    }
```

- [ ] **Step 5: Run selection tests**

Run:

```powershell
python -m pytest tests/test_selection.py -q
```

Expected:

```text
7 passed
```

- [ ] **Step 6: Run all tests so far**

Run:

```powershell
python -m pytest -q
```

Expected:

```text
11 passed
```

- [ ] **Step 7: Commit or record skip**

Run `git status --short`; if not a git repo, record the commit skip note.

---

### Task 4: Briefing Generator

**Files:**
- Create: `D:\AI Project\好物搜集agent\src\gadget_scout\briefing.py`
- Create: `D:\AI Project\好物搜集agent\tests\test_briefing.py`

- [ ] **Step 1: Write failing briefing tests**

Create `D:\AI Project\好物搜集agent\tests\test_briefing.py`:

```python
from gadget_scout.briefing import format_daily_briefing
from gadget_scout.models import SourceRegion
from gadget_scout.selection import select_top_products_by_region
from gadget_scout.sources import load_fixture_candidates


def test_format_daily_briefing_includes_top_items_and_actions():
    selected = select_top_products_by_region(load_fixture_candidates("tests/fixtures/candidates.json"))

    briefing = format_daily_briefing(selected, run_date="2026-06-23")

    assert "今日好物雷达 2026-06-23" in briefing
    assert "国内入选 1 个，海外入选 2 个。" in briefing
    assert "国内 Top" in briefing
    assert "海外 Top" in briefing
    assert "DeskBot Companion｜展厅合作｜91" in briefing
    assert "AI Pocket Projector｜供应链推进｜82" in briefing
    assert "Smart Ring Lab｜内容优先｜80" in briefing
    assert "链接：" in briefing


def test_format_daily_briefing_for_no_qualified_items():
    briefing = format_daily_briefing(
        {SourceRegion.DOMESTIC: [], SourceRegion.OVERSEAS: []},
        run_date="2026-06-23",
    )

    assert "今日无高置信推荐，未强行凑数。" in briefing
    assert "观察到的弱信号：" in briefing
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_briefing.py -q
```

Expected: FAIL with missing `gadget_scout.briefing`.

- [ ] **Step 3: Create briefing implementation**

Create `D:\AI Project\好物搜集agent\src\gadget_scout\briefing.py`:

```python
from __future__ import annotations

from gadget_scout.models import SelectedProduct, SourceRegion


def format_daily_briefing(
    selected_by_region: dict[SourceRegion, list[SelectedProduct]], run_date: str
) -> str:
    domestic = selected_by_region.get(SourceRegion.DOMESTIC, [])
    overseas = selected_by_region.get(SourceRegion.OVERSEAS, [])
    if not domestic and not overseas:
        return (
            f"今日好物雷达 {run_date}\n\n"
            "今日无高置信推荐，未强行凑数。\n\n"
            "观察到的弱信号：\n"
            "- 候选质量未达到高置信阈值，建议保留观察但不推进。"
        )

    lines = [
        f"今日好物雷达 {run_date}",
        "",
        f"国内入选 {len(domestic)} 个，海外入选 {len(overseas)} 个。",
        "",
    ]

    for title, items in (("国内 Top", domestic), ("海外 Top", overseas)):
        lines.extend([title, ""])
        if not items:
            lines.extend(["无高置信推荐。", ""])
            continue
        for index, item in enumerate(items, start=1):
            candidate = item.candidate
            lines.extend(
                [
                    (
                        f"{index}. {candidate.product_name}｜"
                        f"{item.recommendation_action.value}｜{item.score.total}"
                    ),
                    candidate.highlight,
                    f"为什么值得看：{candidate.trend_reason}",
                    f"下一步建议：{candidate.commercial_judgment}",
                    f"链接：{candidate.source_url}",
                    "",
                ]
            )

    lines.extend(["今日信号：", "- 国内和海外分别评分、分别排序；未设置未来好物/趋势好物固定比例。"])
    return "\n".join(lines).strip()
```

- [ ] **Step 4: Run briefing tests**

Run:

```powershell
python -m pytest tests/test_briefing.py -q
```

Expected:

```text
2 passed
```

- [ ] **Step 5: Run all tests so far**

Run:

```powershell
python -m pytest -q
```

Expected:

```text
13 passed
```

- [ ] **Step 6: Commit or record skip**

Run `git status --short`; if not a git repo, record the commit skip note.

---

### Task 5: WeCom Schema And Payload Builders

**Files:**
- Create: `D:\AI Project\好物搜集agent\src\gadget_scout\wecom.py`
- Create: `D:\AI Project\好物搜集agent\tests\test_wecom.py`

- [ ] **Step 1: Write failing WeCom tests**

Create `D:\AI Project\好物搜集agent\tests\test_wecom.py`:

```python
from gadget_scout.briefing import format_daily_briefing
from gadget_scout.models import SourceRegion
from gadget_scout.selection import select_top_products_by_region
from gadget_scout.sources import load_fixture_candidates
from gadget_scout.wecom import build_smartsheet_records, build_wecom_text_payload


def test_build_smartsheet_records_uses_expected_fields_without_owner():
    selected = select_top_products_by_region(load_fixture_candidates("tests/fixtures/candidates.json"))

    records = build_smartsheet_records(selected, run_date="2026-06-23")

    first_values = records[SourceRegion.OVERSEAS][0]["values"]
    assert "负责人" not in first_values
    assert first_values["日期"][0]["text"] == "2026-06-23"
    assert first_values["来源区域"][0]["text"] == "海外"
    assert first_values["推荐动作"][0]["text"] == "展厅合作"
    assert first_values["综合分"][0]["text"] == "91"
    assert "去重ID" in first_values

    domestic_values = records[SourceRegion.DOMESTIC][0]["values"]
    assert domestic_values["来源区域"][0]["text"] == "国内"
    assert domestic_values["推荐动作"][0]["text"] == "供应链推进"


def test_build_wecom_text_payload_wraps_briefing():
    selected = select_top_products_by_region(load_fixture_candidates("tests/fixtures/candidates.json"))
    briefing = format_daily_briefing(selected, run_date="2026-06-23")

    payload = build_wecom_text_payload(briefing)

    assert payload == {
        "msgtype": "text",
        "text": {"content": briefing},
    }
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_wecom.py -q
```

Expected: FAIL with missing `gadget_scout.wecom`.

- [ ] **Step 3: Create WeCom builders**

Create `D:\AI Project\好物搜集agent\src\gadget_scout\wecom.py`:

```python
from __future__ import annotations

from gadget_scout.models import SelectedProduct, SourceRegion


def _text(value: object) -> list[dict[str, str]]:
    return [{"type": "text", "text": str(value)}]


def build_smartsheet_records(
    selected_by_region: dict[SourceRegion, list[SelectedProduct]], run_date: str
) -> dict[SourceRegion, list[dict[str, dict[str, list[dict[str, str]]]]]]:
    output: dict[SourceRegion, list[dict[str, dict[str, list[dict[str, str]]]]]] = {
        SourceRegion.DOMESTIC: [],
        SourceRegion.OVERSEAS: [],
    }
    region_label = {
        SourceRegion.DOMESTIC: "国内",
        SourceRegion.OVERSEAS: "海外",
    }
    for region, selected in selected_by_region.items():
        for item in selected:
            candidate = item.candidate
            values = {
                "日期": _text(run_date),
                "分类": _text(item.classification.value),
                "产品名": _text(candidate.product_name),
                "一句话亮点": _text(candidate.highlight),
                "来源链接": _text(candidate.source_url),
                "国家/地区": _text(candidate.country_region),
                "来源区域": _text(region_label[region]),
                "产品阶段": _text(candidate.stage.value),
                "预计上市时间": _text("未知"),
                "品类": _text(", ".join(candidate.product_category)),
                "目标人群": _text(candidate.target_audience),
                "为什么新奇": _text(candidate.novelty_reason),
                "为什么可能火": _text(candidate.trend_reason),
                "关键证据": _text("；".join(candidate.evidence)),
                "商业判断": _text(candidate.commercial_judgment),
                "展厅适配建议": _text(candidate.showroom_fit),
                "风险": _text("；".join(candidate.risks)),
                "综合分": _text(item.score.total),
                "推荐动作": _text(item.recommendation_action.value),
                "去重ID": _text(item.dedupe_id),
            }
            output[region].append({"values": values})
    return output


def build_wecom_text_payload(content: str) -> dict[str, object]:
    return {
        "msgtype": "text",
        "text": {"content": content},
    }
```

- [ ] **Step 4: Run WeCom tests**

Run:

```powershell
python -m pytest tests/test_wecom.py -q
```

Expected:

```text
2 passed
```

- [ ] **Step 5: Run all tests so far**

Run:

```powershell
python -m pytest -q
```

Expected:

```text
15 passed
```

- [ ] **Step 6: Commit or record skip**

Run `git status --short`; if not a git repo, record the commit skip note.

---

### Task 6: CLI Dry Run

**Files:**
- Create: `D:\AI Project\好物搜集agent\src\gadget_scout\cli.py`
- Create: `D:\AI Project\好物搜集agent\tests\test_cli.py`
- Create: `D:\AI Project\好物搜集agent\config\sources.json`

- [ ] **Step 1: Write failing CLI test**

Create `D:\AI Project\好物搜集agent\tests\test_cli.py`:

```python
import json
from pathlib import Path

from gadget_scout.cli import run_dry_run


def test_run_dry_run_writes_json_and_markdown(tmp_path):
    result = run_dry_run(
        fixture_path=Path("tests/fixtures/candidates.json"),
        output_dir=tmp_path,
        run_date="2026-06-23",
        max_items_per_region=10,
        min_score=75,
    )

    report = json.loads(result.json_path.read_text(encoding="utf-8"))
    markdown = result.markdown_path.read_text(encoding="utf-8")

    assert result.domestic_selected_count == 1
    assert result.overseas_selected_count == 2
    assert report["domestic_selected_count"] == 1
    assert report["overseas_selected_count"] == 2
    assert report["max_items_per_region"] == 10
    assert "今日好物雷达 2026-06-23" in markdown
```

- [ ] **Step 2: Run tests to verify they fail**

Run:

```powershell
python -m pytest tests/test_cli.py -q
```

Expected: FAIL with missing `gadget_scout.cli`.

- [ ] **Step 3: Create CLI implementation**

Create `D:\AI Project\好物搜集agent\src\gadget_scout\cli.py`:

```python
from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from gadget_scout.briefing import format_daily_briefing
from gadget_scout.models import SourceRegion
from gadget_scout.selection import select_top_products_by_region
from gadget_scout.sources import load_fixture_candidates
from gadget_scout.wecom import build_smartsheet_records, build_wecom_text_payload


@dataclass(frozen=True)
class DryRunResult:
    domestic_selected_count: int
    overseas_selected_count: int
    json_path: Path
    markdown_path: Path


def run_dry_run(
    fixture_path: Path,
    output_dir: Path,
    run_date: str,
    max_items_per_region: int = 10,
    min_score: int = 75,
) -> DryRunResult:
    candidates = load_fixture_candidates(fixture_path)
    selected = select_top_products_by_region(
        candidates,
        max_items_per_region=max_items_per_region,
        min_score=min_score,
    )
    briefing = format_daily_briefing(selected, run_date=run_date)
    records = build_smartsheet_records(selected, run_date=run_date)
    bot_payload = build_wecom_text_payload(briefing)

    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / f"{run_date}-dry-run.json"
    markdown_path = output_dir / f"{run_date}-briefing.md"

    json_payload = {
        "run_date": run_date,
        "max_items_per_region": max_items_per_region,
        "min_score": min_score,
        "domestic_selected_count": len(selected[SourceRegion.DOMESTIC]),
        "overseas_selected_count": len(selected[SourceRegion.OVERSEAS]),
        "records": records,
        "bot_payload": bot_payload,
    }
    json_path.write_text(
        json.dumps(json_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    markdown_path.write_text(briefing, encoding="utf-8")
    return DryRunResult(
        domestic_selected_count=len(selected[SourceRegion.DOMESTIC]),
        overseas_selected_count=len(selected[SourceRegion.OVERSEAS]),
        json_path=json_path,
        markdown_path=markdown_path,
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the daily gadget scout pipeline.")
    parser.add_argument("--fixtures", default="tests/fixtures/candidates.json")
    parser.add_argument("--out", default="runs")
    parser.add_argument("--run-date", default=date.today().isoformat())
    parser.add_argument("--max-items-per-region", type=int, default=10)
    parser.add_argument("--min-score", type=int, default=75)
    args = parser.parse_args()

    result = run_dry_run(
        fixture_path=Path(args.fixtures),
        output_dir=Path(args.out),
        run_date=args.run_date,
        max_items_per_region=args.max_items_per_region,
        min_score=args.min_score,
    )
    print(f"domestic_selected_count={result.domestic_selected_count}")
    print(f"overseas_selected_count={result.overseas_selected_count}")
    print(f"json_path={result.json_path}")
    print(f"markdown_path={result.markdown_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 4: Create source allowlist config**

Create `D:\AI Project\好物搜集agent\config\sources.json`:

```json
{
  "recency_window_hours": 48,
  "sources": [
    {"name": "Kickstarter", "region": "international", "tier": "crowdfunding", "enabled": true},
    {"name": "Indiegogo", "region": "international", "tier": "crowdfunding", "enabled": true},
    {"name": "Crowd Supply", "region": "international", "tier": "crowdfunding", "enabled": true},
    {"name": "Product Hunt", "region": "international", "tier": "launch", "enabled": true},
    {"name": "Hackaday", "region": "international", "tier": "maker-media", "enabled": true},
    {"name": "TechCrunch", "region": "international", "tier": "tech-media", "enabled": true},
    {"name": "Wired Gear", "region": "international", "tier": "tech-media", "enabled": true},
    {"name": "The Verge", "region": "international", "tier": "tech-media", "enabled": true},
    {"name": "Engadget", "region": "international", "tier": "tech-media", "enabled": true},
    {"name": "New Atlas", "region": "international", "tier": "design-tech-media", "enabled": true},
    {"name": "Yanko Design", "region": "international", "tier": "design-media", "enabled": true},
    {"name": "36氪", "region": "domestic", "tier": "business-tech-media", "enabled": true},
    {"name": "极客公园", "region": "domestic", "tier": "tech-media", "enabled": true},
    {"name": "爱范儿", "region": "domestic", "tier": "lifestyle-tech-media", "enabled": true},
    {"name": "少数派", "region": "domestic", "tier": "consumer-tech-media", "enabled": true},
    {"name": "IT之家", "region": "domestic", "tier": "tech-news", "enabled": true}
  ]
}
```

- [ ] **Step 5: Run CLI tests**

Run:

```powershell
python -m pytest tests/test_cli.py -q
```

Expected:

```text
1 passed
```

- [ ] **Step 6: Run a real dry run**

Run:

```powershell
python -m gadget_scout.cli --fixtures tests/fixtures/candidates.json --out runs --run-date 2026-06-23
```

Expected output:

```text
domestic_selected_count=1
overseas_selected_count=2
json_path=runs\2026-06-23-dry-run.json
markdown_path=runs\2026-06-23-briefing.md
```

- [ ] **Step 7: Run all tests**

Run:

```powershell
python -m pytest -q
```

Expected:

```text
16 passed
```

- [ ] **Step 8: Commit or record skip**

Run `git status --short`; if not a git repo, record the commit skip note.

---

### Task 7: Codex Automation Prompt Draft

**Files:**
- Create: `D:\AI Project\好物搜集agent\config\codex-automation-prompt.md`

- [ ] **Step 1: Create the Codex automation prompt**

Create `D:\AI Project\好物搜集agent\config\codex-automation-prompt.md`:

```markdown
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
```

- [ ] **Step 2: Validate the prompt exists**

Run:

```powershell
Test-Path 'config\codex-automation-prompt.md'
```

Expected:

```text
True
```

- [ ] **Step 3: Confirm no external model key is required**

Record this note in the task log:

```text
Codex App automation wakes Codex and uses the daily-gadget-scout skill for analysis. OPENAI_API_KEY is not required for the Codex-first automation route.
```

- [ ] **Step 4: Commit or record skip**

Run `git status --short`; if not a git repo, record the commit skip note.

---

### Task 8: Create The Codex Skill

**Files:**
- Create: `C:\Users\Administrator\.codex\skills\daily-gadget-scout\SKILL.md`
- Create: `C:\Users\Administrator\.codex\skills\daily-gadget-scout\references\scouting-rules.md`
- Create: `C:\Users\Administrator\.codex\skills\daily-gadget-scout\references\sources.md`
- Create: `C:\Users\Administrator\.codex\skills\daily-gadget-scout\references\wecom-output.md`
- Create: `C:\Users\Administrator\.codex\skills\daily-gadget-scout\agents\openai.yaml`

- [ ] **Step 1: Initialize the skill folder**

Run:

```powershell
python 'C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\init_skill.py' daily-gadget-scout --path 'C:\Users\Administrator\.codex\skills' --resources references --interface display_name='Daily Gadget Scout' --interface short_description='Finds high-potential electronic products daily' --interface default_prompt='Use $daily-gadget-scout to scout today’s high-potential electronic products and prepare a WeCom-ready briefing.'
```

Expected:

```text
Created skill at C:\Users\Administrator\.codex\skills\daily-gadget-scout
```

If the exact success wording differs, continue only if the directory exists.

- [ ] **Step 2: Replace `SKILL.md`**

Write this exact content to `C:\Users\Administrator\.codex\skills\daily-gadget-scout\SKILL.md`:

```markdown
---
name: daily-gadget-scout
description: Scout, classify, and brief high-potential electronic products for YUMIUNIQ-style offline showroom and online electronic trend-product operations. Use when the user asks to find overseas or domestic novel electronic products, future gadgets, trend products, crowdfunding hardware, showroom-worthy products, supply-chain candidates, WeCom smart sheet product scouting, daily good-product radar, or a scheduled product discovery run.
---

# Daily Gadget Scout

Use this skill to run or design a daily scouting workflow for novel electronic products. Optimize for high-quality recommendations, not volume.

## Run Modes

Start by identifying the mode:

- `design`: refine scouting sources, fields, scoring, or workflow.
- `dry-run`: use fixture or manually supplied candidates and produce a report without writing to WeCom.
- `production-run`: collect candidates, score them, write selected records to WeCom, and send a briefing.
- `source-expansion`: evaluate new source websites or social-media channels.

For production actions that send messages or write to live WeCom documents, confirm the target sheet/chat/webhook before executing.

## Required References

Read only the reference files needed for the current mode:

- For scoring or recommendation questions, read `references/scouting-rules.md`.
- For source selection or expansion, read `references/sources.md`.
- For WeCom sheet or bot output, read `references/wecom-output.md`.

## Core Workflow

1. Gather candidates from the configured source allowlist or the user-provided candidate set.
2. Keep only consumer electronic, AI hardware, maker hardware, smart home, wearable, audio, robot, mobility, design-tech, or future-lifestyle products.
3. Normalize each candidate into the shared fields described in the WeCom output reference.
4. Deduplicate by normalized product name and canonical source domain.
5. Score candidates with the 100-point model in `scouting-rules.md`.
6. Classify each candidate as `未来好物`, `趋势好物`, or `观察池`.
7. Assign each candidate to `domestic` or `overseas`.
8. Assign exactly one recommendation action: `内容优先`, `供应链推进`, `展厅合作`, `观察池`, or `暂不推荐`.
9. Select at most 10 domestic high-confidence Top items and at most 10 overseas high-confidence Top items. Select fewer in either pool when fewer qualify.
10. Do not enforce any fixed ratio between `未来好物` and `趋势好物`.
11. Write domestic and overseas results to separate WeCom smart sheets, then send one combined bot briefing.
12. Produce a local Markdown/JSON report for auditability.

## Quality Bar

Prefer missing a weak product over padding the daily briefing. If no item qualifies, say `今日无高置信推荐，未强行凑数。`
```

- [ ] **Step 3: Create scouting rules reference**

Write this exact content to `C:\Users\Administrator\.codex\skills\daily-gadget-scout\references\scouting-rules.md`:

```markdown
# Scouting Rules

## Classifications

- `未来好物`: concept, prototype, lab technology, early crowdfunding, design fiction, or future-lifestyle product with 3-5 year signal value.
- `趋势好物`: launched, shipping, preorder, or evidence-backed product with 6-18 month commercial potential.
- `观察池`: interesting but insufficiently evidenced, weakly differentiated, or not ready for action.

## Recommendation Actions

- `内容优先`: strong story, visual, novelty, demo, or discussion value; not ready for sourcing.
- `供应链推进`: mature enough for supplier search, sample request, price/margin evaluation, or distribution discussion.
- `展厅合作`: strong brand/project value for residency, co-exhibition, pop-up, launch, or exclusive display.
- `观察池`: worth tracking, not strong enough for action today.
- `暂不推荐`: noisy, similar, risky, low evidence, or outside category.

## 100-Point Score

Use these dimensions:

| Dimension | Points |
|---|---:|
| Novelty | 20 |
| Product-market relevance | 15 |
| Evidence strength | 15 |
| Content value | 15 |
| Commercial value | 15 |
| Showroom fit | 10 |
| Trend signal | 10 |

Risk deductions:

- Deduct 5-20 points for likely vaporware, unclear claims, weak evidence, severe delivery risk, excessive similarity, or poor category fit.
- Deduct 5-15 points for inaccessible details, suspicious marketing claims, or missing product status.

Thresholds:

- `75+`: eligible for daily Top items.
- `65-74`: observation only unless strategically important.
- `<65`: discard or keep only in raw logs.

## Selection Rules

- Score and rank domestic and overseas pools independently.
- Select at most 10 domestic daily Top items.
- Select at most 10 overseas daily Top items.
- Select fewer than 10 in either pool when fewer meet the bar.
- Do not compare domestic and overseas items against each other for final slots.
- Do not force a fixed `未来好物` / `趋势好物` ratio.
- Avoid repeated products unless there is a meaningful update.
- Prefer category diversity when scores are close.
```

- [ ] **Step 4: Create sources reference**

Write this exact content to `C:\Users\Administrator\.codex\skills\daily-gadget-scout\references\sources.md`:

```markdown
# Sources

## 1.0 International Sources

- Kickstarter technology/design discovery pages.
- Indiegogo technology/design discovery pages.
- Crowd Supply.
- Product Hunt, subject to API and usage policy approval.
- Hackaday and Hackaday.io.
- TechCrunch hardware/AI/gadget coverage.
- Wired Gear.
- The Verge.
- Engadget.
- New Atlas.
- Yanko Design.
- Designboom technology/design product posts.

## 1.0 Domestic Sources

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

## 2.0 Social Sources

Treat Xiaohongshu, Douyin, Bilibili, Weibo, 即刻, X, TikTok, Instagram, YouTube, and Reddit as 2.0 sources. Use official APIs, approved connectors, manual exports, monitored accounts, or compliant data providers where possible. Do not design an anti-bot bypass as a normal feature.

## Source Quality Rules

- Prefer official product pages, crowdfunding pages, credible media, hands-on videos, preorder pages, funding data, founder updates, and retail availability.
- Mark items with only vague social chatter as `观察池` unless there is independent evidence.
- Preserve the canonical source URL for every candidate.
```

- [ ] **Step 5: Create WeCom output reference**

Write this exact content to `C:\Users\Administrator\.codex\skills\daily-gadget-scout\references\wecom-output.md`:

```markdown
# WeCom Output

## Smart Sheet Columns

Use two smart sheets with the same columns: one domestic sheet and one overseas sheet. Do not include `负责人`:

- 日期
- 分类
- 产品名
- 一句话亮点
- 来源链接
- 国家/地区
- 来源区域
- 产品阶段
- 预计上市时间
- 品类
- 目标人群
- 为什么新奇
- 为什么可能火
- 关键证据
- 商业判断
- 展厅适配建议
- 风险
- 综合分
- 推荐动作
- 去重ID

## Bot Briefing Format

Use this format when items qualify:

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

Use this format when nothing qualifies:

```text
今日好物雷达 YYYY-MM-DD

今日无高置信推荐，未强行凑数。

观察到的弱信号：
- ...
```

## Live Output Safety

Before writing to a live smart sheet or sending a bot message, confirm the target docid/sheet_id/chat/webhook and whether this is a production run.
```

- [ ] **Step 6: Ensure `agents/openai.yaml` has matching interface metadata**

If `init_skill.py` did not create this content, write this exact file to `C:\Users\Administrator\.codex\skills\daily-gadget-scout\agents\openai.yaml`:

```yaml
interface:
  display_name: "Daily Gadget Scout"
  short_description: "Finds high-potential electronic products daily"
  default_prompt: "Use $daily-gadget-scout to scout today's high-potential electronic products and prepare a WeCom-ready briefing."

policy:
  allow_implicit_invocation: true
```

- [ ] **Step 7: Validate the skill**

Run:

```powershell
python 'C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'C:\Users\Administrator\.codex\skills\daily-gadget-scout'
```

Expected: validation succeeds with no errors.

---

### Task 9: Create PAUSED Codex Worktree Automation

**Files:**
- Read: `D:\AI Project\好物搜集agent\config\codex-automation-prompt.md`
- Mutates Codex App automation state through `automation_update`

- [ ] **Step 1: Read the automation prompt**

Run:

```powershell
Get-Content -LiteralPath 'config\codex-automation-prompt.md' -Encoding UTF8
```

Expected: the prompt includes:

```text
Use $daily-gadget-scout to run the daily product scouting workflow for YUMIUNIQ.
OPENAI_API_KEY is not required
国内 Top
海外 Top
```

- [ ] **Step 2: Create a PAUSED worktree automation proposal**

Use the Codex App `automation_update` tool with these exact fields:

```json
{
  "mode": "suggested_create",
  "kind": "cron",
  "name": "Daily Gadget Scout",
  "rrule": "FREQ=DAILY;BYHOUR=8;BYMINUTE=0;BYSECOND=0",
  "cwds": ["D:\\AI Project\\好物搜集agent"],
  "executionEnvironment": "worktree",
  "status": "PAUSED",
  "model": "gpt-5.4",
  "reasoningEffort": "high",
  "prompt": "Use $daily-gadget-scout to run the daily product scouting workflow for YUMIUNIQ.\n\nRun mode: production-run unless required configuration is missing.\n\nRules:\n- Use Codex to analyze, classify, score, and summarize products. Do not require OPENAI_API_KEY or any external model provider key.\n- Scout both domestic and overseas sources.\n- Split candidates into domestic and overseas pools before final ranking.\n- Score domestic and overseas candidates independently.\n- Select at most 10 domestic items and at most 10 overseas items.\n- Select fewer in either pool when fewer candidates meet the quality bar.\n- Do not enforce a fixed `未来好物` / `趋势好物` ratio.\n- Write domestic selected records to the domestic WeCom smart sheet.\n- Write overseas selected records to the overseas WeCom smart sheet.\n- Send one combined WeCom briefing with `国内 Top` and `海外 Top` sections.\n- Do not include `负责人` in either smart sheet.\n- If WeCom smart sheet IDs, bot target, or source access are missing, do not perform live writes; produce a clear configuration-missing report instead.\n- Do not send external messages or modify production data unless the target sheet/chat/webhook is configured.\n\nExpected report:\n- Domestic selected count.\n- Overseas selected count.\n- Items written to each smart sheet, or the exact missing configuration that prevented writing.\n- Combined WeCom briefing text, or the exact missing configuration that prevented sending.\n- Source failures and skipped candidates."
}
```

Expected: Codex App renders an automation card/proposal. The automation should remain `PAUSED` until the user reviews and enables it.

- [ ] **Step 3: Verify the automation route does not require an external model key**

Record this note in the task log:

```text
The production route is Codex App automation using the daily-gadget-scout skill. OPENAI_API_KEY is not required unless the team later replaces Codex analysis with an independent external script.
```

---

### Task 10: Final Verification

**Files:**
- Verify all created files.

- [ ] **Step 1: Run all Python tests**

Run:

```powershell
python -m pytest -q
```

Expected:

```text
16 passed
```

- [ ] **Step 2: Run dry-run pipeline**

Run:

```powershell
python -m gadget_scout.cli --fixtures tests/fixtures/candidates.json --out runs --run-date 2026-06-23
```

Expected:

```text
domestic_selected_count=1
overseas_selected_count=2
json_path=runs\2026-06-23-dry-run.json
markdown_path=runs\2026-06-23-briefing.md
```

- [ ] **Step 3: Inspect generated briefing**

Run:

```powershell
Get-Content -LiteralPath 'runs\2026-06-23-briefing.md' -Encoding UTF8
```

Expected content includes:

```text
今日好物雷达 2026-06-23
DeskBot Companion｜展厅合作｜91
AI Pocket Projector｜供应链推进｜82
Smart Ring Lab｜内容优先｜80
```

- [ ] **Step 4: Validate skill again**

Run:

```powershell
python 'C:\Users\Administrator\.codex\skills\.system\skill-creator\scripts\quick_validate.py' 'C:\Users\Administrator\.codex\skills\daily-gadget-scout'
```

Expected: validation succeeds with no errors.

- [ ] **Step 5: Confirm no owner field in code or references except explanatory text**

Run:

```powershell
rg --encoding utf-8 -n "负责人" .
```

Expected matches may appear only in the design/plan text or the `wecom-output.md` sentence saying not to include `负责人`. There must be no `"负责人"` key in `src\gadget_scout\wecom.py`.

- [ ] **Step 6: Commit or record skip**

Run `git status --short`; if not a git repo, record the commit skip note.

---

## Spec Coverage Self-Review

- Daily 08:00 Codex run: Task 7 drafts the Codex automation prompt; Task 9 creates a PAUSED Codex App worktree cron automation with `FREQ=DAILY;BYHOUR=8;BYMINUTE=0;BYSECOND=0`.
- Domestic and overseas sources: Task 6 creates `config\sources.json`; Task 8 creates source guidance.
- Future/trend/watchlist classes: Task 2 and Task 8 implement and document them.
- Recommendation actions: Task 2 implements `内容优先`, `供应链推进`, `展厅合作`, `观察池`, `暂不推荐`.
- Domestic/overseas max 10 and fewer when weak: Task 3 enforces `max_items_per_region=10` and threshold filtering per region.
- No fixed category ratio: Task 3 tests all-future selection.
- Two WeCom smart sheets without `负责人`: Task 5 tests domestic/overseas field mapping.
- Combined bot briefing: Task 4 implements the grouped compact briefing and no-qualified fallback.
- Codex automation without relying on this chat window: Task 9 provides a PAUSED scheduled Codex App worktree automation.
- Social sources deferred to 2.0: Task 8 documents this in the skill source reference.

## Known Follow-Up After This Plan

- Add live collectors for RSS/API/web pages after the deterministic pipeline passes.
- Add an authenticated WeCom writer once the docid, sheet_id, field types, and bot target are confirmed.
- Decide whether to initialize this workspace as a git repository before production work.

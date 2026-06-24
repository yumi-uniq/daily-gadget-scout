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

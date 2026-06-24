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
            signals.get("risk_penalty", min(20, len(candidate.risks) * 3)),
            "risk_penalty",
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
        candidate.stage in {ProductStage.LAUNCHED, ProductStage.SHIPPING}
        and score.commercial_value >= 13
        and score.evidence_strength >= 12
    ):
        action = RecommendationAction.SUPPLY_CHAIN
    elif (
        score.showroom_fit >= 9
        and score.commercial_value >= 12
        and candidate.stage in mature_stages
    ):
        action = RecommendationAction.SHOWROOM_PARTNERSHIP
    elif score.content_value >= 13 and score.novelty >= 14:
        action = RecommendationAction.CONTENT_FIRST
    elif score.total >= 65:
        action = RecommendationAction.WATCHLIST
    else:
        action = RecommendationAction.NOT_RECOMMENDED

    return category, action

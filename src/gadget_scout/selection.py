from __future__ import annotations

from gadget_scout.dedupe import make_dedupe_id
from gadget_scout.models import (
    CandidateProduct,
    RecommendationAction,
    SelectedProduct,
    SourceRegion,
)
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

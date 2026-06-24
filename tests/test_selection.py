from dataclasses import replace

from gadget_scout.dedupe import make_dedupe_id, normalize_text
from gadget_scout.models import ProductStage, SourceRegion
from gadget_scout.selection import select_top_products, select_top_products_by_region
from gadget_scout.sources import load_fixture_candidates


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

    selected = select_top_products_by_region(
        candidates, max_items_per_region=10, min_score=75
    )

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
            "risk_penalty": 10,
        },
    )

    selected = select_top_products([low], max_items=10, min_score=75)

    assert selected == []
